"""
Copyright (c) 2011, The MITRE Corporation.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. All advertising materials mentioning features or use of this software
   must display the following acknowledgement:
   This product includes software developed by the author.
4. Neither the name of the author nor the
   names of its contributors may be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

"""
ExerciseIntellect

Description: Exercises the Intellect object

Initial Version: Feb 9, 2011

@author: Michael Joseph Walsh
"""

import sys, logging

from intellect.Intellect import Intellect
from intellect.Intellect import Callable


class MyIntellect(Intellect):

    @Callable
    def bar(self):
        self.log(">>>>>>>>>>>>>>  called MyIntellect's bar method as it was decorated as callable.")


if __name__ == "__main__":

    # tune down logging inside Intellect
    logger = logging.getLogger('intellect')
    logger.setLevel(logging.DEBUG) # change this to ERROR for less output
    consoleHandler = logging.StreamHandler(stream=sys.stdout)
    consoleHandler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s%(message)s'))
    logger.addHandler(consoleHandler)

    # set up logging for the example
    logger = logging.getLogger('example')
    logger.setLevel(logging.DEBUG)
    
    consoleHandler = logging.StreamHandler(stream=sys.stdout)
    consoleHandler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s%(message)s'))
    logger.addHandler(consoleHandler)

    print "*"*80
    print """create an instance of MyIntellect extending Intellect, create some facts, and exercise the MyIntellect's ability to learn and forget"""
    print "*"*80

    myIntellect = MyIntellect()

    policy_a = myIntellect.learn("./rulesets/test_a.policy")
    policy_d = myIntellect.learn("./rulesets/test_d.policy")

    myIntellect.reason(["test_d", "test_a"])

    myIntellect.forget_all()

    from intellect.examples.testing.subModule.ClassB import ClassB

    # keep an identifier (b1) around to a ClassB, to demonstrate that a rule
    # can modify the object and the change is reflected in b1
    b = ClassB( property1="apple", property2 = 11)
    myIntellect.learn(b)

    b = ClassB( property1="pear", property2 = 11)
    myIntellect.learn(b)

    # learn policy at '../rulesets/test_a.policy'
    policy_a = myIntellect.learn("./rulesets/test_a.policy")
    policy_a = myIntellect.learn("./rulesets/test_b.policy")
    #print policy.str_tree()
    #print str(policy_a)

    print "*"*80
    print "message MyIntellect to reason over the facts in knowledge"
    print "*"*80

    myIntellect.reason(["test_a"])

    print "*"*80
    print "facts in knowledge after applying policies"
    print "*"*80

    print  myIntellect.knowledge

    for fact in myIntellect.knowledge:
        print "type: {0}, __dict__: {1}".format(type(fact), fact.__dict__)

    print "*"*80
    print "forget all, learn a policy from a string"
    print "*"*80

    myIntellect.forget_all()

    policy = myIntellect.learn("""rule rule_inline:
    then:
        a = 1
        b = 2
        c = a + b
        print("{0} + {1} = {2}".format(a, b, c))
""")

    myIntellect.reason()

    print "*"*80
    print 'forget all, learn test_c.policy, reason over ["1", "2", "3", "4", "5", "6"]'
    print "*"*80

    myIntellect.forget_all()

    policy_c = myIntellect.learn("./rulesets/test_c.policy")

    myIntellect.reason(["1", "2", "3", "4", "5", "6"])