"""
Name:    RailParser
Author:  Allen Retzler
Date:    Apr 11, 2017
Updated: NOV 5,  2017
"""

import itertools
import warnings

def simplify(rule): # TODO: simplify the _railParse
    ptr = rule
    ptrIsSimple = True
    """Simplify the parse rule"""
    while type(ptr) != str:
        if type(ptr) == _railParse:
            ptr = ptr.rule
        if type(ptr) == type(Sequence()):
            ptrIsSimple = False
            
    return _railParse(ptr)

## TODO: \/\/\/\/\/
## TODO:  \/\/\/\/
## TODO:   DON'T CALL _railParse FOR EVERY SINGLE CALL !!!!
## TODO:  /\/\/\/\
## TODO: /\/\/\/\/\

## MATCHING RULES

class _railParse:
    """Internal Class Used to Match Parse Rules"""
    #TODO: Allow Regex and File input as well
    def __init__(self, rule=""):
            self.parseType = "Once"
            self.rule = rule
    def __str__(self):
        warnings.warn("Not Fully Implemented! Results may not be accurate")
        try:
            if type(self.rule) == str:
                return self.parseType + "(\""+ str(self.rule) + "\")"
            else:
                return self.parseType + "(\n"+ str(self.rule) + "\n)"
        except AttributeError:
            return self.parseType + "("+ str(",".join(["\""+str(x)+"\"" if type(x) == str else str(x) for x in self.rules])) + ")"
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
        """returns a set of all points that match the rule """
        if type(self.rule) == str:
            newPoints = set()
            for start in startingPoints:
                if start + len(self.rule) <= len(stringToParse) and stringToParse[start: start + len(self.rule)] == self.rule:
                    newPoints.add(start + len(self.rule))
            return newPoints;
        else:
            typ = type(self.rule).__name__
            try:
                return self.rule.parse(stringToParse, startingPoints)
            except AttributeError:
                pass
            raise TypeError('"' + typ + '" can not be converted into railParse')
        

    def simplify(self):
        __doc__ = simplify.__doc__
        return simplify(self)

    def inh(self, stringToFind):
        raise NotImplemented
    def findStart(self, stringToFind, startingPoint =0, endingPoint =-1):
        raise NotImplemented
    def findEnd(self, stringToFind, startingPoint =0, endingPoint =-1):
        raise NotImplemented

    def toRegex(outputType = "Regex"):
        """Converts the _railParse to a regex.Pattern or String"""
        raise NotImplemented("Not Yet Implemted")





    def __eq__(self, other):
        warnings.warn("Not Fully Implemented! Results may not be accurate")
        return True if self.simplify().rule == other.simplify().rule else False
    def __lt__(self, other):
        warnings.warn("Not Fully Implemented! Results may not be accurate")
        return False
    def __gt__(self, other):
        warnings.warn("Not Fully Implemented! Results may not be accurate")
        return False
    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)
    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)
    def __ne__(self, other):
        return not self.__eq__(other)
    def __add__(self, ruleOrString):
        if type(self) == _railParse and self.parseType == "Sequence":
            if type(ruleOrString) == _railParse and self.parseType == "Sequence":
                return(Sequence(*self.rules, *ruleOrString.rules))
            else:
                return(Sequence(*self.rules, ruleOrString))
        else:
            if type(ruleOrString) == _railParse and self.parseType == "Sequence":
                return(Sequence(self, *ruleOrString.rules))
            else:
                return(Sequence(self, ruleOrString))
    def __radd__(self, ruleOrString):
        if type(self) == _railParse and self.parseType == "Sequence":
            if type(ruleOrString) == _railParse and self.parseType == "Sequence":
                return(Sequence(*ruleOrString.rules, *self.rules))
            else:
                return(Sequence(ruleOrString, *self.rules))
        else:
            if type(ruleOrString) == _railParse and self.parseType == "Sequence":
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


def Once(rule=""):
    """Matches a rule exactly Once"""
    if type(rule) == _railParse:
        return rule
    else:
        return _railParse(rule)
        
One = Once()



def Sequence(*rules):
    """A set of rules that have to be matched in order"""
    self = _railParse()
    self.parseType = "Sequence"
    del self.rule


    tmpRules = []
    for x in rules:
        if type(x) == _railParse and x.parseType == "Sequence":
            tmpRules.append(*x.rules)
        else:
            tmpRules.append(x)
            
    rules = [x.rule if type(x) == _railParse and x.parseType == "Once" else x  for x in tmpRules] 
    #https://stackoverflow.com/a/47168956/3381689
    rules = [x for cls, grp in itertools.groupby(rules, type)
          for x in ((''.join(grp),) if cls is str else grp)]
            
    if 0 <= len(rules) <= 1:
        return Once(*rules)
    self.rules = rules
    
    def parse(stringToParse, startingPoints = set([0])):
        for i in self.rules:
            startingPoints = Once(i).parse(stringToParse, startingPoints)
        return startingPoints
    self.parse = parse
    return self
