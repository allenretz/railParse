# railParse
This is an alternative to regex with the goal being human readability / comprehension instead of limiting the number of characters typed.

## Matching Rules
* Matching rules may be combined to create more complex rules
* Matching rules have multiple functions
   * parse(stringToParse, startingPoints=set([0])) - returns a set of ending points that match the rule when starting from each starting point
   
   
   * match(stringToMatch) - returns True if the entire string matches the rule
   * matches(stringToMatch)
   
   
   * exact(stringToMatch) - returns True if the entire string matches the rule and no other substrings starting at zero match.
   * exactMatch(stringToMatch)
   * exactlyMatches(stringToMatch)
   

   * \_\_eq\_\_(ruleOrString) - returns True if the ruleOrString will always yield the same result as the rule when .parse() is called no matter what string is passed to .parse(). If ruleOrString is a string, it will be treated as Sequence(ruleOrString).
   * ==
   
   
   
   * \_\_ne\_\_(ruleOrString) - returns The opposite of \_\_eq\_\_(ruleOrString)
   * !=
   
   
   
   * \_\_add\_\_(ruleOrString) - returns Sequence(originalRule, ruleOrString)
   * \_\_and\_\_(ruleOrString)
   * \_\_iadd\_\_(ruleOrString)
   * \_\_iand\_\_(ruleOrString)
   * +
   * &
   * +=
   * &=
   
   
   * \_\_or\_\_(ruleOrString) - returns Or(originalRule, ruleOrString)
   * \_\_ior\_\_(ruleOrString)
   * |
   * |=
   
   
   
   
### Example
```python

# .match() or .matches returns True / False based on if the entire
# string matches the rules
Sequence("abc", "d", Or(" ", "e"), "f").match("abcdef") #True
Sequence("abc", "d", Or(" ", "e"), "f").match("abcd f") #True
Sequence("abc", "d", Or(" ", "e"), "f").match("abcd!f") #False
Sequence("abc", "d", Or(" ", "e"), "f").match("abcd")   #False

# .parse() returns a set of all possible ending points that match
# the string when starting from the beginning
Sequence("abc", "d", Or(" ", "e"), "f").parse("abcdef") #{6}        #"abcdef" can be found once in "abcdef"
Sequence("abc", "d", Or(" ", "e"), "f").parse("abc")    #set()      #Empty set, neither "abcdef" nor "abcd f"
                                                                    #can be found in "abc"
Or("a", "ab").parse("ab")                               #{1, 2}     #both "a" and "ab" can be found in "ab"
```
### Rules
* Once(rule) - mostly used internally. It checks if a string matches the rule
* One(rule)


* Chain(\*rules) - a set of rules that have to all be matched in order
* Sequence(\*rules)
* And(\*rules)


* Or(\*rules) - a set of alternate rules where atleast one choice has to match
* Choice(\*rules)


* Optional(rule) - a rule that matches 0 - 1 time
* ZeroOrOne(rule)


* OneOrMore(rule) - a rule that matches 1+ times


* ZeroOrMore(rule) - a rule that matches 0+ times


* Next(rule) - "Positive Look Ahead", a rule that checks the next characters in the string to determine if the current ending character should still be an ending character.
* LookAhead(rule)


* NotNext(rule) - "Negative Look Ahead"


* Previous(rule) - "Positive Look Behind" - starts at every point prior to the starting points and checks that from one atleast one of those points the starting point can be reached by following the rule
* LookBehind(rule)


* Min(rule) - matches only the first (smallest) match
* Lazy(rule)


* Max(rule) - matches only the last (largest) match
* Greedy(rule)


* Not - TODO (INCOMPLETE)
### Find In TODO (INCOMPLETE)
* In 
* FindStart
* FindEnd
* Find
### Special (Predefined) Cases - TODO (INCOMPLETE)
* newline
* nl
* whitespacechar
* wsc
* whitespace
* ws
* upper
* lower
* alpha
* alnum
* digit
* wild
* exclude(charsToExlcude)
