"""
Name:    RailParser
Author:  Allen Retzler
Date:    Apr 11, 2017
Updated: NOV 5,  2017
"""



## MATCHING RULES
class Once:
    """Matches the rule exactly once
       This is the base Parse Rule and
       is called and inherrited by others"""
    #TODO: Allow Regex and File input as well
    def __init__(self, rule):
        self.rule = rule
    def match(self, stringToMatch):
        """returns True if the entire string matches"""
        return len(stringToMatch) in self.parse(stringToMatch)
    matches = match



    def exact(self, stringToMatch):
        """returns True if the entire string matches the rule and no other substrings (starting at zero) also matches."""
        return Min(self.rule).match(stringToMatch)
    exactMatch = exact
    exactlyMatches = exact




    def parse(self, stringToParse, startingPoints = set([0])):
        if type(self.rule) == type(""):
            newPoints = set()
            for start in startingPoints:
                if start + len(self.rule) <= len(stringToParse) and stringToParse[start: start + len(self.rule)] == self.rule:
                    newPoints.add(start + len(self.rule))
            return newPoints;
        else:
            return self.rule.parse(stringToParse, startingPoints)


    def in(self, stringToFind):
        raise NotImplemented
    def findStart(self, stringToFind, startingPoint =0, endingPoint =-1):
        raise NotImplemented
    def findEnd(self, stringToFind, startingPoint =0, endingPoint =-1):
        raise NotImplemented

    def toRegex(outputType = "Regex"):
        """Converts the parserule to a regex.Pattern or String"""
        raise NotImplemented("Not Yet Implemted")





    def __eq__(self, ruleOrString):
        raise NotImplemented("Not Yet Implemented")
    def __ne__(self, ruleOrString):
        return not __eq__(ruleOrString)
    def __add__(self, ruleOrString):
        if type(self) == type(Sequence()):
            if type(ruleOrString) == type(Sequence()):
                return(Sequence(*self.rules, *ruleOrString.rules))
            else:
                return(Sequence(*self.rules, ruleOrString))
        else:
            if type(ruleOrString) == type(Sequence()):
                return(Sequence(self, *ruleOrString.rules))
            else:
                return(Sequence(self, ruleOrString))
    def __radd__(self, ruleOrString):
        if type(self) == type(Sequence()):
            if type(ruleOrString) == type(Sequence()):
                return(Sequence(*ruleOrString.rules, *self.rules))
            else:
                return(Sequence(ruleOrString, *self.rules))
        else:
            if type(ruleOrString) == type(Sequence()):
                return(Sequence(*ruleOrString.rules, self))
            else:
                return(Sequence(ruleOrString, self))
    def __and__(self, ruleOrString):
        raise NotImplemented
        
    def __or__(self, ruleOrString):
        if type(self) == type(Or()):
            if type(ruleOrString) == type(Or()):
                return(Or(*self.rules, *ruleOrString.rules))
            else:
                return(Or(*self.rules, ruleOrString))
        else:
            if type(ruleOrString) == type(Or()):
                return(Or(self, *ruleOrString.rules))
            else:
                return(Or(self, ruleOrString))

    __rand__ = __and__
    __ror__  = __or__    

        
One = Once



class Sequence(Once):
    """A set of rules that have to be matched in order"""
    def __init__(self, *rules):
        self.rules = [Once(x) for x in  rules]

    def parse(self,stringToParse, startingPoints = set([0])):
        for i in self.rules:
            startingPoints = i.parse(stringToParse, startingPoints)
        return startingPoints
Chain = Sequence


class And(Once):
    """A set of rules that all have to match in order for characters to be added"""
    raise NotImplemented("Not Yet Implemented")


class Or(Once):
    """A set of rules where atleast one choice has to match"""
    #TODO Run Equivalence Checks Before storing the rules
    def __init__(self, *rules):
        self.rules = [Once(x) for x in  rules]
        
    def parse(self,stringToParse, startingPoints = set([0])):
        newPoints =set()
        
        for i in self.rules:
            newPoints |= i.parse(stringToParse, startingPoints)
        return newPoints
