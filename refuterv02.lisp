;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Refuter Prototype (Architected: Core/Data Library + Execution Wrapper)
;;;
;;; This code implements the Refuter prototype following the
;;; "Core Logic/Data as Library with Execution Wrapper" architectural pattern.
;;;
;;; It is split into two packages:
;;; #:REFUTER-CORE: Contains the core logical system definition,
;;;                 formula data structures, rules, axioms, and
;;;                 knowledge base data structures.
;;; #:REFUTER-PROGRAM: Contains the program execution logic,
;;;                    orchestration, parsing,
;;;                    output formatting, and the main entry point.
;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Package: #:REFUTER-CORE (Core Logic & Data Management Library)
;;;
;;; Defines the logical system, formula representation,
;;; rules, axioms, and knowledge base data structures.
;;; Operates purely on internal data structures.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(defpackage #:refuter-core
  (:use #:cl)
  (:export
   ;; Formula Representation
   #:make-incon #:make-dep #:make-ind #:make-dual
   #:formula-type #:formula-arguments
   ;; Core Refutation Logic Entry Point
   #:core-refute-formula
   ;; Knowledge Base Data Structures (Accessed by Program layer)
   #:make-refutation-kbs
   #:refutation-kbs-kb-refuted
   #:refutation-kbs-kb-failed-refutation
   ;; Logical Constants
   #:incon-symbol #:dep-symbol #:ind-symbol #:dual-symbol))

(in-package #:refuter-core)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Logical Constants (Symbols)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defconstant incon-symbol 'incon "Symbol representing inconsistency.")
(defconstant dep-symbol 'dep "Symbol representing dependence.")
(defconstant ind-symbol 'ind "Symbol representing independence.")
(defconstant dual-symbol 'dual "Symbol representing duality.")

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Formula Representation (WFF as Lisp Lists) - Data Management
;;;
;;; Functions to create and access the S-expression representation of formulas.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun make-incon () (list incon-symbol))
(defun make-dep (formula1 formula2) (list dep-symbol formula1 formula2))
(defun make-ind (formula1 formula2) (list ind-symbol formula1 formula2))
(defun make-dual (formula) (list dual-symbol formula))

(defun formula-type (formula)
  "Extracts the operator type (the first element) from a formula S-expression.
   Assumes formula is a non-empty list."
  (first formula))

(defun formula-arguments (formula)
  "Extracts the arguments (the rest of the list) from a formula S-expression."
  (rest formula))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Knowledge Base Data Structures - Data Management
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defstruct refutation-kbs
  "Holds the knowledge bases for a single refutation run."
  (kb-refuted (make-hash-table :test 'equal) :type hash-table)
  (kb-failed-refutation (make-hash-table :test 'equal) :type hash-table))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Core Refutation Logic (Rules and Axioms) - Core Logic
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Forward declaration for recursive calls
(declaim (ftype (function (t refutation-kbs) t) core-refute-formula))

;; InconL Axiom: (incon) is refuted immediately.
(defun axiom-inconl (formula kbs)
  "Axiom InconL: Refutes (incon) - Base case for refutation.
   Returns formula if it's (incon), nil otherwise."
  (declare (ignore kbs))
  (if (and (consp formula) (eq (formula-type formula) incon-symbol)) ; Ensure formula is a list
      formula
      nil))

;; Rule dualL: Handles (dual A) cases based on revised semantics.
(defun rule-dual-l (formula kbs)
  "Rule dualL: Handles (dual A) cases based on revised semantics.
   - (dual 'incon) is NOT refuted.
   - (dual (incon)) is NOT refuted.
   - (dual (dual B)) is refuted if B is refuted.
   - Any other (dual A) is NOT refuted."
  (if (and (consp formula) (eq (formula-type formula) dual-symbol)) ; Ensure formula is a list
      (let ((formulaA (second formula))) ; This is the argument 'A'
        (cond
          ;; Case 1: A is the atomic 'incon-symbol'
          ((eq formulaA incon-symbol)
           nil) ; (dual 'incon) is NOT refuted

          ;; Case 2: A is the formula (incon)
          ((and (consp formulaA) (eq (formula-type formulaA) incon-symbol))
           nil) ; (dual (incon)) is NOT refuted

          ;; Case 3: A is (dual B), so original formula is (dual (dual B))
          ((and (consp formulaA) (eq (formula-type formulaA) dual-symbol))
           (let ((formulaB (second formulaA))) ; This is 'B'
             (if (core-refute-formula formulaB kbs) ; If B is refuted
                 formula  ; Then (dual (dual B)) IS refuted
                 nil)))   ; Else (B not refuted), so (dual (dual B)) is NOT refuted

          ;; Case 4: Any other (dual A) - these are not refuted by this rule
          (t
           nil))) ; Not refuted by this rule
      nil)) ; Not a 'dual' formula or not a list


;; Rule independenceL: Refutes (ind A B) if A is (incon), B is (incon), A is refuted, or B is refuted.
(defun rule-independence-l (formula kbs)
  "Independence Left Rule (rule independenceL) - Handles (ind A B) cases.
   Refutes if A is (incon), B is (incon), A is refuted, or B is refuted.
   Returns formula if refuted, nil otherwise."
  (if (and (consp formula) (eq (formula-type formula) ind-symbol)) ; Ensure formula is a list
      (let ((formula1 (second formula))
            (formula2 (third formula)))
        (cond
          ;; Base cases: If either argument is the formula (incon), (ind A B) is refuted.
          ((and (consp formula1) (eq (formula-type formula1) incon-symbol)) formula)
          ((and (consp formula2) (eq (formula-type formula2) incon-symbol)) formula)
          ;; Recursive cases: If either argument is refuted, (ind A B) is refuted.
          ((core-refute-formula formula1 kbs) formula)
          ((core-refute-formula formula2 kbs) formula)
          (t nil)))
      nil))

;; Rule dependenceL: Refutes (dep A B) if both A and B are refuted.
(defun rule-dependence-l (formula kbs)
  "Dependence Left Rule (rule dependenceL) - Handles (dep A B) formulae.
   Refutes if and only if both A and B are refuted.
   Returns formula if refuted, nil otherwise."
  (if (and (consp formula) (eq (formula-type formula) dep-symbol)) ; Ensure formula is a list
      (let ((formula1 (second formula))
            (formula2 (third formula)))
        (let ((refutation1-result (core-refute-formula formula1 kbs))
              (refutation2-result (core-refute-formula formula2 kbs)))
          (if (and refutation1-result refutation2-result)
              formula
              nil)))
      nil))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Core Refutation Logic Entry Point
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun core-refute-formula (formula kbs)
  "Core refutation logic for a single formula.
   Checks KBs, applies rules/axioms, and updates KBs.
   Returns the formula if refuted, NIL if not refuted.
   Handles atomic symbols by treating them as not refutable by these rules."

  ;; If formula is not a list (e.g., an atomic symbol like 'X, or 'INCON itself),
  ;; it cannot be processed by rules that expect a formula structure (op arg1 arg2).
  ;; Such atoms are considered "not refuted" by this system's current rules.
  ;; Add it to failed refutations and return nil.
  (unless (consp formula)
    (setf (gethash formula (refutation-kbs-kb-failed-refutation kbs)) t) ;; Record atom in failed KB
    (return-from core-refute-formula nil))

  ;; 1. Check KB_Refuted: If formula is already known to be refuted, return it.
  (when (gethash formula (refutation-kbs-kb-refuted kbs))
    (return-from core-refute-formula formula))

  ;; 2. Check KB_FailedRefutation: If formula is known to have failed refutation, return NIL.
  (when (gethash formula (refutation-kbs-kb-failed-refutation kbs))
    (return-from core-refute-formula nil))

  ;; 3. Attempt to apply rules/axioms based on formula type.
  (let ((refutation-result
          (let ((type (formula-type formula))) ; Get type once
            (cond
              ((eq type incon-symbol) (axiom-inconl formula kbs))
              ((eq type ind-symbol) (rule-independence-l formula kbs))
              ((eq type dep-symbol) (rule-dependence-l formula kbs))
              ((eq type dual-symbol) (rule-dual-l formula kbs))
              (t nil))))) ; No applicable rule/axiom for this formula type

  ;; 4. Update KBs based on the result and return.
  (if refutation-result
      (progn
        (setf (gethash formula (refutation-kbs-kb-refuted kbs)) t)
        refutation-result) ; Return the (refuted) formula itself
      (progn
        (setf (gethash formula (refutation-kbs-kb-failed-refutation kbs)) t)
        nil))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Package: #:REFUTER-PROGRAM (Program Execution Wrapper)
;;;
;;; Handles input parsing, orchestrates the
;;; refutation process using the core library, manages
;;; KBs for a run, formats output, and provides the main entry point.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(defpackage #:refuter-program
  (:use #:cl)
  (:import-from #:refuter-core
                #:make-incon #:make-dep #:make-ind #:make-dual
                ;; formula-type and formula-arguments are used internally by core,
                ;; but parser might need to know about symbols.
                #:core-refute-formula
                #:make-refutation-kbs
                #:refutation-kbs-kb-refuted
                #:refutation-kbs-kb-failed-refutation
                #:incon-symbol #:dep-symbol #:ind-symbol #:dual-symbol))

(in-package #:refuter-program)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Input Parsing with Symbol Interning
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun intern-formula-symbols (form target-package)
  "Recursively traverses a parsed S-expression and interns known operator
   symbols (INCON, DEP, IND, DUAL) into the target-package.
   Other symbols are left as they are (could be variables in an extended system)."
  (cond
    ((null form) nil)
    ((symbolp form)
     (let ((name (symbol-name form)))
       (cond
         ;; Check for exact symbol names that are part of the logic
         ((string-equal name (symbol-name refuter-core::incon-symbol)) (intern name target-package))
         ((string-equal name (symbol-name refuter-core::dep-symbol)) (intern name target-package))
         ((string-equal name (symbol-name refuter-core::ind-symbol)) (intern name target-package))
         ((string-equal name (symbol-name refuter-core::dual-symbol)) (intern name target-package))
         (t form)))) ; Return the original symbol if not a known operator
    ((consp form)
     (cons (intern-formula-symbols (car form) target-package)
           (intern-formula-symbols (cdr form) target-package)))
    (t form))) ; Return non-symbol, non-list atoms (e.g. numbers) as is

(defun parse-formula-string (formula-string)
  "Parses the string to an S-expression and interns known operator
   symbols into the REFUTER-CORE package."
  (handler-case
      (let ((raw-form (read-from-string formula-string nil nil)) ; read, don't error on eof for empty/whitespace
            (core-package (find-package '#:refuter-core)))
        (if raw-form
            (intern-formula-symbols raw-form core-package)
            (error "Parsing error: Input string is empty or invalid.")))
    (error (e)
      ;; Catch read errors or errors from intern-formula-symbols if any
      (error "Parsing error: ~A on string \"~A\"" e formula-string))))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Orchestration & KB Management
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun run-refuter (formula-string)
  "Runs the refuter on a formula provided as a string."
  (handler-case
      (let* ((formula (parse-formula-string formula-string))
             (kbs (refuter-core::make-refutation-kbs))
             (refuted-formula (refuter-core::core-refute-formula formula kbs)))
        (if refuted-formula
            (list :refuted refuted-formula)
            (list :not-refuted (generate-counterwitness-info formula kbs))))
    (error (e)
      (list :error (format nil "~A" e))))) ; Return the error message directly

(defun generate-counterwitness-info (original-formula kbs)
  "Generates information about why a formula was not refuted."
  (declare (ignore original-formula))
  (let ((failed-formulas ()))
    (maphash (lambda (key value)
               (declare (ignore value))
               (push key failed-formulas))
             (refuter-core::refutation-kbs-kb-failed-refutation kbs))
    (list :failed-formulas (nreverse failed-formulas)))) ; Reverse for potentially chronological order

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Output Formatting
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun format-refuter-output (result)
  "Formats the output of run-refuter into a human-readable string."
  (case (first result)
    (:refuted
     (format nil "Formula Refuted: ~S" (second result)))
    (:not-refuted
     (format nil "Formula Not Refuted. Counterwitness Info: ~S" (second result)))
    (:error
     (format nil "Error: ~A" (second result)))
    (t
     (format nil "Unexpected refuter result format: ~S" result))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Main Entry Point
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun main ()
  "Main function to run the refuter with example string inputs."
  (format t "Starting Architected Refuter Prototype.~%")

  (let ((test-formulas
          '("(incon)"                                         ; Should be Refuted
            "(dep (incon) (incon))"                           ; Should be Refuted
            "(ind (incon) (dual (dual (incon))))"             ; Should be Refuted
            "(dual (dual (incon)))"                           ; Should be Refuted
            "(dual incon)"                                    ; Should be Not Refuted (atomic incon) - NOW ALSO NOT REFUETD BY DUAL RULE
            "(dual (incon))"                                  ; Should be Not Refuted (formula (incon)) - NOT REFUETD BY DUAL RULE
            "(dual (dep (incon) (dual (dual (incon)))))"      ; A = (dep (incon) (incon)) -> A is Refuted. So (dual A) is Not Refuted by DUAL rule.
            "(dep (dual incon) (incon))"                      ; (dual 'incon) is Not Refuted. (incon) is Refuted. dep needs both refuted. So Not Refuted.
            "(dep incon (dual incon))"                        ; 'incon is Not Refuted. (dual 'incon) is Not Refuted. dep needs both. So Not Refuted.
            "(dep (dual incon) (dual incon))"                 ; (dual 'incon) is Not Refuted. Not Refuted.
            "(ind (dual incon) (dual (incon)))"               ; (dual 'incon) Not Refuted. (dual (incon)) Not Refuted. ind needs one refuted. So Not Refuted.
            ;; Complex examples from original list, adapted for clarity if needed
            "(dep (ind (incon) (incon)) (dual (dual (incon))))" ; (ind T T)->T. (dual (dual (incon))) -> (incon) -> T. (dep T T) -> T. Refuted.
            "(ind (dual (dep (incon) (incon))) (dep (incon) (incon)))" ; (dep (I) (I)) is R. (dual R) is NR by DUAL rule. (ind NR R) is R. Refuted.
            "(dual (dual foo))"                               ; B='foo'. 'foo' is NR. (dual (dual 'foo')) is NR by DUAL rule.
            "(dual bar)"                                      ; bar is NR. (dual bar) is NOW NOT R by DUAL rule.
            "(invalid formula syntax"                         ; Test parsing error
            "()"                                              ; Test empty list parsing
            "justaword"                                       ; Test atom parsing. Should now show JUSTAWORD in failed list.
            )))

    (dolist (formula-string test-formulas)
      (format t "~%--- Refuting formula string: ~S ---~%" formula-string)
      (let ((result (run-refuter formula-string)))
        (format t "~A~%" (format-refuter-output result)))))

  (format t "~%Architected Refuter Prototype Finished.~%"))

;; Run the main function when the script is loaded
;; For CL environments like SLIME, it's often better to load the file
;; and then call (refuter-program:main) from the REPL.
(main)

