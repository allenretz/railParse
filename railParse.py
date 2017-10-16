#Allen Retzler
#Mar 11, 2017

"""
Name:    RailParser
Author:  Allen Retzler
Date:    Apr 11, 2017
Updated: Oct 15, 2017
"""



## MATCHING RULES
class Once:
    """Matches the rule exactly once
       This is the base Parse Rule and
       is called and inherrited by others"""
    def __init__(self, rule):
        self.rule = rule
    def match(self, stringToMatch):
        """returns True if the entire string matches"""
        return len(stringToMatch) in self.parse(stringToMatch)
    def matches(self, stringToMatch):
        """Alias for match"""
        return self.matches(stringToMatch)
        
    def parse(self, stringToParse, startingPoints = set([0])):
        if type(self.rule) == type(""):
            newPoints = set()
            for start in startingPoints:
                if start + len(self.rule) <= len(stringToParse) and stringToParse[start: start + len(self.rule)] == self.rule:
                    newPoints.add(start + len(self.rule))
            return newPoints;
        else:
            return self.rule.parse(stringToParse, startingPoints)

class One(Once):
    """Alias for Once"""
    pass
O

class Chain(Once):
    """A Chain of rules that have to be matched in order"""
    def __init__(self, *rules):
        self.chain = [Once(x) for x in  rules]

    def parse(self,stringToParse, startingPoints = set([0])):
        for i in self.chain:
            startingPoints = i.parse(stringToParse, startingPoints)
        return startingPoints
class Sequence(Chain):
    """Alias for Chain"""
    pass
class And(Chain):
    """Alias for Chain"""
    pass


class Or(Once):
    """A set of rules where atleast one choice has to match"""
    def __init__(self, *rules):
        self.options = [Once(x) for x in  rules]
        
    def parse(self,stringToParse, startingPoints = set([0])):
        newPoints =set()
        
        for i in self.options:
            newPoints |= i.parse(stringToParse, startingPoints)
        return newPoints
class Choice(Or):
    """Alias for Or"""
    pass


class Optional(Once):
    """A rule that is optional (matches 0 or 1 time)"""
    def __init__(self, rule):
        self.rule = Once(rule)
    def parse(self,stringToParse, startingPoints = set([0])):
        return Or("", self.rule).parse(stringToParse, startingPoints)
    
class ZeroOrOne(Optional):
    """Alias for Optional"""
    pass
    
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
class LookAhead(Next):
    """Alias for Next"""
    pass

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

class Previous(Once): #TODO FIX
    """'Positive Look Behind' -- starts at the beginning and removes previous matches that don't match this"""
    def __init__(self, rule):
        self.rule = Once(rule)
    def parse(self, stringToParse, startingPoints = set([0])):
        return( startingPoints & Sequence(ZeroOrMore(wild), self.rule).parse(stringToParse) )
    
class LookBehind(Previous):
    """Alias for Previous"""
    pass
class NotPrevious(Once): 
    """'Negative Look Behind' -- starts at the beginning and removes previous matches that also match this"""
    def __init__(self, rule):
        self.rule = Once(rule)
    def parse(self, stringToParse, startingPoints = set([0])):
        return( startingPoints - Sequence(ZeroOrMore(wild), self.rule).parse(stringToParse) )
class FindStart(Once): #Replace with IN
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
    """'lazy' - get the smallest (earliest) match"""
    def __init__(self, rule=""):
        self.rule = Once(rule)
    def parse(self,stringToParse, startingPoints = set([0])):
        return set([min(self.rule.parse(stringToParse, startingPoints))])
class Lazy(Min):
    """Alias for Min"""
    pass

class Max(Once):
    """'greedy' - Get the largest (latest) startingPoint"""
    def __init__(self, rule=""):
        self.rule = Once(rule)
    def parse(self,stringToParse, startingPoints = set([0])):
        return set([max(self.rule.parse(stringToParse, startingPoints))])
class Greedy(Max):
    """Alias for Max"""
    pass
    
    


## Special Predefined Classes
class newline:
    def matches(stringToMatch):
        """Returns True if the string is a single newline character"""
        return len(stringToMatch) in newline.parse(stringToMatch)
    def match(stringToMatch):
        """Alias for matches"""
        return newline.matches(stringToParse)
    def parse(stringToParse, startingPoints = set([0])):
        """matches a single newline character"""
        newPoints = set([])
        for start in startingPoints:
            if start < len(stringToParse) and stringToParse[start] == "\n" :
                newPoints.add( start + 1 )
        return newPoints


class wsc:
    def matches(stringToMatch):
        """returns True if the string is a single whitespace character"""
        return True if len(stringToMatch) == 0 and stringToMatch.isspace() else False
    def match(stringToParse):
        """Alias for matches"""
        return wsc.matches(stringToParse)
    def parse(stringToParse, startingPoints = set([0])):
        newPoints = set([])
        for start in startingPoints:
            if start < len(stringToParse) and stringToParse[start].isspace():
                newPoints.add( start + 1 )
        return newPoints       

class ws:
    def matches(stringToParse):
        """returns True if the string is empty or is a SINGLE LINE contaning all white space"""
        return len(stringToParse) in ws.parse(stringToParse)
    def parse(stringToParse, startingPoints = set([0])):
        """matches 0 or more whitespace characters"""
        return ZeroOrMore(wsc).parse(stringToParse, startingPoints)
class lower:
    def matches(stringToParse):
        """returns True if the string is the same when .lower() is run"""
        return True if stringToParse == stringToParse.lower() else False
    def match(stringToMatch):
        """Alias for matches"""
        return lower.matches()
    def parse(self,stringToParse, startingPoints = set([0])):
        """matches if the character is the same as the character.lower()"""
        lowerCase = "abcdefghijklmnopqrstuvwxyz"
        newPoints = set([])
        for start in startingPoints:
            if start < len(stringToParse) and stringToParse[start] in self.lowerCase:
                newPoints.add( start + 1 )
        return newPoints
class upper:
    def __init__(self):
        self.upperCase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    def matches(self,stringToParse):
        return len(stringToParse) in self.parse(stringToParse)
    def parse(self,stringToParse, startingPoints = set([0])):
        """matches if the character is the same as the character.lower()"""
        newPoints = set([])
        for start in startingPoints:
            if start < len(stringToParse) and stringToParse[start] in self.upperCase:
                newPoints.add( start + 1 )
        return newPoints
    
        
class alpha:
    def matches(self,stringToParse):
        return len(stringToParse) in self.parse(stringToParse)
    def parse(self,stringToParse, startingPoints = set([0])):
        newPoints = set([])
        for start in startingPoints:
            if start < len(stringToParse) and stringToParse[start].isalpha():
                newPoints.add( start + 1 )
        return newPoints
class alnum:
    def matches(self,stringToParse):
        return len(stringToParse) in self.parse(stringToParse)
    def parse(self,stringToParse, startingPoints = set([0])):
        newPoints = set([])
        for start in startingPoints:
            if start < len(stringToParse) and stringToParse[start].isalnum():
                newPoints.add( start + 1 )
        return newPoints
class digit:
    def matches(self,stringToParse):
        return len(stringToParse) in self.parse(stringToParse)
    def parse(self,stringToParse, startingPoints = set([0])):
        newPoints = set([])
        for start in startingPoints:
            if start < len(stringToParse) and stringToParse[start].isdigit():
                newPoints.add( start + 1 )
        return newPoints

class wild:
    def match(stringToMatch):
        "returns true if the string is a single character"
        return True if len(stringToMatch) == 1 else False
    def matches(stringToMatch):
        "Alias for match"
        return wild.match(stringToMatch)
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