Chain = Sequence


#class And(_railParse):
#    """A set of rules that all have to match in order for characters to be added"""
#    raise NotImplemented("Not Yet Implemented")


def Or(*rules):
    """A set of rules where atleast one choice has to match"""
    #TODO Run Equivalence Checks Before storing the rules
    """A set of rules that have to be matched in order"""
    self = _railParse()
    self.parseType = "Or"
    del self.rule
    self.rules = rules
        
    def parse(stringToParse, startingPoints = set([0])):
        newPoints =set()
        
        for i in self.rules:
            newPoints |= Once(i).parse(stringToParse, startingPoints)
        return newPoints
    self.parse = parse
    return self
Choice = Or



def Optional(rule):
    """A rule that is optional (matches 0 or 1 time)"""
    self = _railParse()
    self.parseType = "Optional"
    self.rule = rule
    def parse(stringToParse, startingPoints = set([0])):
        return Or("", Once(self.rule)).parse(stringToParse, startingPoints)
    self.parse = parse
    return self
ZeroOrOne = Optional


    
def OneOrMore(rule, joinRule = ""):
    """A rule that is matches 1 or more times. If more than _railParse, joinRule is required between each match"""
    self = _railParse()
    self.rule = rule
    self.join = joinRule
    self.parseType = "OneOrMore"

    def parse(stringToParse, startingPoints = set([0])):
        startingPoints = Once(self.rule).parse(stringToParse, startingPoints)
        newPoints = set() | startingPoints
        while startingPoints != set():
            startingPoints = Chain(self.join, self.rule).parse(stringToParse, startingPoints)
            newPoints |= startingPoints
            
        return newPoints
    
    self.parse = parse
    return self



def ZeroOrMore(rule, joinRule=""):
    """A rule that matches 0 or more times. If more than _railParse, joinRule is required between each match"""
    self = _railParse()
    self.rule = rule
    self.join = joinRule
    self.parseType = "ZeroOrMore"

    def parse(stringToParse, startingPoints = set([0])):
        return Or("", OneOrMore(self.rule, self.join)).parse(stringToParse, startingPoints)

    self.parse = parse
    return self



def Next(rule):
    """'Positive Look Ahead' -- A rule that checks the next characters and determines if it matches"""
    self = _railParse()
    self.rule = rule
    self.parseType = "Next"
    def parse(stringToParse, startingPoints = set([0])):
        newPoints = set()
        for start in startingPoints:
            if Once(self.rule).parse(stringToParse, set([start])) != set():
                newPoints.add(start)
        return newPoints

    self.parse = parse
    return self
LookAhead = Next



def NotNext(rule): #FIX
    """'Negative Look Ahead' -- A rule that checks the next characters in the string and determines if it doesn't match"""
    self = _railParse()
    self.rule = Once(rule)
    self.parseType = "NotNext"
    def parse(stringToParse, startingPoints = set([0])):
        newPoints = set()
        for start in startingPoints:
            if self.rule.parse(stringToParse, set([start])) == set():
                newPoints.add(start)
        return newPoints

    self.parse = parse
    return self



def Previous(rule): #FIX
    """'Positive Look Behind' -- starts at the beginning and removes previous matches that don't match this"""
    self = _railParse()
    self.rule = Once(rule)
    self.parseType = "Previous"
    def parse(stringToParse, startingPoints = set([0])):
        return( startingPoints & Sequence(ZeroOrMore(wild), self.rule).parse(stringToParse) )

    self.parse = parse
    return self
LookBehind = Previous



def NotPrevious(rule):#CHECK
    """'Negative Look Behind' -- starts at the beginning and removes previous matches that also match this"""
    self = _railParse()
    self.rule = Once(rule)
    self.parseType = "NotPrevious"
    def parse(stringToParse, startingPoints = set([0])):
        return( startingPoints - Sequence(ZeroOrMore(wild), self.rule).parse(stringToParse) )
    
    self.parse = parse
    return self


    
def FindStart(rule):#CHECK
    """If a rule matches any substring(s) of the text, all possible starting points will be returned"""
    self = _railParse()
    self.rule = Once(rule)
    self.parseType = "FindStart"
    def parse(stringToParse, startingPoints = set([0])):
        return Chain(ZeroOrMore(wild), Next(self.rule)).parse(stringToParse)

    self.parse = parse
    return self


        
def FindEnd(rule): #CHECK
    """If a rule matches any substring(s) of the text, all possible ending points will be returned"""
    self = _railParse()
    self.rule = Once(rule)
    self.parseType = "FindEnd"
    def parse(stringToParse, startingPoints = set([0])):
        return Chain(ZeroOrMore(wild), self.rule).parse(stringToParse)
    
    self.parse = parse
    return self



    
def Min(rule): #CHECK
    """'lazy' - get the ending point of the earliest match. DIFFERENT FROM REGEX"""
    self = _railParse()
    self.rule = Once(rule)
    self.parseType = "Min"
    def parse(stringToParse, startingPoints = set([0])):
        return set([min(self.rule.parse(stringToParse, startingPoints))])

    self.parse = parse
    return self
