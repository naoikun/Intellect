_My apologies, a better readme will follow..._

# Overview

Let's clear up what Intellect is.

Intellect is a DSL (“Domain-Specific Language”) and Rule Engine for Python
I authored for expressing policies to orchestrate and control a dynamic 
network defense cyber-security platform being researched in The 
MITRE Corporation's Innovation Program. 

The language and rule engine form a "production rule system", where computer
algorithms are used to provide some form of artificial intelligence, which
consists primarily of a set of rules about behavior. For platform in the
Innovation Program, the network defender uses the DSL to confer policy, 
how the platform is to respond to network events mounted over covert 
network channels, but there are no direct ties written into the language 
nor the rule engine to cyber-security, and thus the system in its 
entirety can be more broadly used in other domains.

Many production rule system implementations have been open-sourced, such as
JBoss Drools, Rools, Jess, Lisa, et cetera.  If you've seen Drools, the 
syntax should look familiar. (I'm not saying it is based on it, because
it is not, but when I was working the syntax I checked with Drools and
if made sense to push in the direction of Drools, I did.)  The aforementioned 
implementations are available for other languages for expressing production 
rules, but it is my belief that Python is under-represented, and as such 
it was my thought the language and rule engine could benefit from being
open sourced, and so put a request in. 

The MITRE Corporation granted release August 4, 2011.

Thus, releasing the domain-specific language (DSL) and Rule Engine to Open
Source in the hopes doing so will extend its use and increase its chances 
for possible adoption, while at the same time mature the project with more 
interested eyeballs being placed on it.

# Background 

Starting out, it was initially assumed the aforementioned platform would 
be integrated with the best Open Source rules engine available for 
Python as there are countless implementation for Ruby, Java, and Perl, 
but surprisingly I found none fitting the project's needs. This led to 
the thought of inventing one; simply typing the keywords “python rules 
engine” into Google though will return to you the advice “to not invent 
yet another rules language”, but instead you are advised to “just write 
your rules in Python, import them, and execute them.” The basis for this 
advice can be coalesced down to doing so otherwise does not fit with the 
“Python Philosophy.” At the time, I did not believe this to be true, nor 
fully contextualized, and yet admittedly, I had not yet authored a line 
of Python code (Yes, you're looking at my first Python program. So,
please give me a break.) nor used  ANTLR3 prior to this effort. Looking 
back, I firmly believe the act of inventing a rules engine and abstracting it 
behind a nomenclature that describes and illuminates a specific domain is 
the best way for in case of aforementioned platform the network defender 
to think about the problem. Like I said though the DSL and rules engine
could be used for anything needing a "production rule system".

As there were no rules engines available for Python fitting the platforms
needs, a policy language and naive forward chaining rules engine were built 
from scratch. The policy language's grammar is based on a subset of Python 
language syntax.  The policy DSL is parsed and lexed with the help of the 
ANTLR3 Parse Generator and  Runtime for Python. 


# Walkthrough

A walkthrough to get you jump-started.

## Dependencies

You need to download and install the ANTLR3 3.1.3 Python Runtime, 
and Python itself, if you don't already have it.  I tested the code on
Python 2.7.1 and 2.7.2. 

## Facts (Data being reasoned over)

The interpreter, the rules engine, and the remainder of the code such as 
objects for conferring discrete network conditions, referred to as "facts",
are also authored in Python. Python’s approach to the object-orientated programming
paradigm, where objects consist of data fields and methods, did not easily
lend itself to describing "facts". Because the data fields of a Python object 
referred to syntactically as “attributes” can and often are set on an 
instance of a class, they will not exist prior to a class’s instantiation. 
In order for a rules engine to work, it must be able to fully “introspect” an 
object instance representing a condition. This proves to be very difficult 
unless the property decorator with its two attributes, “getter” and “setter”, 
introduced in Python 2.6, are adopted and formally used for authoring these objects. 
Coincidentally, the use of the “Getter/Setter Pattern” used frequently in 
Java is singularly frowned upon in the Python developer community with the 
cheer of “Python is not Java.”

So, you will need to author you facts as Python object's who attributes 
are formally denoted as properties like so:

	@property
	def property0(self):
		return self._property0
	
	@property0.setter
	def property0(self, value):
		self._property0 = value

## The Policy DSL

Example policy files can be found in intellect/rulesets, and must follow 
the Policy grammar as define in intellect/grammar/Policy.g
 
### Import Statments (_ImportStmts_)

