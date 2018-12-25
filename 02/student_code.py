import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact_or_rule):
        """Retract a fact from the KB

        Args:
            fact (Fact) - Fact to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact_or_rule])
        ####################################################
        # Student code goes here

        if isinstance(fact_or_rule, Fact):
            if fact_or_rule in self.facts:

                temp1 = self.facts.index(fact_or_rule)
                if temp1 != None:
                    fact_retract = self.facts[temp1]
                    if fact_retract.asserted == True:
                        self.facts.remove(fact_or_rule)
                        if len(fact_retract.supports_facts) > 0:
                            for i in fact_retract.supports_facts:
                                i.asserted = True
                                for l in i.supported_by:
                                    for p in l:
                                        if fact_or_rule == p:
                                            l.remove(p)
                                self.kb_retract(i)

                        if len(fact_retract.supports_rules) > 0:
                            for j in fact_retract.supports_rules:
                                for l in j.supported_by:
                                    for p in l:
                                        if fact_or_rule == p:
                                            l.remove(p)
                                self.kb_retract(j)

        elif isinstance(fact_or_rule, Rule):
            if fact_or_rule in self.rules:
                temp1 = self.rules.index(fact_or_rule)
            if temp1 is not None:
                fact_retract = self.rules[temp1]
                if fact_retract.asserted == False:
                    self.rules.remove(fact_or_rule)
                    if len(fact_retract.supports_facts) > 0:
                        for i in fact_retract.supports_facts:
                            i.asserted = True
                            for l in i.supported_by:
                                for p in l:
                                    if fact_or_rule == p:
                                        l.remove(p)
                            self.kb_retract(i)
                    if len(fact_retract.supports_rules) > 0:
                        for j in fact_retract.supports_rules:
                            for l in j.supported_by:
                                for p in l:
                                    if fact_or_rule == p:
                                        l.remove(p)
                            self.kb_retract(j)

        else:
            return







class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # Student code goes here

        left_bindings = match(fact.statement, rule.lhs[0])

        if left_bindings:
            if len(rule.lhs) == 1:
                    temp_statement = instantiate(rule.rhs, left_bindings)
                    supported_by = [[fact,rule]]

                    fact_new =Fact(temp_statement,supported_by)


                    fact.supports_facts.append(fact_new)
                    rule.supports_facts.append(fact_new)

                    kb.kb_add(fact_new)




            else:
                current_lhs = []

                for i in rule.lhs[1:]:

                    current_lhs.append(instantiate(i, left_bindings))

                new_rhs = instantiate(rule.rhs, left_bindings)


                binded_list = [[fact,rule]]



                new_rule = Rule([current_lhs, new_rhs],binded_list)

                fact.supports_rules.append(new_rule)
                rule.supports_rules.append(new_rule)
                kb.kb_add(new_rule)


        else:
            return
