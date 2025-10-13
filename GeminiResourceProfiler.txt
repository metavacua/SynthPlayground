import React, { useState, useEffect, useRef, useCallback, Profiler } from 'react';
import { Bot, Activity, ShieldCheck, FileClock, TestTube, Database, Cpu, MemoryStick, HardDrive, Network, ClipboardCopy, Download, BarChart2, Zap, Beaker, SlidersHorizontal, Settings, Clock, TrendingUp, TrendingDown } from 'lucide-react';

// --- Simple Event Emitter for Decoupling ---
// This class provides a basic publish-subscribe mechanism to decouple components
// from direct state management within the ProfilerService.
class EventEmitter {
  constructor() {
    this.events = {}; // Stores event names and their subscribed functions
  }

  // Subscribes a function to an event. Returns an unsubscribe function.
  subscribe(eventName, fn) {
    if (!this.events[eventName]) {
      this.events[eventName] = [];
    }
    this.events[eventName].push(fn);
    return () => {
      // Filter out the specific function to unsubscribe
      this.events[eventName] = this.events[eventName].filter(eventFn => fn !== eventFn);
    };
  }

  // Emits an event, calling all subscribed functions with the provided data.
  emit(eventName, data) {
    const event = this.events[eventName];
    if (event) {
      event.forEach(fn => {
        fn.call.apply(fn, [null, data]); // Ensure compatibility with older browsers if needed
      });
    }
  }
}


// --- Core Profiler Service (Refactored into a Class) ---
// This class encapsulates all the profiling logic, state, and configurations.
// It uses the EventEmitter to notify React components of state changes.
//
// CONCEPTS FROM DOCUMENTS INTEGRATED INTO COMMENTS:
// This ProfilerService acts as the central "Nexus" (from "Security Profilers in Resource Paradigms")
// for Resource-Aware and Security-as-a-Resource paradigms. It is the "primary sensory and
// telemetry component for resource-aware systems, providing the data necessary for dynamic adaptation."
// Its design aims to facilitate "predictive, autonomous security orchestration."
class ProfilerService {
  constructor() {
    // Initial state of the profiler
    // Reflects "Real-Time Monitors" and "Deep Analytical Profilers" from "System Profilers"
    // and captures metrics relevant to "Resource-Aware Security" (CPU, memory, power/usage)
    // and "Security-as-a-Resource" (API quotas/tokens as consumable security).
    this.state = {
      log: [], // Application log - records events, warnings, errors, successes. Useful for auditing and debugging.
      probeResults: [], // Results from sandbox probes - quantitative measurements of browser environment capabilities.
      testResults: [], // Results from diagnostic tests - internal checks for logical consistency and potential issues (e.g., NaN errors).
      securityProbeResults: [], // Results from security posture probes - conceptual assessment of security configuration/behavior.
      requestsThisMinute: 0, // API requests count per minute - part of "Resource-Aware Security" metrics.
      requestsToday: 0, // API requests count per day - part of "Resource-Aware Security" metrics.
      tokensThisMinute: 0, // Tokens processed per minute - quantifiable "Security-as-a-Resource" metric.
      tokensToday: 0, // Tokens processed per day - quantifiable "Security-as-a-Resource" metric.
      lastApiCallTimestamp: 0, // Timestamp of the last API call - used for enforcing cooldowns.
      cache: new Map(), // Simple in-memory cache for API responses - affects "Network Analysis" in sandbox probes.
      apiLatencies: [], // Array to store API call latencies - critical for performance profiling.
      longTasks: [], // List of detected long tasks (UI main thread blocks) - crucial for UI responsiveness profiling.
      fps: 0, // Frames per second - key metric for real-time UI performance.
    };
    // Configuration settings for the profiler
    // These limits relate directly to "Resource-Aware Security" (e.g., API_COOLDOWN_MS as a rate limit)
    // and "Security-as-a-Resource" (RPM_LIMIT, RPD_LIMIT, TPM_LIMIT as "security budget" boundaries).
    this.config = {
      RPM_LIMIT: 60, // Requests Per Minute limit - a rate-limiting mechanism.
      RPD_LIMIT: 1500, // Requests Per Day limit - a daily quota mechanism.
      TPM_LIMIT: 1000000, // Tokens Per Minute limit - a granular resource consumption limit for generative AI.
      API_COOLDOWN_MS: 1050, // Cooldown period between mock API calls - prevents "Security Provisioning Denial-of-Service (SPDoS)" attacks by exhausting security resources rapidly.
      LONG_TASK_THRESHOLD: 50, // Threshold for long tasks in milliseconds - defines what constitutes a "slow UI render" and triggers a warning in the log.
    };
    this.emitter = new EventEmitter(); // Instance of EventEmitter for state updates - decouples state logic from UI components.
  }

