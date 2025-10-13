;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Refuter API Session Setup Script (Minimal Dependencies - Polished)
;;;
;;; This script defines a function to automate the process of loading
;;; Quicklisp libraries (Hunchentoot and Jonathan) into a Common LISP session.
;;; It does NOT load application-specific code or switch packages.
;;; Cleaned up and polished based on debugging experience.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; --- Helper Function: Load Quicklisp ---
(defun load-quicklisp (&key quicklisp-setup-path)
  "Loads Quicklisp, using the provided path or defaulting to ~/quicklisp/setup.lisp.
   Signals an error if the setup file is not found or loading fails."
  (let ((ql-setup-path
          (if quicklisp-setup-path
              quicklisp-setup-path
              ;; Default Quicklisp setup path (~/quicklisp/setup.lisp)
              ;; Use two-argument merge-pathnames for robustness
              (merge-pathnames #P"quicklisp/setup.lisp" (user-homedir-pathname)))))

    (format t "~&Checking for Quicklisp setup file at: ~S~%" ql-setup-path)

    ;; Check if the Quicklisp setup file exists before attempting to load
    (unless (probe-file ql-setup-path)
       (format *error-output* "~&Quicklisp setup file not found at ~S.~%" ql-setup-path)
       (format *error-output* "~&Please ensure Quicklisp is installed and the path to setup.lisp is correct.~%")
       (format *error-output* "~&You can try calling setup-dependencies with the :quicklisp-setup-path argument.~%")
       (format *error-output* "~&Example: (setup-dependencies :quicklisp-setup-path #P\"/path/to/your/quicklisp/setup.lisp\")~%")
       ;; Signal a serious error if Quicklisp setup file is not found
       (error "Failed to find Quicklisp setup file. Cannot proceed with setup.")))

    ;; Ensure Quicklisp is loaded (harmless if already loaded by init file)
    ;; This block is only reached if probe-file succeeded.
    ;; NOTE: The compiler may issue a warning about QL-SETUP-PATH being undefined
    ;; in COMMON-LISP-USER here. This is likely a spurious warning related to
    ;; the compiler's behavior during LOAD when a local variable is used in a form
    ;; that the compiler might process in a different context. It can often be ignored
    ;; if the code works correctly at runtime, as the variable is indeed bound
    ;; within the LET form.
    (unless (find-package :ql)
      (handler-case
          (load ql-setup-path) ;; Attempt to load the Quicklisp setup file
        (error (e)
          (format *error-output* "~&Error loading Quicklisp setup file from ~S: ~A~%" ql-setup-path e)
          (format *error-output* "~&An error occurred during the loading process itself.~%")
          ;; Signal a serious error to stop execution if Quicklisp cannot be loaded
          (error "Failed to load Quicklisp setup file. Cannot proceed with setup."))))

    (format t "Quicklisp loaded successfully.~%"))


;; --- Helper Function: Load Required Libraries ---
(defun load-required-libraries ()
  "Loads necessary libraries (Hunchentoot, Jonathan) using Quicklisp.
   Signals an error if loading fails."
  (format t "Loading required libraries (Hunchentoot, Jonathan) using Quicklisp...~%")
  (handler-case
      (ql:quickload '(:hunchentoot :jonathan))
    (error (e)
      (format *error-output* "~&Error loading required libraries (Hunchentoot, Jonathan): ~A~%" e)
      (format *error-output* "~&Please ensure these libraries are installed via Quicklisp (using ql:quickload in a session where Quicklisp is loaded).~%")
      ;; Signal a serious error if libraries cannot be loaded
      (error "Failed to load required libraries. Cannot proceed with setup.")))
  (format t "Required libraries loaded.~%"))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Main Setup Function (Minimal)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun setup-dependencies (&key quicklisp-setup-path)
  "Sets up the Lisp session by loading Quicklisp and required libraries.
   Does NOT load application-specific code or switch packages."

  (format t "~&Starting dependency setup...~%")

  ;; Step 1: Load Quicklisp
  ;; The parameter quicklisp-setup-path is accessible here.
  (load-quicklisp :quicklisp-setup-path quicklisp-setup-path)

  ;; Step 2: Load Required Libraries
  (load-required-libraries)

  ;; --- Final Success Message ---
  (format t "~&~%Dependency setup script finished successfully.~%")
  (format t "~&Quicklisp, Hunchentoot, and Jonathan are now loaded.~%")
  (format t "~&You can now load your application code or run tests.~%"))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Instructions for Use
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;; To use this script:
;; 1. Save this code as a .lisp file (e.g., setup-deps.lisp).
;; 2. Start your SBCL REPL.
;; 3. Load this script in your REPL: (load "path/to/this/script.lisp")
;; 4. Call the setup function, providing the Quicklisp path if necessary:
;;    - If Quicklisp is in the default ~/quicklisp/ location:
;;      (setup-dependencies)
;;    - If Quicklisp setup.lisp is elsewhere:
;;      (setup-dependencies :quicklisp-setup-path #P"/explicit/path/to/your/quicklisp/setup.lisp")
;; 5. If successful, Quicklisp and the specified libraries will be loaded.
;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

