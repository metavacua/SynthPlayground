;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Refactored RelNet Weaver Core (Formula-Aware Prototype) - L Rules Only - Operator-Specific Rules - REFUTER (Concise Output) - REFINED INCON/DUAL-INCON
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Data Structures (Minimal for Prototype) - Enhanced Node and Formulae
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defclass relnet-node ()
  ((name :initarg :name :accessor relnet-node-name)
   (type :initarg :type :accessor relnet-node-type)))

(defvar *knowledge-base* nil "Global Knowledge Base (Minimal for Prototype)")

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Complexity Metrics - Global Counters (Kept but not Printed in Concise Output)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defvar *refutation-axiom-applications-count* 0 "Counter for axiom applications in refutation.")
(defvar *refutation-rule-applications-count* 0 "Counter for rule applications in refutation.")


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Formula Representation (WFF and RFF as Lisp Lists)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun make-incon () '(incon))
(defun make-dep (formula1 formula2) `(dep ,formula1 ,formula2))
(defun make-ind (formula1 formula2) `(ind ,formula1 ,formula2))

(defun formula-type (formula)
  (first formula))

(defun formula-arguments (formula)
  (rest formula))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Axioms - COMPLEXITY COUNTING - InconL Axiom for IndL(A,A) & Incon Base Case
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; InconL Axiom: IndL(A, A) is refuted immediately
;; Incon Base Case: (incon) is refuted immediately

