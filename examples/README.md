# Example automata

* [aa.json](aa.json) - Only the string `aa`
* [aaORbb.json](aaORbb.json) - If there exists `aa` then does not exists
  `bb` and vice-versa.
* [bad\_case.json](bad_case.json) - Accepts the language:
  `(a|b)*b(a|b)(a|b)(a|b)`, it is a bad case for the powerset construction,
  because the deterministic automaton gets pretty big.
* [bb.json](bb.json) - Only the string `bb` and epsilon
* [bdiv3.json](bdiv3.json) - Numbers of `b`s divisible by 3
* [div3.json](div3.json) - Language of binaries divisible by 3
* [div5.json](div5.json) - Language of binaries divisible by 5
* [empty.json](empty.json) - An empty automata
* [endsWbb.json](endsWbb.json) - String ends with `bb`
* [one1.json](one1.json) - There is only one `1` character
