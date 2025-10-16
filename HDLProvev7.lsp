(defstruct rule
  name
  type
  calculus_type
  operator
  direction
  input-sequent
  output-sequent
  premise-condition
  description)

;; Function to check if a symbol is a variable (starts with '?')
(defun variablep (symbol)
  (and (symbolp symbol)
       (char= (char (symbol-name symbol) 0) #\?)))

(defun sequent-equal (sequent1 sequent2)
  (equalp sequent1 sequent2))

;; Function to substitute bindings into a template (basic)
(defun substitute-bindings (template bindings)
  (cond ((variablep template) (cdr (assoc template bindings)))
        ((consp template) (cons (substitute-bindings (car template) bindings)
                                 (substitute-bindings (cdr template) bindings)))
        (t template)))

;; Function to match patterns (basic version)
(defun pattern-match (pattern input bindings)
  (cond ((equal pattern input) bindings)
        ((variablep pattern) (if (assoc pattern bindings)
                                   (if (equal (cdr (assoc pattern bindings)) input) bindings nil)
                                   (acons pattern input bindings)))
        ((and (consp pattern) (consp input)
              (pattern-match (car pattern) (car input) bindings))
         (pattern-match (cdr pattern) (cdr input) (pattern-match (car pattern) (car input) bindings)))
        (t nil)))


(defparameter con_r-rule
  (make-rule
   :name 'con_R
   :type :axiom
   :calculus_type :non-contextual-minimal-hypersequent-calculus
   :operator :con
   :output-sequent '(() con)
   :description "Axiom: Provability of consistency (con). Output is minimal sequent (entails con), represented as (() con)."))

(defparameter incon_l-rule
  (make-rule
   :name 'incon_L
   :type :axiom
   :calculus_type :non-contextual-minimal-hypersequent-calculus
   :operator :incon
   :output-sequent '((incon) ())
   :description "Axiom: Refutability of inconsistency (incon). Output is minimal sequent (incon entails), represented as ((incon) ())."))

(defparameter duality_r_dualR-rule
  (make-rule
   :name 'NonContextual_duality_R_dualR
   :type :sequent-rule
   :calculus_type :non-contextual-minimal-hypersequent-calculus
   :operator :duality
   :direction :right
   :input-sequent '((?A) ())
   :output-sequent '(() (dual ?A))
   :description "Duality Right Rule (dualR): Transforms minimal sequent (A entails), represented as ((?A) ()), to minimal sequent (entails dual A), represented as (() (dual ?A)). Uses 'dual' for duality operator in code."))

(defparameter duality_l_dualL-rule
  (make-rule
   :name 'NonContextual_duality_L_dualL
   :type :sequent-rule
   :calculus_type :non-contextual-minimal-hypersequent-calculus
   :operator :duality
   :direction :left
   :input-sequent '(() (dual ?A))
   :output-sequent '((?A) ())
   :description "Duality Left Rule (dualL): Transforms minimal sequent (entails dual A), represented as (() (dual ?A)), to minimal sequent (A entails), represented as ((?A) ()). Uses 'dual' for duality operator in code."))

(defparameter hypersequent_independence_r_indepR-rule
  (make-rule
   :name 'Hypersequent_independence_R_indepR
   :type :hypersequent-rule
   :calculus_type :non-contextual-minimal-hypersequent-calculus
   :operator :independence
   :direction :right
   :input-sequent '(() (indep ?A ?B)) ; Input sequent for indepR rule
   :output-sequent '(() (indep ?A ?B)) ; Output sequent is the same as input in indepR - corrected input and output
   :premise-condition '(or (entails (() ?A)) (entails (() ?B)))
   :description "Hypersequent Independence Right Rule (indepR): From premise (entails A) or (entails B), infer minimal sequent (entails indep A B). Uses 'indep' for independence operator in code."))

(defparameter hypersequent_independence_l_indepL-rule
  (make-rule
   :name 'Hypersequent_independence_L_indepL
   :type :hypersequent-rule
   :calculus_type :non-contextual-minimal-hypersequent-calculus
   :operator :independence
   :direction :left
   :input-sequent '(((indep ?A ?B) ())) ; Input sequent for indepL rule
   :output-sequent '(((indep ?A ?B) ())) ; Output sequent same as input in indepL - corrected input and output
   :premise-condition '(or (entails (?A ())) (entails (?B ())))
   :description "Hypersequent Independence Left Rule (indepL): From premise (A entails) or (B entails), infer minimal sequent (indep A B entails). Uses 'indep' for independence operator in code."))

(defparameter dependence_r_depR-rule
  (make-rule
   :name 'Dependence_R_depR
   :type :sequent-rule
   :calculus_type :non-contextual-minimal-hypersequent-calculus
   :operator :dependence
   :direction :right
   :input-sequent '(() (dep ?A ?B)) ; Input sequent for depR rule
   :output-sequent '(() (dep ?A ?B)) ; Output sequent same as input for depR - corrected input and output
   :premise-condition '(and (entails (() ?A)) (entails (() ?B)))
   :description "Dependence Right Rule (depR): From premise (entails A) and (entails B), infer minimal sequent (entails dep A B). Uses 'dep' for dependence operator in code."))

(defparameter dependence_l_depL-rule
  (make-rule
   :name 'Dependence_L_depL
   :type :sequent-rule
   :calculus_type :non-contextual-minimal-hypersequent-calculus
   :operator :dependence
   :direction :left
   :input-sequent '(((dep ?A ?B) ())) ; Input sequent for depL rule
   :output-sequent '(((dep ?A ?B) ())) ; Output sequent same as input for depL - corrected input and output
   :premise-condition '(and (entails (?A ())) (entails (?B ())))
   :description "Dependence Left Rule (depL): From premise (A entails) and (B entails), infer minimal sequent (dep A B entails). Uses 'dep' for dependence operator in code."))


;; Revised 'entails' function with Independence and Dependence Rules
(defun entails (sequent)
  (format t "Entails called with sequent: ~S~%" sequent)   ; Debugging print

  ;; 1. Check Axioms (con_R and incon_l)
  (if (sequent-equal sequent (rule-output-sequent con_r-rule))
      (progn
        (format t "  Matched axiom: con_r~%")    ; Debugging print
        (return-from entails t)))

  (if (sequent-equal sequent (rule-output-sequent incon_l-rule))
      (progn
        (format t "  Matched axiom: incon_l~%")    ; Debugging print
        (return-from entails t)))

  ;; 2. Try Duality Rules (duality_r_dualR and duality_l_dualL)
  (let ((bindings (pattern-match (rule-input-sequent duality_r_dualR-rule) sequent nil)))
    (if bindings
        (progn
          (format t "  Matched rule: duality_r_dualR with bindings: ~S~%" bindings)     ; Debugging print
          (let ((output-sequent (substitute-bindings (rule-output-sequent duality_r_dualR-rule) bindings)))
            (format t "  Applying rule, new sequent: ~S~%" output-sequent)   ; Debugging print
            (if (entails output-sequent)     ; Recursive call
                (return-from entails t))))))

  (let ((bindings (pattern-match (rule-input-sequent duality_l_dualL-rule) sequent nil)))
    (if bindings
        (progn
          (format t "  Matched rule: duality_l_dualL with bindings: ~S~%" bindings)     ; Debugging print
          (let ((output-sequent (substitute-bindings (rule-output-sequent duality_l_dualL-rule) bindings)))
            (format t "  Applying rule, new sequent: ~S~%" output-sequent)   ; Debugging print
            (if (entails output-sequent)    ; Recursive call
                (return-from entails t))))))

  ;; 3. Try Independence Right Rule (indep_r_indepR)
  (let ((bindings (pattern-match (rule-input-sequent hypersequent_independence_r_indepR-rule) sequent nil)))
    (if bindings
        (progn
          (format t "  Matched rule: hypersequent_independence_r_indepR with bindings: ~S~%" bindings)
          (let* ((condition-template (rule-premise-condition hypersequent_independence_r_indepR-rule))
                 (sequent-template1 (second (second condition-template)))
                 (sequent-template2 (second (third condition-template)))
                 (sequent1 (substitute-bindings sequent-template1 bindings))
                 (sequent2 (substitute-bindings sequent-template2 bindings))
                 (premise-condition-met (or (entails sequent1) (entails sequent2))))
            (format t "  Premise condition for indep_r_indepR: (OR (ENTAILS ~S) (ENTAILS ~S)), Condition Value: ~S~%"
                    sequent1 sequent2 premise-condition-met)
            (if premise-condition-met
                (progn
                  (format t "  Premise condition met for indep_r_indepR. Proof is complete.~%")
                  (return-from entails t)))))))

  ;; 4. Try Independence Left Rule (indep_l_indepL)
  (let ((bindings (pattern-match (rule-input-sequent hypersequent_independence_l_indepL-rule) sequent nil)))
    (if bindings
        (progn
          (format t "  Matched rule: hypersequent_independence_l_indepL with bindings: ~S~%" bindings)
          (let* ((condition-template (rule-premise-condition hypersequent_independence_l_indepL-rule))
                 (sequent-template1 (second (second condition-template)))
                 (sequent-template2 (second (third condition-template)))
                 (sequent1 (substitute-bindings sequent-template1 bindings))
                 (sequent2 (substitute-bindings sequent-template2 bindings))
                 (premise-condition-met (or (entails sequent1) (entails sequent2))))
            (format t "  Premise condition for indep_l_indepL: (OR (ENTAILS ~S) (ENTAILS ~S)), Condition Value: ~S~%"
                    sequent1 sequent2 premise-condition-met)
            (if premise-condition-met
                (progn
                  (format t "  Premise condition met for indep_l_indepL. Proof is complete.~%")
                  (return-from entails t)))))))

  ;; 5. Try Dependence Right Rule (dep_r_depR)
  (let ((bindings (pattern-match (rule-input-sequent dependence_r_depR-rule) sequent nil)))
    (if bindings
        (progn
          (format t "  Matched rule: dependence_r_depR with bindings: ~S~%" bindings)
          (let* ((condition-template (rule-premise-condition dependence_r_depR-rule))
                 (sequent-template1 (second (second condition-template)))
                 (sequent-template2 (second (third condition-template)))
                 (sequent1 (substitute-bindings sequent-template1 bindings))
                 (sequent2 (substitute-bindings sequent-template2 bindings))
                 (premise-condition-met (and (entails sequent1) (entails sequent2))))
            (format t "  Premise condition for dep_r_depR: (AND (ENTAILS ~S) (ENTAILS ~S)), Condition Value: ~S~%"
                    sequent1 sequent2 premise-condition-met)
            (if premise-condition-met
                (progn
                  (format t "  Premise condition met for dep_r_depR. Proof is complete.~%")
                  (return-from entails t)))))))

  ;; 6. Try Dependence Left Rule (dep_l_depL)
  (let ((bindings (pattern-match (rule-input-sequent dependence_l_depL-rule) sequent nil)))
    (if bindings
        (progn
          (format t "  Matched rule: dependence_l_depL with bindings: ~S~%" bindings)
          (let* ((condition-template (rule-premise-condition dependence_l_depL-rule))
                 (sequent-template1 (second (second condition-template)))
                 (sequent-template2 (second (third condition-template)))
                 (sequent1 (substitute-bindings sequent-template1 bindings))
                 (sequent2 (substitute-bindings sequent-template2 bindings))
                 (premise-condition-met (and (entails sequent1) (entails sequent2))))
            (format t "  Premise condition for dep_l_depL: (AND (ENTAILS ~S) (ENTAILS ~S)), Condition Value: ~S~%"
                    sequent1 sequent2 premise-condition-met)
            (if premise-condition-met
                (progn
                  (format t "  Premise condition met for dep_l_depL. Proof is complete.~%")
                  (return-from entails t)))))))


  ;; 7. No rule applied or proof not found
  (format t "  No rule applied or proof not found for: ~S~%" sequent)   ; Debugging print
  nil)



;;;; Unit Tests for Pattern Matching and Substitution ;;;;

;;; 1. Unit Tests for pattern-match function ;;;

(defun run-pattern-match-tests ()
  (test-description "Pattern Match Tests")
  (test-pattern-match-exact-match)
  (test-pattern-match-variable-binding)
  (test-pattern-match-variable-binding-existing)
  (test-pattern-match-recursive-match)
  (test-pattern-match-no-match)
  (test-pattern-match-mismatch-variable-binding)
  (test-pattern-match-variable-order-recursive))   ; Added test for variable order in recursive match

(defun test-description (description)
  (format t ";;;; ~A ;;;;~%" description))

(defun test-pattern-match-exact-match ()
  (let ((pattern '(a b c))
        (input '(a b c)))
    (assert-equal (pattern-match pattern input nil) nil "Exact Match Test Failed")))

(defun test-pattern-match-variable-binding ()
  (let ((pattern '(?x b c))
        (input '(a b c))
        (expected-bindings '((?x . a))))
    (assert-bindings-equal (pattern-match pattern input nil) expected-bindings "Variable Binding Test Failed")))

(defun test-pattern-match-variable-binding-existing ()
  (let ((pattern '(?x b c))
        (input '(a b c))
        (initial-bindings '((?x . a)))
        (expected-bindings '((?x . a))))
    (assert-bindings-equal (pattern-match pattern input initial-bindings) expected-bindings "Existing Variable Binding Test Failed")))

(defun test-pattern-match-recursive-match ()
  (let ((pattern '((?x) b (?y)))
        (input '((a) b (c)))
        (expected-bindings '((?x . a) (?y . c))))
    (assert-bindings-equal (pattern-match pattern input nil) expected-bindings "Recursive Match Test Failed")))

(defun test-pattern-match-no-match ()
  (let ((pattern '(a b d))
        (input '(a b c)))
    (assert-equal (pattern-match pattern input nil) nil "No Match Test Failed")))

(defun test-pattern-match-mismatch-variable-binding ()
  (let ((pattern '(?x b c))
        (input '(d b c))
        (initial-bindings '((?x . a))))
    (assert-equal (pattern-match pattern input initial-bindings) nil "Mismatch Variable Binding Test Failed")))

(defun test-pattern-match-variable-order-recursive ()
  (let ((pattern '((?y) b (?x)))    ; Variables in different order than input
        (input '((a) b (c)))
        (expected-bindings '((?y . a) (?x . c))))
    (assert-bindings-equal (pattern-match pattern input nil) expected-bindings "Variable Order Recursive Match Test Failed")))


;;; 2. Unit Tests for substitute-bindings function ;;;

(defun run-substitute-bindings-tests ()
  (test-description "Substitute Bindings Tests")
  (test-substitute-bindings-variable-substitution)
  (test-substitute-bindings-recursive-substitution)
  (test-substitute-bindings-no-substitution)
  (test-substitute-bindings-mixed-substitution))

(defun test-substitute-bindings-variable-substitution ()
  (let ((template '(?x b c))
        (bindings '((?x . a)))
        (expected-output '(a b c)))
    (assert-equal (substitute-bindings template bindings) expected-output "Variable Substitution Test Failed")))

(defun test-substitute-bindings-recursive-substitution ()
  (let ((template '((?x) b (?y)))
        (bindings '((?x . a) (?y . c)))
        (expected-output '((a) b (c))))
    (assert-equal (substitute-bindings template bindings) expected-output "Recursive Substitution Test Failed")))

(defun test-substitute-bindings-no-substitution ()
  (let ((template '(a b c))
        (bindings '((?x . a)))
        (expected-output '(a b c)))
    (assert-equal (substitute-bindings template bindings) expected-output "No Substitution Test Failed")))

(defun test-substitute-bindings-mixed-substitution ()
  (let ((template '((?x) b literal (?y)))
        (bindings '((?x . a) (?y . c)))
        (expected-output '((a) b literal (c))))
    (assert-equal (substitute-bindings template bindings) expected-output "Mixed Substitution Test Failed")))


;;; 3. Assertion Helper Functions ;;;

(defun assert-equal (actual expected test-name)
  (if (equal actual expected)
      (format t "~A: PASS~%" test-name)
      (format t "~A: FAIL - Expected:~%  ~S~%Actual:~%  ~S~%" test-name expected actual)))

(defun assert-bindings-equal (actual expected test-name)
  (flet ((bindings-to-set (bindings)
           (sort (copy-list bindings) #'string< :key #'car))) ; Sort bindings for order-insensitive comparison
    (let ((actual-set (bindings-to-set actual))
          (expected-set (bindings-to-set expected)))
      (if (equalp actual-set expected-set)
          (format t "~A: PASS~%" test-name)
          (format t "~A: FAIL - Expected Bindings:~%  ~S~%Actual Bindings:~%  ~S~%" test-name expected actual)))))


;;; 4. Run all tests ;;;
(run-pattern-match-tests)
(run-substitute-bindings-tests)

(print con_r-rule)
(print incon_l-rule)
(print duality_r_dualR-rule)
(print duality_l_dualL-rule)
(print hypersequent_independence_r_indepR-rule)
(print hypersequent_independence_l_indepL-rule)
(print dependence_r_depR-rule)
(print dependence_l_depL-rule)

;;;; Unit Tests for Entails Function ;;;;

(defun run-entails-tests ()
  (test-description "Entails Function Tests")
  (test-entails-axiom-con-r)
  (test-entails-axiom-incon-l)
  (test-entails-duality-r)
  (test-entails-duality-l)
  (test-entails-independence-r-premise-true-a)
  (test-entails-independence-r-premise-true-b)
  (test-entails-independence-l-premise-true-a)
  (test-entails-independence-l-premise-true-b)
  (test-entails-dependence-r-premise-true)
  (test-entails-dependence-l-premise-true)
  (test-entails-non-entailment))


(defun test-entails-axiom-con-r ()
  (let ((sequent '(() con)))
    (assert-entails-equal (entails sequent) t "Entails Axiom con_R Test Failed")))

(defun test-entails-axiom-incon-l ()
  (let ((sequent '((incon) ())))
    (assert-entails-equal (entails sequent) t "Entails Axiom incon_L Test Failed")))

(defun test-entails-duality-r ()
  (let ((sequent '((foo) ())))  ; Assume 'foo' is not provable/refutable by axioms alone
    (assert-entails-equal (entails sequent) nil "Entails Duality Right Rule (dualR) Test (Start) - Should be nil before rule application")
    (assert-entails-equal (entails '(() (dual foo))) nil "Entails Duality Right Rule (dualR) Test (End) -  Still nil as no base case for 'foo'"))) ; Should remain nil as we have no base case for 'foo'

(defun test-entails-duality-l ()
  (let ((sequent '(() (dual bar)))) ; Assume 'bar' is not provable/refutable by axioms alone
    (assert-entails-equal (entails sequent) nil "Entails Duality Left Rule (dualL) Test (Start) - Should be nil before rule application")
    (assert-entails-equal (entails '((bar) ())) nil "Entails Duality Left Rule (dualL) Test (End) - Still nil as no base case for 'bar'"))) ; Should remain nil as we have no base case for 'bar'


(defun test-entails-independence-r-premise-true-a ()
  (let ((sequent '(() (indep con baz))))  ; 'con' is provable
     (assert-entails-equal (entails '(() con)) t "Premise (entails con) should be true")
     (assert-entails-equal (entails sequent) t "Entails Independence Right Rule (indepR) Test (Premise A)")))

(defun test-entails-independence-r-premise-true-b ()
  (let ((sequent '(() (indep baz con))))  ; 'con' is provable, order swapped
     (assert-entails-equal (entails '(() con)) t "Premise (entails con) should be true")
     (assert-entails-equal (entails sequent) t "Entails Independence Right Rule (indepR) Test (Premise B)")))

(defun test-entails-independence-l-premise-true-a ()
  (let ((sequent '(((indep incon baz) ()))))  ; 'incon' is refutable
     (assert-entails-equal (entails '((incon) ())) t "Premise (incon entails) should be true")
     (assert-entails-equal (entails sequent) t "Entails Independence Left Rule (indepL) Test (Premise A)")))

(defun test-entails-independence-l-premise-true-b ()
  (let ((sequent '(((indep baz incon) ()))))  ; 'incon' is refutable, order swapped
     (assert-entails-equal (entails '((incon) ())) t "Premise (incon entails) should be true")
     (assert-entails-equal (entails sequent) t "Entails Independence Left Rule (indepL) Test (Premise B)")))


(defun test-entails-dependence-r-premise-true ()
  (let ((sequent '(() (dep con con)))) ; Both premises are 'con', which is provable
     (assert-entails-equal (entails '(() con)) t "Premise (entails con) should be true")
     (assert-entails-equal (entails sequent) t "Entails Dependence Right Rule (depR) Test")))

(defun test-entails-dependence-l-premise-true ()
  (let ((sequent '(((dep incon incon) ())))) ; Both premises are 'incon', which is refutable
     (assert-entails-equal (entails '((incon) ())) t "Premise (incon entails) should be true")
     (assert-entails-equal (entails sequent) t "Entails Dependence Left Rule (depL) Test")))


(defun test-entails-non-entailment ()
  (let ((sequent '(() foo)))  ; 'foo' is not provable by axioms or rules
    (assert-entails-equal (entails sequent) nil "Entails Non-Entailment Test Failed")))


;;; 5. Assertion Helper Function for Entails Tests ;;;

(defun assert-entails-equal (actual expected test-name)
  (if (equal actual expected)
      (format t "~A: PASS~%" test-name)
      (format t "~A: FAIL - Expected:~%  ~S~%Actual:~%  ~S~%" test-name expected actual)))


;;; 6. Run Entails Tests ;;;
(run-entails-tests)