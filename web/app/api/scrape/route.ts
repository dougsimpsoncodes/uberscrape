import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import { writeFile, unlink, readFile } from 'fs/promises';
import { join } from 'path';
import { tmpdir } from 'os';

const execAsync = promisify(exec);

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

interface ScrapeRequest {
  urls: string[];
  schema: Record<string, string>;
}

export async function POST(request: NextRequest) {
  try {
    const { urls, schema }: ScrapeRequest = await request.json();

    if (!urls || urls.length === 0) {
      return NextResponse.json({ error: 'No URLs provided' }, { status: 400 });
    }

    if (!schema || Object.keys(schema).length === 0) {
      return NextResponse.json({ error: 'No schema provided' }, { status: 400 });
    }

    // Create temp files
    const urlsFile = join(tmpdir(), `uberscrape-urls-${Date.now()}.txt`);
    const schemaFile = join(tmpdir(), `uberscrape-schema-${Date.now()}.json`);
    const outputFile = join(tmpdir(), `uberscrape-output-${Date.now()}.json`);

    try {
      // Write input files
      await writeFile(urlsFile, urls.join('\n'));
      await writeFile(schemaFile, JSON.stringify(schema, null, 2));

      // Get project root (parent of web/)
      const projectRoot = join(process.cwd(), '..');

      // Run Python scraper
      const command = `cd ${projectRoot} && GEMINI_API_KEY="${process.env.GEMINI_API_KEY}" python3 -m uberscrape.cli extract --urls ${urlsFile} --schema ${schemaFile} --output ${outputFile}`;
      
      const { stdout, stderr } = await execAsync(command, {
        timeout: 120000, // 2 minute timeout
      });

      // Read results
      const resultsRaw = await readFile(outputFile, 'utf-8');
      const results = JSON.parse(resultsRaw);

      // Clean up temp files
      await Promise.all([
        unlink(urlsFile).catch(() => {}),
        unlink(schemaFile).catch(() => {}),
        unlink(outputFile).catch(() => {}),
      ]);

      return NextResponse.json({
        success: true,
        results: results.map((r: any) => ({
          url: r.url,
          data: r.parse_error ? undefined : r,
          error: r.parse_error ? r.error : undefined,
        })),
      });

    } catch (execError: any) {
      // Clean up on error
      await Promise.all([
        unlink(urlsFile).catch(() => {}),
        unlink(schemaFile).catch(() => {}),
        unlink(outputFile).catch(() => {}),
      ]);

      throw execError;
    }

  } catch (error: any) {
    console.error('Scrape error:', error);
    return NextResponse.json(
      { 
        error: error.message || 'Scraping failed',
        details: error.stderr || error.stdout,
      },
      { status: 500 }
    );
  }
}
