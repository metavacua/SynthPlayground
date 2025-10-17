;; Function to substitute bindings into a template (basic) - Defined FIRST
(defun substitute-bindings (template bindings)
  (cond ((variablep template) (cdr (assoc template bindings)))  ; Substitute variable
        ((consp template) (cons (substitute-bindings (car template) bindings)  ; Recursive substitution for lists
                                 (substitute-bindings (cdr template) bindings)))
        (t template)))  ; Return as is if not variable or list

;; Stub 'entails' function - always returns nil for now - No change
(defun entails (sequent)
  (declare (ignore sequent))
  nil)

;; Function to check if a symbol is a variable (starts with '?') - No change
(defun variablep (symbol)
  (and (symbolp symbol)
       (char= (char (symbol-name symbol) 0) #\?)))

;; Function to match patterns (basic version - needs more robustness later) - No change
(defun pattern-match (pattern input bindings)
  (cond ((equal pattern input) bindings)   ; Exact match
        ((variablep pattern) (if (assoc pattern bindings)    ; Variable already bound?
                                 (if (equal (cdr (assoc pattern bindings)) input) bindings nil)    ; Check existing binding
                                 (acons pattern input bindings)))    ; Bind variable
        ((and (consp pattern) (consp input)    ; Recursive matching for lists
              (pattern-match (car pattern) (car input) bindings))
         (pattern-match (cdr pattern) (cdr input) (pattern-match (car pattern) (car input) bindings)))
        (t nil)))   ; No match


;;;; Unit Tests for Pattern Matching and Substitution ;;;;

;;; 1. Unit Tests for pattern-match function ;;;

(defun run-pattern-match-tests ()
  (test-description "Pattern Match Tests") ; Renamed to test-description
  (test-pattern-match-exact-match)
  (test-pattern-match-variable-binding)
  (test-pattern-match-variable-binding-existing)
  (test-pattern-match-recursive-match)
  (test-pattern-match-no-match)
  (test-pattern-match-mismatch-variable-binding))

(defun test-description (description) ; Renamed to test-description
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


;;; 2. Unit Tests for substitute-bindings function ;;;

(defun run-substitute-bindings-tests ()
  (test-description "Substitute Bindings Tests") ; Renamed to test-description
  (test-substitute-bindings-variable-substitution) ; Call tests directly
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
  (if (bindings-equal actual expected)
      (format t "~A: PASS~%" test-name)
      (format t "~A: FAIL - Expected Bindings:~%  ~S~%Actual Bindings:~%  ~S~%" test-name expected actual)))

(defun bindings-equal (bindings1 bindings2)
  (and
   (cond ((and (null bindings1) (null bindings2)) t)
         ((or (null bindings1) (null bindings2)) nil)
         (t (and (binding-equal (car bindings1) (car bindings2))
                 (bindings-equal (cdr bindings1) (cdr bindings2)))))))

(defun binding-equal (binding1 binding2)
  (and (equal (car binding1) (car binding2))
       (equal (cdr binding1) (cdr binding2))))


;;; 4. Run all tests ;;;
(run-pattern-match-tests)
(run-substitute-bindings-tests)