Lazy = Min



def Max(rule): #CHECK
    """'greedy' - Get the ending point of the latest match. DIFFERENT FROM REGEX"""
    self = _railParse()
    self.rule = Once(rule)
    self.parseType = "Max"
    def parse(stringToParse, startingPoints = set([0])):
        return set([max(self.rule.parse(stringToParse, startingPoints))])
    
    self.parse = parse
    return self
Greedy = Max
    
    


## Special Predefined Classes
newLine = _railParse("\n")
newline = newLine
nL      = newLine
nl      = newLine



class wsc(_railParse): #CHECK
    def __init__(self):
        pass
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



class ws(_railParse):#CHECK
    def __init__(self):
        pass
    def parse(stringToParse, startingPoints = set([0])):
        """matches 0 or more whitespace characters"""
        return ZeroOrMore(wsc).parse(stringToParse, startingPoints)
ws         = ws()
wS         = ws
whiteSpace = ws
whitespace = ws



class lower(_railParse):#CHECK
    def __init__(self):
        pass
    def parse(self,stringToParse, startingPoints = set([0])):
        """matches if the character is the same as the character.lower()"""
        newPoints = set([])
        for start in startingPoints:
            if start < len(stringToParse) and stringToParse[start] == stringToParse[start].lower():
                newPoints.add( start + 1 )
        return newPoints
lower         = lower()
lowercase     = lower
class upper(_railParse):#CHECK
    def __init__(self):
        pass
    def parse(self,stringToParse, startingPoints = set([0])):
        """matches if the character is the same as the character.lower()"""
        newPoints = set([])
        for start in startingPoints:
            if start < len(stringToParse) and stringToParse[start] == stringToParse[start].upper():
                newPoints.add( start + 1 )
        return newPoints

upper = upper()
uppercase = upper

        
class alpha(_railParse):#CHECK
    def __init__(self):
        pass
    def parse(self,stringToParse, startingPoints = set([0])):
        newPoints = set([])
        for start in startingPoints:
            if start < len(stringToParse) and stringToParse[start].isalpha():
                newPoints.add( start + 1 )
        return newPoints
alpha = alpha()
class alnum(_railParse):#CHECK
    def __init__(self):
        pass
    def parse(self,stringToParse, startingPoints = set([0])):
        newPoints = set([])
        for start in startingPoints:
            if start < len(stringToParse) and stringToParse[start].isalnum():
                newPoints.add( start + 1 )
        return newPoints
alnum = alnum()
alphaNum    = alnum
alphanum    = alnum
class digit(_railParse):#CHECK
    def __init__(self):
        pass
    def matches(self,stringToParse):
        return len(stringToParse) in self.parse(stringToParse)
    def parse(self,stringToParse, startingPoints = set([0])):
        newPoints = set([])
        for start in startingPoints:
            if start < len(stringToParse) and stringToParse[start].isdigit():
                newPoints.add( start + 1 )
        return newPoints

class wildCard(_railParse):#CHECK
    def __init__(self):
        pass
    def parse(self,stringToParse, startingPoints = set([0])):
        """matches any single character"""
        newPoints = set([])
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
wild         = wildCard


class exclude:#CHECK
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
    try:
        ## SIMPLE TEST CASES
        success &= Once("A").match("A")
        success &= not Once("A").match("")
        success &= Once("MULTIPLE CHARS").match("MULTIPLE CHARS")
        success &= Sequence("A").match("A")
        success &= not Sequence("A").match("")
        success &= Sequence("M", "U", "L", "T", "IP", "LE CHARS").match("MULTIPLE CHARS")
        success &= Or("A").match("A")
        success &= Or("A", "BA").match("BA")
        success &= not Or("A", "B").match("")
        #success &= AND(...
        success &= Optional("A").match("A")
        success &= Optional("AB").match("")
        success &= OneOrMore("A").match("A")
        success &= OneOrMore("AB").match("ABABABABAB")
        success &= OneOrMore("AB", ", ").match("AB, AB, AB, AB, AB")
        success &= ZeroOrMore("A").match("A")
        success &= ZeroOrMore("A").match("AA")
        success &= ZeroOrMore("A").match("")
        success &= ZeroOrMore("AB").match("ABABABABAB")
        success &= ZeroOrMore("AB", ", ").match("AB, AB, AB, AB, AB")
        success &= Next("A").parse("bA", set([1])) == set([1])
        success &= Next("A").parse("bA", set([1])) == set([1])
        success &= NotNext("A").parse("bD", set([1])) == set([1])
        success &= NotNext("A").parse("bA", set([1])) == set()
        #success &= NotNext("AD").parse("bA", set([1])) == set()
        #success &= Previous("A").parse("Ab", set([1])) == set([1])
        

        ## COMPLEX TEST CASES
    except:
        success = False
    
    if success:
        print("Tests Completed Successfully")
    else:
        print("Failed One Or More Tests")
