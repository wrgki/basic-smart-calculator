from collections import deque
var_dict = {}
operators = "+-*/^"


def commands(command):
    if command.startswith("/"):
        if command == "/exit":
            return True
        elif command == "/help":
            print("""This is a program that adds, 
                subtracts, multiplies, divides, 
                expotentiate. It supports variables 
                and parentheses. Use /postfix to 
                transform an expression 
                into postfix notation.""")
            return None
        elif command == "/postfix":
            print("Provide an expression:")
            print(" ".join(postfix(input())))
            return None
        else:
            print("Unknown command")
            return None
    else:
        return False


def process_input(inpt):
    myoperators = deque()
    myvars = deque()
    digits = deque()
    result = deque()
    for achar in inpt:
        if achar == " ":
            continue
        if achar.isalpha():
            if myvars:
                print("Invalid expression")
                break
            myvars.append(achar)
            if myoperators:
                result.append("".join(myoperators))
                myoperators = deque()
            result.append(achar)
        if achar.isdecimal():
            if myvars:
                print("Invalid expression")
                break
            digits.append(achar)
            if myoperators:
                result.append("".join(myoperators))
                myoperators = deque()
        if achar in "*/^":
            if myoperators:
                print("Invalid expression")
                break
        if achar in "+-*/^":
            myoperators.append(achar)
        if achar in "+-*/^()":
            if digits:
                result.append("".join(digits))
                digits = deque()
            if myvars:
                myvars = deque()
        if achar in "()":
            if myoperators:
                result.append("".join(myoperators))
                myoperators = deque()
            result.append(achar)
        if result.count("(") < result.count(")"):
            print("Invalid expression")
            break
    if digits:
        result.append("".join(digits))
    for m in range(len(result)):
        if "+" in result[m] or "-" in result[m]:
            if result[m].count("-") % 2 == 0:
                result[m] = "+"
            else:
                result[m] = "-"
    return result


def postfix(inpt):
    result = deque()
    exp = deque()
    for oper in inpt:
        if oper.isdecimal() or oper.isalpha():
            result.append(oper)
        if oper in operators:
            if len(exp) == 0 or exp[0] == "(" or operators.index(oper)//2 > operators.index(exp[0])//2:
                exp.appendleft(oper)
            elif operators.index(oper)//2 <= operators.index(exp[0])//2:
                while len(exp) > 0 and exp[0] != "(" and operators.index(oper)//2 <= operators.index(exp[0])//2:
                    result.append(exp.popleft())
                else:
                    exp.appendleft(oper)
        if oper == "(":
            exp.appendleft(oper)
        if oper == ")":
            while exp[0] != "(":
                result.append(exp.popleft())
            else:
                exp.popleft()
    for _n in range(len(exp)):
        result.append(exp.popleft())
    return result


def valid_var(avar):
    if avar in var_dict.keys():
        return int(var_dict[avar])
    else:
        print("Unknown variable")


def variables_assign(inpt):
    inpt_splt = inpt.split("=")
    if len(inpt_splt) == 2:
        avar = inpt_splt[0].strip(" ")
        aval = inpt_splt[1].strip(" ")
        if avar.isalpha():
            if aval.isalpha():
                var_dict[avar] = valid_var(aval)
            elif aval.isdecimal():
                var_dict[avar] = aval
            else:
                print("Invalid assignment")
        else:
            print("Invalid identifier")
    else:
        print("Invalid assignment")


def validate_check(inpt):
    if inpt.count("(") != inpt.count(")"):
        print("Invalid expression")
        return True
    if inpt == '':
        return True
    if inpt.isalpha():
        return False
    if "=" in inpt:
        variables_assign(inpt)
        return True


def calculate(input_string):
    output_deque = deque()
    adeque = postfix(process_input(input_string))
    for elem in adeque:
        if elem.isdecimal():
            output_deque.append(elem)
        if elem.isalpha():
            output_deque.append(valid_var(elem))
        if elem in "+-*/^":
            b = int(output_deque.pop())
            a = int(output_deque.pop())
            if elem == "+":
                output_deque.append(a + b)
            if elem == "-":
                output_deque.append(a - b)
            if elem == "*":
                output_deque.append(a * b)
            if elem == "/":
                output_deque.append(a / b)
            if elem == "^":
                output_deque.append(a ** b)
    return output_deque[0]


while True:
    output = 0
    x = input()
    if commands(x):
        break
    elif commands(x) is None:
        continue
    elif validate_check(x):
        continue
    else:
        print(calculate(x))
print("Bye!")
