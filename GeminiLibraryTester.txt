import React, { useState, useRef, useCallback, useEffect } from 'react';

// --- Helper Functions ---
const getTimestamp = () => new Date().toISOString().split('T')[1].slice(0, -1);

// --- Main Application Component ---
const App = () => {
  const [libraryUrl, setLibraryUrl] = useState('https://unpkg.com/acorn@8.11.3/dist/acorn.js');
  const [status, setStatus] = useState('idle'); // idle, analyzing, generating, testing, finished
  
  const [staticAnalysis, setStaticAnalysis] = useState(null);
  const [generatedTests, setGeneratedTests] = useState('');
  const [dynamicTestLog, setDynamicTestLog] = useState([]);
  const [sessionResults, setSessionResults] = useState({});
  const [copySuccess, setCopySuccess] = useState('');

  const consoleBackup = useRef({});

  // Load Acorn once
  useEffect(() => {
    if (document.getElementById('acorn-script')) return;
    const acornScript = document.createElement('script');
    acornScript.id = 'acorn-script';
    acornScript.src = 'https://unpkg.com/acorn@8.11.3/dist/acorn.js';
    acornScript.async = true;
    document.body.appendChild(acornScript);
  }, []);

  const handleStaticAnalysis = async () => {
    setStatus('analyzing');
    setStaticAnalysis(null);
    setGeneratedTests('');
    setDynamicTestLog([]);

    if (!libraryUrl) {
      setStaticAnalysis({ error: "Please provide a library URL." });
      setStatus('finished');
      return;
    }
    
    if (typeof acorn === 'undefined') {
        setStaticAnalysis({ error: "Acorn parser is not loaded yet. Please wait a moment and try again." });
        setStatus('finished');
        return;
    }

    try {
      const response = await fetch(libraryUrl);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const code = await response.text();
      
      let ast;
      try {
        ast = acorn.parse(code, { ecmaVersion: 2020, silent: true, locations: true });
      } catch (e) {
         setStaticAnalysis({ error: `Acorn failed to parse the library code. It might not be standard JavaScript. Error: ${e.message}` });
         setStatus('finished');
         return;
      }
      
      const analysisResult = {
          linesOfCode: code.split('\n').length,
          size: new Blob([code]).size,
          // Heuristic: Roughly 4 characters per token
          estimatedTokens: Math.round(new Blob([code]).size / 4),
          functionsFound: ast.body.filter(node => node.type === 'FunctionDeclaration' && node.id).map(node => node.id.name),
          usesEval: /eval\(/.test(code),
          usesWorker: /new Worker\(/.test(code),
          code: code,
      };
      
      setStaticAnalysis(analysisResult);
      setStatus('generating');

    } catch (error) {
      setStaticAnalysis({ error: `Failed to fetch or parse library: ${error.message}` });
      setStatus('finished');
    }
  };
  
  const handleGenerateTests = () => {
      setStatus('generating');
      setGeneratedTests(`// AI-Generated unit tests (placeholder)\n// Goal: Verify basic functionality while being token-efficient.\n\ntry {\n  console.log("Running placeholder test for ${libraryUrl}...");\n  if (typeof window.acorn !== 'undefined') {\n     console.log('Library (acorn) is attached to the window object.');\n     const ast = acorn.parse('1+1', {ecmaVersion: 2020});\n     console.log('Successfully parsed a simple string.');\n  } else {\n     console.warn('Library global variable not found on window object.');\n  }\n  console.log("Placeholder test passed.");\n} catch(e) {\n  console.error("Placeholder test failed:", e);\n}\n`);
      setStatus('testing');
  };
  
  const captureConsole = (logArray) => {
      const methods = ['log', 'warn', 'error', 'info', 'debug'];
      methods.forEach(method => {
          consoleBackup.current[method] = console[method];
          console[method] = (...args) => {
              const formattedArgs = args.map(arg => {
                  if (arg instanceof Error) {
                      return arg.stack || arg.message;
                  }
                  if (typeof arg === 'object' && arg !== null) {
                      try {
                          return JSON.stringify(arg, null, 2);
                      } catch (e) {
                          return '[Unserializable Object]';
                      }
                  }
                  return String(arg);
              }).join(' ');

              const newLog = { level: method, message: formattedArgs, timestamp: getTimestamp(), id: Date.now() + Math.random() };
              logArray.push(newLog);
              setDynamicTestLog(prev => [...prev, newLog]);
              consoleBackup.current[method](...args); 
          };
      });
  };

  const releaseConsole = () => {
      if(Object.keys(consoleBackup.current).length === 0) return;
      Object.keys(consoleBackup.current).forEach(method => {
          console[method] = consoleBackup.current[method];
      });
      consoleBackup.current = {};
  };


  const handleRunTests = () => {
      setStatus('testing');
      setDynamicTestLog([]);
      
      const currentTestLog = []; 
      captureConsole(currentTestLog);
      
      let testError = null;

      const finishRun = (status) => {
        releaseConsole();
        setSessionResults(prev => ({...prev, [libraryUrl]: { status, log: currentTestLog } }));
        setStatus('finished');
      };

      const oldScript = document.getElementById('dynamic-test-script');
      if(oldScript) oldScript.remove();

      const script = document.createElement('script');
      script.id = 'dynamic-test-script';
      script.src = libraryUrl;
      script.async = true;

      script.onload = () => {
          console.log(`Library from ${libraryUrl} loaded successfully.`);
          try {
              new Function(generatedTests)();
          } catch (e) {
              console.error(`Error executing generated tests: ${e.message}`);
              testError = e;
          } finally {
              finishRun(testError ? 'FAILURE' : 'SUCCESS');
          }
      };

      script.onerror = () => {
          console.error(`Failed to load script from ${libraryUrl}.`);
          finishRun('FAILURE');
      };

      document.body.appendChild(script);
  };
  
   const handleDownloadReport = () => {
        let report = `# Library Test Suite Report\n\nDate: ${new Date().toUTCString()}\n\n`;
        Object.entries(sessionResults).forEach(([url, result]) => {
            report += `## Test for: ${url}\n`;
            report += `**Status:** ${result.status}\n\n`;
            report += '### Console Log\n';
            report += '```\n';
            result.log.forEach(entry => {
                report += `[${entry.timestamp}] [${entry.level.toUpperCase()}] ${entry.message}\n`;
            });
            report += '```\n\n---\n\n';
        });

        const blob = new Blob([report], { type: 'text/markdown' });
        const downloadUrl = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = `test-suite-report-${Date.now()}.md`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(downloadUrl);
  };


  const InfoTooltip = ({ text }) => (
    <div className="relative inline-block ml-2 group">
        <svg className="w-4 h-4 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd"></path>
        </svg>
        <div className="absolute bottom-full left-1/2 z-20 w-64 p-2 mb-2 text-sm leading-tight text-white transform -translate-x-1/2 bg-black/70 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            {text}
        </div>
    </div>
  );


  return (
    <div className="bg-gray-900 text-gray-200 min-h-screen font-sans p-4 sm:p-6 lg:p-8 flex gap-8">
      {/* --- Left Panel: Setup --- */}
      <div className="w-1/2 flex flex-col gap-8">
        <div className="text-center">
          <h1 className="text-4xl sm:text-5xl font-bold text-cyan-400">Library Test Suite Generator</h1>
          <p className="text-gray-400 mt-2 text-lg">A "Code Golf" tool for Gemini</p>
        </div>

        <div className="bg-gray-800 p-6 rounded-lg shadow-2xl space-y-4">
            <div>
                <label htmlFor="cdnUrl" className="block text-sm font-medium text-gray-300 mb-2">Library CDN URL</label>
                <input
                  type="text"
                  id="cdnUrl"
                  value={libraryUrl}
                  onChange={(e) => setLibraryUrl(e.target.value)}
                  placeholder="https://example.com/library.min.js"
                  className="w-full bg-gray-900 border border-gray-700 rounded-md px-4 py-2 text-gray-200 focus:ring-2 focus:ring-cyan-500 focus:outline-none"
                  disabled={status !== 'idle' && status !== 'finished'}
                />
            </div>
            <div className="text-right">
                <button
                  onClick={handleStaticAnalysis}
                  disabled={status !== 'idle' && status !== 'finished'}
                  className="bg-cyan-600 text-white font-bold py-2 px-6 rounded-md hover:bg-cyan-700 transition-colors duration-300 disabled:bg-gray-600 disabled:cursor-not-allowed"
                >
                  {status === 'analyzing' ? 'Analyzing...' : '1. Analyze Library'}
                </button>
            </div>
        </div>
        
        <div className="bg-gray-800 p-6 rounded-lg shadow-2xl space-y-4">
           <h2 className="text-2xl font-bold text-gray-300 mb-4 border-b border-gray-700 pb-2">Static Analysis</h2>
            {staticAnalysis ? (
                <div className="space-y-2 text-sm">
                    {staticAnalysis.error ? (
                         <p className="text-red-400">{staticAnalysis.error}</p>
                    ) : (
                        <>
                            <div><strong>Size:</strong> {(staticAnalysis.size / 1024).toFixed(2)} KB</div>
                            {/* *** FIX: Changed parent <p> to a <div> to prevent nesting error *** */}
                            <div className="flex items-center">
                                <strong>Estimated Tokens:</strong>
                                <span className="font-bold text-cyan-400 ml-2">{staticAnalysis.estimatedTokens.toLocaleString()}</span>
                                <InfoTooltip text="Based on the heuristic of ~4 characters per token. This is a rough estimate for comparing library sizes." />
                            </div>
                            <div><strong>Lines of Code:</strong> {staticAnalysis.linesOfCode}</div>
                            <div><strong>Potential `eval()` use:</strong> <span className={staticAnalysis.usesEval ? 'text-red-400 font-bold' : 'text-green-400'}>{staticAnalysis.usesEval ? 'Detected' : 'Not Detected'}</span></div>
                            <div><strong>Potential Web Worker use:</strong> <span className={staticAnalysis.usesWorker ? 'text-red-400 font-bold' : 'text-green-400'}>{staticAnalysis.usesWorker ? 'Detected' : 'Not Detected'}</span></div>
                            <div><strong>Top-Level Functions:</strong> {staticAnalysis.functionsFound.length > 0 ? staticAnalysis.functionsFound.join(', ') : 'None found'}</div>
                        </>
                    )}
                    {status === 'generating' && (
                         <div className="text-center pt-4">
                            <button
                              onClick={handleGenerateTests}
                              className="bg-green-600 text-white font-bold py-2 px-6 rounded-md hover:bg-green-700"
                            >
                              2. Generate Unit Tests
                            </button>
                         </div>
                    )}
                </div>
            ) : <p className="text-gray-500">Run analysis to see results.</p>}
        </div>

      </div>
      
      {/* --- Right Panel: Results --- */}
      <div className="w-1/2 flex flex-col gap-8">
        <div className="bg-gray-800 p-6 rounded-lg shadow-2xl">
           <h2 className="text-2xl font-bold text-gray-300 mb-4 border-b border-gray-700 pb-2">Session Results</h2>
           <div className="space-y-2 max-h-48 overflow-y-auto">
                {Object.keys(sessionResults).length > 0 ? (
                    Object.entries(sessionResults).map(([url, result]) => (
                        <div key={url} className="flex justify-between items-center bg-gray-900/50 p-2 rounded-md">
                            <span className="text-gray-300 text-sm truncate" title={url}>{url}</span>
                            <span className={`font-bold text-sm px-2 py-1 rounded-full ${result.status === 'SUCCESS' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                                {result.status}
                            </span>
                        </div>
                    ))
                ) : <p className="text-gray-500 text-sm">No tests run in this session yet.</p>}
           </div>
           {Object.keys(sessionResults).length > 0 && 
            <div className="text-right mt-4">
                    <button onClick={handleDownloadReport} className="bg-purple-600 text-white font-bold py-1 px-4 text-sm rounded-md hover:bg-purple-700 transition-colors">Download Full Session Report</button>
            </div>
           }
        </div>

        <div className="bg-gray-800 p-6 rounded-lg shadow-2xl flex-grow flex flex-col">
          <h2 className="text-2xl font-bold text-gray-300 mb-4 border-b border-gray-700 pb-2">Generated Tests & Dynamic Log</h2>
          {generatedTests ? (
              <div className="flex flex-col flex-grow gap-4">
                  <div>
                      <h3 className="font-bold mb-2 text-gray-400">Generated Test Code:</h3>
                      <pre className="bg-black text-xs font-mono p-4 rounded-md h-32 overflow-auto">{generatedTests}</pre>
                  </div>
                  <div className="text-center">
                      <button
                          onClick={handleRunTests}
                          disabled={status !== 'testing'}
                          className="bg-purple-600 text-white font-bold py-2 px-6 rounded-md hover:bg-purple-700 disabled:bg-gray-600"
                      >
                        {status === 'testing' ? '3. Run Tests' : 'Tests Finished'}
                      </button>
                  </div>
                   <div className="flex-grow flex flex-col mt-4">
                        <h3 className="font-bold mb-2 text-gray-400">Dynamic Test Log:</h3>
                        <div className="font-mono text-sm bg-black rounded-md flex-grow overflow-y-auto p-4 space-y-2">
                          {dynamicTestLog.map(log => (
                             <div key={log.id}>
                                <span className="text-gray-600 mr-2">{log.timestamp}</span>
                                <span className={
                                    log.level === 'error' ? 'text-red-400' :
                                    log.level === 'warn' ? 'text-yellow-400' : 'text-gray-300'
                                }>[{log.level.toUpperCase()}] {log.message}</span>
                             </div>
                          ))}
                        </div>
                   </div>
              </div>
           ) : <p className="text-gray-500">Generate tests after analysis is complete.</p>}
        </div>
      </div>
    </div>
  );
};

export default App;
