     
"""
CNF
Start symbol generating ε. For example, A → ε.
A non-terminal generating two non-terminals. For example, S → AB.
A non-terminal generating a terminal. For example, S → a.
"""

def find_var_to_terminal(terminal, ex = None):
    global CFG
    keys = [k for k, v in CFG.items() if (terminal in v and k != ex)]
    if keys:
        return keys[0]
    return None


def generate_var(start_char = 'A', mod = 10):
    global count_var 
    var = chr(ord(start_char) + int(count_var/mod)) + str(count_var%mod)
    count_var += 1
    return var

def assign_to_new_var(rule):
    global CFG
    var = generate_var()
    CFG[f"{var}"] = [rule]
    return var

def insert(key, val):
    global CFG
    if key in CFG:
       CFG[f"{key}"].append(val)
    else :
        CFG[f"{key}"] = [val]

def is_terminal(string):
    return string[0] == "'"

def find_long_prod():
    global CFG
    result = []
    for (k, v) in CFG.items():
        for i in range (len(v)):
            l_rule = v[i].split()
            if len(l_rule) >= 2:
                result.append([k,v,i])
            else:
                continue
    return result

def convert_long_prod():
    global CFG
    long_prod_list = find_long_prod()
    for (k, v, i) in long_prod_list:
        l_rule = v[i].split()
        v[i] = arr_to_string(convert_long(l_rule))
        CFG[k] = v
    

def convert_long(list):
    global CFG
    if len(list) == 2:
        return list
    elif len(list) == 3:
        temp = list[:]
        key = find_var_to_terminal(arr_to_string(list[1:3]))
        if key is None:
            var = assign_to_new_var(arr_to_string(list[1:3]))
        else :
            var = key
        temp[1:3] = [var]
        return temp
    else :
        temp = list[:]
        var_used = []
        i = 0
        while (i < len(temp) - (len(temp) % 2)):
            rule_subs = temp[i:i+2]
            str_rule_subs = arr_to_string(rule_subs)
            key = find_var_to_terminal(str_rule_subs)
            if key is None:
                var = assign_to_new_var(str_rule_subs)           
                var_used.append(var)
            else:
                var_used.append(key)
            i += 2
        if (len(temp) % 2 == 1) : 
            var_used.append(temp[len(temp) - 1])            
        return convert_long(var_used)

def remove_unreached_var():
    global CFG
    list_unreached_var = []
    for key in CFG:
        if find_var_to_terminal(str(key)) == None:
            list_unreached_var.append(key)

def arr_to_string(arr):
    result = ""
    for i in range (len(arr) - 1):
        result += arr[i] + ' '
    for i in range (len(arr) - 1, len(arr)):
        result += arr[i]
    return result

def remove_unit_prod():
    global CFG
    temp = {}
    for k in CFG:
        temp[k] = []
    
    for (k, v) in CFG.items():
        for rule in v:
            l_rule = rule.split()
            if (len(l_rule) == 1 and not is_terminal(l_rule[0])):
                l_prod = CFG[l_rule[0]]
                for prod in l_prod:
                    if prod == 'E5':
                        print(l_rule[0])
                    temp[k].append(prod)
                continue
            else:   
                temp[k].append(rule)
    # print(temp)
        # unit_prod_list.append([k, temp_val])
        # return
        # temp_val = [] 
    # for (k, prod) in unit_prod_list:
    #     CFG[k] = prod
        
def load(path = r"src/cfg.txt"):
    """
    membaca file grammar dan memasukkan ke dictionary
    """
    f = open(path, "r")

    for line in f.readlines():
        line = line.strip().split('->') 
        LHS = line[0].strip()
        RHS = line[1:][0].split('|')

        for expression in RHS:
            insert(LHS, expression.lstrip().rstrip())

def assign_unassinged_terminal():
    """
    mencari terminal yang belum di assign ke suatu variable
    """
    global CFG 
    terminal_assigned = []
    var_to_assign = []
    for (key, value) in CFG.items():
        temp = value[:]
        changed = False
        for k in range (len(temp)):
            rule = temp[k]
            components = rule.split()
            for i in range (len(components)):
                component = components[i]
                if is_terminal(component):
                    var = find_var_to_terminal(component, ex = key)
                    if var is not None and var == key:
                        continue
                    elif var is None and component not in terminal_assigned:
                        new_var = generate_var()
                        terminal_assigned.append(component)
                        var_to_assign.append([new_var, [component]])
                        components[i] = new_var
                    elif var is None and component in terminal_assigned:
                        idx = var_to_assign[:][1].index(component)
                        components[i] = var_to_assign[idx][1]
                    else :
                        components[i] = var
                    changed = True
                else: 
                    continue
            temp[k] = arr_to_string(components)
        if changed : var_to_assign.append([key, temp])

    for k, v in var_to_assign:
        CFG[k] = v

CFG = {}
count_var = 0
if __name__ == "__main__":
    load()
    assign_unassinged_terminal()
    convert_long_prod()
    remove_unit_prod()
    remove_unreached_var()
    # print(find_var_to_terminal('IF_METHOD'))
    # for (k, v) in CFG.items():
    #     print(k, " : ", v)

 




