## CS 502: AI
## Assignment 1: Q6
## Russell Gillette
## Node Expansion with constraints

import string

class Node:
    def __init__(self, name, domain):
        self.domain = list(domain)
        # iterate over the domain to find solution
        self.value  = 0
        self.rules  = []
        self.active = False
        self.next_node = None
        self.last = None
        self.name = name

    def __repr__(self):
        return "{0}={1} ".format(self.name, self.value)


    def push(self, next_node):
        self.next_node = next_node
        next_node.last = self

    def check_rules(self):
        for rule in self.rules: # check all rules
            if (rule.active()):
                if not rule.check():
                    return False
        return True

    def iterate(self, state):
        # set my state
        # check all rules
        # iterate to next node
        # if returns false, swap

        leaf_count = 0
        self.active = 1
        for value in self.domain:  # set my state
            self.value = value
            if not self.check_rules():
                leaf_count += 1
                print "{0} {1} failure".format(state, self)
                continue
            elif self.next_node == None:
                leaf_count += 1
                print "{0} {1} solution".format(state, self)
            else:
                leaf_count += self.next_node.iterate("{0} {1}".format(state, self))
        self.active = 0
        return leaf_count

class Rule:
    def __init__(self, node1, node2, operation):
        self.node1 = node1
        self.node2 = node2
        self.operation = operation
        node1.rules.append(self)
        node2.rules.append(self)

    def active(self):
        return self.node1.active and self.node2.active

    def check(self):
        return self.operation(self.node1, self.node2)

# n1 < n2
def lt(node1, node2):
    return node1.value < node2.value

# n1 < n2 - 1
def lt_minus_1(node1, node2):
    return node1.value < (node2.value - 1)

# n1 != (n2 - 2)
def ne_minus_2(node1, node2):
    return node1.value != (node2.value - 2)

# n1 > n2
def gt(node1, node2):
    return node1.value > node2.value

# n1 != n2
def ne(node1, node2):
    return node1.value != node2.value

# n1 - n2 is even
def abs_diff_even(node1, node2):
    return abs(node2.value - node1.value) % 2 == 0

# |n1 - n2| is odd
def abs_diff_odd(node1, node2):
    return abs(node2.value - node1.value) % 2 == 1

# |n1 - n2| == 1
def abs_diff_eq_1(node1, node2):
    return abs(node2.value - node1.value) == 1

def Solve():
    domain   = [1, 2, 3, 4]

    #define nodes
    A = Node('A', domain)
    B = Node('B', domain)
    C = Node('C', domain)
    D = Node('D', domain)
    E = Node('E', domain)
    F = Node('F', domain)

    # link nodes
    A.push(B)
    B.push(C)
    C.push(D)
    D.push(E)
    E.push(F)

    #define rules
    rules = []
    rules.append(Rule(A, B, lt))
    rules.append(Rule(A, C, abs_diff_eq_1))
    rules.append(Rule(B, C, abs_diff_even))
    rules.append(Rule(B, D, ne))
    rules.append(Rule(D, A, gt))
    rules.append(Rule(D, C, ne))
    rules.append(Rule(E, C, ne))
    rules.append(Rule(E, D, lt_minus_1))
    rules.append(Rule(E, B, ne_minus_2))
    rules.append(Rule(A, F, ne))
    rules.append(Rule(B, F, ne))
    rules.append(Rule(C, F, ne))
    rules.append(Rule(D, F, ne))
    rules.append(Rule(E, F, abs_diff_odd))

    num = A.iterate("")

    print "This node selection results in {} leaf nodes".format(num)

Solve()
