import read, copy
from util import *
from logical_classes import *


class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def kb_assert(self, fact):
        """Assert a fact or rule into the KB

        Args:
            fact (Fact or Rule): Fact or Rule we're asserting in the format produced by read.py
        """

        print("Asserting {!r}".format(fact))

        if isinstance(fact, Fact):
            # checking if fact already exists in the fact list
            if fact not in self.facts:
                self.facts.append(fact)
        
        
        


    def kb_ask(self, fact):
        print("Asking  {!r}".format(fact))

        #creating an object of class ListofBindings

        a = ListOfBindings()

        # creating an empty list for supporting facts and rules 
        c = []
    

        for i in self.facts:

            b = match(i.statement, fact.statement)

            
            

            if b:
                


                c.append(i.statement)
                a.add_bindings(b, c)





        if a:
            
            return a

            


        

        


            

            



        




