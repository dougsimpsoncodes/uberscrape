'use client';

import { useState } from 'react';
import { Upload, FileText, Download } from 'lucide-react';

type Step = 'upload' | 'processing' | 'results';

interface ScrapeResult {
  url: string;
  data?: Record<string, any>;
  error?: string;
}

export default function Home() {
  const [step, setStep] = useState<Step>('upload');
  const [urls, setUrls] = useState('');
  const [schema, setSchema] = useState('{\n  "title": "string",\n  "description": "string"\n}');
  const [results, setResults] = useState<ScrapeResult[]>([]);
  const [processing, setProcessing] = useState(false);

  const handleScrape = async () => {
    setProcessing(true);
    setStep('processing');

    try {
      const urlList = urls.split('\n').filter(u => u.trim());
      const schemaObj = JSON.parse(schema);

      const response = await fetch('/api/scrape', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ urls: urlList, schema: schemaObj }),
      });

      const data = await response.json();
      setResults(data.results || []);
      setStep('results');
    } catch (error) {
      alert('Error: ' + (error as Error).message);
    } finally {
      setProcessing(false);
    }
  };

  const downloadCSV = () => {
    if (results.length === 0) return;

    const successful = results.filter(r => !r.error && r.data);
    if (successful.length === 0) return;

    // Get all unique keys
    const keys = new Set<string>();
    successful.forEach(r => Object.keys(r.data!).forEach(k => keys.add(k)));
    const headers = Array.from(keys);

    // Build CSV
    const rows = [
      headers.join(','),
      ...successful.map(r => 
        headers.map(h => {
          const val = r.data![h];
          if (typeof val === 'object') return JSON.stringify(val);
          return String(val || '');
        }).join(',')
      )
    ];

    const csv = rows.join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'uberscrape-results.csv';
    a.click();
  };

  const downloadJSON = () => {
    const json = JSON.stringify(results, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'uberscrape-results.json';
    a.click();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white">
      <div className="max-w-6xl mx-auto p-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            UberScrape
          </h1>
          <p className="text-gray-400 text-lg">
            AI-powered web scraping that returns structured data, not HTML walls
          </p>
        </div>

        {/* Step Indicators */}
        <div className="flex justify-center items-center gap-4 mb-12">
          {['upload', 'processing', 'results'].map((s, i) => (
            <div key={s} className="flex items-center gap-2">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold ${
                step === s ? 'bg-blue-500 text-white' :
                (step === 'processing' && s === 'upload') || step === 'results' ? 'bg-green-500 text-white' :
                'bg-gray-700 text-gray-400'
              }`}>
                {i + 1}
              </div>
              <span className={`text-sm ${step === s ? 'text-white' : 'text-gray-500'}`}>
                {s === 'upload' ? 'Setup' : s === 'processing' ? 'Scraping' : 'Results'}
              </span>
              {i < 2 && <div className="w-16 h-px bg-gray-700" />}
            </div>
          ))}
        </div>

        {/* Upload Step */}
        {step === 'upload' && (
          <div className="bg-gray-800 rounded-xl border border-gray-700 p-8">
            <div className="grid md:grid-cols-2 gap-8">
              {/* URLs */}
              <div>
                <label className="block text-sm font-medium mb-2 flex items-center gap-2">
                  <FileText size={16} />
                  URLs to Scrape
                </label>
                <textarea
                  value={urls}
                  onChange={(e) => setUrls(e.target.value)}
                  placeholder="https://example.com&#10;https://example.org&#10;..."
                  className="w-full h-64 bg-gray-900 border border-gray-700 rounded-lg p-4 font-mono text-sm focus:outline-none focus:border-blue-500"
                  spellCheck={false}
                />
                <p className="text-xs text-gray-500 mt-2">One URL per line</p>
              </div>

              {/* Schema */}
              <div>
                <label className="block text-sm font-medium mb-2 flex items-center gap-2">
                  <FileText size={16} />
                  Data Schema (JSON)
                </label>
                <textarea
                  value={schema}
                  onChange={(e) => setSchema(e.target.value)}
                  className="w-full h-64 bg-gray-900 border border-gray-700 rounded-lg p-4 font-mono text-sm focus:outline-none focus:border-blue-500"
                  spellCheck={false}
                />
                <p className="text-xs text-gray-500 mt-2">
                  Define fields to extract. Types: string, number, boolean, array, object
                </p>
              </div>
            </div>

            <button
              onClick={handleScrape}
              disabled={!urls.trim() || processing}
              className="mt-8 w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white font-medium py-4 px-6 rounded-lg flex items-center justify-center gap-2 transition-colors"
            >
              <Upload size={20} />
              Start Scraping
            </button>
          </div>
        )}

        {/* Processing Step */}
        {step === 'processing' && (
          <div className="bg-gray-800 rounded-xl border border-gray-700 p-12 text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-4 border-gray-700 border-t-blue-500 mx-auto mb-6" />
            <h3 className="text-xl font-medium mb-2">Scraping in progress...</h3>
            <p className="text-gray-400">Extracting structured data from {urls.split('\n').filter(u => u.trim()).length} URLs</p>
          </div>
        )}

        {/* Results Step */}
        {step === 'results' && (
          <div className="space-y-6">
            {/* Summary */}
            <div className="bg-gray-800 rounded-xl border border-gray-700 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-medium mb-2">Scraping Complete</h3>
                  <p className="text-gray-400">
                    <span className="text-green-400 font-medium">{results.filter(r => !r.error).length} successful</span>
                    {results.filter(r => r.error).length > 0 && (
                      <span className="ml-4 text-red-400 font-medium">{results.filter(r => r.error).length} failed</span>
                    )}
                  </p>
                </div>
                <div className="flex gap-3">
                  <button
                    onClick={downloadJSON}
                    className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg flex items-center gap-2"
                  >
                    <Download size={16} />
                    JSON
                  </button>
                  <button
                    onClick={downloadCSV}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2"
                  >
                    <Download size={16} />
                    CSV
                  </button>
                </div>
              </div>
            </div>

            {/* Results Table */}
            <div className="bg-gray-800 rounded-xl border border-gray-700 overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-900 border-b border-gray-700">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">URL</th>
                      {results[0] && results[0].data && Object.keys(results[0].data).map(key => (
                        <th key={key} className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">{key}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-700">
                    {results.map((result, i) => (
                      <tr key={i} className={result.error ? 'bg-red-900/20' : ''}>
                        <td className="px-6 py-4 text-sm text-gray-300 max-w-xs truncate">
                          {result.url}
                        </td>
                        {result.error ? (
                          <td colSpan={100} className="px-6 py-4 text-sm text-red-400">
                            Error: {result.error}
                          </td>
                        ) : result.data && Object.values(result.data).map((val, j) => (
                          <td key={j} className="px-6 py-4 text-sm text-gray-300">
                            {typeof val === 'object' ? JSON.stringify(val) : String(val)}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <button
              onClick={() => { setStep('upload'); setUrls(''); setResults([]); }}
              className="w-full bg-gray-700 hover:bg-gray-600 text-white font-medium py-3 px-6 rounded-lg"
            >
              Start New Scrape
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
