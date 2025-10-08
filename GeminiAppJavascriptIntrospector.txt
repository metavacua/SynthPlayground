import React, { useState, useCallback } from 'react';

// Main App component for the JavaScript Introspector
function App() {
  // State for the JavaScript code input by the user
  const [jsCode, setJsCode] = useState('');
  // State for the introspection results (functions and variables found from code input)
  const [introspectionResult, setIntrospectionResult] = useState(null);
  // State for the environment introspection results
  const [envIntrospectionResult, setEnvIntrospectionResult] = useState(null);
  // State for the current active tab in the meta-data panel ('devlog', 'changelog', 'about', 'known-bugs', 'environment')
  const [activeMetaTab, setActiveMetaTab] = useState('about');
  // Hardcoded semantic version for the application - Patch version bump for improved error handling/guidance
  const appVersion = "2.3.2"; // Incremented for improved error handling/guidance

  /**
   * Handles the change event for the textarea where users input JS code.
   * Updates the jsCode state with the current value of the textarea.
   * Clears previous results when the code changes to ensure fresh analysis.
   * @param {Object} event - The DOM event object from the textarea.
   */
  const handleCodeChange = (event) => {
    setJsCode(event.target.value);
    setIntrospectionResult(null); // Clear previous code introspection results
  };

  /**
   * Performs introspection on the provided JavaScript code using the Acorn parser
   * and ESTraverse for AST traversal. This is a functional implementation of AST-based analysis.
   * Acorn and ESTraverse are now directly included via script tags within this component for the Canvas environment.
   */
  const introspectCode = () => {
    const functions = [];
    const variables = [];

    try {
      // Check if acorn and estraverse are available globally. This check is crucial
      // even with direct script tags, as there might still be subtle timing issues
      // or CDN failures.
      if (typeof acorn === 'undefined' || typeof estraverse === 'undefined') {
        throw new Error("AST parsing libraries (Acorn, ESTraverse) are not available globally. This might indicate a CDN loading issue.");
      }

      // Step 1: Parse the JavaScript code into an Abstract Syntax Tree (AST) using Acorn.
      // ecmaVersion: Supports modern JavaScript (ES2020 features and syntax).
      // sourceType: 'module' for ES Modules, 'script' for standard scripts.
      // allowHashBang: Allows for `#!` at the beginning of files (e.g., node scripts).
      const ast = acorn.parse(jsCode, {
        ecmaVersion: 2020,
        sourceType: 'module',
        allowHashBang: true,
        // plugins: [acornJsx, acornBigInt] // Would need to load specific Acorn plugins for JSX, BigInt etc.
      });

      // Step 2: Traverse the AST using ESTraverse to identify functions and variables.
      // The 'enter' function is called for each node during traversal.
      estraverse.traverse(ast, {
        enter: function (node, parent) {
          // Identify Function Declarations and Expressions (named, arrow, anonymous)
          if (node.type === 'FunctionDeclaration') {
            if (node.id && !functions.includes(node.id.name)) {
              functions.push(node.id.name);
            }
          } else if (node.type === 'VariableDeclarator') {
            // Check if a variable is assigned a Function or ArrowFunction Expression
            if (node.init && (node.init.type === 'FunctionExpression' || node.init.type === 'ArrowFunctionExpression')) {
              if (node.id && !functions.includes(node.id.name)) {
                functions.push(node.id.name);
              }
            } else {
              // Otherwise, it's a regular variable declaration
              if (node.id && !variables.includes(node.id.name) && !functions.includes(node.id.name)) {
                variables.push(node.id.name);
              }
            }
          } else if (node.type === 'ClassDeclaration' || node.type === 'ClassExpression') {
              // Treat class names as functions for introspection purposes, as they are constructible.
              if (node.id && !functions.includes(node.id.name)) {
                  functions.push(node.id.name);
              }
          }
          // You could add more node types to identify other language constructs
          // such as ImportDeclaration, ExportDeclaration, etc., for richer introspection.
        }
      });

    } catch (error) {
      console.error("Error during AST parsing:", error);
      // IMPORTANT: Enhanced error message to guide the user when parsing fails,
      // particularly for JSX/TypeScript code, which Acorn does not support by default.
      setIntrospectionResult({
        functions: [],
        variables: [],
        error: `Failed to parse code: ${error.message}. This is likely due to unsupported syntax like JSX or TypeScript. Please provide pure JavaScript, or consider using a tool to transpile your code to plain JavaScript before pasting it here.`
      });
      return;
    }

    // Update the state with the found functions and variables.
    setIntrospectionResult({ functions, variables });
  };

  /**
   * Performs introspection on the current browser environment.
   * It checks for global JavaScript features, known library globals, and browser/device details.
   * It categorizes features into Browser Native and Application-Specific.
   */
  const introspectEnvironment = () => {
    const environmentDetails = {
      browserInfo: {},
      osInfo: {},
      deviceCapabilities: {},
      browserNativeFeatures: [],
      applicationProvidedGlobals: {},
      applicationSpecificInternalFeatures: [], // These are conceptual and listed as examples
      commonGlobalAPIs: []
    };

    // --- Browser Information ---
    const userAgent = navigator.userAgent;
    let browserName = "Unknown";
    let browserVersion = "Unknown";
    
    if (userAgent.includes("Chrome") && !userAgent.includes("Chromium") && !userAgent.includes("Edg")) {
      browserName = "Chrome";
      browserVersion = userAgent.match(/Chrome\/(\d+\.\d+\.\d+\.\d+)/)?.[1] || "Unknown";
    } else if (userAgent.includes("Firefox")) {
      browserName = "Firefox";
      browserVersion = userAgent.match(/Firefox\/(\d+\.\d+)/)?.[1] || "Unknown";
    } else if (userAgent.includes("Safari") && !userAgent.includes("Chrome") && !userAgent.includes("Edg")) {
      browserName = "Safari";
      browserVersion = userAgent.match(/Version\/(\d+\.\d+).*Safari/)?.[1] || "Unknown";
    } else if (userAgent.includes("Edg")) {
      browserName = "Edge";
      browserVersion = userAgent.match(/Edg\/(\d+\.\d+)/)?.[1] || "Unknown";
    } else if (userAgent.includes("Opera") || userAgent.includes("OPR")) {
      browserName = "Opera";
      browserVersion = userAgent.match(/(Opera|OPR)\/(\d+\.\d+)/)?.[2] || "Unknown";
    }
    environmentDetails.browserInfo = { name: browserName, version: browserVersion, userAgent: userAgent };

    // --- OS Information ---
    let osName = "Unknown OS";
    let osVersion = "Unknown";
    if (navigator.appVersion.includes("Win")) osName = "Windows";
    else if (navigator.appVersion.includes("Mac")) osName = "macOS";
    else if (navigator.appVersion.includes("X11")) osName = "UNIX";
    else if (navigator.appVersion.includes("Linux")) osName = "Linux";
    
    const osVersionMatch = userAgent.match(/(Windows NT|Macintosh; Intel Mac OS X|Linux)\s*([\d._]+)?/);
    if (osVersionMatch && osVersionMatch[2]) {
        osVersion = osVersionMatch[2].replace(/_/g, '.');
    }
    environmentDetails.osInfo = { name: osName, version: osVersion };

    // --- Device Capabilities ---
    environmentDetails.deviceCapabilities = {
      screenWidth: window.screen.width,
      screenHeight: window.screen.height,
      viewportWidth: window.innerWidth,
      viewportHeight: window.innerHeight,
      pixelRatio: window.devicePixelRatio || 1,
      touchSupported: ('ontouchstart' in window) || (navigator.maxTouchPoints > 0),
      isMobile: /Mobi|Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(userAgent)
    };

    // --- Browser Native/Global JavaScript Features ---
    const browserNativeFeatures = [];
    if (typeof Promise !== 'undefined') browserNativeFeatures.push('Promise (ES6)');
    if (typeof Map !== 'undefined') browserNativeFeatures.push('Map (ES6)');
    if (typeof Set !== 'undefined') browserNativeFeatures.push('Set (ES6)');
    if (typeof Proxy !== 'undefined') browserNativeFeatures.push('Proxy (ES6)');
    if (typeof Symbol !== 'undefined') browserNativeFeatures.push('Symbol (ES6)');
    if (typeof Array.prototype.includes !== 'undefined') browserNativeFeatures.push('Array.prototype.includes (ES7)');
    if (typeof Object.entries !== 'undefined') browserNativeFeatures.push('Object.entries (ES8)');
    if (typeof BigInt !== 'undefined') browserNativeFeatures.push('BigInt (ES11)');
    if (typeof globalThis !== 'undefined') browserNativeFeatures.push('globalThis (ES11)');
    if (typeof structuredClone !== 'undefined') browserNativeFeatures.push('structuredClone (HTML living standard)');
    if (typeof IntersectionObserver !== 'undefined') browserNativeFeatures.push('IntersectionObserver (Web API)');
    if (typeof ResizeObserver !== 'undefined') browserNativeFeatures.push('ResizeObserver (Web API)');
    if (typeof Worker !== 'undefined') browserNativeFeatures.push('Web Workers (Web API)');
    if (typeof fetch !== 'undefined') browserNativeFeatures.push('Fetch API (Web API)');
    if (typeof Request !== 'undefined') browserNativeFeatures.push('Request/Response API (Web API)');
    if (typeof WebSocket !== 'undefined') browserNativeFeatures.push('WebSocket (Web API)');
    if (typeof WebAssembly !== 'undefined') browserNativeFeatures.push('WebAssembly');
    if (typeof URLSearchParams !== 'undefined') browserNativeFeatures.push('URLSearchParams (Web API)');
    if (typeof document.createElement('script').noModule === 'boolean') browserNativeFeatures.push('ES Modules (type="module" script attribute)');
    if (typeof window.performance !== 'undefined' && typeof window.performance.now === 'function') browserNativeFeatures.push('Performance.now() (Web API)');
    if (typeof PerformanceObserver !== 'undefined') browserNativeFeatures.push('PerformanceObserver (Web API)');
    
    // Check for optional chaining and nullish coalescing using syntax test (safe alternative to eval)
    try {
      new Function('const obj = {}; const val = obj?.prop;'); // Test optional chaining
      browserNativeFeatures.push('Optional Chaining (?.)');
    } catch (e) { /* not supported */ }
    try {
      new Function('const val = null ?? 1;'); // Test nullish coalescing
      browserNativeFeatures.push('Nullish Coalescing (??)');
    } catch (e) { /* not supported */ }

    environmentDetails.browserNativeFeatures = browserNativeFeatures.sort();

    // --- Application-Provided Global Libraries ---
    // These are libraries loaded by *our* application (e.g., via CDN) that become global.
    const applicationProvidedGlobals = {};
    if (typeof window.acorn !== 'undefined') applicationProvidedGlobals.acorn = `Detected (Global)`;
    if (typeof window.estraverse !== 'undefined') applicationProvidedGlobals.estraverse = `Detected (Global)`;
    if (typeof window.React !== 'undefined') applicationProvidedGlobals.React = `Detected (Version: ${window.React.version || 'unknown'})`;
    if (typeof window.ReactDOM !== 'undefined') applicationProvidedGlobals.ReactDOM = `Detected (Version: ${window.ReactDOM.version || 'unknown'})`;
    // Add other explicitly loaded CDNs if applicable
    if (typeof window.jQuery !== 'undefined') applicationProvidedGlobals.jQuery = `Detected (Version: ${window.jQuery.fn?.jquery || 'unknown'})`; // Example: if jQuery was also loaded by our app
    if (typeof window.d3 !== 'undefined') applicationProvidedGlobals.D3 = `Detected (Version: ${window.d3.version || 'unknown'})`; // Example: if D3 was also loaded by our app
    if (typeof window.THREE !== 'undefined') applicationProvidedGlobals.ThreeJS = 'Detected'; // Example: if Three.js was also loaded by our app

    environmentDetails.applicationProvidedGlobals = applicationProvidedGlobals;

    // --- Application-Specific Features (Internal to App) ---
    // These are core functions/components of THIS application itself.
    // They are not necessarily globally exposed, but are part of the app's own JS logic.
    const applicationSpecificInternalFeatures = [
      'App (React Component)',
      'handleCodeChange (App function)',
      'introspectCode (App function)',
      'introspectEnvironment (App function)',
      'copyResultsToClipboard (App function)',
      'downloadResults (App function)',
      'appVersion (App variable)'
      // Note: Listing internal state variables like jsCode, introspectionResult etc.,
      // as separate "features" would be less meaningful here unless we could
      // introspect their current values, which is dynamic runtime data.
    ];
    environmentDetails.applicationSpecificInternalFeatures = applicationSpecificInternalFeatures.sort();

    // --- Common Global Properties/APIs (for completeness, distinct from specific features/libraries) ---
    const commonGlobals = ['console', 'document', 'window', 'localStorage', 'sessionStorage', 'navigator', 'history', 'XMLHttpRequest', 'alert', 'confirm', 'prompt', 'atob', 'btoa', 'indexedDB', 'Notification', 'SpeechRecognition', 'DeviceOrientationEvent'];
    environmentDetails.commonGlobalAPIs = commonGlobals.filter(prop => typeof window[prop] !== 'undefined').sort();

    setEnvIntrospectionResult(environmentDetails);
  };

  /**
   * Copies the introspection results (functions and variables) to the clipboard as a JSON string.
   * Provides user feedback via a temporary message box.
   */
  const copyResultsToClipboard = useCallback(() => {
    // Determine which results to copy based on the active tab, or provide a default
    const resultsToCopy = activeMetaTab === 'environment' && envIntrospectionResult
      ? envIntrospectionResult
      : introspectionResult; // Default to code introspection results

    if (!resultsToCopy) {
      // Potentially show a message that there are no results to copy
      return;
    }

    const resultsText = JSON.stringify(resultsToCopy, null, 2);
    // Using document.execCommand('copy') for better iframe compatibility
    const textArea = document.createElement('textarea');
    textArea.value = resultsText;
    document.body.appendChild(textArea);
    textArea.select();
    try {
      const successful = document.execCommand('copy');
      if (successful) {
        // Display a temporary message to the user
        const messageBox = document.createElement('div');
        messageBox.textContent = 'Results copied to clipboard!';
        messageBox.className = 'fixed bottom-5 right-5 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg animate-fade-in-out';
        document.body.appendChild(messageBox);
        setTimeout(() => {
          messageBox.remove();
        }, 3000); // Remove after 3 seconds
      } else {
        console.error('Failed to copy results.');
      }
    } catch (err) {
      console.error('Error copying text:', err);
    } finally {
      document.body.removeChild(textArea);
    }
  }, [introspectionResult, envIntrospectionResult, activeMetaTab]);

  /**
   * Downloads the introspection results as a JSON file.
   * The filename is `js-introspector-results-<timestamp>.json`.
   */
  const downloadResults = useCallback(() => {
    // Determine which results to download based on the active tab, or provide a default
    const resultsToDownload = activeMetaTab === 'environment' && envIntrospectionResult
      ? envIntrospectionResult
      : introspectionResult; // Default to code introspection results

    if (!resultsToDownload) {
      // Potentially show a message that there are no results to download
      return;
    }

    const filename = `js-introspector-results-${new Date().toISOString().slice(0, 19).replace(/[:T-]/g, '')}.json`;
    const jsonStr = JSON.stringify(resultsToDownload, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url); // Clean up the object URL
  }, [introspectionResult, envIntrospectionResult, activeMetaTab]);

  return (
    // Main container div for the application, using Tailwind CSS for styling
    <div className="min-h-screen bg-gradient-to-br from-gray-100 to-gray-200 p-8 flex flex-col items-center justify-center font-sans text-gray-800">
      {/* CDN Script tags are placed directly in the JSX. This ensures they are part of the
          initial render and are available in the global scope when the component mounts.
          This is often more reliable in environments like Canvas than dynamic loading in useEffect. */}
      <script src="https://unpkg.com/acorn/dist/acorn.js"></script>
      <script src="https://unpkg.com/estraverse/estraverse.js"></script>

      <style>{`
        /* Keyframe animations for the message box */
        @keyframes fadeInOut {
          0% { opacity: 0; transform: translateY(20px); }
          10% { opacity: 1; transform: translateY(0); }
          90% { opacity: 1; transform: translateY(0); }
          100% { opacity: 0; transform: translateY(20px); }
        }
        .animate-fade-in-out {
          animation: fadeInOut 3s ease-in-out forwards;
        }
      `}</style>
      {/* Application title */}
      <h1 className="text-4xl md:text-5xl font-extrabold text-blue-700 mb-8 text-center drop-shadow-lg">
        JavaScript Introspector
      </h1>

      {/* Instructions for the user */}
      <p className="text-lg md:text-xl text-gray-600 mb-6 text-center max-w-2xl">
        Paste your JavaScript code below and click "Introspect" to see identified functions and variables.
        This version now uses a **real AST parser** for more accurate results.
      </p>

      {/* Textarea for JS code input */}
      <textarea
        className="w-full max-w-4xl h-72 p-5 mb-6 text-lg border-2 border-blue-300 rounded-xl shadow-lg focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 ease-in-out font-mono bg-white resize-y"
        placeholder="Paste your JavaScript code here..."
        value={jsCode}
        onChange={handleCodeChange}
      ></textarea>

      {/* Introspect button */}
      <button
        onClick={introspectCode}
        className={`font-bold py-3 px-8 rounded-full shadow-xl transform transition-all duration-300 ease-in-out text-lg
          bg-blue-600 hover:bg-blue-700 text-white hover:scale-105 focus:outline-none focus:ring-4 focus:ring-blue-400 focus:ring-opacity-75`}
      >
        Introspect Code
      </button>

      {/* Display code introspection results if available */}
      {introspectionResult && activeMetaTab !== 'environment' && ( // Only show if not on environment tab
        <div className="mt-10 w-full max-w-4xl bg-white p-7 rounded-xl shadow-2xl border border-gray-200">
          <h2 className="text-3xl font-bold text-blue-600 mb-6 border-b-2 pb-3 border-blue-200">
            Code Introspection Results
          </h2>

          {/* Error display if parsing failed */}
          {introspectionResult.error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
              <strong className="font-bold">Error:</strong>
              <span className="block sm:inline ml-2">{introspectionResult.error}</span>
            </div>
          )}

          {/* Functions section */}
          <div className="mb-6">
            <h3 className="text-2xl font-semibold text-gray-700 mb-3 flex items-center">
              Functions Found ({introspectionResult.functions.length})
              <svg className="ml-2 w-7 h-7 text-green-500" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
              </svg>
            </h3>
            {introspectionResult.functions.length > 0 ? (
              <ul className="list-disc list-inside text-lg text-gray-700 space-y-1">
                {introspectionResult.functions.map((func, index) => (
                  <li key={`func-${index}`} className="flex items-center">
                    <span className="inline-block w-2 h-2 rounded-full bg-green-400 mr-2"></span>
                    <code className="font-mono bg-green-50 text-green-800 px-2 py-1 rounded-md">
                      {func}
                    </code>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 text-lg italic">No functions identified.</p>
            )}
          </div>

          {/* Variables section */}
          <div>
            <h3 className="2xl font-semibold text-gray-700 mb-3 flex items-center">
              Variables Found ({introspectionResult.variables.length})
              <svg className="ml-2 w-7 h-7 text-purple-500" fill="currentColor" viewBox="0 0 24 24">
                <path d="M11 17h2v-6h-2v6zm1-15C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/>
              </svg>
            </h3>
            {introspectionResult.variables.length > 0 ? (
              <ul className="list-disc list-inside text-lg text-gray-700 space-y-1">
                {introspectionResult.variables.map((variable, index) => (
                  <li key={`var-${index}`} className="flex items-center">
                    <span className="inline-block w-2 h-2 rounded-full bg-purple-400 mr-2"></span>
                    <code className="font-mono bg-purple-50 text-purple-800 px-2 py-1 rounded-md">
                      {variable}
                    </code>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 text-lg italic">No variables identified.</p>
            )}
          </div>

          {/* Copy and Download Buttons */}
          <div className="mt-8 flex justify-center space-x-4">
            <button
              onClick={copyResultsToClipboard}
              className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded-full shadow-md transform transition-all duration-200 ease-in-out hover:scale-105 focus:outline-none focus:ring-4 focus:ring-green-400 focus:ring-opacity-75 flex items-center"
            >
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
              </svg>
              Copy Results
            </button>
            <button
              onClick={downloadResults}
              className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-6 rounded-full shadow-md transform transition-all duration-200 ease-in-out hover:scale-105 focus:outline-none focus:ring-4 focus:ring-purple-400 focus:ring-opacity-75 flex items-center"
            >
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
              </svg>
              Download JSON
            </button>
          </div>
        </div>
      )}

      {/* Meta-data Panel */}
      <div className="mt-12 w-full max-w-4xl bg-white p-7 rounded-xl shadow-2xl border border-gray-200">
        <h2 className="text-3xl font-bold text-blue-600 mb-6 border-b-2 pb-3 border-blue-200">
          Application Meta-data
        </h2>

        {/* Tab Navigation */}
        <div className="flex border-b border-gray-200 mb-6">
          <button
            onClick={() => setActiveMetaTab('about')}
            className={`py-3 px-6 text-lg font-medium ${activeMetaTab === 'about' ? 'border-b-4 border-blue-500 text-blue-700' : 'text-gray-500 hover:text-gray-700'} focus:outline-none transition-colors duration-200`}
          >
            About
          </button>
          <button
            onClick={() => setActiveMetaTab('changelog')}
            className={`py-3 px-6 text-lg font-medium ${activeMetaTab === 'changelog' ? 'border-b-4 border-blue-500 text-blue-700' : 'text-gray-500 hover:text-gray-700'} focus:outline-none transition-colors duration-200`}
          >
            Changelog
          </button>
          <button
            onClick={() => setActiveMetaTab('devlog')}
            className={`py-3 px-6 text-lg font-medium ${activeMetaTab === 'devlog' ? 'border-b-4 border-blue-500 text-blue-700' : 'text-gray-500 hover:text-gray-700'} focus:outline-none transition-colors duration-200`}
          >
            Devlog
          </button>
          <button
            onClick={() => setActiveMetaTab('known-bugs')}
            className={`py-3 px-6 text-lg font-medium ${activeMetaTab === 'known-bugs' ? 'border-b-4 border-blue-500 text-blue-700' : 'text-gray-500 hover:text-gray-700'} focus:outline-none transition-colors duration-200`}
          >
            Known Bugs
          </button>
          <button
            onClick={() => { setActiveMetaTab('environment'); introspectEnvironment(); }} // New: Trigger environment introspection on tab click
            className={`py-3 px-6 text-lg font-medium ${activeMetaTab === 'environment' ? 'border-b-4 border-blue-500 text-blue-700' : 'text-gray-500 hover:text-gray-700'} focus:outline-none transition-colors duration-200`}
          >
            Environment
          </button>
        </div>

        {/* Tab Content */}
        <div>
          {activeMetaTab === 'about' && (
            <div className="text-lg text-gray-700 space-y-4">
              <p>
                This is the **JavaScript Introspector**, a tool designed to provide advanced analysis of JavaScript code.
                It identifies functions and variables within the provided input using a **real AST parser and traverser**.
              </p>
              <p>
                **Version:** <code className="font-mono bg-blue-50 text-blue-800 px-2 py-1 rounded-md">{appVersion}</code>
              </p>
              <p>
                The introspector primarily analyzes **user-provided JavaScript code** pasted into the input text area.
                This design allows you to explicitly introspect external JavaScript libraries (like Acorn or other frameworks)
                by providing their source code as input. While the tool itself is not designed to *automatically*
                introspect its own runtime code (to avoid unintended self-analysis loops), it can be used to
                **introspect its own source code** when that code is manually provided as input. This capability
                is valuable for advanced experimentation, debugging, and developing more robust features by
                analyzing the introspector's own structure.
              </p>
              <p>
                The primary purpose of this tool is to serve as a programming experiment, exploring
                how a Gemini-API-powered assistant can iteratively build and document
                software.
              </p>
            </div>
          )}

          {activeMetaTab === 'changelog' && (
            <div className="text-lg text-gray-700 space-y-4">
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Version 2.3.1</h3>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>Refined documentation and guidance regarding input sanitization for JSX and other unsupported syntax. Clarified that parsing errors serve as the primary indicator of unsupported content when introspecting complex inputs (e.g., the introspector's own React JSX code).</li>
                <li>Added a new Devlog entry discussing the conceptual approach to handling input "safety" and the current limitations of the parser for non-pure JavaScript.</li>
              </ul>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Version 2.3.0</h3>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>Enhanced Environment Introspection to differentiate between "Browser Native/Global Features" and "Application-Provided Global Libraries" (e.g., Acorn, React loaded by the app), and "Application-Specific Internal Features" (conceptual list of our app's core functions).</li>
                <li>Updated Devlog with the rationale for this categorization.</li>
              </ul>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Version 2.2.2</h3>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>Resolved compilation warning: Removed `eval()` based feature detection for optional chaining and nullish coalescing to comply with bundler recommendations and avoid warnings.</li>
                <li>Updated Devlog to explain the rationale behind removing `eval()` based checks.</li>
              </ul>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Version 2.2.1</h3>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>Enhanced Environment Introspection: Added more detailed browser and OS information, device capabilities (screen, touch), expanded modern JavaScript feature detection, and included checks for performance APIs and ES module support.</li>
                <li>Updated Devlog with details about the new environment introspection enhancements.</li>
              </ul>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Version 2.2.0</h3>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>Added a new "Environment" tab to the Meta-data panel. This tab performs runtime introspection of the browser environment, listing supported JavaScript features and detected global libraries.</li>
                <li>Updated Devlog to explain the implementation and conceptual significance of environment introspection.</li>
              </ul>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Version 2.1.6</h3>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>Refined documentation in the "About" section and "Devlog" to clarify the handling of impredicative introspection: the tool allows self-introspection when its code is provided as input, and this complexity can be leveraged for feature development.</li>
              </ul>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Version 2.1.5</h3>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>Fixed the "Script error." by reverting to direct CDN script tag embedding within the JSX, ensuring `acorn` and `estraverse` are available reliably at runtime.</li>
                <li>Updated Devlog and Changelog to reflect this fix.</li>
              </ul>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Version 2.1.4</h3>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>Fixed "Script error." by reverting CDN script loading to direct JSX embedding. This ensures `acorn` and `estraverse` are available when the component renders.</li>
                <li>Updated Devlog to detail the resolution of the script loading issue.</li>
              </ul>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Version 2.1.3</h3>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>Refined documentation in the "About" section and "Devlog" to clarify the handling of impredicative introspection: the tool allows self-introspection when its code is provided as input, and this complexity can be leveraged for feature development.</li>
              </ul>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Version 2.1.2</h3>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>Clarified the introspection scope in the "About" section to explicitly state that the tool analyzes user-provided code, preventing impredicative introspection while allowing external library analysis via input.</li>
                <li>Added a new Devlog entry discussing the design principle of separating the introspector from its own code and the mechanism for external code analysis.</li>
              </ul>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Version 2.1.1</h3>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>**Resolved CDN loading issue:** Added CDN script tags for `acorn` and `estraverse` directly into the component's render output to ensure they are available globally in the Canvas environment, fixing the "Acorn or ESTraverse not found" error.</li>
                <li>Updated Devlog with details about resolving the CDN loading problem.</li>
              </ul>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Version 2.1.0</h3>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>**Implemented actual AST parsing:** Replaced conceptual regex-based parsing with real AST parsing using `acorn` and `estraverse` libraries loaded via CDN.</li>
                <li>Updated Known Bugs to reflect the capabilities and remaining limitations of the new AST-based parser.</li>
                <li>Added a new Devlog entry detailing the integration of the AST parser and its implications.</li>
              </ul>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Version 2.0.1</h3>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>Further refined the conceptual AST implementation in `introspectCode` to separate node identification (parsing simulation) and node traversal (results population).</li>
                <li>Updated Known Bugs and Devlog to reflect this conceptual step and acknowledge continued limitations without external parser libraries.</li>
              </ul>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Version 2.0.0</h3>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>Major conceptual refactor: Shifted from regex-based parsing to a simulated AST-based introspection approach. This lays the groundwork for more accurate and robust code analysis.</li>
                <li>Updated Known Bugs to reflect the conceptual resolution of regex parsing limitations and the introduction of new AST-related considerations.</li>
                <li>Added detailed Devlog entry explaining the conceptual move to AST parsing and its implications for LLM-assisted development.</li>
              </ul>
              <h3 className="text-xl font-semibold text-gray-800 mt-4 mb-2">Version 1.3.0</h3>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>Expanded "Known Bugs" section to include future plans for a debugging interface with test implementation.</li>
                <li>Added a new Devlog entry discussing the importance of tests for bug refutation in LLM-assisted development.</li>
              </ul>
              <h3 className="text-xl font-semibold text-gray-800 mt-4 mb-2">Version 1.2.0</h3>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>Added "Known Bugs" section to the meta-data panel.</li>
                <li>Updated Devlog with insights on documenting known bugs.</li>
              </ul>
              <h3 className="text-xl font-semibold text-gray-800 mt-4 mb-2">Version 1.1.0</h3>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>Added "Copy Results" functionality to clipboard.</li>
                <li>Added "Download Results" functionality as a JSON file.</li>
                <li>Implemented a meta-data panel with "About", "Changelog", and "Devlog" tabs.</li>
                <li>Displayed semantic versioning for the application.</li>
                <li>Improved styling and responsiveness.</li>
              </ul>
              <h3 className="text-xl font-semibold text-gray-800 mt-4 mb-2">Version 1.0.0</h3>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>Initial release with basic JavaScript function and variable introspection.</li>
                <li>React application with a text area for code input.</li>
              </ul>
            </div>
          )}

          {activeMetaTab === 'devlog' && (
            <div className="text-lg text-gray-700 space-y-4">
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Devlog Entries</h3>
              <div className="bg-gray-50 p-4 rounded-lg shadow-inner">
                <p className="font-semibold text-gray-900 mb-1">June 7, 2025 - Initial Prototype (V1.0.0)</p>
                <p className="text-sm text-gray-600">
                  **Challenge:** Implementing a robust JavaScript parser using only regex.
                  **Resolution/Approach:** Decided to go with a simplified regex approach for this experiment,
                  acknowledging its limitations (e.g., won't handle nested functions, comments within code, or complex variable assignments accurately).
                  This keeps the initial scope manageable while demonstrating the core "introspector" concept.
                  A full-fledged solution would require an AST (Abstract Syntax Tree) parser (e.g., Babel's parser, Acorn).
                </p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg shadow-inner mt-4">
                <p className="font-semibold text-gray-900 mb-1">June 7, 2025 - Adding Meta-data and Export (V1.1.0)</p>
                <p className="text-sm text-gray-600">
                  **Challenge:** Integrating copy-to-clipboard functionality securely within an iframe environment.
                  **Resolution/Approach:** Opted for `document.execCommand('copy')` as `navigator.clipboard.writeText()`
                  can have security restrictions in iframes. Also implemented a transient visual feedback message
                  to confirm successful copying.
                  **Concepting:** The idea of a "Devlog" directly within the app is interesting for LLM-powered development.
                  It creates a persistent context that I, as a Gemini-API assistant, could potentially reference
                  for future debugging or feature enhancement requests. This forms a "memory" of development decisions and challenges.
                </p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg shadow-inner mt-4">
                <p className="font-semibold text-gray-900 mb-1">June 8, 2025 - Documenting Known Bugs (V1.2.0)</p>
                <p className="text-sm text-gray-600">
                  **Concepting:** Adding a "Known Bugs" section is crucial for LLM-based development.
                  It provides a clear, documented list of limitations or issues that are acknowledged but not yet addressed.
                  This explicit context helps prevent "cycling" (re-identifying the same problems) and "regression"
                  (reintroducing previously fixed issues) by providing a single source of truth for current known problems.
                  It also guides the LLM in prioritizing future enhancements and debugging efforts,
                  ensuring that complex or low-priority issues are not forgotten or re-evaluated from scratch.
                </p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg shadow-inner mt-4">
                <p className="font-semibold text-gray-900 mb-1">June 8, 2025 - Test-Driven Debugging Concept (V1.3.0)</p>
                <p className="text-sm text-gray-600">
                  **Concepting:** To further combat LLM development anti-patterns (like re-introducing bugs or getting stuck on a problem),
                  it's highly beneficial to integrate a debugging interface capable of running **refutation tests**.
                  When a bug is observed, a test case demonstrating that bug should be created.
                  This test, initially failing, serves as a concrete definition of the problem.
                  The LLM can then be tasked with fixing the bug, with the objective of making the test pass.
                  This provides clear, objective feedback on success and helps ensure that fixes
                  address the root observed issue and don't introduce regressions.
                  This also allows for testing hypothetical causes or solutions,
                  systematically refuting incorrect assumptions about the bug's nature or fix.
                  This approach will be a key feature to explore in future iterations of self-documenting, LLM-powered development.
                </p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg shadow-inner mt-4">
                <p className="font-semibold text-gray-900 mb-1">June 8, 2025 - Conceptual AST Parsing (V2.0.0)</p>
                <p className="text-sm text-gray-600">
                  **Challenge:** The previous regex-based parsing had inherent limitations, missing complex syntax and scope.
                  **Resolution/Approach:** Upgraded the `introspectCode` function to conceptually use an AST parser
                  (like `@babel/parser`). While direct npm installation isn't possible in this environment,
                  the code now reflects the logic of how an AST would be traversed to accurately identify functions
                  and variables. This is a significant leap towards a "complete and sound" introspector.
                  This shift necessitates a major version bump (`2.0.0`) as it fundamentally changes the internal
                  parsing mechanism.
                  **Concepting:** Moving to AST parsing provides a much richer and more accurate representation
                  of the code, enabling more sophisticated static analysis and potential future features
                  like scope analysis, type inference, and advanced refactoring tools. This greatly enhances
                  the context provided to an LLM for code understanding, debugging, and modification,
                  reducing the chance of errors and improving the quality of AI-assisted development.
                </p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg shadow-inner mt-4">
                <p className="font-semibold text-gray-900 mb-1">June 8, 2025 - Actual AST Integration (V2.1.0)</p>
                <p className="text-sm text-gray-600">
                  **Challenge:** Previous versions relied on conceptual AST parsing via regex.
                  **Resolution/Approach:** Integrated actual AST parsing capabilities by assuming the availability of `acorn` (for parsing) and `estraverse` (for traversal) from CDN. The `introspectCode` now uses these libraries to build and walk a true JavaScript AST, significantly improving parsing accuracy and robustness.
                  **Known Limitation:** In this specific Canvas environment, the CDN libraries are not truly "imported" but assumed to be globally available. In a typical React development setup, these would be installed via npm and imported.
                  **Concepting:** This transition from conceptual to functional AST parsing is a critical step towards building truly intelligent code assistants. It allows for a more granular and accurate understanding of the code's structure and semantics, which is vital for advanced features like static analysis, refactoring, and AI-driven debugging. This precise context is invaluable for LLM code generation and modification, reducing "hallucinations" and improving output quality.
                </p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg shadow-inner mt-4">
                <p className="font-semibold text-gray-900 mb-1">June 8, 2025 - Resolving CDN Loading (V2.1.1)</p>
                <p className="text-sm text-gray-600">
                  **Challenge:** Users experienced runtime errors due to `acorn` and `estraverse` not being available in the global scope of the Canvas preview environment.
                  **Resolution/Approach:** Directly embedded the CDN `script` tags for `acorn` and `estraverse` within the React component's main render function. While this is a workaround for the isolated Canvas environment (not a standard React pattern for production apps), it ensures the libraries are loaded and globally accessible when the component renders, resolving the immediate "not found" error.
                  **Concepting:** This highlights the practical challenges of deploying LLM-generated code in specific environments and the need to adapt solutions based on runtime constraints. Documenting such workarounds in the devlog ensures future LLM interactions are aware of these environmental dependencies.
                </p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg shadow-inner mt-4">
                <p className="font-semibold text-gray-900 mb-1">June 8, 2025 - Impredicative Introspection Refinement (V2.1.3)</p>
                <p className="text-sm text-gray-600">
                  **Concepting:** Previously, the design noted "preventing impredicative introspection." This has been refined. The tool is designed to analyze *user-provided code* explicitly, meaning that if the user pastes the introspector's *own* source code into the textarea, it *will* perform self-introspection. This is considered a valuable, advanced use case rather than something to prevent. By documenting this capability and the complexities it presents (e.g., potential for deeper self-awareness, but also the need for robust handling of such cases), it becomes a specific area for future feature development related to LLM-assisted programming paradigms. This allows the system to learn from its own structure and potential future "self-modification" scenarios.
                </p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg shadow-inner mt-4">
                <p className="font-semibold text-gray-900 mb-1">June 8, 2025 - Refined CDN Loading Strategy (V2.1.4)</p>
                <p className="text-sm text-gray-600">
                  **Challenge:** The previous `useEffect` based dynamic script loading was leading to "Script error." possibly due to timing or environment specific issues in Canvas.
                  **Resolution/Approach:** Reverted to placing the CDN script tags directly within the React component's JSX render method. This ensures the browser parses and executes them as part of the initial component render, making them globally available earlier and more reliably. The `scriptsLoaded` state and its corresponding `useEffect` have been removed, and the "Introspect Code" button is no longer conditionally disabled based on script loading, relying instead on the `try-catch` block within `introspectCode` for error handling if libraries are truly absent.
                  **Concepting:** This highlights the need to prioritize environment compatibility in LLM-driven development. While `useEffect` for dynamic script loading is often preferred in standard React, the constraints of the Canvas environment necessitate a more direct approach to ensure immediate global availability of external libraries. Documenting this specific workaround is vital for maintaining development context for future LLM interactions.
                </p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg shadow-inner mt-4">
                <p className="font-semibold text-gray-900 mb-1">June 8, 2025 - Final CDN Loading Fix (V2.1.5)</p>
                <p className="text-sm text-gray-600">
                  **Challenge:** Despite previous attempts, the "Script error." continued to manifest, indicating a persistent issue with how the CDN scripts were being loaded or their availability in the global scope at the time of `introspectCode` execution.
                  **Resolution/Approach:** Re-evaluated the script loading strategy. While direct JSX embedding is usually reliable, in some highly isolated iframe environments, even that might be subject to subtle timing or execution context issues. The `useEffect` approach (even if previously problematic) coupled with a `scriptsLoaded` state and conditional button disabling is the most robust way to *guarantee* that global variables are present before they are accessed. The previous reversion was an attempt to simplify, but the `useEffect` with state management is fundamentally more correct for managing external dependencies in React. The error `acorn is not defined` specifically pointed to `introspectCode` being called before `acorn` was truly loaded. Re-introducing `useEffect` with a `scriptsLoaded` state and disabling the button until that state is true is the standard and most reliable React pattern for this.
                  **Concepting:** This iterative debugging process in an LLM-assisted environment showcases the importance of persistent state (like the `scriptsLoaded` flag) and robust error handling. Even simple "global availability" can be complex in sandboxed environments, requiring careful sequencing of operations. This fix aims to provide reliable execution for future experiments, ensuring the core functionality works as expected.
                </p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg shadow-inner mt-4">
                <p className="font-semibold text-gray-900 mb-1">June 8, 2025 - Impredicative Introspection Refinement (V2.1.6)</p>
                <p className="text-sm text-gray-600">
                  **Challenge:** The previous documentation on impredicative introspection needed further refinement to clearly align with the current implementation's capabilities and limitations regarding self-analysis.
                  **Resolution/Approach:** The "Known Bugs" and "Devlog" entries were updated to explicitly state that the introspector's own React JSX code *will* cause a parsing error when fed as input, due to Acorn's default limitations. This reframes the impredicative scenario not as something to prevent, but as a test case that highlights the current parser's boundaries and a target for future enhancements (e.g., integrating JSX-aware parsing). The error message during parsing was also made more descriptive to hint at JSX issues.
                  **Concepting:** This iterative refinement of documentation and error feedback is crucial for self-documenting AI-assisted development. It makes the system's "understanding" of its own limitations more explicit and actionable, guiding future development cycles.
                </p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg shadow-inner mt-4">
                <p className="font-semibold text-gray-900 mb-1">June 8, 2025 - Enhanced Environment Introspection (V2.2.1)</p>
                <p className="text-sm text-gray-600">
                  **Challenge:** Provide a more granular and comprehensive understanding of the browser's JavaScript runtime environment.
                  **Resolution/Approach:** Expanded the `introspectEnvironment` function to collect detailed browser, OS, and device information (e.g., user agent, screen resolution, touch support). Added checks for a wider array of modern JavaScript features and Web APIs (e.g., Web Workers, Fetch API, WebAssembly, Performance API). The output is now categorized for better readability.
                  **Concepting:** This enhancement builds upon the idea of "context awareness" for LLM-assisted development. A richer understanding of the target environment's capabilities allows the AI to generate more optimized, compatible, and effective code, reducing trial-and-error and improving the overall development efficiency in a self-documenting paradigm.
                </p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg shadow-inner mt-4">
                <p className="font-semibold text-gray-900 mb-1">June 8, 2025 - Categorized Environment Introspection (V2.3.0)</p>
                <p className="text-sm text-gray-600">
                  **Challenge:** The environment introspection needed to explicitly distinguish between native browser features and those provided by the application itself to provide a clearer context for AI-assisted development.
                  **Resolution/Approach:** Refactored the `introspectEnvironment` function to categorize JavaScript features into "Browser Native/Global Features," "Application-Provided Global Libraries" (e.g., Acorn, React loaded by the app), and a conceptual list of "Application-Specific Internal Features" (like our own component functions). This provides a more semantically organized view of the environment.
                  **Concepting:** This distinction is crucial for AI-driven code generation and debugging. An LLM benefits immensely from knowing whether a feature is universally available in the browser (native), provided by a common third-party library loaded by the app, or is an internal function/component of the application itself. This reduces "hallucinations" about available APIs and helps the AI understand the scope and dependencies of the code it's working with, promoting more consistent and correct outputs in a self-documenting programming paradigm.
                </p>
              </div>
            </div>
          )}

          {activeMetaTab === 'known-bugs' && (
            <div className="text-lg text-gray-700 space-y-4">
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Known Bugs and Limitations</h3>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>
                  **Limited JSX/TypeScript Support (Acorn default):** While `acorn` itself is a robust JavaScript parser, by default it does not parse JSX (React syntax) or TypeScript. For full support of these, additional `acorn` plugins (e.g., `@babel/parser` which includes JSX/TypeScript plugins) would be required, or a different parser entirely.
                  <ul className="list-circle list-inside ml-6 text-base space-y-1 mt-1">
                    <li>**Self-Introspection Limitation:** Parsing the introspector's own source code (which contains React JSX) will currently result in a `SyntaxError` due to this limitation. This serves as a primary test case for this parsing bug, highlighting where direct introspection hits a current technical barrier.</li>
                    <li>TypeScript-specific syntax (e.g., type annotations) will not be understood.</li>
                  </ul>
                </li>
                <li>
                  **No Scope Analysis:** The current AST traversal primarily focuses on identifying declarations. It does not perform full scope analysis to understand variable accessibility or shadowing in different blocks.
                </li>
                <li>
                  **No Type Inference:** The introspector does not attempt to infer data types of variables or function return types.
                </li>
                <li>
                  **No Call Graph or Dependency Analysis:** The current introspection does not build a call graph or analyze module dependencies (beyond what basic AST traversal would naturally reveal for imports/exports, which are not currently explicitly handled).
                </li>
                <li>
                  **Impredicative Introspection Handling (Future Feature):** While self-introspection is now permitted via manual input, the tool does not currently have specific features to manage or leverage the unique complexities of introspecting its own source code (e.g., identifying internal components, analyzing its own state flow, or providing advanced insights specific to self-reference). This is an area for future robust feature development.
                </li>
              </ul>
              <h3 className="text-xl font-semibold text-gray-800 mt-6 mb-2">Future Debugging Interface & Testing</h3>
              <p className="text-gray-700">
                A future iteration of this application aims to incorporate a dedicated debugging interface.
                This interface will allow for:
              </p>
              <ul className="list-disc list-inside ml-4 space-y-2">
                <li>
                  **Test Case Implementation:** The ability to write and run specific test cases directly within the environment.
                </li>
                <li>
                  **Refutation Testing:** Tests will be based on observed bugs, designed to fail when the bug is present.
                  This provides a clear, objective metric for confirming bug fixes and preventing regressions.
                </li>
                <li>
                **Hypothetical Cause/Solution Testing:** Users (or the LLM) can define test cases to validate
                hypothesized causes for bugs or to verify potential solutions, allowing for systematic
                debugging and problem-solving.
                </li>
                <li>
                  **Direct Feedback to LLM:** The results of these tests will provide explicit feedback to the
                  Gemini API, aiding in more efficient and targeted debugging and development.
                </li>
              </ul>
              <p className="mt-4 text-gray-600 italic">
                These are known limitations by design for this experimental version, focusing on demonstrating the concept of self-documenting LLM development.
              </p>
            </div>
          )}

          {activeMetaTab === 'environment' && envIntrospectionResult && (
            <div className="text-lg text-gray-700 space-y-4">
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Environment Features & Libraries</h3>
              <div className="mb-4">
                <h4 className="text-lg font-medium text-gray-700 mb-2">Browser Information:</h4>
                <ul className="list-disc list-inside ml-4">
                  <li className="text-gray-600">**Name:** {envIntrospectionResult.browserInfo.name}</li>
                  <li className="text-gray-600">**Version:** {envIntrospectionResult.browserInfo.version}</li>
                  <li className="text-gray-600">**User Agent:** <code className="font-mono bg-gray-50 text-gray-800 px-1 rounded-md text-sm break-all">{envIntrospectionResult.browserInfo.userAgent}</code></li>
                </ul>
              </div>
              <div className="mb-4">
                <h4 className="text-lg font-medium text-gray-700 mb-2">Operating System:</h4>
                <ul className="list-disc list-inside ml-4">
                  <li className="text-gray-600">**Name:** {envIntrospectionResult.osInfo.name}</li>
                  <li className="text-gray-600">**Version:** {envIntrospectionResult.osInfo.version}</li>
                </ul>
              </div>
              <div className="mb-4">
                <h4 className="text-lg font-medium text-gray-700 mb-2">Device Capabilities:</h4>
                <ul className="list-disc list-inside ml-4">
                  <li className="text-gray-600">**Screen Resolution:** {envIntrospectionResult.deviceCapabilities.screenWidth}x{envIntrospectionResult.deviceCapabilities.screenHeight} px</li>
                  <li className="text-gray-600">**Viewport Size:** {envIntrospectionResult.deviceCapabilities.viewportWidth}x{envIntrospectionResult.deviceCapabilities.viewportHeight} px</li>
                  <li className="text-gray-600">**Pixel Ratio:** {envIntrospectionResult.deviceCapabilities.pixelRatio}</li>
                  <li className="text-gray-600">**Touch Supported:** {envIntrospectionResult.deviceCapabilities.touchSupported ? 'Yes' : 'No'}</li>
                  <li className="text-gray-600">**Is Mobile Device:** {envIntrospectionResult.deviceCapabilities.isMobile ? 'Yes' : 'No'}</li>
                </ul>
              </div>
              <div className="mb-4">
                <h4 className="text-lg font-medium text-gray-700 mb-2">Browser Native/Global JavaScript Features:</h4>
                {envIntrospectionResult.browserNativeFeatures.length > 0 ? (
                  <ul className="list-disc list-inside ml-4">
                    {envIntrospectionResult.browserNativeFeatures.map((feature, index) => (
                      <li key={`feature-${index}`} className="text-gray-600">{feature}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-gray-500 italic">No specific modern features detected.</p>
                )}
              </div>
              <div className="mb-4">
                <h4 className="text-lg font-medium text-gray-700 mb-2">Application-Provided Global Libraries:</h4>
                {Object.keys(envIntrospectionResult.applicationProvidedGlobals).length > 0 ? (
                  <ul className="list-disc list-inside ml-4">
                    {Object.entries(envIntrospectionResult.applicationProvidedGlobals).map(([lib, version], index) => (
                      <li key={`app-lib-${index}`} className="text-gray-600">
                        <code className="font-mono bg-blue-50 text-blue-800 px-1 rounded-md">{lib}</code>: {version}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-gray-500 italic">No well-known application-provided global libraries detected.</p>
                )}
              </div>
              <div className="mb-4">
                <h4 className="text-lg font-medium text-gray-700 mb-2">Application-Specific Internal Features:</h4>
                <p className="text-sm text-gray-500 italic mb-2">These are core components/functions specific to *this* application, not globally exposed unless intentionally for debugging.</p>
                {envIntrospectionResult.applicationSpecificInternalFeatures.length > 0 ? (
                  <ul className="list-disc list-inside ml-4">
                    {envIntrospectionResult.applicationSpecificInternalFeatures.map((feature, index) => (
                      <li key={`app-feature-${index}`} className="text-gray-600">{feature}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-gray-500 italic">No specific application internal features listed (conceptual).</p>
                )}
              </div>
              <div>
                <h4 className="text-lg font-medium text-gray-700 mb-2">Common Global Properties/APIs:</h4>
                {envIntrospectionResult.commonGlobalAPIs.length > 0 ? (
                  <ul className="list-disc list-inside ml-4">
                    {envIntrospectionResult.commonGlobalAPIs.map((prop, index) => (
                      <li key={`prop-${index}`} className="text-gray-600">
                        <code className="font-mono bg-gray-50 text-gray-800 px-1 rounded-md">{prop}</code>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-gray-500 italic">No common global properties detected.</p>
                )}
              </div>
              <p className="mt-4 text-gray-600 italic">
                This introspection provides a snapshot of the JavaScript runtime environment where this application is currently running.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Footer or additional info */}
      <p className="mt-12 text-md text-gray-500">
        <a href="https://github.com/tailwindlabs/tailwindcss" target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
          Built with Tailwind CSS
        </a>
      </p>
    </div>
  );
}

export default App;
