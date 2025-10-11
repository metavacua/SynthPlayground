;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Refuter API Back-end (Common LISP with Hunchentoot)
;;;
;;; Serves static frontend files and provides API endpoints
;;; for the Refuter application.
;;; Uses Hunchentoot's easy-acceptor with :document-root
;;; for efficient static file serving and define-easy-handler
;;; for API routing. Includes graceful shutdown on SIGINT.
;;;
;;; FIXED: Corrected JSON formatting in error handlers.
;;; FIXED: Corrected variable name typos in restart-refuter-api.
;;; FIXED: Corrected typo in *refuter-api-file-path*.
;;; FIXED: Added method check in /refute handler.
;;; FIXED: Switched to easy-acceptor in start-refuter-api.
;;; FIXED: Moved define-easy-handler forms before start-refuter-api.
;;; FIXED: Corrected TRUENAME call in start-refuter-api when defaulting frontend-dir.
;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Define a package for the API code to avoid conflicts
(defpackage #:refuter-api
  ;; Use standard CL, Hunchentoot, and Jonathan for JSON.
  ;; Import necessary symbols from sb-posix for file system operations and signal handling.
  ;; Note: SIGNAL is not external in SB-POSIX, so we use sb-posix:signal directly.
  (:use #:cl #:hunchentoot #:jonathan)
  (:import-from #:sb-posix #:chdir #:getcwd #:sigint) ;; Import chdir, getcwd, sigint
  (:import-from #:sb-sys #:enable-interrupt) ;; Import enable-interrupt for signal handling
  (:import-from #:sb-ext #:*load-truename*) ;; Import *load-truename* for self-path
  ;; Export server control and frontend directory variable
  (:export #:start-refuter-api #:stop-refuter-api #:*frontend-directory*
           #:restart-refuter-api #:*api-server* #:*refuter-api-file-path*)) ;; Export public interface

(in-package #:refuter-api)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Configuration Variables
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defvar *frontend-directory* nil
  "The absolute path to the directory containing the frontend HTML, CSS, and JS files.
   Defaults to the current working directory if NIL when START-REFUTER-API is called.")

(defvar *api-server* nil
  "Holds the current Hunchentoot acceptor instance for the refuter API.
   Used by the restart function and signal handler to stop a running server.")

;; FIXED: Corrected variable name typo
(defvar *refuter-api-file-path* nil
  "Stores the absolute pathname of the refuter-api.lisp file after it has been loaded.
   Used by restart-refuter-api to reload the source file.
   This variable is set automatically when the file is loaded.")

;; Global variables to store the last used startup arguments for restart
(defvar *last-started-port* 8080
  "Stores the port number used in the most recent START-REFUTER-API call.")

(defvar *last-started-frontend-dir* nil
  "Stores the frontend directory pathname used in the most recent START-REFUTER-API call.")


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Automation: Set script path on load
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; This form is evaluated when the file is loaded.
(when *load-truename*
  ;; FIXED: Corrected variable name typo
  (setf *refuter-api-file-path* (truename *load-truename*))
  ;; FIXED: Corrected variable name typo in format string
  (format t "~&[INFO] Refuter API script path automatically set to: ~S~%" *refuter-api-file-path*)
  (finish-output))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Server Control Functions
;;; (Functions defined in order of dependency to avoid forward references)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun stop-refuter-api ()
  "Stops the running refuter API server.
   Includes FINISH-OUTPUT and small sleep for immediate REPL feedback."
  (when *api-server*
    (format t "~&[INFO] Stopping refuter API server...~%")
    (finish-output) ;; Ensure message is displayed immediately
    (sleep 0.01) ;; Small sleep to potentially aid output flushing
    (handler-case
        (stop *api-server*)
      (error (e)
        (format *error-output* "~&[ERROR] Error stopping Hunchentoot acceptor: ~A~%" e)
        (format *error-output* "~&[ERROR] The server instance may not have shut down cleanly.~%")
        (finish-output *error-output*)
        ;; Continue even if stopping failed, to attempt setting *api-server* to nil
        ))
    (setf *api-server* nil)
    (format t "~&[INFO] API server stopped.~%")
    (finish-output) ;; Ensure message is displayed immediately
    (sleep 0.01))) ;; Small sleep to potentially aid output flushing

;; Define the signal handler before the function that uses it.
(defun handle-termination-signal (signal &rest args)
  "Handler function for termination signals (SIGINT, SIGTERM).
   Calls STOP-REFUTER-API and exits the Lisp process.
   Accepts &rest args to handle potential unexpected arguments from sb-sys:enable-interrupt."
  (declare (ignore args)) ;; Ignore the rest of the arguments
  (format t "~&[INFO] Received signal ~A. Stopping server...~%" signal)
  (finish-output) ;; Ensure message is displayed immediately
  (sleep 0.01) ;; Small sleep to potentially aid output flushing
  (stop-refuter-api)
  (format t "~&[INFO] Server stopped by signal.~%")
  (finish-output) ;; Ensure message is displayed immediately
  (sleep 0.01) ;; Small sleep to potentially aid output flushing
  ;; Exit the Lisp process cleanly after stopping the server
  (sb-ext:exit :code 0))

;; Helper to restart the server for convenience during testing
;; (Defined after START-REFUTER-API, but relies on its definition being evaluated)
(defun restart-refuter-api (&key (port nil port-provided-p) (frontend-dir nil frontend-dir-provided-p))
  "Restarts the refuter API server.
   If PORT or FRONTEND-DIR are not provided, uses the values from the last successful start.
   Includes FINISH-OUTPUT and small sleeps for immediate REPL feedback."
  (format t "~&[INFO] Attempting to restart refuter API server...~%")
  (finish-output) ;; Ensure message is displayed immediately
  (sleep 0.01) ;; Small sleep to potentially aid output flushing
  (when *api-server*
    (format t "~&[INFO] Stopping existing server before restart...~%")
    (finish-output) ;; Ensure message is displayed immediately
    (sleep 0.01) ;; Small sleep to potentially aid output flushing
    (stop-refuter-api)
    (format t "~&[INFO] Existing server stopped.~%")
    (finish-output) ;; Ensure message is displayed immediately
    (sleep 0.01)) ;; Small sleep to potentially aid output flushing
  (let ((restart-port (if port-provided-p port *last-started-port*))
        (restart-frontend-dir (if frontend-dir-provided-p frontend-dir *last-started-frontend-dir*)))
    (format t "~&[INFO] Starting server with port ~A and frontend directory ~S...~%"
            restart-port restart-frontend-dir)
    (finish-output) ;; Ensure message is displayed immediately
    (sleep 0.01) ;; Small sleep to potentially aid output flushing
    ;; Note: We need to reload the source file here to pick up any code changes
    ;; before restarting. This requires *refuter-api-file-path* to be set (which is now automated).
    ;; FIXED: Corrected variable name typo
    (let ((source-file *refuter-api-file-path*))
      (if source-file
          (progn
            (format t "~&[INFO] Reloading source file: ~S~%" source-file)
            (finish-output)
            (load source-file))
          ;; Wrapped the two forms in the ELSE clause of the IF in a PROGN
          (progn
            (format t "~&[WARNING] Cannot reload source file: *refuter-api-file-path* is not set.~%")
            (finish-output)))))
    ;; FIXED: Use the correct variable names (restart-port, restart-frontend-dir)
    (start-refuter-api :port restart-port :frontend-dir restart-frontend-dir))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Web Endpoints
;;; define-easy-handler registers these with the default easy-acceptor.
;;; THESE ARE DEFINED *BEFORE* THE SERVER START FUNCTION.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Web endpoint to stop the server.
(define-easy-handler (stop-server-endpoint :uri "/stop-server") ()
  "Web endpoint to stop the refuter API server gracefully."
  (format t "~&[INFO] Entering /stop-server handler...~%")
  (finish-output)

  (setf (hunchentoot:content-type*) "application/json")
  (handler-case
      (progn
        ;; Call the stop function. This will check if *api-server* is non-nil.
        (stop-refuter-api)
        (jojo:to-json '(:obj ("status" . "success") ("message" . "Server stop requested."))))
    (error (e)
      (setf (hunchentoot:return-code*) hunchentoot:+http-internal-server-error+)
      ;; FIXED: Corrected JSON formatting for error message
      (jojo:to-json (list :obj (cons "status" "error") (cons "message" (format nil "Error stopping server: ~A" e)))))))

;; Web endpoint to restart the server. Uses last used arguments.
(define-easy-handler (restart-server-endpoint :uri "/restart-server") ()
  "Web endpoint to restart the refuter API server. Uses last used arguments."
  (format t "~&[INFO] Entering /restart-server handler...~%")
  (finish-output)

  (setf (hunchentoot:content-type*) "application/json")
  (handler-case
      (progn
        ;; Call the restart function.
        (restart-refuter-api)
        (jojo:to-json '(:obj ("status" . "success") ("message" . "Server restart requested."))))
    (error (e)
      (setf (hunchentoot:return-code*) hunchentoot:+http-internal-server-error+)
      ;; FIXED: Corrected JSON formatting for error message
      (jojo:to-json (list :obj (cons "status" "error") (cons "message" (format nil "Error restarting server: ~A" e)))))))

;; Placeholder for the Refute API endpoint
;; FIXED: Corrected :uri specification to a string.
;; Added method check within the handler.
(define-easy-handler (refute-endpoint :uri "/refute") ()
  "Placeholder API endpoint to receive a formula for refutation."
  (format t "~&[INFO] Entering /refute handler (placeholder)...~%")
  (finish-output)

  ;; FIXED: Check if the request method is POST
  (unless (eq (hunchentoot:request-method*) :post)
    (setf (hunchentoot:return-code*) hunchentoot:+http-method-not-allowed+)
    (setf (hunchentoot:header-out "Allow") "POST") ;; Indicate that only POST is allowed
    (setf (hunchentoot:content-type*) "text/plain")
    (return-from refute-endpoint "Method Not Allowed. Only POST requests are accepted for /refute."))

  (setf (content-type*) "application/json")
  ;; For now, just acknowledge receipt of data
  (let ((request-body (raw-post-data :force-text t)))
    (format t "~&[DEBUG] Received request body: ~S~%" request-body)
    (finish-output)
    (jojo:to-json '(:obj ("status" . "received") ("message" . "Formula received by placeholder endpoint."))))
  )


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Main Server Start Function
;;; Uses easy-acceptor with :document-root.
;;; THIS FUNCTION IS DEFINED *AFTER* THE WEB ENDPOINTS.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun start-refuter-api (&key (port 8080) (frontend-dir nil frontend-dir-provided-p))
  "Starts the Hunchentoot web server for the refuter API and serves frontend files.
   Defaults *frontend-directory* to the script's directory if not provided.
   Includes error handling for 'address in use'.
   Changes the process's CWD to *frontend-directory* (useful for other file ops).
   Installs a SIGINT handler for graceful shutdown.
   Uses easy-acceptor with :document-root for static file serving."

  (format t "~&[INFO] Starting refuter API server...~%")
  (finish-output) ;; Ensure message is displayed immediately
  (sleep 0.01) ;; Small sleep to potentially aid output flushing

  ;; Determine the frontend directory: use provided, or default to script's directory
  (let ((effective-frontend-dir-designator ;; Use a new variable name to indicate it's a designator
          (if frontend-dir-provided-p
              frontend-dir ;; Use the provided designator directly
              ;; FIXED: Corrected variable name typo
              (if *refuter-api-file-path*
                  ;; If defaulting to script's directory, get the list and make a pathname from it
                  ;; FIXED: Corrected variable name typo
                  (make-pathname :directory (pathname-directory *refuter-api-file-path*))
                  ;; Fallback to CWD string
                  (getcwd)))))

    ;; Set the frontend directory and ensure it's an absolute directory pathname
    (if effective-frontend-dir-designator ;; Check if a designator was found
        ;; Use truename on the effective-frontend-dir-designator
        (let ((dir-string (namestring (truename effective-frontend-dir-designator)))) ;; Use truename to resolve symlinks etc.
          (unless (char= (aref dir-string (1- (length dir-string))) #\/)
            (setf dir-string (concatenate 'string dir-string "/")))
          (setf *frontend-directory* (pathname dir-string))
          (format t "~&[INFO] Frontend directory set to: ~S~%" *frontend-directory*)
          (finish-output) ;; Ensure message is displayed immediately
          (sleep 0.01)) ;; Small sleep to potentially aid output flushing
        (progn
          ;; This case should ideally not be reached with the fallback to CWD
          (setf *frontend-directory* nil)
          (format t "~&[ERROR] Frontend directory could not be determined. Static file serving will not be configured via :document-root.~%")
          (format t "~&[INFO] Please provide the :frontend-dir argument to start-refuter-api if this issue persists.~%")
          (finish-output) ;; Ensure message is displayed immediately
          (sleep 0.01)))) ;; Small sleep to potentially aid output flushing


  ;; Change the process's current working directory to the frontend directory.
  ;; Still useful for general Lisp process context, even if not directly
  ;; used by :document-root serving.
  (if *frontend-directory*
      (handler-case
          (chdir (namestring *frontend-directory*))
        (error (e)
          (format *error-output* "~&[ERROR] Error changing current directory to ~S: ~A~%"
                  (namestring *frontend-directory*) e)
          (format *error-output* "~&[WARNING] Process CWD might not be as expected.~%")
          (finish-output *error-output*) ;; Ensure error message is displayed immediately
          (sleep 0.01))) ;; Small sleep to potentially aid output flushing
      (progn
        (format t "~&[INFO] Skipping CWD change as frontend directory is not set.~%")
        (finish-output) ;; Ensure message is displayed immediately
        (sleep 0.01))) ;; Small sleep to potentially aid output flushing

  (format t "[INFO] Attempting to start server on port ~A, CWD is ~A...~%"
          port (getcwd))
  (finish-output) ;; Ensure message is displayed immediately
  (sleep 0.01) ;; Small sleep to potentially aid output flushing

  ;; --- Use easy-acceptor with :document-root ---
  ;; easy-acceptor automatically picks up handlers defined with define-easy-handler.
  (handler-case
      (progn
        (setf *api-server*
              (start (make-instance 'easy-acceptor ;; Switched to easy-acceptor
                                    :port port
                                    ;; Use the :document-root initarg - will be NIL if frontend-dir couldn't be determined
                                    :document-root *frontend-directory*)))

        ;; Store the arguments used for a potential restart
        (setf *last-started-port* port)
        (setf *last-started-frontend-dir* *frontend-directory*)

        ;; Enable signal handlers for graceful shutdown
        (format t "~&[INFO] Server started on port ~A. Press Ctrl+C in the REPL to stop gracefully.~%" port)
        (finish-output) ;; Ensure message is displayed immediately
        (sleep 0.01) ;; Small sleep to potentially aid output flushing
        (format t "~&[INFO] Registering signal handlers for SIGINT and SIGTERM...~%")
        (finish-output) ;; Ensure message is displayed immediately
        (sleep 0.01) ;; Small sleep to potentially aid output flushing

        ;; Enable handler for SIGINT (Ctrl+C) using sb-sys:enable-interrupt
        (sb-sys:enable-interrupt sb-unix:sigint #'handle-termination-signal)

        ;; Enable handler for SIGTERM (termination signal) using sb-sys:enable-interrupt
        (sb-sys:enable-interrupt sb-unix:sigterm #'handle-termination-signal)

        ;; Keep the main thread alive while the server is running.
        ;; The signal handlers will interrupt this loop.
        (loop (sleep 1))) ;; Sleep to avoid busy-waiting
    (usocket:address-in-use-error (e)
      (format *error-output* "~&[ERROR] Error: Port ~A is already in use.~%" port)
      (format *error-output* "~&[ERROR] Original error: ~A~%" e)
      (finish-output *error-output*) ;; Ensure error message is displayed immediately
      (setf *api-server* nil)
      nil)
    (error (e)
      (format *error-output* "~&[ERROR] An unexpected error occurred during server startup: ~A~%" e)
      (finish-output *error-output*) ;; Ensure error message is displayed immediately
      (setf *api-server* nil)
      nil)))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Instructions for Use
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;; To use this script:
;;
;; 1. Save this code as a .lisp file (e.g., refuter-api.lisp).
;;
;; 2. Create a directory for your frontend static files (e.g., 'frontend').
;;    Place your index.html, style.css, script.js, etc. in this directory.
;;    For the automated default to work, this directory should ideally be
;;    the same directory where you save the refuter-api.lisp file.
;;
;; 3. Start your SBCL REPL.
;;
;; 4. Load the necessary dependencies using your minimal setup script (QHJ.lisp):
;;    (load "path/to/your/QHJ.lisp")
;;    (setup-dependencies)
;;
;; 5. Load this API script:
;;    (load "path/to/refuter-api.lisp")
;;    *refuter-api-file-path* will be set automatically during this step.
;;    The web endpoints will also be registered during this load.
;;
;; 6. Start the API server:
;;    (refuter-api:start-refuter-api) ;; Uses default port 8080 and defaults frontend-dir to the script's directory.
;;    OR
;;    (refuter-api:start-refuter-api :port 9090 :frontend-dir #P"/absolute/path/to/your/custom/frontend/") ;; Specify custom port and directory.
;;
;; 7. Access the server in your web browser at http://localhost:8080/ (or the custom port).
;;    You should see your index.html page if it's in the default or specified frontend directory.
;;
;; 8. To stop the server gracefully from the REPL, return to the SBCL REPL and press Ctrl+C.
;;    The signal handler will stop the Hunchentoot acceptor and exit the Lisp process cleanly.
;;
;; 9. You can also use (refuter-api:stop-refuter-api) or
;;    (refuter-api:restart-refuter-api) from the REPL.
;;    RESTART-REFUTER-API will reload the source file and restart the server
;;    using the last used port and frontend directory.
;;
;; 10. The /stop-server and /restart-server web endpoints are also available.
;;     You can test these using your frontend buttons or tools like curl.
;;     They should now work correctly after loading the file.
;;
;; 11. The /refute endpoint is a placeholder. It will accept POST requests
;;     and print the received body to the REPL, returning a placeholder JSON response.
;;     The next step is to integrate the refuter logic here.
;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

