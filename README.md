# railParse
This is an alternative to regex with the goal being human readability / comprehension instead of limiting the number of characters typed.

## Matching Rules
Matching rules may be combined to create more complex rules
Matching rules have multiple functions

* parse(stringToParse, startingPoints=set([0]))<br>
&nbsp;&nbsp;&nbsp;&nbsp;returns a set of ending points that match the rule when starting from each starting point
   
* match(stringToMatch)<br>
* matches(stringToMatch)
&nbsp;&nbsp;&nbsp;&nbsp;returns True if the entire string matches the rule
   
   
* exact(stringToMatch) 
* exactMatch(stringToMatch)
* exactlyMatches(stringToMatch)
<br>&nbsp;&nbsp;&nbsp;&nbsp;returns True if the entire string matches the rule and no other substrings starting at zero match.
   
## Comparisons
   * == 
     <br>&nbsp;&nbsp;&nbsp;&nbsp;True if the ruleOrString will always yield the same result as the rule when .parse() is called no matter what string is passed to .parse(). If ruleOrString is a string, it will be treated as Sequence(ruleOrString).
   * != 
   <br>&nbsp;&nbsp;&nbsp;&nbsp;True if the ruleOrString will not always yield the same result as the rule when .parse() is called no matter what string is passed to .parse(). If ruleOrString is a string, it will be treated as Sequence(ruleOrString).
   
   
## Operators  
   * \+
   * &
   * +=
   * &=
   <br>&nbsp;&nbsp;&nbsp;&nbsp;creates a new Sequence() of the original and the ruleOrString
   
   * |
   * |=
   <br>&nbsp;&nbsp;&nbsp;&nbsp;creates a new Or() of the original and the ruleOrString
   
   
   
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
* Once(rule)
* One(rule)
<br>&nbsp;&nbsp;&nbsp;&nbsp;Used internally. It checks if a string matches the rule.


* Chain(\*rules)
* Sequence(\*rules)
* And(\*rules)
<br>&nbsp;&nbsp;&nbsp;&nbsp;A set of rules that have to all be matched in order.


* Or(\*rules)
* Choice(\*rules)
<br>&nbsp;&nbsp;&nbsp;&nbsp;A set of alternate rules where atleast one choice has to match.


* Optional(rule)
* ZeroOrOne(rule)
<br>&nbsp;&nbsp;&nbsp;&nbsp;A rule that matches 0 - 1 time.


* OneOrMore(rule)
<br>&nbsp;&nbsp;&nbsp;&nbsp;A rule that matches 1+ times.


* ZeroOrMore(rule)
<br>&nbsp;&nbsp;&nbsp;&nbsp;A rule that matches 0+ times.


* Next(rule)
* LookAhead(rule)
<br>&nbsp;&nbsp;&nbsp;&nbsp;"Positive Look Ahead", a rule that checks the next characters in the string to determine if the current ending character should still be an ending character.


* NotNext(rule) - "Negative Look Ahead"
<br>&nbsp;&nbsp;&nbsp;&nbsp;


* Previous(rule)
* LookBehind(rule)
<br>&nbsp;&nbsp;&nbsp;&nbsp;"Positive Look Behind" - starts at every point prior to the starting points and checks that from one atleast one of those points the starting point can be reached by following the rule.


* Min(rule) - matches only the first (smallest) match
* Lazy(rule)
<br>&nbsp;&nbsp;&nbsp;&nbsp;


* Max(rule) - matches only the last (largest) match
* Greedy(rule)
<br>&nbsp;&nbsp;&nbsp;&nbsp;


* Not - TODO (INCOMPLETE)
<br>&nbsp;&nbsp;&nbsp;&nbsp;

### Find TODO (INCOMPLETE)
* FindStart
<br>&nbsp;&nbsp;&nbsp;&nbsp;


* FindEnd
<br>&nbsp;&nbsp;&nbsp;&nbsp;
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