Import statement basically follow Python's with a few limitations (For 
example, The wild card form of import is not supported for the reasons
elaborated
[here](http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html#importing)) 
and follow the Python 2.7.2 grammar. _ImportStmt_s exist only at the same level of 
_ruleStmt_s as per the grammar, and are typically at the top of a policy 
file, but are not limited to. In fact if you break up your policy 
across several files the last imported as class or module wins as the
one being named.

### globals

To be written.

### Rule Statements (_ruleStmt_) 

A rule statement at its simplest looks like so:

	22	rule "print":	
	23	        then:
	24	                print("hello world!!!!")

Rule "print" will always print "hello world!!!!" to the 'sys.stdout'.

More generally, a rule will have both a _when_- and _then_-portion, and
depending on the _when_-portion constraint will match facts in knowledge 
and return them to operated over in the _then-_portion of the rule. 

Such as in the rule "delete those that don't match", all facts of type 
ClassD who's property1 value is either a 1 or 2 or 3 will be deleted 
in _then-_portion of the rule. 

	1	from intellect.testing.ClassCandD import ClassD
	
	-- snip --
	
	10	rule "delete those that don't match":
	11	        when:
	12	                not $bar := ClassD(property1 in [1,2,3])
	13	        then:
	14	                delete $bar  


### Regular Expressions in _ruleCondition_._classConstraint_._constraints_:

You can also use regular expressions in a Rules' _ruleCondition_ by 
importing the regular expression library straight from Python and 
then using like so...

From example:

	2	from intellect.testing.subModule.ClassB import ClassB 
	
	-- snip ---
	
	4	import re
	5	
	6	rule rule_a:
	7	        when:
	8	                $classB := ClassB( re.search(r"\bapple\b", "apple")!=None and property2>5 and test.greaterThanTen(property2) and aMethod() == "a")

To keep the policy files from turning into just another Python script you
will want to keep as little code out of the policy file was possible... Use
the _modify_, _delete_, _insert_ grammar defined actions in the _then_-portions of
the _ruleStmt_ as well as using _simpleStatements_. If you are writing very
complicated constraints in the when-portions of a _ruleStmt_, consider moving 
the constraint into a method of fact being reasoned over.

For example, the above regular expression example would become:

	4	import re
	5	
	6	rule rule_a:
	7	        when:
	8	                $classB := ClassB(property1ContainsTheStrApple() and property2>5 and test.greaterThanTen(property2) and aMethod() == "a")

If you were to add the method

	def property1ContainsTheStrApple()
       		return re.search(r"\bapple\b", property1) != None

to ClassB. 

### _not_'ed _ruleCondition_:

A _ruleCondition_ may be _not_'ed as follows:

	21	rule rule_b:
	22	        when:
	23	                not $classB := ClassB( property1.startswith("apple") and property2>5 and test.greaterThanTen(property2) and aMethod() == "a")


and thus negate the condition and return matches as such to the then-portion
of the rule to be operated on. 

### exists ruleCondition:

A ruleCondition may be prepended with _exists_ as follows:

	31	rule rule_c:
	32	        when:
	33	                exists $classB := ClassB(property1.startswith("apple") and property2>5 and test.greaterThanTen(property2) and aMethod() == "a")
	34	        then:
	35	                print("matches" + " exist")     
	36	                a = 1
	37	                b = 2
	38	                c = a + b
	39	                print(c)
	40	                test.helloworld()               
	41	                # call MyIntellect's bar method as it is decorated as callable
	42			bar()

and thus the _then_-portion of the _ruleStmt_ will be called once if there are
any object in memory matching the condition. The _action_ statements
_modify_ and _delete_ may not be used in the _then_-portion of a _ruleStmt_, 
if _exists_' pre-pends the _when_-portions's _ruleCondition_. 

### _agenda-group_ rule property

To be written.

### modify, delete, and insert actions:

Earlier, I mentioned the use of _modify_, _delete_, _insert_ grammar 
defined _action_s in the _then_-portions of a rule.

The following:
 
	13	                modify $classB:
	14	                        # add " hell world" to 'property1' of 'ClassB' matches
	15	                        property1 = $classB.property1 + " " + test.helloworld()
	16	                        # return true from the ClassB's 'trueValue()' method and use it to set the matches modified property
	17	                        modified = $classB.trueValue()
	18	                        # increment the match's 'property2' value by 1000
	19	                        property2 = $classB.property2 + 1000

illustrates the use of a _modify_ _action_ to modify each match returned by
rule_a's _when_-portion. Cannot be used in conjunction with _exists_. The
_modify_ _action_ can also be used to chain _ruleStmts_, what you do is 
modify the fact (toggle a boolean property, set a property's value, et cetera) 
and then use this property to evaluate in the proceeding _ruleStmt_.

A rule entitled  "delete those that don't match" might look like the following:

	10	rule "delete those that don't match":
	11	        when:
	12	                not $bar := ClassD(property1 in [1,2,3])
	13	        then:
	14	                delete $bar    

illustrates the use of a _delete_ _action_ to delete each match returned by
the rule's _when_-portion. Cannot be used in conjunction with _exists_.

For _insert_, rule "insert ClassD" might look like the following:

	26	rule "insert ClassD":
	27	        then:
	28	                insert ClassD("foobar")

and illustrates the use of an insert action to insert a ClassD fact. 

### Simple Statments (_SimpleStmt_):

_SimpleStmts_ are supported actions for _then_-portion of a rule, and so one 
can do the following:

	31	rule rule_c:
	32	        when:
	33	                exists $classB := ClassB(property1.startswith("apple") and property2>5 and test.greaterThanTen(property2) and aMethod() == "a")
	34	        then:
	35	                print("matches" + " exist")     
	36	                a = 1
	37	                b = 2
	38	                c = a + b
	39	                print(c)
	40	                test.helloworld()               
	41	                intellect.bar()

The _simpleStmt_s on lines 35 through 41 can be executed if any facts in
knowledge exist matching the _ruleCondition_.

### _attribute_ statements

To be written.

## Creating and using a Rules Engine with a policy


At its simplest a rules engine can be created and used like so:

	1	import sys, logging
	2	
	3	from intellect.Intellect import Intellect
	4	from intellect.Intellect import Callable
	5
	6	# set up logging
	7	logging.basicConfig(level=logging.DEBUG,
	8	format='%(asctime)s %(name)-12s%(levelname)-8s%(message)s',
	9		#filename="rules.log")
	10		stream=sys.stdout)
	11
	12	intellect = Intellect()
	13
	14	policy_a = intellect.learn("../rulesets/test_a.policy")
	15
	16	intellect.reason()
	17
	18 	intellect.forget_all()


It may be preferable for you to sub-class intellect.Intellect.Intellect in 
order to add @Callable decorated methods in order to permit these methods
to be called from a the _then_-portion of the rule.
 
For example, MyIntellect is created to sub-class Intellect:

	1	import sys, logging
	2
	3	from intellect.Intellect import Intellect
	4	from intellect.Intellect import Callable
	5
	6	class MyIntellect(Intellect):
	7
	8		@Callable
	9		def bar(self):
	10			self.log(logging.DEBUG, ">>>>>>>>>>>>>>  called MyIntellect's bar method as it was decorated as callable.")
	11
	12	if __name__ == "__main__":
	13
	14		# set up logging
	15		logging.basicConfig(level=logging.DEBUG,
	16			format='%(asctime)s %(name)-12s%(levelname)-8s%(message)s',
	17			#filename="rules.log")
	18			stream=sys.stdout)
	19
	20		print "*"*80
	21		print """create an instance of MyIntellect extending Intellect, create some facts, and exercise the MyIntellect's ability to learn and forget"""
	22		print "*"*80
	23
	24		myIntellect = MyIntellect()
	25
	26		policy_a = myIntellect.learn("../rulesets/test_a.policy")
	27
	28		myIntellect.reason()
	29
	30		myIntellect.forget_all()

The policy could then be authored, where _MyIntellect_'s _bar_-method is called on line 22 for matches 
to the _ruleCondition_ on line 11, like so:

	1	from intellect.testing.subModule.ClassB import ClassB
	2	import intellect.testing.Test as Test
	3	import logging
	4
	5	fruits_of_interest = ["apple", "grape", "mellon", "pear"]
	6	count = 5
	7
	8	rule rule_a:
        9		agenda-group test_a
        10		when:
        11	        	$classB := ClassB( property1 in fruits_of_interest and property2>count ) 
        12		then:
        13	        	# mark the 'ClassB' matches in memory as modified
        14	        	modify $classB:
        15	                	property1 = $classB.property1 + " pie"
        16	                	modified = True
        17	                	# increment the match's 'property2' value by 1000
        18	                	property2 = $classB.property2 + 1000
        19	        	attribute count = $classB.property2
        20	        	print "count = {0}".format( count )
        21	        	# call MyIntellect's bar method as it is decorated as callable
        22	        	bar()
        23	        	log(logging.DEBUG, "rule_a fired")