Choice = Or



class Optional(Once):
    """A rule that is optional (matches 0 or 1 time)"""
    def __init__(self, rule):
        self.rule = Once(rule)
    def parse(self,stringToParse, startingPoints = set([0])):
        return Or("", self.rule).parse(stringToParse, startingPoints)    
ZeroOrOne = Optional


    
class OneOrMore(Once):
    """A rule that is matches 1 or more times. If more than once, joinRule is required between each match"""
    def __init__(self, rule, joinRule = ""):
        self.rule = Once(rule)
        self.join = Once(joinRule)

    def parse(self,stringToParse, startingPoints = set([0])):
        startingPoints = self.rule.parse(stringToParse, startingPoints)
        newPoints = set() | startingPoints
        while startingPoints != set():
            startingPoints = Chain(self.join, self.rule).parse(stringToParse, startingPoints)
            newPoints |= startingPoints
            
        return newPoints



class ZeroOrMore(Once):
    """A rule that matches 0 or more times. If more than once, joinRule is required between each match"""
    def __init__(self, rule, joinRule = ""):
        self.rule = Once(rule)
        self.join = Once(joinRule)

    def parse(self,stringToParse, startingPoints = set([0])):
        return Or("", OneOrMore(self.rule, self.join)).parse(stringToParse, startingPoints)



class Next(Once):
    """'Positive Look Ahead' -- A rule that checks the next characters and determines if it matches"""
    def __init__(self, rule):
        self.rule = Once(rule)
    def parse(self,stringToParse, startingPoints = set([0])):
        newPoints = set()
        for start in startingPoints:
            if self.rule.parse(stringToParse, set([start])) != set():
                newPoints.add(start)
        return newPoints
LookAhead = Next



class NotNext(Once):
    """'Negative Look Ahead' -- A rule that checks the next characters in the string and determines if it doesn't match"""
    def __init__(self, rule):
        self.rule = Once(rule)
    def parse(self,stringToParse, startingPoints = set([0])):
        newPoints = set()
        for start in startingPoints:
            if self.rule.parse(stringToParse, set([start])) == set():
                newPoints.add(start)
        return newPoints



class Previous(Once): #TODO FIX ????( Not Sure If This Needs Fixing)
    """'Positive Look Behind' -- starts at the beginning and removes previous matches that don't match this"""
    def __init__(self, rule):
        self.rule = Once(rule)
    def parse(self, stringToParse, startingPoints = set([0])):
        return( startingPoints & Sequence(ZeroOrMore(wild), self.rule).parse(stringToParse) )    
LookBehind = Previous



class NotPrevious(Once): 
    """'Negative Look Behind' -- starts at the beginning and removes previous matches that also match this"""
    def __init__(self, rule):
        self.rule = Once(rule)
    def parse(self, stringToParse, startingPoints = set([0])):
        return( startingPoints - Sequence(ZeroOrMore(wild), self.rule).parse(stringToParse) )


    
class FindStart(Once):
    """If a rule matches any substring(s) of the text, all possible starting points will be returned"""
    def __init__(self, rule):
        self.rule = Once(rule)
    def parse(self,stringToParse, startingPoints = set([0])):
        return Chain(ZeroOrMore(wild), Next(self.rule)).parse(stringToParse)


        
class FindEnd(Once): #TODO CHECK
    """If a rule matches any substring(s) of the text, all possible ending points will be returned"""
    def __init__(self, rule):
        self.rule = Once(rule)
    def parse(self,stringToParse, startingPoints = set([0])):
        return Chain(ZeroOrMore(wild), self.rule).parse(stringToParse)



    
class Min(Once):
    """'lazy' - get the ending point of the earliest match. DIFFERENT FROM REGEX"""
    def __init__(self, rule=""):
        self.rule = Once(rule)
    def parse(self,stringToParse, startingPoints = set([0])):
        return set([min(self.rule.parse(stringToParse, startingPoints))])