(defun axiom-inconl (formula)
  "Axiom InconL: Refutes (ind A A) and (incon) - Base case for refutation.
   Formula-aware.
   [Complexity Metric: refutation-axiom-applications-count]
   [Output: Concise - No verbose output]
   MODIFIED: Now handles both (ind A A) and (incon) base cases."
  (incf *refutation-axiom-applications-count*)
  (cond
    ((eq (formula-type formula) 'incon) formula)              ; Base case: (incon) is refuted
    ((and (eq (formula-type formula) 'ind)
          (equal (second formula) (third formula))) formula) ; Axiom: (ind A A) is refuted
    (t nil)))                                                 ; Axiom does not apply, return nil


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Rules (Dependence & Independence & Dual - Formula-Aware & Threaded) - COMPLEXITY COUNTING - OPERATOR-SPECIFIC RULES
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun rule-independence-l (formula kb)
  "Independence Left Rule (rule independenceL) - Now handles ONLY (ind A B) - Parallel OR.
   Formula-aware. Parallel OR in Refutation.
   Applies to (ind A B) formulae.
   [Complexity Metric: refutation-rule-applications-count]
   [Output: Concise - No verbose output]
   MODIFIED: Now ONLY handles (ind A B) formulae."
  (incf *refutation-rule-applications-count*)

  ;; Axiom Check First: InconL - for (ind A A) - moved to axiom-inconl
  (let ((axiom-result (axiom-inconl formula)))         ; Check if InconL axiom applies (for ind A A and incon)
    (if axiom-result
        (return-from rule-independence-l axiom-result))) ; If axiom applies, return result immediately

  (if (eq (formula-type formula) 'ind)
      (let ((formula1 (second formula))
            (formula2 (third formula)))
        (let ((premise1-result nil)
              (premise2-result nil))

          ;; Premise 1 for formula1 (alternative refutation path 1)
          (setf premise1-result (run-refuter formula1)) ; Recursive call to refuter for formula1

          ;; Premise 2 for formula2 (alternative refutation path 2)
          (setf premise2-result (run-refuter formula2)) ; Recursive call to refuter for formula2


          (if premise1-result                                       ; If formula1 is refuted, rule succeeds (OR)
              (return-from rule-independence-l formula)         ; Return original formula as refuted
              (if premise2-result                                       ; If formula2 is refuted, rule succeeds (OR)
                  (return-from rule-independence-l formula)         ; Return original formula as refuted
                  (return-from rule-independence-l nil)))))       ; Rule fails if neither premise refuted, return nil
      (rule-dependence-l formula kb)))                    ; Try rule-dependence-l next if not (ind formula)


(defun rule-dependence-l (formula kb)
  "Dependence Left Rule (rule dependenceL) - Formula-aware & SEQUENTIAL AND in Refutation (NOR dual).
   Applies to (dep A B) formulae.
   [Complexity Metric: refutation-rule-applications-count]
   [Output: Concise - No verbose output]
   MODIFIED: Now ONLY handles (dep A B) formulae."
  (incf *refutation-rule-applications-count*)

  (if (eq (formula-type formula) 'dep)
      (let ((formula1 (second formula))
            (formula2 (third formula)))
        (let ((refutation1-result (run-refuter formula1))  ; Recursive call to refuter for formula1
              (refutation2-result (run-refuter formula2)))  ; Recursive call to refuter for formula2
          (if (and refutation1-result refutation2-result)        ; Check if both sub-refutations returned a formula (success - AND)
              formula                                          ; Rule applied, return original formula as refuted
              nil)))                                          ; Rule failed, return nil
      nil))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Thread Functions (Refutation - Formula-Aware) -  REMOVED refutation-function
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; - refutation-function is now embodied within run-refuter (and rule dispatch)



;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Parallel Interface and Orchestration (Formula-Aware Prototype) - COMPLEXITY REPORTING
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun initialize-refutation-knowledge-base ()
  "Initializes the global *knowledge-base* and resets complexity counters for refutation."
  (setf *knowledge-base* nil)
  (reset-refutation-complexity-counters))

(defun reset-refutation-complexity-counters ()
  "Resets complexity counters for refutation."
  (setf *refutation-axiom-applications-count* 0)
  (setf *refutation-rule-applications-count* 0))


(defun run-refuter (formula)
  "Runs the theorem refuter prototype with refutation threads on a given formula.
   Orchestrates refutation attempts and determines the overall refuter result.
   [Complexity Reporting: refutation-axiom-applications-count, refutation-rule-applications-count]
   Now formula-aware: takes a formula as input.
   Outputs formula if refuted, nil if not.
   **MODIFIED: Refactored to dispatch to operator-specific rules. Incon and dual-incon base cases refined.**"
  (initialize-refutation-knowledge-base)
  (cond
    ((eq (formula-type formula) 'incon) (axiom-inconl formula))       ; Base case: incon - axiom check
    ((eq (formula-type formula) 'ind) (rule-independence-l formula *knowledge-base*)) ; Rule for ind
    ((eq (formula-type formula) 'dep) (rule-dependence-l formula *knowledge-base*))    ; Rule for dep
    (t nil)))                                                        ; No rule applies

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Main Entry Point - Run Refuter with Formula - COMPLEXITY REPORTING and TESTING
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun main ()
  (format t "Starting Formula-Aware Theorem Refuter Prototype (L-Rules Only - Operator-Specific Rules - Refined Incon/Dual-Incon).~%")

  ;; Example Formula Construction
  (let* ((incon-formula (make-incon))
         (dep-formula (make-dep incon-formula incon-formula))
         (ind-formula (make-ind incon-formula incon-formula))
         (self-ind-formula (make-ind incon-formula incon-formula)) ; (ind A A) where A is (incon) - for InconL axiom test
         (complex-formula (make-ind dep-formula ind-formula))
         (self-ref-formula (make-ind incon-formula incon-formula))) ; another (ind A A) for testing InconL axiom


    (format t "~%--- Testing with incon formula ---~%")
    (reset-refutation-complexity-counters)
    (let ((refuter-result (run-refuter incon-formula)))
      (format t "~%Refuter Result for formula ~A: ~A~%" incon-formula refuter-result)) ; EXPECTED: (INCON)

    (format t "~%--- Testing with (dep incon incon) formula ---~%")
    (reset-refutation-complexity-counters)
    (let ((refuter-result (run-refuter dep-formula)))
      (format t "~%Refuter Result for formula ~A: ~A~%" dep-formula refuter-result)) ; EXPECTED: NIL

    (format t "~%--- Testing with (ind incon incon) formula ---~%")
    (reset-refutation-complexity-counters)
    (let ((refuter-result (run-refuter ind-formula)))
      (format t "~%Refuter Result for formula ~A: ~A~%" ind-formula refuter-result)) ; EXPECTED: (IND (INCON) (INCON))

    (format t "~%--- Testing with (ind incon incon) - Self Independence Axiom (InconL) ---~%")
    (reset-refutation-complexity-counters)
    (let ((refuter-result (run-refuter self-ind-formula))) ; Testing (ind incon incon) - InconL axiom
      (format t "~%Refuter Result for formula ~A: ~A~%" self-ind-formula refuter-result)) ; EXPECTED: (IND (INCON) (INCON))

    (format t "~%--- Testing with (ind (dep incon incon) (ind incon incon)) formula ---~%")
    (reset-refutation-complexity-counters)
    (let ((refuter-result (run-refuter complex-formula)))
      (format t "~%Refuter Result for formula ~A: ~A~%" complex-formula refuter-result)) ; EXPECTED: (IND (DEP (INCON) (INCON)) (IND (INCON) (INCON)))

    (format t "~%--- Testing with another (ind incon incon) - Self Ref Axiom (InconL) ---~%")
    (reset-refutation-complexity-counters)
    (let ((refuter-result (run-refuter self-ref-formula))) ; Another test for (ind incon incon) - InconL axiom
      (format t "~%Refuter Result for formula ~A: ~A~%" self-ref-formula refuter-result)) ; EXPECTED: (IND (INCON) (INCON))

    (format t "~%Formula-Aware Theorem Refuter Prototype Finished (L-Rules Only - Operator-Specific Rules - Refined Incon/Dual-Incon).~%")))

(main)
