# Automata examples

* [div3.json](div3.json) - Language of binaries divisible by 3
* [aaORbb.json](aaORbb.json) - If there exists `aa` then does not exists
  `bb` and vice-versa.
* [endsWbb.json](endsWbb.json) - String ends with `bb`
* [bdiv3.json](bdiv3.json) - Numbers of `b`s divisible by 3
* [one1.json](one1.json) - There is only one `1` character
* [aa.json](aa.json) - Only the string `aa`
* [bb.json](bb.json) - Only the string `bb` and epsilon
* [empty.json](empty.json) - An empty automata
* [bad\_case.json](bad_case.json) - Accepts the language:
  `(a|b)*b(a|b)(a|b)(a|b)`, it is a bad case for the powerset construction,
  because the deterministic automaton gets pretty big.
