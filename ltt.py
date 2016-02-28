import string


class Stack:
    def __init__(self):
        self.stack = []
    def __repr__(self):
        return str(self.stack)
    def push(self, thing):
        self.stack = [thing] + self.stack
    def pop(self):
        thing = self.stack[-1]
        self.stack = self.stack[:len(self.stack)-1]
        return thing


def filter(l):
    nl = []
    for o in l:
        if o not in nl:
            nl = nl + [o]
    return nl

def AND(p,q):
    return p and q

def OR(p,q):
    return p or q

def NOT(p):
    return not p

def THEN(p,q):
    return (not p) or q

def IFF(p,q):
    return THEN(p,q) and THEN(q,p)

def getAtoms(prop):
    return filter([a for a in prop if a in string.ascii_letters])

def getTAs(p):
    n = len(getAtoms(p))
    assigns = []
    for i in range(2**(n-1)):
       assigns = assigns + ["0"*i + "1"*(n-i)]
       assigns = assigns + ["1"*i + "0"*(n-i)]
    return assigns

def makeMathMode(word, piecewise = True):
     if piecewise == True:
         tokens = []
         for token in word:
             if token in string.ascii_letters:
                 tokens = tokens + ["$" + token + "$"]
             elif token == "&":
                 tokens = tokens + ["$\wedge$"]
             elif token == "|":
                 tokens = tokens + ["$\vee$"]
             elif token =="!":
                 tokens = tokens + ["$\\neg$"]
             else:
                 print("Invalid token entered.")
         return tokens
     else:
         tokens = ""
         for token in word:
              if token in string.ascii_letters:
                  tokens = tokens + token
              elif token == "&":
                  tokens = tokens + "\wedge "
              elif token == "|":
                  tokens = tokens + "\\vee "
              elif token =="!":
                  tokens = tokens + "\\neg "
              elif token == "=":
                  tokens = tokens + "\leftrightarrow "
              elif token == ">":
                  tokens = tokens + "\\to "
              else:
                 print("Invalid token entered.")
         return ["$" + tokens + "$"]


def makeStatement(prop, ta):
    atoms = getAtoms(prop)
    newProp = [l for l in prop]
    s = 0
    for a in atoms:
        t = 0
        for l in prop:
            if a == l:

                newProp[t] = ta[s]
            t = t + 1
        s = s + 1
    return ''.join(newProp)

def evalStatement(s):
    s = s[::-1]
    stack = Stack()
    num = [str(i) for i in range(2)]
    for char in s:
        if char == ' ':
            pass
        elif char in num:
            stack.push(char)
        elif char == "&":
            stack.push(AND(int(stack.pop()),int(stack.pop())))
        elif char == "|":
            stack.push(OR(int(stack.pop()),int(stack.pop())))
        elif char =="!":
            stack.push(NOT(int(stack.pop())))
        elif char == "=":
            stack.push(int(IFF(int(stack.pop()),int(stack.pop()))))
        elif char == ">":
            stack.push(int(THEN(int(stack.pop()),int(stack.pop()))))
        else:
            print("Invalid statement entered.")
            break
    return str(stack.pop())

def getTruthVals(prop):
    tas = getTAs(prop)
    statements = [makeStatement(prop, ta) for ta in tas]
    truthVals = []
    t = 0
    for s in statements:
        truthVals = truthVals + [(tas[t], evalStatement(s))]
        t = t + 1
    return truthVals

def buildTable(truthVals, names):
    preamble = "\\begin{table}[h]\n\centering\n\\begin{tabular}" +"{"+"|l"*(len(names))+"|}\n\hline\n"
    header = ''.join(["\t %s \t &"%(n) for n in names])[:-1] + "\\\ \hline\n"
    body = ""
    for row in truthVals:
        for block in row:
            for bit in block:
                body = body + ''.join(["\t T \t &" if bit == "1" else "\t F \t &"])
        body = body[:-1] + "\\\ \hline\n"
    return preamble + header + body + "\end{tabular}\n\end{table}"

def run():
    print("\nThis is the Latex Truth Table Generator built at CruddyLabs late one night.")
    while True:
        print("\nEnter a logical proposition in polish notation to obtain code for \nthe corresponding latex truth table.")
        print("Use '&', '|', and '!' as connectives and '>' for implication, '=' for if and only if.")
        print("Enter 'done' to finish.\n")
        prop = input("ltt >> ")
        if prop == 'done':
            print("Peace, yo.")
            break
        else:
            print("\n" + buildTable(getTruthVals(prop), makeMathMode(''.join(getAtoms(prop))) + makeMathMode(prop, False)))

run()
