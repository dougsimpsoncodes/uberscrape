"""
Command-line interface for UberScrape
"""

import asyncio
import click
import json
import csv
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv
import os

from .core.scraper import WebScraper
from .utils.schema import load_schema
from .utils.export import export_results

# Load environment variables
load_dotenv()

console = Console()

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    UberScrape - AI-powered web scraping that returns structured data
    
    Extract structured data from websites using Claude AI instead of brittle CSS selectors.
    """
    pass

@cli.command()
@click.option('--url', help='Single URL to scrape')
@click.option('--urls', type=click.Path(exists=True), help='File containing URLs (one per line)')
@click.option('--schema', type=click.Path(exists=True), required=True, help='JSON schema file defining fields to extract')
@click.option('--output', type=click.Path(), required=True, help='Output file path (.json or .csv)')
@click.option('--parallel', default=5, help='Number of parallel requests (default: 5)')
@click.option('--browser/--no-browser', default=False, help='Use browser for JavaScript rendering (slower)')
@click.option('--timeout', default=30, help='Request timeout in seconds')
def extract(url, urls, schema, output, parallel, browser, timeout):
    """
    Extract structured data from one or more URLs.
    
    Examples:
    
      # Single URL
      uberscrape extract --url https://example.com --schema rental.json --output results.json
      
      # Multiple URLs
      uberscrape extract --urls urls.txt --schema product.json --output results.csv --parallel 10
      
      # With JavaScript rendering
      uberscrape extract --url https://spa-site.com --schema data.json --output out.json --browser
    """
    asyncio.run(_extract(url, urls, schema, output, parallel, browser, timeout))

async def _extract(url, urls_file, schema_path, output_path, parallel, use_browser, timeout):
    """Async extraction logic"""
    
    # Validate inputs
    if not url and not urls_file:
        console.print("[red]Error: Provide either --url or --urls[/red]")
        return
    
    if url and urls_file:
        console.print("[red]Error: Provide only one of --url or --urls[/red]")
        return
    
    # Load schema
    try:
        schema = load_schema(schema_path)
    except Exception as e:
        console.print(f"[red]Error loading schema: {e}[/red]")
        return
    
    # Get API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        console.print("[red]Error: ANTHROPIC_API_KEY not found in environment[/red]")
        console.print("Create a .env file or set the environment variable")
        return
    
    # Parse URLs
    if url:
        urls_list = [url]
    else:
        with open(urls_file, 'r') as f:
            urls_list = [line.strip() for line in f if line.strip()]
    
    console.print(f"\n[bold]UberScrape Extraction[/bold]")
    console.print(f"URLs: {len(urls_list)}")
    console.print(f"Schema: {Path(schema_path).name}")
    console.print(f"Browser: {'Yes' if use_browser else 'No'}")
    console.print(f"Parallel: {parallel}\n")
    
    # Initialize scraper
    scraper = WebScraper(
        anthropic_key=api_key,
        use_browser=use_browser,
        timeout=timeout,
        max_concurrent=parallel
    )
    
    # Extract with progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(f"Extracting from {len(urls_list)} URLs...", total=None)
        
        results = await scraper.extract_batch(urls_list, schema, parallel=True)
        
        progress.update(task, completed=True)
    
    # Show summary
    successful = [r for r in results if not r.get('parse_error')]
    failed = [r for r in results if r.get('parse_error')]
    
    console.print(f"\n[bold green]✓ {len(successful)} successful[/bold green]")
    if failed:
        console.print(f"[bold red]✗ {len(failed)} failed[/bold red]")
    
    # Show errors
    if failed:
        console.print("\n[bold]Errors:[/bold]")
        for item in failed[:5]:  # Show first 5 errors
            console.print(f"  [red]•[/red] {item.get('url', 'unknown')}: {item.get('error', 'unknown error')}")
        if len(failed) > 5:
            console.print(f"  ... and {len(failed) - 5} more")
    
    # Export results
    try:
        export_results(results, output_path)
        console.print(f"\n[bold green]Results saved to {output_path}[/bold green]")
    except Exception as e:
        console.print(f"\n[red]Error saving results: {e}[/red]")
        return
    
    # Show preview
    if successful:
        console.print("\n[bold]Preview (first result):[/bold]")
        _print_result(successful[0])
    
    await scraper.close()

def _print_result(result: dict):
    """Print a single result in a nice table"""
    table = Table(show_header=False, box=None)
    table.add_column("Field", style="cyan")
    table.add_column("Value")
    
    for key, value in result.items():
        if key not in ['source', 'parse_error']:
            if isinstance(value, (list, dict)):
                value = json.dumps(value, indent=2)
            table.add_row(key, str(value))
    
    console.print(table)

@cli.command()
@click.argument('schema_name')
def schema(schema_name):
    """
    Show available schemas or display a specific schema.
    
    Examples:
    
      uberscrape schema rental-listing
      uberscrape schema product
    """
    from importlib import resources
    
    # List available schemas
    schemas_dir = Path(__file__).parent / 'schemas'
    available = [f.stem for f in schemas_dir.glob('*.json')]
    
    if not schema_name:
        console.print("[bold]Available schemas:[/bold]")
        for name in available:
            console.print(f"  • {name}")
        return
    
    # Show specific schema
    schema_path = schemas_dir / f"{schema_name}.json"
    if not schema_path.exists():
        console.print(f"[red]Schema '{schema_name}' not found[/red]")
        console.print(f"\nAvailable: {', '.join(available)}")
        return
    
    with open(schema_path) as f:
        schema_data = json.load(f)
    
    console.print(f"\n[bold]{schema_name} schema:[/bold]\n")
    console.print(json.dumps(schema_data, indent=2))

if __name__ == '__main__':
    cli()
