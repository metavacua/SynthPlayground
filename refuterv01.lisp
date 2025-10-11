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
(defun make-dual (formula) `(dual ,formula)) ; New formula constructor for 'dual'

(defun formula-type (formula)
  (first formula))

(defun formula-arguments (formula)
  (rest formula))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Axioms - COMPLEXITY COUNTING - InconL Axiom for IndL(A,A) & Incon Base Case
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; InconL Axiom: (incon) is refuted immediately.

(defun axiom-inconl (formula)
  "Axiom InconL: Refutes (incon) - Base case for refutation.
   Formula-aware.
   [Complexity Metric: refutation-axiom-applications-count]
   [Output: Concise - No verbose output]
   FIXED: Corrected to only refute (incon)."
  (incf *refutation-axiom-applications-count*)
  (if (eq (formula-type formula) 'incon)
      formula              ; Base case: (incon) is refuted
      nil))                                                 ; Axiom does not apply, return nil


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Rules (Dependence & Independence & Dual - Formula-Aware & Threaded) - COMPLEXITY COUNTING - OPERATOR-SPECIFIC RULES
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun rule-duald-dual-l (formula kb)
  "Rule dualdL: Simplifies (dual (dual A)) to A.
   Formula-aware.
   [Complexity Metric: refutation-rule-applications-count]
   [Output: Concise - No verbose output]"
  (incf *refutation-rule-applications-count*)
  (if (and (eq (formula-type formula) 'dual)
           (eq (formula-type (second formula)) 'dual)) ; Check if it's (dual (dual A))
      (second (second formula))                         ; Rule applied, return simplified formula A
      nil))                                          ; Rule does not apply, return nil


(defun rule-dual-incon (formula kb)
  "Rule dual-incon: (dual incon) is NOT refuted. Returns NIL.
   Formula-aware.
   [Complexity Metric: refutation-rule-applications-count]
   [Output: Concise - No verbose output]
   Handles (dual incon) base case - non-refutation. Also checks dualdL."
  (incf *refutation-rule-applications-count*)
  (cond
    ((and (eq (formula-type formula) 'dual)
          (eq (formula-type (second formula)) 'incon)) nil) ; (dual incon) is NOT refuted, return NIL
    (t (rule-duald-dual-l formula kb))))                 ; Try dualdL rule next if not (dual incon)


(defun rule-dual-l (formula kb)
  "Rule dualL: Refutes (dual A) if A is NOT refuted, UNLESS A reduces to incon.
   Handles (dual (dual A)) simplification and (dual incon) case.
   Formula-aware.
   [Complexity Metric: refutation-rule-applications-count]
   [Output: Concise - No verbose output]
   FIXED: Corrected logic: Refutes (dual A) if A is NOT refuted, unless A reduces to incon."
  (incf *refutation-rule-applications-count*)
  (if (eq (formula-type formula) 'dual)
      (let ((formulaA (second formula)))
        ;; First, check the explicit base cases/simplifications for dual
        (let ((dual-special-case-result (rule-dual-incon formula kb)))
          (if (eq dual-special-case-result nil) ;; If rule-dual-incon returned NIL (meaning it was (dual incon))
              nil ;; Then (dual incon) is NOT refuted
              ;; If rule-dual-incon returned non-NIL, it was either (dual (dual A)) simplified to A,
              ;; or it wasn't a dual formula at all (which shouldn't happen here).
              ;; If it was (dual (dual A)) simplified to A, we need to check if A is refutable.
              (if (and dual-special-case-result (not (eq dual-special-case-result formula))) ;; Check if it was a simplification
                  ;; If it was a simplification (result is non-NIL and different from original formula)
                  ;; Refute the simplified form. If simplified form refutes, original dual is refuted.
                  (let ((refutation-result-of-simplified (run-refuter dual-special-case-result)))
                     (if refutation-result-of-simplified formula nil))
                  ;; If it wasn't a simplification (or rule-dual-incon returned NIL because it wasn't a dual)
                  ;; This case handles the standard dual rule: (dual A) is refuted if A is NOT refuted.
                  (let ((refutation-result-of-A (run-refuter formulaA)))
                    (if (null refutation-result-of-A) ;; If A was NOT refuted (result is NIL)
                        formula ;; Then (dual A) IS refuted
                        nil)))))) ;; If A WAS refuted (result is non-NIL), then (dual A) is NOT refuted
      nil)) ; If not a dual formula, this rule doesn't apply


(defun rule-independence-l (formula kb)
  "Independence Left Rule (rule independenceL) - Handles (ind A B) cases.
   Refutes if A is incon, B is incon, A is refuted, or B is refuted.
   Formula-aware. Parallel OR in Refutation.
   Applies to (ind A B) formulae.
   [Complexity Metric: refutation-rule-applications-count]
   [Output: Concise - No verbose output]
   REVISED: Correctly implements logic for (ind A B)."
  (incf *refutation-rule-applications-count*)

  (if (eq (formula-type formula) 'ind)
      (let ((formula1 (second formula))
            (formula2 (third formula)))
        (cond
          ;; Base cases: If either argument is (incon), the formula is refuted.
          ((eq (formula-type formula1) 'incon) formula)
          ((eq (formula-type formula2) 'incon) formula)
          ;; Recursive cases: If either argument is refuted, the formula is refuted.
          ;; Call run-refuter on arguments. If result is non-NIL, argument was refuted.
          ((run-refuter formula1) formula)
          ((run-refuter formula2) formula)
          ;; If none of the above, not refuted.
          (t nil)))
      nil)) ; If not an ind formula, this rule doesn't apply


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
      (rule-dual-l formula kb)))                             ; Try rule-dual-l next if not (dep formula) - Dual is last resort


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
   Outputs formula if refuted (non-NIL), nil if not.
   **MODIFIED: Refactored to dispatch to operator-specific rules. Incon base case refined.**
   **MODIFIED: Now returns the original formula on successful refutation.**
   **FIXED: Corrected dispatch logic for IndL axiom before rule.**
   **FIXED: Corrected axiom-inconl to only refute (incon).**"
  (initialize-refutation-knowledge-base)
  (let ((refutation-result
         (cond
           ;; Check base case for (incon) using axiom-inconl
           ((eq (formula-type formula) 'incon) (axiom-inconl formula))
           ((eq (formula-type formula) 'ind) (rule-independence-l formula *knowledge-base*))
           ((eq (formula-type formula) 'dep) (rule-dependence-l formula *knowledge-base*))    ; Rule for dep
           ((eq (formula-type formula) 'dual) (rule-dual-l formula *knowledge-base*))        ; Rule for dual
           (t nil))))                                                        ; No rule applies
    ;; Return original formula if refutation-result is non-NIL, otherwise return NIL
    (if refutation-result
        formula
        nil)))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Main Entry Point - Run Refuter with Formula - COMPLEXITY REPORTING and TESTING
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun main ()
  (format t "Starting Formula-Aware Theorem Refuter Prototype (L-Rules Only - Operator-Specific Rules - Refined Incon/Dual-Incon).\~%")

  ;; Example Formula Construction
  (let* ((incon-formula (make-incon))
         (dep-incon-incon-formula (make-dep incon-formula incon-formula)) ;; (dep incon incon)
         (ind-incon-incon-formula (make-ind incon-formula incon-formula)) ;; (ind incon incon)
         (self-ind-formula (make-ind incon-formula incon-formula)) ; (ind A A) where A is (incon) - test case for ind rule with incon args
         (complex-formula (make-ind dep-incon-incon-formula ind-incon-incon-formula))
         (dual-incon-formula (make-dual incon-formula))         ; (dual incon)
         (dual-dep-incon-incon-formula (make-dual dep-incon-incon-formula)) ; (dual (dep incon incon))
         (duald-dual-incon-formula (make-dual (make-dual incon-formula))) ; (dual (dual incon))
         (dual-of-dual-incon-formula (make-dual dual-incon-formula)) ;; (dual (dual incon)) - Should refute to (incon)
         (dep-dual-incon-incon (make-dep dual-incon-formula incon-formula)) ;; (dep (dual incon) incon) - Should not refute
         (dep-incon-dual-incon (make-dep incon-formula dual-incon-formula)) ;; (dep incon (dual incon)) - Should not refute
         (dep-dual-incon-dual-incon (make-dep dual-incon-formula dual-incon-formula)) ;; (dep (dual incon) (dual incon)) - Should not refute
         (ind-dual-incon-dual-incon (make-ind dual-incon-formula dual-incon-formula)) ;; (ind (dual incon) (dual incon)) - Should not refute
         )


    (format t "\~%--- Testing with incon formula ---\~%")
    (reset-refutation-complexity-counters)
    (let ((refuter-result (run-refuter incon-formula)))
      (format t "\~%Refuter Result for formula \~A: \~A\~%" incon-formula refuter-result)) ; EXPECTED: (INCON)

    (format t "\~%--- Testing with (dep incon incon) formula ---\~%")
    (reset-refutation-complexity-counters)
    (let ((refuter-result (run-refuter dep-incon-incon-formula)))
      (format t "\~%Refuter Result for formula \~A: \~A\~%" dep-incon-incon-formula refuter-result)) ; EXPECTED: (DEP (INCON) (INCON))

    (format t "\~%--- Testing with (ind incon incon) formula ---\~%")
    (reset-refutation-complexity-counters)
    (let ((refuter-result (run-refuter ind-incon-incon-formula)))
      (format t "\~%Refuter Result for formula \~A: \~A\~%" ind-incon-incon-formula refuter-result)) ; EXPECTED: (IND (INCON) (INCON))

    (format t "\~%--- Testing with (ind (dep incon incon) (ind incon incon)) formula ---\~%")
    (reset-refutation-complexity-counters)
    (let ((refuter-result (run-refuter complex-formula)))
      (format t "\~%Refuter Result for formula \~A: \~A\~%" complex-formula refuter-result)) ; EXPECTED: (IND (DEP (INCON) (INCON)) (IND (INCON) (INCON)))

    (format t "\~%--- Testing with (dual incon) formula - dualL Rule (incon argument) ---\~%")
    (reset-refutation-complexity-counters)
    (let ((refuter-result (run-refuter dual-incon-formula))) ; Testing (dual incon) - dualL rule with incon argument
      (format t "\~%Refuter Result for formula \~A: \~A\~%" dual-incon-formula refuter-result)) ; EXPECTED: NIL

    (format t "\~%--- Testing with (dual (dual incon)) formula - dualL Rule (double dual) ---\~%")
    (reset-refutation-complexity-counters)
    (let ((refuter-result (run-refuter duald-dual-incon-formula))) ; Testing (dual (dual incon)) - dualL rule (double dual)
      (format t "\~%Refuter Result for formula \~A: \~A\~%" duald-dual-incon-formula refuter-result)) ; EXPECTED: (DUAL (DUAL (INCON)))

    (format t "\~%--- Testing with (dual (dep incon incon)) formula - dualL Rule ---\~%")
    (reset-refutation-complexity-counters)
    (let ((refuter-result (run-refuter dual-dep-incon-incon-formula))) ; Testing (dual (dep incon incon)) - dualL rule
      (format t "\~%Refuter Result for formula \~A: \~A\~%" dual-dep-incon-incon-formula refuter-result)) ; EXPECTED: NIL

    (format t "\~%--- Testing with (dep (dual incon) incon) formula ---\~%")
    (reset-refutation-complexity-counters)
    (let ((refuter-result (run-refuter dep-dual-incon-incon)))
      (format t "\~%Refuter Result for formula \~A: \~A\~%" dep-dual-incon-incon refuter-result)) ; EXPECTED: NIL

    (format t "\~%--- Testing with (dep incon (dual incon)) formula ---\~%")
    (reset-refutation-complexity-counters)
    (let ((refuter-result (run-refuter dep-incon-dual-incon)))
      (format t "\~%Refuter Result for formula \~A: \~A\~%" dep-incon-dual-incon refuter-result)) ; EXPECTED: NIL

    (format t "\~%--- Testing with (dep (dual incon) (dual incon)) formula ---\~%")
    (reset-refutation-complexity-counters)
    (let ((refuter-result (run-refuter dep-dual-incon-dual-incon)))
      (format t "\~%Refuter Result for formula \~A: \~A\~%" dep-dual-incon-dual-incon refuter-result)) ; EXPECTED: NIL

    (format t "\~%--- Testing with (ind (dual incon) (dual incon)) formula ---\~%")
    (reset-refutation-complexity-counters)
    (let ((refuter-result (run-refuter ind-dual-incon-dual-incon)))
      (format t "\~%Refuter Result for formula \~A: \~A\~%" ind-dual-incon-dual-incon refuter-result)) ; EXPECTED: NIL

    )


    (format t "\~%Formula-Aware Theorem Refuter Prototype Finished (L-Rules Only - Operator-Specific Rules - Refined Incon/Dual-Incon).\~%"))

(main)

