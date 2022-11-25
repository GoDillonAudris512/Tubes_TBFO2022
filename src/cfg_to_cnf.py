"""
CNF
Start symbol generating ε. For example, A → ε.
A non-terminal generating two non-terminals. For example, S → AB.
A non-terminal generating a terminal. For example, S → a.
"""

# Global dictionary used for storing the rules.
CFG = {}

def load_grammar_as_list(filename):
    with open(filename) as cfg:
        lines = cfg.readlines()
    return [x.replace("->", "").split() for x in lines]

def is_terminal(rule):
    return rule[0] == "'"

def insert(rule):
    global CFG
    if rule[0] not in CFG:
        CFG[rule[0]] = []
    CFG[rule[0]].append(rule[1:])


def load_grammar_as_cnf(filename, write_to_file = False):
    # Remove all the productions of the type A -> X B C or A -> B a.
    global CFG
    list_grammar = load_grammar_as_list(filename)
    unit_productions, result = [], []
    index = 0

    for rule in list_grammar:
        temp_rules = []
        if len(rule) == 2 and rule[1][0] != "'":
            # Rule is in form A -> X, so back it up for later and continue with the next rule.
            unit_productions.append(rule)
            insert(rule)
            continue
        elif len(rule) > 2:
            # Rule is in form A -> X B C [...] or A -> X a.
            terminals = [(item, i) for i, item in enumerate(rule) if is_terminal(item)]
            if terminals:
                for item in terminals:
                    # Create a new non terminal symbol and replace the terminal symbol with it.
                    # The non terminal symbol derives the replaced terminal symbol.
                    rule[item[1]] = f"{rule[0]}{str(index)}"
                    temp_rules += [f"{rule[0]}{str(index)}", item[0]]
                index += 1
            while len(rule) > 3:
                temp_rules.append([f"{rule[0]}{str(index)}", rule[1], rule[2]])
                rule = [rule[0]] + [f"{rule[0]}{str(index)}"] + rule[3:]
                index += 1
        # Adds the modified or unmodified (in case of A -> x i.e.) rules.
        insert(rule)
        result.append(rule)
        if temp_rules:
            result.extend(temp_rules)
    # Handle the unit productions (A -> X)
    while unit_productions:
        rule = unit_productions.pop()
        if rule[1] in CFG:
            for item in CFG[rule[1]]:
                new_rule = [rule[0]] + item
                if len(new_rule) > 2 or is_terminal(new_rule[1]):
                    result.insert(0, new_rule)
                else:
                    unit_productions.append(new_rule)
                insert(new_rule)
    string = ""
    for (k, v) in CFG.items():
        temp = []
        for rules in v:
            string = " ".join(rules)
            temp.append(string)
        CFG[k] = temp

    if (write_to_file):
        with open('cnf.txt', 'w') as file:
            for element in result:
                if len(element)==3:
                    file.write(f'{element[0]} -> {element[1]} {element[2]}\n')
                elif len(element)==2:
                    file.write(f'{element[0]} -> {element[1]}\n')

    return result

# path = (r"./src/cfg2.txt")
# load_grammar_as_cnf(path, True)
# print(CFG)