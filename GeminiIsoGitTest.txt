import React, { useState, useEffect, useRef, useCallback } from 'react';
import { GitBranch, Play, XCircle, CheckCircle, Loader } from 'lucide-react';

const App = () => {
  const [log, setLog] = useState([]);
  const [status, setStatus] = useState('idle'); // idle, loading, running, success, failure
  const [fs, setFs] = useState(null);
  const [git, setGit] = useState(null);
  
  const logRef = useRef(null);

  const addLog = (message, level = 'info') => {
    const timestamp = new Date().toLocaleTimeString();
    setLog(prev => [...prev, { timestamp, message, level }]);
  };

  useEffect(() => {
    // Scroll to bottom of log
    if (logRef.current) {
      logRef.current.scrollTop = logRef.current.scrollHeight;
    }
  }, [log]);

  const loadInitialScripts = useCallback(() => {
    setStatus('loading');
    addLog('Initiating script loading...');

    const loadScript = (id, src) => {
      return new Promise((resolve, reject) => {
        if (document.getElementById(id)) {
          resolve();
          return;
        }
        const script = document.createElement('script');
        script.id = id;
        script.src = src;
        script.async = true;
        script.onload = () => {
          addLog(`Successfully loaded ${src}`);
          resolve();
        };
        script.onerror = () => {
          addLog(`Failed to load script: ${src}`, 'error');
          reject(new Error(`Failed to load ${src}`));
        };
        document.head.appendChild(script);
      });
    };

    Promise.all([
      loadScript('lightning-fs-script', 'https://unpkg.com/@isomorphic-git/lightning-fs'),
      loadScript('isomorphic-git-script', 'https://unpkg.com/isomorphic-git')
    ]).then(() => {
      if (window.LightningFS && window.git) {
        addLog('All base libraries loaded and available on window object.');
        const fsInstance = new window.LightningFS('isogit-poc-fs');
        setFs(fsInstance);
        setGit(window.git);
        setStatus('idle');
      } else {
        throw new Error('One or more base libraries failed to attach to the window object.');
      }
    }).catch(error => {
      addLog(error.message, 'error');
      setStatus('failure');
    });

  }, []);

  useEffect(() => {
    loadInitialScripts();
  }, [loadInitialScripts]);

  const runCloneTest = async () => {
    if (!fs || !git) {
      addLog('Libraries not ready. Please wait.', 'error');
      return;
    }
    setStatus('running');
    setLog([]);
    addLog('Starting git clone test...');

    const dir = '/tutorial';
    const url = 'https://github.com/isomorphic-git/isomorphic-git';
    
    try {
      // FIX: Instead of loading the http client from a URL (which is blocked by CSP),
      // we provide a minimal, in-memory implementation of the expected interface.
      // This bypasses the security policy that prevents dynamic script loading.
      const http = {
        request: async ({ url, method, headers, body }) => {
          addLog(`Making HTTP request: ${method} ${url}`);
          const res = await fetch(url, { method, headers, body: body ? await new Response(body).arrayBuffer() : undefined });
          return {
            url: res.url,
            method: method,
            statusCode: res.status,
            statusMessage: res.statusText,
            body: [new Uint8Array(await res.arrayBuffer())],
            headers: Object.fromEntries(res.headers.entries()),
          };
        }
      };

      addLog('Using in-memory http client implementation.');
      addLog(`Cloning ${url} into virtual directory '${dir}'...`);

      await git.clone({
        fs,
        http,
        dir,
        url,
        corsProxy: 'https://cors.isomorphic-git.org',
        onProgress: (progress) => {
           // This might be too noisy, but useful for debugging
           // addLog(`Progress: ${progress.phase} - ${progress.loaded}/${progress.total}`);
        }
      });
      
      addLog('Clone successful!', 'success');
      
      addLog('Verifying repository contents...');
      const files = await fs.promises.readdir(dir);
      addLog(`Files in '${dir}': ${files.join(', ')}`);

      if (files.includes('package.json')) {
        addLog('Verification successful: package.json found.', 'success');
        setStatus('success');
      } else {
        throw new Error("Verification failed: package.json not found in cloned repo.");
      }

    } catch (error) {
      console.error(error);
      addLog(`Clone test failed: ${error.message}`, 'error');
      setStatus('failure');
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'loading': return <Loader className="animate-spin" />;
      case 'running': return <Loader className="animate-spin" />;
      case 'success': return <CheckCircle className="text-green-400" />;
      case 'failure': return <XCircle className="text-red-400" />;
      default: return <Play />;
    }
  };

  return (
    <div className="bg-gray-900 text-gray-200 min-h-screen font-sans p-4 sm:p-6 lg:p-8">
      <div className="max-w-4xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-4xl sm:text-5xl font-bold text-cyan-400 flex items-center justify-center gap-4">
            <GitBranch size={48} />
            isomorphic-git Proof-of-Concept
          </h1>
          <p className="text-gray-400 mt-3 text-lg">Testing in-browser git clone functionality by providing the required `fs` and `http` dependencies.</p>
        </header>

        <div className="bg-gray-800 p-6 rounded-lg shadow-2xl mb-8">
            <button
                onClick={runCloneTest}
                disabled={status === 'loading' || status === 'running'}
                className="w-full bg-cyan-600 text-white font-bold py-3 px-6 rounded-md hover:bg-cyan-700 transition-colors duration-300 flex items-center justify-center gap-3 text-xl disabled:bg-gray-600 disabled:cursor-not-allowed"
            >
                {getStatusIcon()}
                {status === 'loading' ? 'Loading Libraries...' : status === 'running' ? 'Running Test...' : 'Run Clone Test'}
            </button>
        </div>
        
        <div className="bg-gray-800 p-6 rounded-lg shadow-2xl flex flex-col" style={{height: '50vh'}}>
             <h2 className="text-2xl font-bold text-gray-300 mb-4 border-b border-gray-700 pb-2">Execution Log</h2>
             <div ref={logRef} className="font-mono text-sm bg-black rounded-md flex-grow overflow-y-auto p-4 space-y-2">
                 {log.length === 0 ? (
                    <p className="text-gray-500">Log is empty. Click "Run Clone Test" to begin.</p>
                 ) : (
                    log.map((entry, index) => (
                        <div key={index} className="flex gap-2 items-start">
                            <span className="text-gray-600 flex-shrink-0">{entry.timestamp}</span>
                            <span className={
                                entry.level === 'error' ? 'text-red-400' :
                                entry.level === 'success' ? 'text-green-400' : 'text-gray-300'
                            }>{entry.message}</span>
                        </div>
                    ))
                 )}
             </div>
        </div>
      </div>
    </div>
  );
};

export default App;
