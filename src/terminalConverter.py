terminalDictionary = [
                    ["if", "'IF'"],
                    ["else", "'ELSE'"],
                    ["switch", "'SWITCH'"],
                    ["case", "'CASE'"],
                    ["for", "'FOR'"],
                    ["while", "'WHILE'"],
                    ["const", "'CONST'"],
                    ["var", "'VAR'"],
                    ["let", "'LET'"],
                    ["break", "'BREAK'"],
                    ["continue", "'CONTINUE'"],
                    ["throw", "'THROW'"],
                    ["finally", "'FINALLY'"],
                    ["true", "'BOOL_TRUE'"],
                    ["false", "'BOOL_FALSE'"],
                    ["(", "'PAREN_OPEN'"],
                    [")", "'PAREN_CLOSE'"],
                    ["[", "'BRACKET_OPEN'"],
                    ["]", "'BRACKET_CLOSE'"],
                    ["{", "'CURLY_BRACKET_OPEN'"],
                    ["}", "'CURLY_BRACKET_CLOSE'"],
                    ["+", "'PLUS_OP'"],
                    ["-", "'MINUS_OP'"],
                    ["*", "'MULTIPLY_OP'"],
                    ["/", "'DIVIDE_OP'"],
                    ["**", "'EXPONENT_OP'"],
                    ["%", "'MODULO_OP'"],
                    ["++", "'INCREMENT_OP'"],
                    ["--", "'DECREMENT_OP'"],
                    ["~", "'NEGATE_OP'"],
                    ["<<", "'SHIFTLEFT_OP'"],
                    [">>", "'SHIFTRIGHT_OP'"],
                    [">>>", "'U_SHIFTRIGHT_OP'"],
                    ["^", "'XOR_OP'"],
                    ["&", "'AND_OP'"],
                    ["|", "'OR_OP'"],
                    ["&&", "'AND_LOP'"],
                    ["||", "'OR_LOP'"],
                    ["!", "'NOT_LOP'"],
                    ["==", "'EQUAL_TO'"],
                    ["===", "'VALUETYPE_EQUAL_TO'"],
                    ["!=", "'NOT_EQUAL_TO'"],
                    ["!==", "'VALUETYPE_NOT_EQUAL_TO'"],
                    [">=", "'GREATER_EQUAL'"],
                    [">", "'GREATER'"],
                    ["<=", "'LESSER_EQUAL'"],
                    ["<", "'LESSER'"],
                    ["=", "'ASSIGNMENT'"],
                    ["+=", "'PLUS_ASSIGNMENT'"],
                    ["-=", "'MINUS_ASSIGNMENT'"],
                    ["*=", "'MULTIPLY_ASSIGNMENT'"],
                    ["/=", "'DIVIDE_ASSIGNMENT'"],
                    ["%=", "'MODULO_ASSIGNMENT'"],
                    ["**=", "'EXPONENT_ASSIGNMENT'"]
                    ]

def getTerminal(input):
    global terminalDictionary

    for rule in terminalDictionary:
        if (input == rule[0]):
            return rule[1]

    return "'OBJECT'"

def convertToTerminal(inputLine):
    startingTerminal = ["{", "}", "[", "]", "(", ")", "+", "-", "*", "%", "~", "<", ">", "^", "&", "|", "!", "="]
    uncomplete = ["+", "-", "*", "**", "/", "%", "<", ">", ">>", "&", "|", "=", "==", "!", "!="]
    complement = ["+", "-", "*", "<", ">", "&", "|", "="]
    terminal = []
    tempWord = ""

    for i in range (len(inputLine)):
        if (inputLine[i] == " "):
            if (tempWord != ""):
                terminal.append(getTerminal(tempWord))
            tempWord = ""
        elif ((tempWord not in uncomplete) and (inputLine[i] in uncomplete)):
            if (tempWord != ""):
                terminal.append(getTerminal(tempWord))
            tempWord = inputLine[i]
        elif (tempWord in uncomplete and inputLine[i] in complement):
            tempWord += inputLine[i]
            if (tempWord not in uncomplete):
                terminal.append(getTerminal(tempWord))
                tempWord = ""
        elif (tempWord in startingTerminal):
            if (tempWord not in uncomplete or inputLine[i] not in startingTerminal):
                terminal.append(getTerminal(tempWord))
                tempWord = inputLine[i]
            else:
                tempWord += inputLine[i]
        elif (inputLine[i] in startingTerminal and (tempWord not in uncomplete)):
            if (tempWord != ""):
                terminal.append(getTerminal(tempWord))
            tempWord = inputLine[i]
        else:
            tempWord += inputLine[i]

    if (tempWord != ""):
        terminal.append(getTerminal(tempWord))

    return terminal

# Untuk Coba
# print(convertToTerminal(r"if (x>= 10 && (y+10 == 15)) {"))