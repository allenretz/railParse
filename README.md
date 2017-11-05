# railParse
This is an alternative to regex with the goal being human readability / comprehension instead of limiting the number of characters typed.

## Matching Rules
* Matching rules may be combined to create more complex rules
* Matching rules have 3 functions
   * parse(stringToMatch, startingPoints=set([0])) - returns a set of ending points that match the rule when starting from each starting point
   * match(stringToMatch) - returns True if the entire string matches the rule
   * matches(stringToMatch) - alias for match
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
* One(rule) - alias for Once
* Chain(\*rules) - a set of rules that have to all be matched in order
* Sequence(\*rules) - alias for Chain
* And(\*rules) - alias for Chain
* Or(\*rules) - a set of alternate rules where atleast one choice has to match
* Choice(\*rules) - alias for Or
* Optional(rule) - a rule that matches 0 - 1 time
* ZeroOrOne(rule) - alias for Optional
* OneOrMore(rule) - a rule that matches 1+ times
* ZeroOrMore(rule) - a rule that matches 0+ times
* Next(rule) - "Positive Look Ahead", a rule that checks the next characters in the string to determine if the current ending character should still be an ending character.
* LookAhead(rule) - alias for Next
* NotNext(rule) - "Negative Look Ahead"
* Previous(rule) - "Positive Look Behind" - starts at every point prior to the starting points and checks that from one atleast one of those points the starting point can be reached by following the rule
* LookBehind(rule) - alias for Previous
* Min(rule) - matches only the first (smallest) match
* Lazy(rule) - alias for Min
* Max(rule) - matches only the last (largest) match
* Greedy(rule) - alias for Max
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