Lazy = Min



class Max(Once):
    """'greedy' - Get the ending point of the latest match. DIFFERENT FROM REGEX"""
    def __init__(self, rule=""):
        self.rule = Once(rule)
    def parse(self,stringToParse, startingPoints = set([0])):
        return set([max(self.rule.parse(stringToParse, startingPoints))])
Greedy = Max
    
    


## Special Predefined Classes
newLine = Once("\n")
newline = newLine
nL      = newLine
nl      = newLine



class wsc(Once):
    def parse(stringToParse, startingPoints = set([0])):
        newPoints = set([])
        for start in startingPoints:
            if start < len(stringToParse) and stringToParse[start].isspace():
                newPoints.add( start + 1 )
        return newPoints       
wsc                 = wsc()
wSC                 = wsc
whiteSpaceChar      = wsc
whitespacechar      = wsc



class ws(Once):
    def parse(stringToParse, startingPoints = set([0])):
        """matches 0 or more whitespace characters"""
        return ZeroOrMore(wsc).parse(stringToParse, startingPoints)
ws         = ws()
wS         = ws
whiteSpace = ws
whitespace = ws



class lower(Once):
    def parse(self,stringToParse, startingPoints = set([0])):
        """matches if the character is the same as the character.lower()"""
        newPoints = set([])
        for start in startingPoints:
            if start < len(stringToParse) and stringToParse[start] == stringToParse[start].lower():
                newPoints.add( start + 1 )
        return newPoints
lower         = lower()
lowercase     = lower
class upper(Once):
    def parse(self,stringToParse, startingPoints = set([0])):
        """matches if the character is the same as the character.lower()"""
        newPoints = set([])
        for start in startingPoints:
            if start < len(stringToParse) and stringToParse[start] == stringToParse[start].upper():
                newPoints.add( start + 1 )
        return newPoints
    
        
class alpha(Once):
    def parse(self,stringToParse, startingPoints = set([0])):
        newPoints = set([])
        for start in startingPoints:
            if start < len(stringToParse) and stringToParse[start].isalpha():
                newPoints.add( start + 1 )
        return newPoints
alpha = alpha()
class alnum(Once):
    def parse(self,stringToParse, startingPoints = set([0])):
        newPoints = set([])
        for start in startingPoints:
            if start < len(stringToParse) and stringToParse[start].isalnum():
                newPoints.add( start + 1 )
        return newPoints
alnum = alnum()
alphaNum    = alnum
alphanum    = alnum
class digit(Once):
    def matches(self,stringToParse):
        return len(stringToParse) in self.parse(stringToParse)
    def parse(self,stringToParse, startingPoints = set([0])):
        newPoints = set([])
        for start in startingPoints:
            if start < len(stringToParse) and stringToParse[start].isdigit():
                newPoints.add( start + 1 )
        return newPoints

class wildCard(Once):
    def parse:
        """matches any single character"""
        for start in startingPoints:
            if start < len(stringToParse):
                newPoints.add( start + 1 )
        return newPoints

wildCard     = wildCard()
wildcard     = wildCard
wildChar     = wildCard
wildchar     = wildCard
wildCardChar = wildCard
wildcardchar = wildCard


class exclude:
    def __init__(self, excludeChars=""):
        """exclusive wild card"""
        self.exclude= excludeChars
    def matches(self,stringToParse):
        return len(stringToParse) in self.parse(stringToParse)
    def parse(self,stringToParse, startingPoints = set([0])):
        newPoints = set([])
        for start in startingPoints:
            if start < len(stringToParse) and (stringToParse[start] not in self.exclude):
                newPoints.add( start + 1 )
        return newPoints

if __name__ == "__main__":
    success  = True
    failedAt = []
    print("Running Tests...")
    if success:
        print("Tests Completed Successfully")
    else:
        print("Failed Some Tests")
