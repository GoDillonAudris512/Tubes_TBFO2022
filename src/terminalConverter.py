terminalDictionary = [
                    ["if", "'IF'"],
                    ["else", "'ELSE'"],
                    ["switch", "'SWITCH'"],
                    ["case", "'CASE'"],
                    ["default", "'DEFAULT'"],
                    ["for", "'FOR'"],
                    ["while", "'WHILE'"],
                    ["const", "'CONST'"],
                    ["var", "'VAR'"],
                    ["let", "'LET'"],
                    ["break", "'BREAK'"],
                    ["continue", "'CONTINUE'"],
                    ["function", "'FUNCTION'"],
                    ["return", "'RETURN'"],
                    ["try", "'TRY'"],
                    ["catch", "'CATCH'"],
                    ["throw", "'THROW'"],
                    ["finally", "'FINALLY'"],
                    ["true", "'TRUE'"],
                    ["false", "'FALSE'"],
                    ["null", "'NULL'"],
                    ["(", "'PAREN_OPEN'"],
                    [")", "'PAREN_CLOSE'"],
                    ["[", "'BRACKET_OPEN'"],
                    ["]", "'BRACKET_CLOSE'"],
                    ["{", "'CURFEW_OPEN'"],
                    ["}", "'CURFEW_CLOSE'"],
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
                    ["**=", "'EXPONENT_ASSIGNMENT'"],
                    ["&=", "'AND_ASSIGNMENT'"],
                    ["|=", "'OR_ASSIGNMENT'"],
                    ["^=", "'XOR_ASSIGNMENT'"],
                    ["&&=", "'AND_LOP_ASSIGNMENT'"],
                    ["||=", "'OR_LOP_ASSIGNMENT'"],
                    ["?", "'TERNARY'"],
                    ["??", "'NULLISH'"],
                    ["??=", "'NULLISH_ASSIGNMENT'"],
                    [".", "'DOT'"],
                    [",", "'COMMA'"],
                    ["//", "'DOUBLE_SLASH'"],
                    ["/*", "'OPEN_SLASH'"],
                    ["*/", "'CLOSE_SLASH'"],
                    [":", "'COLON'"],
                    [";", "'SEMICOLON'"]
                    ]

def getTerminal(input):
    global terminalDictionary

    for rule in terminalDictionary:
        if (input == rule[0]):
            return rule[1]

    try:
        temp = int(input)
        return "'NUM'"
    except:
        return "'OBJECT'"

def convertToTerminal(inputLine):
    startingTerminal = ["{", "}", "[", "]", "(", ")", "+", "-", "*", "%", "~", "<", ">", "^", "&", "|", "!", "=", ".", ",", ":", ";", "?"]
    uncomplete = ["+", "-", "*", "**", "/", "%", "<", ">", ">>", "&", "|", "=", "==", "!", "!=", "^", "&&", "||", "?", "??"]
    complement = ["+", "-", "*", "<", ">", "&", "|", "=", "/", "?"]
    terminal = []
    varName = []
    tempWord = ""
    ignoreVar = False

    for i in range (len(inputLine)):
        if (terminal != [] and terminal[len(terminal) - 1] == "'DOUBLE_SLASH'"):
            ignoreVar = True
            break
        if (terminal != [] and terminal[len(terminal) - 1] == "'OPEN_SLASH'"):
            ignoreVar = True
        if (terminal != [] and terminal[len(terminal) - 1] == "'CLOSE_SLASH'"):
            ignoreVar = False
        if (inputLine[i] == " "):
            if (tempWord != ""):
                terminal.append(getTerminal(tempWord))
                if (terminal[len(terminal) - 1] == "'OBJECT'"  and not ignoreVar):
                    varName.append(tempWord)
            tempWord = ""
        elif ((tempWord not in uncomplete) and (inputLine[i] in uncomplete)):
            if (tempWord != ""):
                terminal.append(getTerminal(tempWord))
                if (terminal[len(terminal) - 1] == "'OBJECT'"  and not ignoreVar):
                    varName.append(tempWord)
            tempWord = inputLine[i]
        elif (tempWord in uncomplete and inputLine[i] in complement):
            tempWord += inputLine[i]
            if (tempWord not in uncomplete):
                terminal.append(getTerminal(tempWord))
                if (terminal[len(terminal) - 1] == "'OBJECT'"  and not ignoreVar):
                    varName.append(tempWord)
                tempWord = ""
        elif (tempWord in startingTerminal):
            if (tempWord not in uncomplete or inputLine[i] not in startingTerminal):
                terminal.append(getTerminal(tempWord))
                if (terminal[len(terminal) - 1] == "'OBJECT'"  and not ignoreVar):
                    varName.append(tempWord)
                tempWord = inputLine[i]
            else:
                tempWord += inputLine[i]
        elif (inputLine[i] in startingTerminal and (tempWord not in uncomplete and tempWord != "")):
            terminal.append(getTerminal(tempWord))
            if (terminal[len(terminal) - 1] == "'OBJECT'"  and not ignoreVar):
                varName.append(tempWord)
            tempWord = inputLine[i]
        else:
            tempWord += inputLine[i]

    if (tempWord != ""):
        terminal.append(getTerminal(tempWord))
        if (terminal[len(terminal) - 1] == "'OBJECT'"  and not ignoreVar):
            varName.append(tempWord)

    return terminal, varName

# Untuk Coba
# print(convertToTerminal(r"if (x>= 10 && (y+10 ?? 15)) { // ini komen"))