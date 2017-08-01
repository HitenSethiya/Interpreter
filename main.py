import operator
cond_operators = {'<=':operator.le,
                  '<':operator.lt,
                  '==':operator.eq,
                  '>=':operator.ge,
                  '>':operator.gt,
                  '!=':operator.ne}
operators = {'*': operator.mul,
             '/': operator.truediv,
             '+': operator.add,
             '-': operator.sub,
             '%': operator.mod,
             }
dictionary = {}

class CompoundStatement:
    def __init__(self):
        self.statements = []
        self.while_substate= []
        self.i = 0
    def eval(self):
        state_iter = iter(self.statements)
        for statement in state_iter:
            self.z = Statement()
            self.z.code = statement.strip(" ") # removed spaces after and before our code

            if (self.i==0 and self.z.code[0:3]=="else"):
                self.i=1

            else:

                self.i = self.z.eval  # i=0 means safe to execute ahead; i=1 means if condition false; i=2 means while executes

            if self.i==1: # i is returned 1 if the consequent lines need not evaluated
                count = 1
                for state in state_iter:
                    if state[0:2]=="if ":
                        count+=1
                    if state[0:2]=="fi":
                        count-=1
                    if count==1 and state[0:3]=="else":
                        self.i=0
                        break
                    if count==0:
                        self.i=0
                        break
            if self.i==2: # in case of while condition satisfies
                self.while_substate.append(self.z.code)
                for state in state_iter:
                    if state[0:4]=="done":
                        break
                    self.while_substate.append(state)
                While =CompoundStatement()
                While.statements = self.while_substate
                While.eval()
            if self.i==3: # i is returned 3 if the consequent lines need not evaluated

                count = 1
                for state in state_iter:
                    if state[0:4]=="while":
                        count+=1
                    if state[0:3]=="done":
                        count-=1
                    if count==0:
                        self.i=0
                        break

class Statement:
    def __init__(self):
        self.code = ""
    @property
    def eval(self):

        self.code = self.code.strip()

        if self.code[0:3] == "if ": #check for conditional if

            self.t=ConditionalStatement()
            self.t.code = self.code
            self.t.condition = self.code [4:len(self.code)-1]
            for cond_oper in cond_operators:
                if str(cond_oper) in self.t.condition:
                    self.t.operator = cond_oper  # re.match return string which matched so this is set
                if self.t.operator is not None:
                    break
            self.t.expressions = self.t.condition.split(self.t.operator)
            self.t.eval()
            if self.t.eval() == 1: # 1 means false
                return 1
            else:
                return 0
        elif ':=' in self.code:
            self.t = AssignmentStatement()
            self.t.code = self.code
            self.t.variable,self.t.expression = self.code.split(':=')
            self.t.eval()
            return 0
        elif 'while ' in self.code:
            self.t = ConditionalStatement()
            self.t.code = self.code
            self.t.condition = self.code[5:len(self.code)]

            for cond_oper in cond_operators:
                if str(cond_oper) in self.t.condition:
                    self.t.operator = cond_oper  # re.match return string which matched so this is set
                if self.t.operator is not None:
                    break

            self.t.expressions = self.t.condition.split(self.t.operator)
            self.t.eval()
            if self.t.eval() == 1:  # 1 means false
                return 3
            else:
                return 2
        elif "println " in self.code:
            print ('\n')
            return 0
        return 0




class AssignmentStatement(Statement):
    def __init__(self):
        super(AssignmentStatement, self).__init__()
        self.variable,self.expression = None,None
    def eval(self):
        self.e = Expression()
        self.e.code = self.expression

        d = self.e.eval()
        dictionary[self.variable.strip()] = d


class ConditionalStatement(Statement):
    def __init__(self):
        super(ConditionalStatement, self).__init__()
        self.condition = ""
        self.operator = None
        self.expressions=["",""]
    def eval(self):

        self.e1 = Expression()
        self.e2 = Expression()
        self.e1.code = self.expressions[0]
        self.e2.code = self.expressions[1]

        m = self.e1.eval()
        n = self.e2.eval()

        if cond_operators[self.operator](m,n)==True:
            return 0
        else:

            return 1

class Expression: #handles expressions and their evaluations
    def __init__(self):
        self.code = ""
        self.l1 = ""
        self.l2 = ""
    def eval(self):
        print(dictionary)
        print(self.code)
        self.code = self.code.strip(" ")

        for operation in operators:# probably will turn in a mistake
            if operation in self.code:
                self.l1 = Expression()
                self.l2 = Expression()
                self.l1.code,self.l2.code = self.code.split(operation)
                return operators[operation](self.l1.eval(),self.l2.eval())
            else:
                print ("no op found")
        if self.code.isalpha():
            return dictionary[self.code]
        elif self.code.isnumeric:
            return float(self.code)


# have to read file and pass the whole string to compound statement to classify
code_compound = CompoundStatement()
with open("code.txt","r") as file_code:
    code_compound.statements = file_code.readlines()
code_compound.statements = [x.strip() for x in code_compound.statements]
code_compound.statements = [x.strip(';') for x in code_compound.statements]
code_compound.eval()
print (dictionary)