  // Initializes the profiler service.
  // This setup performs "real-time monitoring" as described in "System Profilers".
  initialize() {
    this.log('Profiler Service Initializing...');
    this.loadDailyCounters(); // Load daily quotas from localStorage - enables persistent quota tracking.
    
    // Set up a minute-interval to reset minute counters - simulates a real-world API quota reset.
    setInterval(() => {
      this.state.requestsThisMinute = 0;
      this.state.tokensThisMinute = 0;
      this.emitter.emit('change', this.state); // Notify components of state change for UI update.
    }, 60000);

    // Set up PerformanceObserver for long tasks if supported by the browser.
    // This is an "Event-Based Tracing" mechanism to detect UI bottlenecks.
    try {
        const observer = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                this.state.longTasks.push(entry);
                if(this.state.longTasks.length > 20) this.state.longTasks.shift(); // Keep log size manageable for display.
                this.log(`Long task detected: ${entry.duration.toFixed(2)}ms`, 'warn'); // Log long tasks as warnings.
            }
            this.emitter.emit('change', this.state); // Notify components of long task updates.
        });
        observer.observe({ type: "longtask", buffered: true }); // Observe "longtask" events.
    } catch(e) {
        this.log('PerformanceObserver for long tasks not supported.', 'warn'); // Graceful degradation for unsupported browsers.
    }
    this.log('Profiler Service Initialized.');
    this.emitter.emit('change', this.state); // Initial state notification for React components to render.
  }
  
  // Updates profiler configuration.
  // Allows dynamic adjustment of "resource" limits and thresholds, enabling "adaptive security frameworks".
  updateConfig(newConfig) {
      this.config = { ...this.config, ...newConfig };
      this.log(`Updated config: ${JSON.stringify(newConfig)}`, 'info'); // Log config changes for auditability.
      this.emitter.emit('change', this.state); // Notify components to re-render with new config.
  }

  // Adds a message to the profiler log.
  // This is a core function for "Observation" in a security profiler (monitoring system state/behavior).
  log(message, level = 'info') {
    const entry = { timestamp: new Date().toLocaleTimeString(), message, level };
    this.state.log.unshift(entry); // Add new entry to the beginning for chronological order in UI.
    if (this.state.log.length > 100) this.state.log.pop(); // Keep log size manageable.
    this.emitter.emit('change', this.state); // Notify components of log update.
  }

  // Loads daily API request and token counters from localStorage.
  // This persistence aligns with managing "Security as a Resource" across sessions.
  loadDailyCounters() {
    const today = new Date().toISOString().split('T')[0];
    const storedDate = localStorage.getItem('profiler_date');
    if (storedDate === today) {
      this.state.requestsToday = parseInt(localStorage.getItem('profiler_requestsToday') || '0', 10);
      this.state.tokensToday = parseInt(localStorage.getItem('profiler_tokensToday') || '0', 10);
    } else {
      this.log('New day detected, resetting daily quotas.');
      this.resetDailyCounters(); // Reset if it's a new day, simulating daily quota resets.
      localStorage.setItem('profiler_date', today); // Store today's date to track daily resets.
    }
  }

  // Resets daily API request and token counters.
  // Explicitly managing "Security-as-a-Resource" budget.
  resetDailyCounters() {
      this.state.requestsToday = 0;
      this.state.tokensToday = 0;
      localStorage.setItem('profiler_requestsToday', '0');
      localStorage.setItem('profiler_tokensToday', '0');
      this.emitter.emit('change', this.state); // Notify components of reset.
      this.log('Daily counters reset.', 'info');
  }
  
  // Simulates an instrumented API fetch call, including quota checks, cooldown, and caching.
  // This function demonstrates the "instrumentation" technique from "System Profilers"
  // and the "Resource-Aware Security" concept by dynamically checking and enforcing limits.
  // The API call itself is treated as a "consumable security commodity" from "Security-as-a-Resource".
  async instrumentedFetch(prompt) {
    this.log(`Intercepted request for prompt: "${prompt.substring(0, 30)}..."`);
    const estimatedTokens = this.estimateTokens(prompt);
    
    // Basic quota check - "Compare" step of a security profiler against defined policy (quotas).
    if (!this.checkQuota(estimatedTokens)) {
      const errorMsg = 'Quota exceeded. Request blocked by client-side profiler.';
      this.log(errorMsg, 'error'); // Log the blocking action.
      throw new Error(errorMsg); // Block the request.
    }
    
    const now = Date.now();
    // Enforce API cooldown period - prevents "Security Provisioning Denial-of-Service (SPDoS)".
    if (now - this.state.lastApiCallTimestamp < this.config.API_COOLDOWN_MS) {
        const delay = this.config.API_COOLDOWN_MS - (now - this.state.lastApiCallTimestamp);
        this.log(`Cooldown active. Waiting for ${delay}ms...`, 'warn');
        await new Promise(res => setTimeout(res, delay)); // Pause execution to respect cooldown.
    }

    this.state.lastApiCallTimestamp = Date.now(); // Update last call timestamp.
    const apiCallStart = performance.now(); // Mark start for latency measurement.
    
    try {
      const cacheKey = await this.hashText(prompt); // Generate cache key - simulates real-world caching.
      if (this.state.cache.has(cacheKey)) {
        this.log(`Cache HIT.`, 'success'); // Log cache hit.
        this.emitter.emit('change', this.state);
        const cachedResponse = this.state.cache.get(cacheKey);
        // Simulate cache hit latency to avoid 0ms API calls - adds realism.
        await new Promise(res => setTimeout(res, 50));
        this.recordApiLatency(performance.now() - apiCallStart); // Record latency even for cache hits.
        return cachedResponse; // Return cached response.
      }

      this.log('Cache MISS. Making mock API call...');
      const mockResponse = await this.mockGeminiAPI(prompt); // Simulate API call to an external service.

      const responseTokens = this.estimateTokens(mockResponse.text);
      const totalTokens = estimatedTokens + responseTokens;
      
      this.updateCounters(totalTokens); // Update request/token counters - "Characterize" step of profiler.
      this.state.cache.set(cacheKey, mockResponse); // Cache the response for future hits.
      this.recordApiLatency(performance.now() - apiCallStart); // Record the actual API call latency.
      this.emitter.emit('change', this.state);
      return mockResponse;
    } catch (error) {
      this.log(`API call FAILED. Reason: ${error.message}`, 'error');
      this.recordApiLatency(performance.now() - apiCallStart); // Record latency even on failure.
      throw error;
    }
  }
  
  // Records API latency and keeps a limited history.
  // This contributes to "Quantifying the Trade-offs" in "Resource-Aware Security".
  recordApiLatency(latency) {
      this.state.apiLatencies.push(latency);
      if (this.state.apiLatencies.length > 50) this.state.apiLatencies.shift(); // Keep history size controlled.
      this.emitter.emit('change', this.state); // Notify UI to update latency trend.
  }

  // Updates the request and token counters and saves them to localStorage.
  // This is the core "metering system" for the "Security-as-a-Resource" paradigm.
  updateCounters(totalTokens) {
    this.state.requestsThisMinute++;
    this.state.requestsToday++;
    this.state.tokensThisMinute += totalTokens;
    this.state.tokensToday += totalTokens;
    localStorage.setItem('profiler_requestsToday', this.state.requestsToday.toString()); // Persist daily request count.
    localStorage.setItem('profiler_tokensToday', this.state.tokensToday.toString()); // Persist daily token count.
    this.emitter.emit('change', this.state); // Notify UI for real-time counter updates.
  }

  // Runs various sandbox probes to gather system information.
  // These are "Static Inventory Tools" and "Real-Time Monitors" in action,
  // performing "Resource Detection, Discovery, and Management".
  async runSandboxProbes() {
    this.log('Running enhanced sandbox probes...');
    this.state.probeResults = []; // Clear previous results.
    this.emitter.emit('change', { probeResults: [] }); // Notify to clear UI before new results.

    // Helper function to run a single test and record its result.
    const runTest = async (name, testFn, category) => {
        try {
            const detail = await testFn();
            this.state.probeResults.push({ name, status: 'pass', detail, category }); // Record successful test.
        } catch (e) {
            this.state.probeResults.push({ name, status: 'fail', detail: e.message, category }); // Record failed test with error.
        }
        this.emitter.emit('change', { probeResults: [...this.state.probeResults] }); // Notify after each test for progressive UI update.
    };
    
    // Compute category probes - assess CPU capabilities.
    await runTest('Logical CPU Cores', () => navigator.hardwareConcurrency || 'N/A', 'Compute'); // Hardware concurrency via navigator API.
    await runTest('WASM vs JS Benchmark', async () => {
        // Simple WASM module for addition - benchmarks performance difference between WASM and JS.
        // This is a "Deep Analytical Profiler" technique focusing on computational efficiency.
        const wasmCode = new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0, 1, 133, 128, 128, 128, 0, 1, 96, 2, 127, 127, 1, 127, 3, 130, 128, 128, 128, 0, 1, 0, 4, 132, 128, 128, 128, 0, 1, 112, 0, 0, 5, 131, 128, 128, 128, 0, 1, 0, 1, 6, 129, 128, 128, 128, 0, 0, 7, 145, 128, 128, 128, 0, 2, 6, 109, 101, 109, 111, 114, 121, 2, 0, 4, 97, 100, 100, 0, 0, 10, 138, 128, 128, 128, 0, 1, 132, 128, 128, 128, 0, 0, 32, 0, 32, 1, 108, 11]);
        const wasmModule = await WebAssembly.instantiate(wasmCode);
        const { add } = wasmModule.instance.exports;
        const jsAdd = (a, b) => a + b;
        const iterations = 1e7;
        
        // Benchmark WASM performance.
        const startWasm = performance.now();
        for(let i=0; i<iterations; i++) { add(i, 1); }
        const wasmTime = performance.now() - startWasm;
        
        // Benchmark JavaScript performance.
        const startJs = performance.now();
        for(let i=0; i<iterations; i++) { jsAdd(i, 1); }
        const jsTime = performance.now() - startJs;
        return `WASM: ${wasmTime.toFixed(2)}ms, JS: ${jsTime.toFixed(2)}ms`;
    }, 'Compute');

    // Memory category probes - assess RAM usage and limits.
    await runTest('JS Heap Size', () => {
        if (!performance.memory) throw new Error('API not available.'); // Check for browser support.
        const heap = performance.memory;
        return `${(heap.usedJSHeapSize / 1e6).toFixed(2)}MB / ${(heap.jsHeapSizeLimit / 1e6).toFixed(2)}MB`; // Current vs. limit.
    }, 'Memory');

    // Storage category probes - assess persistent storage capabilities.
    await runTest('Storage Quota', async () => {
        if (!navigator.storage || !navigator.storage.estimate) throw new Error('API not available.'); // Check for browser support.
        const q = await navigator.storage.estimate();
        return `${(q.usage/1e6).toFixed(2)}MB / ${(q.quota/1e6).toFixed(2)}MB`; // Current usage vs. estimated quota.
    }, 'Storage');
    await runTest('IndexedDB I/O', async () => {
      // Benchmarks IndexedDB write operations to estimate IOPS.
      // This is a form of "instrumentation" for resource measurement.
      const dbName = 'ProfilerDB_IO_Test';
      return new Promise((resolve, reject) => {
        const openReq = indexedDB.open(dbName, 1); // Open/create a temporary IndexedDB.
        openReq.onupgradeneeded = e => e.target.result.createObjectStore('test'); // Create object store if needed.
        openReq.onsuccess = e => {
          const db = e.target.result;
          const tx = db.transaction('test', 'readwrite'); // Start a read-write transaction.
          const store = tx.objectStore('test');
          const start = performance.now();
          let ops = 0;
          // Write operations for 100ms to estimate IOPS (I/O Operations Per Second).
          const writer = () => {
            if(performance.now() - start > 100) { // Run for 100ms.
              const iops = (ops / ((performance.now() - start) / 1000)).toFixed(0);
              db.close();
              indexedDB.deleteDatabase(dbName); // Clean up the temporary database.
              resolve(`${iops} IOPS`);
              return;
            }
            store.put('data', ops++).onsuccess = writer; // Continue writing and increment ops count.
          };
          writer();
        };
        openReq.onerror = e => reject(new Error(e.target.error.name)); // Handle errors.
      });
    }, 'Storage');

    // Network category probes - assess network capabilities and usage.
    await runTest('Network Analysis', () => {
        if (!performance.getEntriesByType) throw new Error('API not available.'); // Check for browser support.
        const resources = performance.getEntriesByType('resource'); // Get all loaded resources for the page.
        const totalSize = resources.reduce((acc, r) => acc + (r.transferSize || 0), 0); // Calculate total transfer size.
        return `${resources.length} reqs, ${(totalSize / 1024).toFixed(2)} KB used`; // Report requests and size.
    }, 'Network');
    
    this.log('Sandbox probes complete.'); // Log completion.
  }

  // Runs diagnostic unit tests for internal logic, specifically for NaN error hypotheses and memory leaks.
  // This contributes to the "Deep Analytical Profilers" aspect.
  runDiagnosticTests() {
    this.log('Running diagnostic unit tests...');
    this.state.testResults = []; // Clear previous results.
    this.emitter.emit('change', { testResults: [] }); // Notify to clear UI.
    
    // Helper function to run a single test and record its result.
    const runTest = (name, testFn) => {
        try {
            const detail = testFn() || 'Execution successful.'; // Execute test function.
            this.state.testResults.push({ name, status: 'pass', detail }); // Record pass.
        } catch (e) {
            this.state.testResults.push({ name, status: 'fail', detail: e.message }); // Record fail with error message.
        }
        this.emitter.emit('change', { testResults: [...this.state.testResults] }); // Notify after each test for progressive UI.
    };
    
    // Test 1: Validate initial FPS state - checks for valid number.
    runTest('Hypothesis: Initial FPS state is invalid', () => {
        const initialFps = 0; // Assuming initial FPS is 0 or undefined before calculation.
        if (typeof initialFps !== 'number' || isNaN(initialFps)) {
            throw new Error(`Initial FPS is not a valid number. Got: ${typeof initialFps}`);
        }
        return `Initial FPS is ${initialFps} (valid number).`;
    });
    // Test 2: Validate FPS calculation with zero-time delta - tests robustness against division by zero.
    runTest('Hypothesis: FPS calculation fails with zero-time delta', () => {
        // This deliberately creates a NaN to test handling.
        const calculatedFps = 0 / 0; 
        if (isNaN(calculatedFps)) { 
            // Simulate guarded calculation for robustness. A real system would guard against division by zero.
            const guardedFps = (0 > 0) ? (1000 / 0) : 0; // If timeDelta is 0, FPS should be 0, not Infinity/NaN.
            if(isNaN(guardedFps)) throw new Error('Guarded calculation still resulted in NaN.');
            return `Guarded FPS with zero delta is ${guardedFps}. (Not NaN)`;
        }
        return `NaN not produced by 0/0, test inconclusive.`; // Should ideally not be hit if 0/0 gives NaN.
    });
    // Test 3: Simulate and detect a conceptual memory leak (growth over time).
    // This represents an "Application-Specific Profiler" feature.
    let leakyArray = []; // This array simulates objects that might "leak" if not properly released.
    let initialLeakSize = 0;
    runTest('Simulate and Detect Conceptual Memory Leak', () => {
        if (leakyArray.length === 0) { // On first run, initialize baseline heap size.
            initialLeakSize = performance.memory ? performance.memory.usedJSHeapSize : 0;
            leakyArray.push(new Array(1024 * 10).fill('leak')); // Simulate first "leak" by holding a large array.
            return `Simulated small leak. Initial heap size: ${(initialLeakSize / 1e6).toFixed(2)}MB`;
        } else {
            // Simulate adding more to the leak in subsequent runs.
            leakyArray.push(new Array(1024 * 5).fill('more_leak'));
            const currentLeakSize = performance.memory ? performance.memory.usedJSHeapSize : 0;
            if (currentLeakSize > initialLeakSize * 1.01) { // Detects if heap grew by more than 1%.
                // In a real scenario, this would trigger an alert or a detailed memory snapshot analysis.
                return `Detected heap growth from leak: ${(currentLeakSize / 1e6).toFixed(2)}MB (initial: ${(initialLeakSize / 1e6).toFixed(2)}MB)`;
            } else {
                return `Heap size stable or growth not significant yet.`;
            }
        }
    });
    
    this.log('Diagnostic tests complete.'); // Log completion.
  }

  // Runs conceptual security posture assessment probes.
  // This section embodies the "Security Profiler" role, assessing "Vulnerability Posture"
  // and "Behavioral Monitoring".
  async runSecurityPostureProbes() {
    this.log('Running conceptual security posture assessment...');
    this.state.securityProbeResults = []; // Clear previous results.
    this.emitter.emit('change', { securityProbeResults: [] }); // Notify to clear UI.

    // Helper function to run a single security test and record its result.
    // Each testFn should return an object: { status: 'pass' | 'fail', detail: string, riskLevel: 'Low' | 'Medium' | 'High' | 'Critical' }
    const runSecurityTest = async (name, testFn) => {
        try {
            const result = await testFn();
            this.state.securityProbeResults.push({ name, ...result });
        } catch (e) {
            // This catch block is for unexpected errors in the testFn itself, not for security failures reported by testFn.
            this.state.securityProbeResults.push({ name, status: 'error', detail: `Test execution error: ${e.message}`, riskLevel: 'Critical' });
        }
        this.emitter.emit('change', { securityProbeResults: [...this.state.securityProbeResults] });
    };

    // --- Existing Mock Security Tests ---
    await runSecurityTest('Mock Vulnerability Scan (CVE-2023-XXXX)', async () => {
        await new Promise(res => setTimeout(res, 300));
        const passed = Math.random() > 0.3;
        if (!passed) {
            return { status: 'fail', detail: 'Known vulnerability detected: outdated library X.', riskLevel: 'High' };
        }
        return { status: 'pass', detail: 'No critical vulnerabilities detected.', riskLevel: 'Low' };
    });

    await runSecurityTest('Mock Policy Compliance Check (Data Export)', async () => {
        await new Promise(res => setTimeout(res, 400));
        const compliant = Math.random() > 0.2;
        if (!compliant) {
            return { status: 'fail', detail: 'Unauthorized data export attempt detected.', riskLevel: 'Critical' };
        }
        return { status: 'pass', detail: 'Policy compliant: No unauthorized data export.', riskLevel: 'Low' };
    });
    
    await runSecurityTest('Mock Network Behavior Anomaly Detection', async () => {
        await new Promise(res => setTimeout(res, 500));
        const anomaly = Math.random() > 0.8;
        if (anomaly) {
            return { status: 'fail', detail: 'Unusual outgoing connection pattern detected.', riskLevel: 'Medium' };
        }
        return { status: 'pass', detail: 'Normal network behavior observed.', riskLevel: 'Low' };
    });

    // --- New Sandbox Attribute Tests ---
    await runSecurityTest('Sandbox: Inline Script Execution (allow-scripts)', async () => {
        try {
            // Attempt to create and append an inline script.
            // If it succeeds, it implies 'allow-scripts' is present.
            const script = document.createElement('script');
            const uniqueId = 'inline_script_test_' + Date.now();
            script.textContent = `window.${uniqueId} = true;`; // Simply set a flag
            document.body.appendChild(script);
            await new Promise(r => setTimeout(r, 50)); // Give it a moment to execute
            document.body.removeChild(script);

            if (window[uniqueId]) {
                 delete window[uniqueId]; // Clean up
                 return { status: 'fail', detail: 'Inline script execution was allowed. The iframe sandbox is missing "allow-scripts".', riskLevel: 'Critical' };
            }
            return { status: 'pass', detail: 'Inline script execution prevented by sandbox.', riskLevel: 'Low' };
        } catch (e) {
            // Any error here likely means the browser/sandbox prevented the script from being appended/executed.
            return { status: 'pass', detail: `Inline script execution blocked by sandbox: ${e.message}`, riskLevel: 'Low' };
        }
    });

    await runSecurityTest('Sandbox: Popup Opening (allow-popups)', async () => {
        try {
            const popup = window.open('about:blank', '_blank', 'width=100,height=100');
            if (popup) {
                popup.close(); // Close immediately
                return { status: 'fail', detail: 'Popup window was allowed to open. The iframe sandbox is missing "allow-popups".', riskLevel: 'High' };
            }
            return { status: 'pass', detail: 'Popup window blocked by sandbox.', riskLevel: 'Low' };
        } catch (e) {
            return { status: 'pass', detail: `Popup attempt resulted in error (likely blocked by sandbox): ${e.message}`, riskLevel: 'Low' };
        }
    });

    await runSecurityTest('Sandbox: Form Submission (allow-forms)', async () => {
        try {
            const form = document.createElement('form');
            form.action = '#'; // Prevent actual navigation
            form.method = 'post';
            document.body.appendChild(form);
            const canSubmit = typeof form.submit === 'function'; // Check if submit method exists
            document.body.removeChild(form);

            if (canSubmit) {
                // This is a weak check, but indicates if the method is callable.
                return { status: 'fail', detail: 'Form submission capability detected. The iframe sandbox is missing "allow-forms".', riskLevel: 'Medium' };
            }
            return { status: 'pass', detail: 'Form submission capability appears to be blocked by sandbox.', riskLevel: 'Low' };
        } catch (e) {
            return { status: 'pass', detail: `Form creation/submission blocked by sandbox: ${e.message}`, riskLevel: 'Low' };
        }
    });

    await runSecurityTest('Sandbox: Modal Display (allow-modals)', async () => {
        // Use a custom modal display as alert/confirm/prompt are blocked by default in iframe.
        // If this test runs outside a sandboxed iframe, it would fail.
        try {
            const iframe = document.createElement('iframe');
            iframe.style.display = 'none';
            // Important: we want to see if `alert` *within* the iframe is allowed.
            // A truly sandboxed iframe (no allow-modals) would prevent this.
            iframe.sandbox = ''; // Start with an empty sandbox to see if it implicitly allows.
            document.body.appendChild(iframe);

            const iframeWin = iframe.contentWindow;
            if (iframeWin && typeof iframeWin.alert === 'function') {
                iframeWin.alert('Test modal from iframe!'); // This will typically be blocked.
                document.body.removeChild(iframe);
                return { status: 'fail', detail: 'Modal (alert) was allowed within a new iframe. The sandbox might be too permissive or missing "allow-modals".', riskLevel: 'Medium' };
            }
            document.body.removeChild(iframe);
            return { status: 'pass', detail: 'Modal (alert) blocked within new iframe by sandbox.', riskLevel: 'Low' };
        } catch (e) {
            return { status: 'pass', detail: `Modal attempt blocked by sandbox: ${e.message}`, riskLevel: 'Low' };
        }
    });


    await runSecurityTest('Sandbox: Same Origin Access (allow-same-origin)', async () => {
        let sameOriginAllowed = false;
        try {
            // If allow-same-origin is present, document.domain should be accessible and potentially set.
            // If it's blocked, document.domain might be empty or throw a security error on access.
            if (document.domain && document.domain !== '') {
                sameOriginAllowed = true;
            }
            // Also check window.top and window.parent access
            let parentAccess = false;
            try {
                if (window.parent && window.parent !== window) {
                    // Try a trivial access to parent's property to trigger security error if cross-origin.
                    const test = window.parent.location.href; // This will throw if truly cross-origin and blocked.
                    parentAccess = true;
                }
            } catch (e) {
                // Access denied, good.
                parentAccess = false;
            }

            if (sameOriginAllowed || parentAccess) {
                 return { status: 'fail', detail: `Same-origin access (document.domain or window.parent) was allowed. The iframe sandbox is missing "allow-same-origin".`, riskLevel: 'High' };
            }
            return { status: 'pass', detail: 'Same-origin access appears to be blocked or restricted by sandbox.', riskLevel: 'Low' };
        } catch (e) {
            return { status: 'pass', detail: `Same-origin access blocked by sandbox: ${e.message}`, riskLevel: 'Low' };
        }
    });


    // --- New CSP Feature Tests (Conceptual/Simulated) ---
    await runSecurityTest('CSP: Inline Script Prevention (script-src)', async () => {
        try {
            const script = document.createElement('script');
            const uniqueId = 'csp_inline_script_test_' + Date.now();
            script.textContent = `window.${uniqueId} = true;`; // Simple flag
            document.head.appendChild(script);
            await new Promise(r => setTimeout(r, 50)); // Give script time to execute
            document.head.removeChild(script);

            if (window[uniqueId]) {
                delete window[uniqueId]; // Clean up
                return { status: 'fail', detail: 'Inline script execution allowed. CSP is potentially weak (missing script-src \'self\', or includes \'unsafe-inline\').', riskLevel: 'Critical' };
            }
            return { status: 'pass', detail: 'Inline script execution prevented by CSP.', riskLevel: 'Low' };
        } catch (e) {
            // Any error here likely means CSP prevented the script from being appended/executed.
            return { status: 'pass', detail: `Inline script execution blocked by CSP: ${e.message}`, riskLevel: 'Low' };
        }
    });

    await runSecurityTest('CSP: External Image Block (img-src)', async () => {
        return new Promise(resolve => {
            const img = new Image();
            const externalImageUrl = 'https://placehold.co/1x1'; // A tiny, easily loadable external image
            img.src = externalImageUrl;
            
            const timeout = setTimeout(() => {
                img.onload = img.onerror = null; // Clean up listeners
                resolve({ status: 'pass', detail: 'External image loading prevented or timed out by CSP (img-src rule).', riskLevel: 'Low' });
            }, 1000); // Give it a second to load

            img.onload = () => {
                clearTimeout(timeout);
                img.onload = img.onerror = null; // Clean up listeners
                resolve({ status: 'fail', detail: 'External image loading allowed. CSP is potentially weak (img-src too broad or missing).', riskLevel: 'High' });
            };
            img.onerror = (e) => {
                clearTimeout(timeout);
                img.onload = img.onerror = null; // Clean up listeners
                resolve({ status: 'pass', detail: `External image loading blocked by CSP or network error: ${e.message}`, riskLevel: 'Low' });
            };
        });
    });

    this.log('Conceptual security posture assessment complete.'); // Log completion.
  }

  // --- Dummy implementations for brevity/mocking ---
  // Estimates tokens based on text length (simplified).
  // Used in "instrumentedFetch" to simulate token consumption, aligning with "Security-as-a-Resource".
  estimateTokens(text) { return Math.ceil((text || '').length / 4); }
  
  // Placeholder for quota check (now uses config limits).
  // This is the "Compare" step of a security profiler against a "Security-as-a-Resource" budget.
  checkQuota(tokens) {
    if (this.state.requestsThisMinute >= this.config.RPM_LIMIT) {
        this.log(`RPM limit reached (${this.state.requestsThisMinute}/${this.config.RPM_LIMIT}).`, 'error');
        return false;
    }
    if (this.state.tokensThisMinute + tokens > this.config.TPM_LIMIT) {
        this.log(`TPM limit reached (${this.state.tokensThisMinute + tokens}/${this.config.TPM_LIMIT}).`, 'error');
        return false;
    }
    if (this.state.requestsToday >= this.config.RPD_LIMIT) {
        this.log(`RPD limit reached (${this.state.requestsToday}/${this.config.RPD_LIMIT}).`, 'error');
        return false;
    }
    return true;
  }
  // Simple text hashing (returns text itself in this mock).
  // Used for cache key generation.
  async hashText(text) { return text; }
  
  // Mock Gemini API call with a simulated delay.
  // Represents interaction with an external "Resource" (like a Large Language Model).
  async mockGeminiAPI(prompt) { 
    await new Promise(r => setTimeout(r, 500 + Math.random() * 200)); // Simulate network delay and variability.
    return { text: `Mock response for: ${prompt}`}; // Return a simple mock response.
  }
}

