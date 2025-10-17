;The proof axiom is 
(axiom con_R (() con)). 
;The refutation axiom is 
(axiom incon_L (incon ())). 
;The duality rules are 
(rule †R (A ()) (() († A))) and (rule †L (() († A)) (A ())). 
;The independence rules are 
(rule ∥R (∨ (() A) (() B)) (() (∥ A B))) and (rule ∥L (∨ (A ()) (B ()) ) ( (∥ A B) () )). 
;The dependence rules are 
(rule ∦R (∧ (() A) (() B)) ( () (∦ A B) )) and (rule ∦L (∧ (A ()) (B ())) ((∦ A B) () ))).


The proof axiom is (axiom con_R (entails () con)). The refutation axiom is (axiom incon_L (entails incon ())). The duality rules are (rule †R (entails A ()) (entails () († A))) and (rule †L (entails () († A)) (entails A ())). The independence rules are (rule ∥R (∨ (entails () A) (entails () B)) (entails () (∥ A B))) and (rule ∥L (∨ (entails A ()) (entails B ())) (entails (∥ A B) () ))). The dependence rules are (rule ∦R (∧ (entails () A) (entails () B)) (entails () (∦ A B) )) and (rule ∦L (∧ (entails A ()) (entails B ())) (entails (∦ A B) () ))).