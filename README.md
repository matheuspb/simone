# simone

A finite automata editor, you may also express regular languages using regular grammars or expressions and then convert them to a FA.

### Algorithms implemented:

* RegExp to DFA
* Regular grammar to NFA
* NFA to regular grammar
* FA determinization and minimization
* Union, complement and intersection of RLs (via NFAs without epsilon transitions)
* Equivalence and containment of two RLs
* Emptiness and finiteness of RLs

### Some conventions:

* Grammar non-terminals are uppercase letters (optionally followed by a \')
* Grammar terminals are lowercase letters or digits
* RegExp operators are `. | ? *` (e.g. `a?(b|c?d)*`)
* Epsilon = &