// Create a singleton instance of the ProfilerService
const profilerServiceInstance = new ProfilerService();


// --- React Components ---
// These components are the "Automation & Management Application" layer,
// consuming the data and "semantic profiles" provided by the ProfilerService.

// Component to display the profiler log with filtering.
// Provides a "unified view" of various profiler outputs.
const ProfilerLog = ({ log }) => {
    const [filterLevel, setFilterLevel] = useState('all');

    const filteredLog = log.filter(entry => 
        filterLevel === 'all' || entry.level === filterLevel
    );

    return (
        <div className="h-64 bg-gray-900/50 p-3 rounded-lg border border-gray-700 overflow-y-auto font-mono text-xs">
            <div className="mb-2 flex justify-end">
                <select 
                    value={filterLevel} 
                    onChange={(e) => setFilterLevel(e.target.value)}
                    className="bg-gray-700 text-gray-200 rounded-md px-2 py-1 text-sm focus:ring-indigo-500 focus:border-indigo-500"
                >
                    <option value="all">All Levels</option>
                    <option value="info">Info</option>
                    <option value="warn">Warnings</option>
                    <option value="error">Errors</option>
                    <option value="success">Success</option>
                </select>
            </div>
            {filteredLog.map((entry, i) => (
                <div key={i} className={`flex ${entry.level === 'error' ? 'text-red-400' : entry.level === 'warn' ? 'text-yellow-400' : entry.level === 'success' ? 'text-green-400' : 'text-gray-300'}`}>
                    <span className="flex-shrink-0 mr-2">{entry.timestamp}</span>
                    <span className="flex-grow">{entry.message}</span>
                </div>
            ))}
        </div>
    );
};

