(defun sequent-equal (sequent1 sequent2)
  (equalp sequent1 sequent2))

;; Function to substitute bindings into a template (basic) - Defined FIRST
(defun substitute-bindings (template bindings)
  (cond ((variablep template) (cdr (assoc template bindings)))
        ((consp template) (cons (substitute-bindings (car template) bindings)
                                 (substitute-bindings (cdr template) bindings)))
        (t template)))

;; Revised 'entails' function using sequent-equal
(defun entails (sequent)
  (format t "Entails called with sequent: ~S~%" sequent)  ; Debugging print

  ;; 1. Check Axioms (con_R and incon_l)
  (if (sequent-equal sequent (rule-output-sequent con_r-rule))
      (progn
        (format t "  Matched axiom: con_r~%")  ; Debugging print
        (return-from entails t)))

  (if (sequent-equal sequent (rule-output-sequent incon_l-rule))
      (progn
        (format t "  Matched axiom: incon_l~%")  ; Debugging print
        (return-from entails t)))

  ;; 2. Try Duality Rules (duality_r_dualR and duality_l_dualL) - Right Rule First
  (let ((bindings (pattern-match (rule-input-sequent duality_r_dualR-rule) sequent nil)))
    (if bindings
        (progn
          (format t "  Matched rule: duality_r_dualR with bindings: ~S~%" bindings)  ; Debugging print
          (let ((output-sequent (substitute-bindings (rule-output-sequent duality_r_dualR-rule) bindings)))
            (format t "  Applying rule, new sequent: ~S~%" output-sequent)  ; Debugging print
            (if (entails output-sequent)  ; Recursive call
                (return-from entails t))))))

  ;; Duality Left Rule
  (let ((bindings (pattern-match (rule-input-sequent duality_l_dualL-rule) sequent nil)))
    (if bindings
        (progn
          (format t "  Matched rule: duality_l_dualL with bindings: ~S~%" bindings)  ; Debugging print
          (let ((output-sequent (substitute-bindings (rule-output-sequent duality_l_dualL-rule) bindings)))
            (format t "  Applying rule, new sequent: ~S~%" output-sequent)  ; Debugging print
            (if (entails output-sequent)  ; Recursive call
                (return-from entails t))))))

  ;; 3. Try Independence Right Rule (indep_r_indepR)
  (let ((bindings (pattern-match (rule-input-sequent hypersequent_independence_r_indepR-rule) sequent nil)))
    (if bindings
        (progn
          (format t "  Matched rule: hypersequent_independence_r_indepR with bindings: ~S~%" bindings)
          (let ((premise-condition-met
                 (eval (substitute-bindings (rule-premise-condition hypersequent_independence_r_indepR-rule) bindings))))
            (format t "  Premise condition for indep_r_indepR: ~S, Condition Value: ~S~%"
                    (rule-premise-condition hypersequent_independence_r_indepR-rule) premise-condition-met)
            (if premise-condition-met
                (let ((output-sequent (substitute-bindings (rule-output-sequent hypersequent_independence_r_indepR-rule) bindings)))
                  (format t "  Applying rule, new sequent: ~S~%" output-sequent)
                  (if (entails output-sequent)  ; Recursive call
                      (return-from entails t))))))))

  ;; 4. Try Independence Left Rule (indep_l_indepL)
  (let ((bindings (pattern-match (rule-input-sequent hypersequent_independence_l_indepL-rule) sequent nil)))
    (if bindings
        (progn
          (format t "  Matched rule: hypersequent_independence_l_indepL with bindings: ~S~%" bindings)
          (let ((premise-condition-met
                 (eval (substitute-bindings (rule-premise-condition hypersequent_independence_l_indepL-rule) bindings))))
            (format t "  Premise condition for indep_l_indepL: ~S, Condition Value: ~S~%"
                    (rule-premise-condition hypersequent_independence_l_indepL-rule) premise-condition-met)
            (if premise-condition-met
                (let ((output-sequent (substitute-bindings (rule-output-sequent hypersequent_independence_l_indepL-rule) bindings)))
                  (format t "  Applying rule, new sequent: ~S~%" output-sequent)
                  (if (entails output-sequent)  ; Recursive call
                      (return-from entails t))))))))

  ;; 5. Try Dependence Right Rule (dep_r_depR)
  (let ((bindings (pattern-match (rule-input-sequent dependence_r_depR-rule) sequent nil)))
    (if bindings
        (progn
          (format t "  Matched rule: dependence_r_depR with bindings: ~S~%" bindings)
          (let ((premise-condition-met
                 (eval (substitute-bindings (rule-premise-condition dependence_r_depR-rule) bindings))))
            (format t "  Premise condition for dep_r_depR: ~S, Condition Value: ~S~%"
                    (rule-premise-condition dependence_r_depR-rule) premise-condition-met)
            (if premise-condition-met
                (let ((output-sequent (substitute-bindings (rule-output-sequent dependence_r_depR-rule) bindings)))
                  (format t "  Applying rule, new sequent: ~S~%" output-sequent)
                  (if (entails output-sequent)  ; Recursive call
                      (return-from entails t))))))))


  ;; 6. Try Dependence Left Rule (dep_l_depL)
  (let ((bindings (pattern-match (rule-input-sequent dependence_l_depL-rule) sequent nil)))
    (if bindings
        (progn
          (format t "  Matched rule: dependence_l_depL with bindings: ~S~%" bindings)
          (let ((premise-condition-met
                 (eval (substitute-bindings (rule-premise-condition dependence_l_depL-rule) bindings))))
            (format t "  Premise condition for dep_l_depL: ~S, Condition Value: ~S~%"
                    (rule-premise-condition dependence_l_depL-rule) premise-condition-met)
            (if premise-condition-met
                (let ((output-sequent (substitute-bindings (rule-output-sequent dependence_l_depL-rule) bindings)))
                  (format t "  Applying rule, new sequent: ~S~%" output-sequent)
                  (if (entails output-sequent)  ; Recursive call
                      (return-from entails t))))))))


  ;; 7. No rule applied or proof not found
  (format t "  No rule applied or proof not found for: ~S~%" sequent)  ; Debugging print
  nil)


;; Function to check if a symbol is a variable (starts with '?') - No change
(defun variablep (symbol)
  (and (symbolp symbol)
       (char= (char (symbol-name symbol) 0) #\?)))

;; Function to match patterns (basic version - needs more robustness later) - No change
(defun pattern-match (pattern input bindings)
  (cond ((equal pattern input) bindings)
        ((variablep pattern) (if (assoc pattern bindings)
                                   (if (equal (cdr (assoc pattern bindings)) input) bindings nil)
                                   (acons pattern input bindings)))
        ((and (consp pattern) (consp input)
              (pattern-match (car pattern) (car input) bindings))
         (pattern-match (cdr pattern) (cdr input) (pattern-match (car pattern) (car input) bindings)))
        (t nil)))


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
  (test-pattern-match-variable-order-recursive))  ; Added test for variable order in recursive match

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
  (let ((pattern '((?y) b (?x)))  ; Variables in different order than input
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
      (format t "~A: FAIL - Expected:~%  ~S~%Actual:~%  ~S~%" test-name expected actual)))

(defun assert-bindings-equal (actual expected test-name)
  (if (equalp actual expected) ; Using equalp for bindings comparison
      (format t "~A: PASS~%" test-name)
      (format t "~A: FAIL - Expected Bindings:~%  ~S~%Actual Bindings:~%  ~S~%Actual Bindings:~%  ~S~%" test-name expected actual actual)))


;;; 4. Run all tests ;;;
(run-pattern-match-tests)
(run-substitute-bindings-tests)




