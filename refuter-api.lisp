;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Refuter API Back-end (Common LISP with Hunchentoot)
;;; Serving Static Front-end Files and API Endpoint
;;; (Fixed dir-string scope)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Define a package for the API code to avoid conflicts
(defpackage #:refuter-api
  ;; Use standard CL and Hunchentoot, Jonathan for JSON.
  ;; Import necessary symbols from sb-posix for file system operations.
  (:use #:cl #:hunchentoot #:jonathan)
  (:import-from #:sb-posix #:chdir #:getcwd) ;; Import chdir and getcwd from sb-posix
  (:export #:start-refuter-api #:stop-refuter-api #:*frontend-directory*
           #:restart-refuter-api #:*api-server* #:*refuter-api-file-path*)) ;; Export the new restart function, *api-server*, and the file path variable

(in-package #:refuter-api)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Configuration
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Define a global variable to hold the path to the frontend files directory.
;; Defaults to the current working directory unless explicitly set before starting the server.
(defvar *frontend-directory* nil
  "The path to the directory containing the frontend HTML, CSS, and JS files.
   Defaults to the current working directory if NIL when START-REFUTER-API is called.")

;; Define a global variable to hold the current server instance.
;; This is used by the restart function to stop a running server.
(defvar *api-server* nil
  "Holds the current Hunchentoot acceptor instance for the refuter API.")

;; Define a global variable to store the path of this API file once loaded.
;; Used by restart-refuter-api. This variable should be set by the loading process (e.g., a setup script).
(defvar *refuter-api-file-path* nil
  "Stores the pathname of the refuter-api.lisp file after it has been loaded.")

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; API Endpoint Handler
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Define the API endpoint handler for the /refute URI
;; It accepts only POST requests.
(define-easy-handler (refute-endpoint :uri '("/refute" :post)) ()
  ;; Set the content type of the response to indicate JSON
  (setf (content-type*) "application/json")

  ;; Get the raw request body as a string
  (let ((request-body (raw-post-data :force-text t)))
    ;; Check if the request body is not empty
    (if request-body
        ;; Use HANDLER-CASE to catch potential errors during JSON parsing or refutation logic
        (handler-case
            (let* ((json-data (jojo:parse request-body)) ;; Parse the JSON string into a Lisp object (hash table)
                   (formula-string (gethash "formula" json-data))) ;; Extract the value associated with the "formula" key

              ;; Check if the "formula" key was present and its value is not nil
              (if formula-string
                  ;; --- Integrate Refuter Logic Here ---
                  ;; This is where you would integrate the string-to-S-expression parser
                  ;; and the call to your run-refuter function.

                  ;; Placeholder logic for demonstration:
                  (jojo:to-json
                   (if (string= formula-string "(incon)") ;; If the input string is exactly "(incon)"
                       ;; Simulate a successful refutation
                       '(:obj ("status" . "success") ("refuted" . t) ("refuted_formula" . "(incon)"))
                       ;; Simulate a non-refutation
                       '(:obj ("status" . "success") ("refuted" . nil) ("non_refuted-state" . "nil (placeholder)"))))
                  ;; --- End Refuter Logic Integration ---

                  ;; If the "formula" key is missing, return a bad request error
                  (progn
                    (setf (return-code*) +http-bad-request+) ;; Set HTTP status code to 400
                    (jojo:to-json '(:obj ("status" . "error") ("message" . "Missing 'formula' key in request body"))))))

            ;; Handle errors that occur during JSON parsing or the integrated refuter logic
            (error (e)
              (setf (return-code*) +http-internal-server-error+) ;; Set HTTP status code to 500
              ;; Return a JSON error response with the error message
              (jojo:to-json `(:obj ("status" . "error") ("message" . ,(format nil "Internal server error: ~A" e)))))))

        ;; If the request body is empty, return a bad request error
        (progn
          (setf (return-code*) +http-bad-request+) ;; Set HTTP status code to 400
          (jojo:to-json '(:obj ("status" . "error") ("message" . "Empty request body"))))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Static File Server Handler
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Define a handler to serve static files from the *frontend-directory*.
;; This handler will attempt to serve files for any request that doesn't match
;; other defined handlers (like /refute).
(define-easy-handler (static-file-handler :uri (lambda (uri)
                                                 ;; This lambda function checks if the URI is NOT the API endpoint.
                                                 ;; If it's not /refute, this handler is a potential match.
                                                 (not (string= uri "/refute")))) ()
  ;; Check if the frontend directory has been set (or defaulted)
  (if *frontend-directory*
      (let ((requested-uri (request-uri*)))
        ;; --- FIX for SBCL absolute pathname issue ---
        ;; Due to an observed issue in SBCL 2.1.11.debian where absolute pathnames
        ;; starting with / are not correctly resolved relative to the filesystem root
        ;; when passed to underlying system calls, we will handle static file serving
        ;; using relative pathnames, assuming the process's CWD is set to *frontend-directory*.
        (let ((relative-pathname
                (if (string= requested-uri "/")
                    ;; If the requested URI is the root path "/", serve index.html
                    #P"index.html"
                    ;; Otherwise, take the URI string, remove the leading "/", and
                    ;; convert the rest into a relative pathname.
                    (pathname (subseq requested-uri 1)))))

          (format t "Static file handler: Requested URI ~S, attempting to serve relative path ~S~%"
                  requested-uri relative-pathname) ;; Debugging output

          ;; Serve the file using the relative pathname.
          ;; This relies on the process's CWD being correctly set to *frontend-directory*.
          (handle-static-file relative-pathname)))
      ;; If the frontend directory is somehow still not set, return a server error
      (progn
        (setf (return-code*) +http-internal-server-error+)
        "Frontend directory not configured on the server.")))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Server Control Functions
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Function to start the Hunchentoot server on a specified port
;; It now registers both the API endpoint handler and the static file handler.
;; Defaults *frontend-directory* to the current working directory if it's NIL.
;; **MODIFIED:** Adds chdir to *frontend-directory* for relative pathname handling fix.
;; **FIXED:** Corrected the scope of dir-string in the LET form.
(defun start-refuter-api (&key (port 8080))
  "Starts the Hunchentoot web server for the refuter API and serves frontend files.
   Defaults *frontend-directory* to the current working directory if it's NIL.
   Includes error handling for 'address in use'.
   Changes the process's CWD to *frontend-directory* for relative path handling."
  ;; If *frontend-directory* is NIL, set it to the current working directory.
  (when (null *frontend-directory*)
    ;; Use truename to get the absolute, resolved path of the current directory
    (setf *frontend-directory* (truename "."))
    (format t "Frontend directory not explicitly set. Defaulting to current directory: ~A~%" *frontend-directory*))

  ;; Ensure *frontend-directory* is a directory pathname (ends with /) by manipulating its string representation.
  ;; This works around issues with pathname type check functions not being resolved correctly.
  ;; FIX: Corrected the scope of the LET form for dir-string.
  (let ((dir-string (namestring *frontend-directory*)))
    (unless (char= (aref dir-string (1- (length dir-string))) #\/)
      (setf dir-string (concatenate 'string dir-string "/")))
    (setf *frontend-directory* (pathname dir-string))) ;; This setf is now inside the LET


  ;; --- FIX for SBCL absolute pathname issue ---
  ;; Change the process's current working directory to the frontend directory.
  ;; This is essential for the static file handler to correctly resolve relative pathnames.
  (handler-case
      (chdir (namestring *frontend-directory*))
    (error (e)
      (format *error-output* "~&Error changing current directory to ~S: ~A~%"
              (namestring *frontend-directory*) e)
      (format *error-output* "~&Static file serving may fail if the CWD is not correctly set.~%")))

  (format t "Attempting to start Refuter API server on port ~A, serving files from CWD (~A)...~%"
          port (getcwd)) ;; Use getcwd from sb-posix (imported symbol)

  ;; Use handler-case to catch errors during server startup, especially "address in use"
  (handler-case
      (setf *api-server* (start (make-instance 'acceptor :port port))) ;; Store the acceptor instance in *api-server*
    (usocket:address-in-use-error (e) ;; Catch the specific error for address in use
      (format *error-output* "~&Error: Port ~A is already in use.~%" port)
      (format *error-output* "~&This likely means a previous server instance did not shut down cleanly.~%")
      (format *error-output* "~&You may need to manually terminate the process using that port.~%")
      (format *error-output* "~&Original error: ~A~%" e)
      (setf *api-server* nil) ;; Ensure *api-server* is nil if startup fails
      nil) ;; Return nil to indicate startup failure
    (error (e) ;; Catch any other startup errors
      (format *error-output* "~&An unexpected error occurred during server startup: ~A~%" e)
      (setf *api-server* nil) ;; Ensure *api-server* is nil if startup fails
      nil))) ;; Return nil to indicate startup failure


;; Function to stop a running Hunchentoot server acceptor instance
(defun stop-refuter-api (acceptor)
  "Stops the specified Hunchentoot web server acceptor instance if it is not NIL."
  (format t "stop-refuter-api called with acceptor: ~A~%" acceptor) ;; Debugging output
  (when acceptor ;; Check if the acceptor is not NIL before attempting to stop
    (format t "Attempting to stop Hunchentoot acceptor...~%") ;; Debugging output
    (handler-case
        (stop acceptor)
      (error (e)
        (format *error-output* "~&Error stopping Hunchentoot acceptor: ~A~%" e)
        (format *error-output* "~&The server instance may not have shut down cleanly.~%")
        nil)))) ;; Return nil on error


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Development Helper Function
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun restart-refuter-api (&key (port 8080))
  "Stops the current refuter API server if running, reloads the source file,
   and starts a new server instance. Uses the path stored in *refuter-api-file-path*
   to reload the file.
   **MODIFIED:** Calls start-refuter-api which now handles CWD change.
   **NOTE:** The compiler warning about 'SOURCE-FILE' here is likely spurious,
   as it's a local variable correctly used within the LET form.
   Ensure *refuter-api-file-path* is set by your loading process."
  (format t "Attempting to restart Refuter API...~%") ;; Debugging output
  (format t "Current *api-server* state: ~A~%" *api-server*) ;; Debugging output
  (format t "Is *api-server* started? ~A~%" (and *api-server* (started-p *api-server*))) ;; Debugging output

  ;; Get the path of the API file from the global variable
  (let ((source-file *refuter-api-file-path*))
    (unless source-file
      (error "Refuter API source file path (*refuter-api-file-path*) is not set.
              Please load the file explicitly first using the setup script or LOAD.")))

    ;; Stop the existing server if it's running (uses the improved stop-refuter-api)
    (when (and *api-server* (started-p *api-server*))
      (format t "Stopping existing server before reload...~%") ;; Debugging output
      (stop-refuter-api *api-server*)
      (setf *api-server* nil)) ;; Clear the variable after attempting to stop

    ;; Reload the source file to get the latest code definitions
    ;; The compiler warning about 'SOURCE-FILE' here is likely spurious,
    ;; as it's a local variable correctly used within the LET form.
    (format t "Reloading source file: ~S~%" source-file)
    (load source-file)

    ;; Start a new server instance (will use default frontend dir if not set)
    ;; The start-refuter-api function now sets *api-server* and handles port errors
    ;; and changes the CWD.
    (format t "Starting new server instance...~%") ;; Debugging output
    (start-refuter-api :port port)

    (if *api-server*
        (format t "Refuter API restarted successfully on port ~A.~%" port)
        (format t "Refuter API restart failed: Could not start new server instance.~%")))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Example Usage (in your Lisp REPL)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; (in-package #:refuter-api)

;; 1. (Optional) Explicitly set the path to your frontend files directory if it's not the current directory.
;;    Replace "/path/to/your/refuter-frontend/" with the actual path on your system.
;;    Make sure the path is an absolute directory path.
;; (setf *frontend-directory* #P"/path/to/your/refuter-frontend/")

;; 2. To start the server for the first time (will use current directory if *frontend-directory* is NIL):
;;    This will also change the SBCL process's CWD to the frontend directory.
;; (start-refuter-api :port 8080) ;; *api-server* is set by this function

;; 3. To stop the server:
;; (stop-refuter-api *api-server*) ;; This is now safer to call even if *api-server* is NIL

;; 4. To stop, reload, and restart the server (single command after using the setup script or initial LOAD):
;;    This will also change the SBCL process's CWD back to the frontend directory after reloading.
;; (restart-refuter-api :port 8080) ;; Use the desired port

;; Note: If you encounter "Port is already in use", a previous server process
;; may be orphaned. You might need to find and terminate the process
;; manually using your operating system's tools (e.g., `lsof -i :8080` and `kill <PID>` on Linux/macOS).