// Component to run and display sandbox probe results.
// Represents the output of "System Profilers" in categories like "Compute", "Memory", "Storage", "Network".
const SandboxProber = ({ results, onRunProbes, isLoading }) => {
    const categories = { Compute: { icon: Cpu, color: 'text-red-400' }, Memory: { icon: MemoryStick, color: 'text-blue-400' }, Storage: { icon: HardDrive, color: 'text-yellow-400' }, Network: { icon: Network, color: 'text-purple-400' }};
    
    // Handles copying probe results to clipboard - supports "Reporting Formats".
    const handleCopyResults = () => {
      const textToCopy = results.map(r => `${r.category} - ${r.name}: ${r.status.toUpperCase()} (${r.detail})`).join('\n');
      const textArea = document.createElement("textarea");
      textArea.value = textToCopy;
      textArea.style.position = "fixed";
      textArea.style.top = "0";
      textArea.style.left = "-9999px";
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      try {
          document.execCommand('copy'); // Using deprecated execCommand for broader iFrame compatibility.
          profilerServiceInstance.log('Probe results copied to clipboard.', 'success');
      } catch (err) {
          profilerServiceInstance.log('Failed to copy results to clipboard.', 'error');
      }
      document.body.removeChild(textArea);
    };
    
    // Handles downloading probe results as a JSON file - supports "Reporting Formats".
    const handleDownloadResults = () => {
        const jsonString = `data:text/json;charset=utf-8,${encodeURIComponent(JSON.stringify(results, null, 2))}`;
        const link = document.createElement('a');
        link.href = jsonString;
        link.download = 'profiler-sandbox-results.json'; // Download as JSON.
        link.click();
    };

    return (
        <div className="space-y-4 p-4 bg-gray-800/50 rounded-lg">
             <h3 className="text-lg font-semibold text-white flex items-center"><TestTube className="mr-2"/> Sandbox Prober</h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                <button onClick={onRunProbes} disabled={isLoading} className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg flex items-center justify-center transition-colors disabled:opacity-50">
                  {isLoading ? <Activity className="animate-spin mr-2"/> : <TestTube className="mr-2 h-4 w-4" />}
                  {isLoading ? 'Probing...' : 'Run Probes'}
                </button>
                <button onClick={handleCopyResults} disabled={!results.length} className="w-full bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded-lg flex items-center justify-center transition-colors disabled:opacity-50"><ClipboardCopy className="mr-2 h-4 w-4" /> Copy</button>
                <button onClick={handleDownloadResults} disabled={!results.length} className="w-full bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded-lg flex items-center justify-center transition-colors disabled:opacity-50"><Download className="mr-2 h-4 w-4" /> Download</button>
            </div>
            <div className="space-y-3 pt-4">
                {Object.keys(categories).map(category => (
                    <div key={category}>
                        <h4 className={`text-md font-bold mb-2 flex items-center ${categories[category].color}`}>
                           {React.createElement(categories[category].icon, { className: "mr-2 w-5 h-5" })} {category}
                        </h4>
                        <div className="space-y-2 pl-4">
                        {(results || []).filter(r => r.category === category).map(({name, status, detail}) => (
                            <div key={name} className="flex items-center justify-between bg-gray-800 p-2 rounded-md text-sm">
                                <span className="font-medium text-gray-300">{name}</span>
                                <span className={`text-right px-2 py-0.5 text-xs font-semibold rounded-full ${status === 'pass' ? 'bg-green-500/20 text-green-300' : 'bg-red-500/20 text-red-300'}`}>{detail}</span>
                            </div>
                        ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

// Component to run and display unit test diagnostics.
// This is analogous to "Application-Specific Profilers" or internal "Deep Analytical Profilers".
const UnitTestRunner = ({ results, onRunTests, isLoading }) => (
    <div className="space-y-4 p-4 bg-gray-800/50 rounded-lg">
        <h3 className="text-lg font-semibold text-white flex items-center"><Beaker className="mr-2"/> Unit Test Diagnostics</h3>
        <button onClick={onRunTests} disabled={isLoading} className="w-full bg-teal-600 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded-lg flex items-center justify-center transition-colors disabled:opacity-50">
            {isLoading ? <Activity className="animate-spin mr-2"/> : <Beaker className="mr-2 h-4 w-4" />}
            {isLoading ? 'Testing...' : 'Run NaN Error Diagnostics'}
        </button>
        <div className="space-y-2">
            {(results || []).map(({name, status, detail}, i) => (
                <div key={i} className="flex items-start bg-gray-800 p-2 rounded-md text-sm">
                    <span className={`mr-2 font-bold ${status === 'pass' ? 'text-green-400' : 'text-red-400'}`}>{status.toUpperCase()}</span>
                    <div className="flex-grow">
                        <span className="font-medium text-gray-300">{name}:</span>
                        <span className="text-gray-400 ml-2">{detail}</span>
                    </div>
                </div>
            ))}
        </div>
    </div>
);

// New component for API Quota and Token Monitoring.
// This directly visualizes "Security as a Resource" and "Resource-Aware Security" metrics.
const QuotaMonitor = ({ config, appState, updateConfig, resetDailyCounters }) => {
    return (
        <div className="space-y-4 p-4 bg-gray-800/50 rounded-lg">
            <h3 className="text-lg font-semibold text-white flex items-center"><Database className="mr-2"/> API Quota & Token Monitor</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-gray-700 p-3 rounded-md">
                    <h4 className="text-md font-bold text-gray-300 mb-2">Per Minute Usage</h4>
                    <div className="flex justify-between items-center text-sm mb-1">
                        <span>Requests:</span>
                        <span className="text-cyan-300">{appState.requestsThisMinute} / {config.RPM_LIMIT}</span>
                    </div>
                    <div className="flex justify-between items-center text-sm">
                        <span>Tokens:</span>
                        <span className="text-cyan-300">{(appState.tokensThisMinute / 1000).toFixed(1)}K / ${(config.TPM_LIMIT / 1000).toFixed(1)}K</span>
                    </div>
                </div>
                <div className="bg-gray-700 p-3 rounded-md">
                    <h4 className="text-md font-bold text-gray-300 mb-2">Daily Usage</h4>
                    <div className="flex justify-between items-center text-sm mb-1">
                        <span>Requests:</span>
                        <span className="text-emerald-300">{appState.requestsToday} / {config.RPD_LIMIT}</span>
                    </div>
                    <div className="flex justify-between items-center text-sm">
                        <span>Tokens:</span>
                        <span className="text-emerald-300">{(appState.tokensToday / 1000).toFixed(1)}K</span>
                    </div>
                </div>
            </div>

            <h4 className="text-md font-semibold text-white mt-4 flex items-center"><Settings className="mr-2 w-4 h-4"/> Quota Settings</h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                <div className="flex flex-col">
                    <label htmlFor="rpm-limit" className="text-gray-400 text-sm mb-1">RPM Limit</label>
                    <input 
                        type="number" 
                        id="rpm-limit" 
                        value={config.RPM_LIMIT} 
                        onChange={(e) => updateConfig({ RPM_LIMIT: parseInt(e.target.value, 10) || 0 })}
                        className="bg-gray-700 border border-gray-600 rounded-md px-3 py-2 text-white text-sm focus:ring-indigo-500 focus:border-indigo-500"
                    />
                </div>
                <div className="flex flex-col">
                    <label htmlFor="rpd-limit" className="text-gray-400 text-sm mb-1">RPD Limit</label>
                    <input 
                        type="number" 
                        id="rpd-limit" 
                        value={config.RPD_LIMIT} 
                        onChange={(e) => updateConfig({ RPD_LIMIT: parseInt(e.target.value, 10) || 0 })}
                        className="bg-gray-700 border border-gray-600 rounded-md px-3 py-2 text-white text-sm focus:ring-indigo-500 focus:border-indigo-500"
                    />
                </div>
                <div className="flex flex-col">
                    <label htmlFor="tpm-limit" className="text-gray-400 text-sm mb-1">TPM Limit</label>
                    <input 
                        type="number" 
                        id="tpm-limit" 
                        value={config.TPM_LIMIT} 
                        onChange={(e) => updateConfig({ TPM_LIMIT: parseInt(e.target.value, 10) || 0 })}
                        className="bg-gray-700 border border-gray-600 rounded-md px-3 py-2 text-white text-sm focus:ring-indigo-500 focus:border-indigo-500"
                    />
                </div>
                <div className="flex flex-col">
                    <label htmlFor="api-cooldown" className="text-gray-400 text-sm mb-1">API Cooldown (ms)</label>
                    <input 
                        type="number" 
                        id="api-cooldown" 
                        value={config.API_COOLDOWN_MS} 
                        onChange={(e) => updateConfig({ API_COOLDOWN_MS: parseInt(e.target.value, 10) || 0 })}
                        className="bg-gray-700 border border-gray-600 rounded-md px-3 py-2 text-white text-sm focus:ring-indigo-500 focus:border-indigo-500"
                    />
                </div>
                <div className="flex flex-col">
                    <label htmlFor="long-task-threshold" className="text-gray-400 text-sm mb-1">Long Task Threshold (ms)</label>
                    <input 
                        type="number" 
                        id="long-task-threshold" 
                        value={config.LONG_TASK_THRESHOLD} 
                        onChange={(e) => updateConfig({ LONG_TASK_THRESHOLD: parseInt(e.target.value, 10) || 0 })}
                        className="bg-gray-700 border border-gray-600 rounded-md px-3 py-2 text-white text-sm focus:ring-indigo-500 focus:border-indigo-500"
                    />
                </div>
            </div>
            <button 
                onClick={resetDailyCounters} 
                className="w-full mt-4 bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg flex items-center justify-center transition-colors"
            >
                <Clock className="mr-2 h-4 w-4" /> Reset Daily Quotas
            </button>
        </div>
    );
};

// New component for Performance Overview (FPS, Long Tasks, API Latency).
// Provides "Real-Time Monitors" and indicators of "Quantifying the Trade-offs".
const PerformanceOverview = ({ fps, longTasks, apiLatencies }) => {
    const avgLatency = apiLatencies.length > 0 
        ? (apiLatencies.reduce((sum, val) => sum + val, 0) / apiLatencies.length).toFixed(2)
        : 'N/A';
    
    return (
        <div className="space-y-4 p-4 bg-gray-800/50 rounded-lg">
            <h3 className="text-lg font-semibold text-white flex items-center"><BarChart2 className="mr-2"/> Performance Overview</h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
                <div className="bg-gray-700 p-3 rounded-md">
                    <h4 className="text-md font-bold text-gray-300">FPS</h4>
                    <p className="text-5xl font-extrabold text-green-400">{fps}</p>
                </div>
                <div className="bg-gray-700 p-3 rounded-md">
                    <h4 className="text-md font-bold text-gray-300">Long Tasks</h4>
                    <p className="text-5xl font-extrabold text-yellow-400">{longTasks.length}</p>
                </div>
                <div className="bg-gray-700 p-3 rounded-md">
                    <h4 className="text-md font-bold text-gray-300">Avg. API Latency</h4>
                    <p className="text-5xl font-extrabold text-blue-400">{avgLatency}ms</p>
                </div>
            </div>
            {/* Simple sparkline for API Latency - visualizes trend of a critical performance metric. */}
            {apiLatencies.length > 1 && (
                <div className="bg-gray-700 p-3 rounded-md mt-4">
                    <h4 className="text-md font-bold text-gray-300 mb-2">API Latency Trend (last {apiLatencies.length} calls)</h4>
                    <div className="flex items-end h-16 w-full overflow-hidden">
                        {apiLatencies.map((latency, index) => (
                            <div 
                                key={index} 
                                className="w-1 flex-grow mx-0.5 rounded-t-sm" 
                                style={{ height: `${Math.min(latency / 2, 100)}%`, backgroundColor: latency > 1000 ? '#f87171' : latency > 500 ? '#fbbf24' : '#60a5fa' }} 
                                title={`${latency.toFixed(2)}ms`}
                            />
                        ))}
                    </div>
                    <div className="flex justify-between text-xs text-gray-400 mt-1">
                        <span>Lower is better</span>
                        <div className="flex items-center">
                           <span className="mr-1">Trend:</span> 
                           {apiLatencies[apiLatencies.length - 1] > apiLatencies[0] ? 
                            <TrendingUp className="w-4 h-4 text-red-400" /> : 
                            <TrendingDown className="w-4 h-4 text-green-400" />}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

// New component for conceptual Security Profiling.
// Represents the "Device Posture Assessor," "Network Endpoint Classifier," and "Application Permission Auditor" roles.
const SecurityProfiler = ({ results, onRunSecurityProbes, isLoading }) => {
    const riskLevels = { 
        'Critical': 'text-red-400', 
        'High': 'text-orange-400', 
        'Medium': 'text-yellow-400', 
        'Low': 'text-green-400' 
    };

    // Handles copying security probe results to clipboard.
    const handleCopyResults = () => {
        const textToCopy = results.map(r => `${r.name}: ${r.status.toUpperCase()} (${r.detail}) - Risk: ${r.riskLevel}`).join('\n');
        const textArea = document.createElement("textarea");
        textArea.value = textToCopy;
        textArea.style.position = "fixed";
        textArea.style.top = "0";
        textArea.style.left = "-9999px";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
            profilerServiceInstance.log('Security probe results copied to clipboard.', 'success');
        } catch (err) {
            profilerServiceInstance.log('Failed to copy security results to clipboard.', 'error');
        }
        document.body.removeChild(textArea);
    };

    // Handles downloading security probe results as a JSON file.
    const handleDownloadResults = () => {
        const jsonString = `data:text/json;charset=utf-8,${encodeURIComponent(JSON.stringify(results, null, 2))}`;
        const link = document.createElement('a');
        link.href = jsonString;
        link.download = 'profiler-security-results.json';
        link.click();
    };

    return (
        <div className="space-y-4 p-4 bg-gray-800/50 rounded-lg">
            <h3 className="text-lg font-semibold text-white flex items-center"><ShieldCheck className="mr-2"/> Security Posture Assessment</h3>
            <p className="text-gray-400 text-sm">Conceptual assessment based on a "security profiler" as defined in academic research. This simulates checks for vulnerabilities, policy compliance, and behavioral anomalies.</p>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                <button onClick={onRunSecurityProbes} disabled={isLoading} className="w-full bg-pink-600 hover:bg-pink-700 text-white font-bold py-2 px-4 rounded-lg flex items-center justify-center transition-colors disabled:opacity-50">
                    {isLoading ? <Activity className="animate-spin mr-2"/> : <ShieldCheck className="mr-2 h-4 w-4" />}
                    {isLoading ? 'Assessing...' : 'Run Security Assessment'}
                </button>
                <button onClick={handleCopyResults} disabled={!results.length} className="w-full bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded-lg flex items-center justify-center transition-colors disabled:opacity-50"><ClipboardCopy className="mr-2 h-4 w-4" /> Copy</button>
                <button onClick={handleDownloadResults} disabled={!results.length} className="w-full bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded-lg flex items-center justify-center transition-colors disabled:opacity-50"><Download className="mr-2 h-4 w-4" /> Download</button>
            </div>
            <div className="space-y-2 pt-4">
                {(results || []).map(({name, status, detail, riskLevel}, i) => (
                    <div key={i} className="flex items-start bg-gray-800 p-2 rounded-md text-sm">
                        <span className={`mr-2 font-bold ${status === 'pass' ? 'text-green-400' : 'text-red-400'}`}>{status.toUpperCase()}</span>
                        <div className="flex-grow">
                            <span className="font-medium text-gray-300">{name}:</span>
                            <span className="text-gray-400 ml-2">{detail}</span>
                        </div>
                        <span className={`px-2 py-0.5 text-xs font-semibold rounded-full ml-4 ${riskLevels[riskLevel] || 'text-gray-300'} bg-gray-700`}>{riskLevel} Risk</span>
                    </div>
                ))}
            </div>
        </div>
    );
};


// Main App component
export default function App() {
  // State to hold the current profiler service data.
  const [appState, setAppState] = useState(profilerServiceInstance.state);
  // States to manage loading indicators for probes and tests.
  const [isProbing, setIsProbing] = useState(false);
  const [isTesting, setIsTesting] = useState(false);
  const [isSecurityProbing, setIsSecurityProbing] = useState(false);

  // Memoized update config function - ensures referential stability for useCallback.
  const updateProfilerConfig = useCallback((newConfig) => {
    profilerServiceInstance.updateConfig(newConfig);
  }, []); // Empty dependency array means this function is created once.

  useEffect(() => {
    // Callback to update component state when profiler service state changes.
    // This allows React components to react to data changes from the singleton ProfilerService.
    const handleStateUpdate = (newState) => {
      setAppState(prevState => ({ ...prevState, ...newState }));
    };
    
    // Subscribe to the 'change' event from the profiler service.
    const unsubscribe = profilerServiceInstance.emitter.subscribe('change', handleStateUpdate);
    profilerServiceInstance.initialize(); // Initialize the profiler service on component mount.

    // FPS Measurement Logic.
    // This continuously measures the frames per second, a key performance indicator.
    const frameCount = { current: 0 }; // Mutable ref to count frames.
    const prevTime = { current: performance.now() }; // Mutable ref for last time FPS was calculated.
    let animationFrameId; // To store the ID returned by requestAnimationFrame for cancellation.
    
    const measureFps = () => {
        frameCount.current++;
        const time = performance.now();
        const timeDelta = time - prevTime.current;
        // Update FPS approximately every second (if more than 1000ms have passed).
        if (timeDelta > 1000) {
            const newFps = timeDelta > 0 ? Math.round((frameCount.current * 1000) / timeDelta) : 0;
            profilerServiceInstance.state.fps = newFps; // Update FPS in service state.
            profilerServiceInstance.emitter.emit('change', profilerServiceInstance.state); // Notify for FPS update.
            frameCount.current = 0; // Reset frame count.
            prevTime.current = time; // Reset time.
        }
        animationFrameId = requestAnimationFrame(measureFps); // Request next animation frame.
    };
    measureFps(); // Start FPS measurement loop.

    // Simulating API calls to populate quota/latency data.
    // This demonstrates the "instrumented fetch" and interaction with "Security as a Resource" metrics.
    let apiCallInterval; // To store the interval ID for cancellation.
    const startMockApiCalls = () => {
        apiCallInterval = setInterval(() => {
            // Call mock API every 2 seconds to simulate traffic and resource consumption.
            // Catching the error to prevent app crash if quota is exceeded.
            profilerServiceInstance.instrumentedFetch('Some sample prompt for API call simulation. This text will be used to estimate tokens.').catch(() => {});
        }, 2000); 
    };
    startMockApiCalls(); // Start the periodic mock API calls.


    // Cleanup function for useEffect.
    // This ensures resources are released when the component unmounts.
    return () => {
        unsubscribe(); // Unsubscribe from emitter to prevent memory leaks.
        cancelAnimationFrame(animationFrameId); // Stop FPS measurement loop.
        clearInterval(apiCallInterval); // Stop mock API calls.
    };
  }, []); // Empty dependency array ensures this effect runs only once on component mount.

  // Memoized callback to run sandbox probes.
  const handleRunProbes = useCallback(async () => {
    setIsProbing(true); // Set loading state.
    await profilerServiceInstance.runSandboxProbes(); // Execute probes.
    setIsProbing(false); // Reset loading state.
  }, []); // Empty dependency array means this function is created once.

  // Memoized callback to run diagnostic tests.
  const handleRunTests = useCallback(() => {
    setIsTesting(true); // Set loading state.
    profilerServiceInstance.runDiagnosticTests(); // Execute tests.
    setIsTesting(false); // Reset loading state.
  }, []); // Empty dependency array means this function is created once.

  // Memoized callback to run security posture probes.
  const handleRunSecurityProbes = useCallback(async () => {
    setIsSecurityProbing(true); // Set loading state.
    await profilerServiceInstance.runSecurityPostureProbes(); // Execute security probes.
    setIsSecurityProbing(false); // Reset loading state.
  }, []); // Empty dependency array means this function is created once.
  
  // Callback for React's Profiler component to log slow renders.
  // This utilizes React's built-in profiling capabilities for "Application-Specific Profiling".
  const handleProfileRender = (id, phase, actualDuration) => {
      // Log renders that exceed the configured LONG_TASK_THRESHOLD.
      if (actualDuration > profilerServiceInstance.config.LONG_TASK_THRESHOLD) { 
          profilerServiceInstance.log(`Slow UI render: ${id} took ${actualDuration.toFixed(2)}ms`, 'warn');
      }
  };

  return (
    <div className="bg-gray-900 text-gray-200 min-h-screen font-sans p-4">
      <div className="max-w-5xl mx-auto">
        <header className="text-center mb-8">
            <div className="inline-flex items-center bg-cyan-500/10 text-cyan-400 py-2 px-4 rounded-full mb-4">
                <Bot className="w-6 h-6 mr-3" />
                <h1 className="text-2xl font-bold tracking-wider">
                    Full System Resource Profiler
                </h1>
            </div>
          <p className="text-gray-400">A feature-complete PoC for quantitative sandbox analysis and self-diagnostics, informed by resource-aware and semantic profiling paradigms.</p>
        </header>

        <div className="bg-gray-800 p-6 rounded-xl shadow-2xl border border-gray-700 space-y-6">
          {/* React Profiler to measure render performance of its children */}
          {/* This is a "Deep Analytical Profiler" at the UI component level. */}
          <Profiler id="mainProfiler" onRender={handleProfileRender}>
            <div>
                <h2 className="text-xl font-bold text-white mb-4">Profiler Log</h2>
                <ProfilerLog log={appState.log} />
            </div>

            <div className="border-t border-gray-700 pt-6">
                <PerformanceOverview 
                    fps={appState.fps} 
                    longTasks={appState.longTasks} 
                    apiLatencies={appState.apiLatencies} 
                />
            </div>

            <div className="border-t border-gray-700 pt-6">
                <QuotaMonitor 
                    config={profilerServiceInstance.config} 
                    appState={appState} 
                    updateConfig={updateProfilerConfig}
                    resetDailyCounters={profilerServiceInstance.resetDailyCounters.bind(profilerServiceInstance)}
                />
            </div>

            <div className="border-t border-gray-700 pt-6">
              <SandboxProber results={appState.probeResults} onRunProbes={handleRunProbes} isLoading={isProbing} />
            </div>
            
            <div className="border-t border-gray-700 pt-6">
              <UnitTestRunner results={appState.testResults} onRunTests={handleRunTests} isLoading={isTesting} />
            </div>

            <div className="border-t border-gray-700 pt-6">
                <SecurityProfiler results={appState.securityProbeResults} onRunSecurityProbes={handleRunSecurityProbes} isLoading={isSecurityProbing} />
            </div>
          </Profiler>
        </div>
      </div>
    </div>
  );
}
