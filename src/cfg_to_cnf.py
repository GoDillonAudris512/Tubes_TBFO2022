     
"""
CNF
Start symbol generating ε. For example, A → ε.
A non-terminal generating two non-terminals. For example, S → AB.
A non-terminal generating a terminal. For example, S → a.
"""

# def get_key(val):
#     global CFG
#     keys = [k for k, v in CFG.items() if (val == v[0] and len(v) == 1)]
#     if keys:
#         return keys[0]
#     return None

# CFG = {"A" : [1]}
# print(get_key(1))

def generate_var(start_char = 'A', mod = 10):
    global count_var 
    var = chr(ord(start_char) + int(count_var/mod)) + str(count_var%mod)
    count_var += 1
    return var

# def assign(rule):
#     var = find_term_var(rule)
#     if var is None:
#         assign_to_new_var(rule)
#     else :
        

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
    # print(long_prod_list)
    for (k, v, i) in long_prod_list:
        l_rule = v[i].split()
        v[i] = arr_to_string(convert_long(l_rule))
        # for i in range (len(temp)):
        #     l_rule = temp[i].split()
        #     if len(l_rule) >= 2:
        #         temp[i] = arr_to_string(convert_long(l_rule))
        #     else:
        #         continue
        CFG[k] = v
    

def convert_long(list):
    global CFG
    if len(list) == 2:
        return list
    elif len(list) == 3:
        temp = list[:]
        var = assign_to_new_var(arr_to_string(list[1:3]))
        temp[1:3] = [var]
        return temp
    else :
        temp = list[:]
        var_used = []
        i = 0
        while (i < len(temp) - (len(temp) % 2)):
            rule_subs = temp[i:i+2]
            str_rule_subs = arr_to_string(rule_subs)
            var = assign_to_new_var(str_rule_subs)           
            var_used.append(var)
            i += 2
        if (len(temp) % 2 == 1) : 
            var_used.append(temp[len(temp) - 1])            
        return convert_long(var_used)
        
def arr_to_string(arr):
    result = ""
    for i in range (len(arr) - 1):
        result += arr[i] + ' '
    for i in range (len(arr) - 1, len(arr)):
        result += arr[i]
    return result

def find_unit_prod():
    global CFG
    result = []
    for (k, v) in CFG.items():
        temp = []
        # print("b",k, temp, len(temp))
        for i in range (len(v)):
            # print(len(temp))
            # try : 
            l_rule = v[i].split()
            # except:
            #     print("a",k, temp)
            if (len(l_rule) == 1 and not is_terminal(l_rule[0])):
                l_prod = CFG[f"{l_rule[0]}"]
                for prod in l_prod:
                    temp.append(prod)
            else :
                temp.append(v[i])
                # var  = l_rule[0]
                # temp.remove(var)
                # try :
                #     temp.append(prod for prod in CFG[f"{var}"])
                #     subs = []
                #     temp[i] = arr_to_string(l_rule)
                # except:
                #     print("DEBUG")
                #     print(l_rule)
                #     break
                #     # print("DEBUG")
                #     # CFG[f"{l_rule[0]}"]
                    # print(l_rule[0])    
        result.append([k, temp])
    return result
def remove_unit_prod():
    global CFG
    unit_prod_list = find_unit_prod()
    for (k, prod) in unit_prod_list:
        CFG[k] = prod
        
def load(path = r"src/cfg.txt"):
    """
    membaca file grammar dan memasukkan ke dictionary
    """
    f = open(path, "r")

    for line in f.readlines():
        # Memisahkan LHS dan RHS
        line = line.strip().split('->') 
        LHS = line[0].strip()
        RHS = line[1:][0].split('|')

        for expression in RHS:
            insert(LHS, expression.lstrip().rstrip())

def find_term_var(val):
    """
    mencari variable yang berkoresponden dengan terminal
    """
    global CFG
    keys = [k for k, v in CFG.items() if (val in v)]
    if len(keys) != 0:
        return keys[0]
    else :
        return None

def find_unassinged_terminal():
    """
    mencari terminal yang belum di assign ke suatu variable
    """
    global CFG
    result = []
    for (k, v) in CFG.items():
        for rule in v:
            components = rule.split()
            for component in components:
                if is_terminal(component):
                    var = find_term_var(component)
                    if var is None:
                        result.append(component)
                    else: 
                        continue
                else: 
                    continue
def assign_unassigned_terminal():
    """
    Menambahkan variable menuju terminal jika belum ada variable yang menuju terminal
    """
    unassigned_terminal = find_unassinged_terminal()
    if unassigned_terminal is not None :
        for terminal in unassigned_terminal:
            assign_to_new_var(terminal)
    else :
        return

CFG = {}
count_var = 0
if __name__ == "__main__":
    load()
    # assign_unassigned_terminal()
    convert_long_prod()
    remove_unit_prod()
    for (k, v) in CFG.items():
        print(k, " : ", v)
    # subs_unit_prod()

    # for (k, v) in CFG.items():
    #     for rule in v:
    #         components = rule.split()
    #         for component in components:
    #             if is_terminal(component):
    #                 var = find_term_var(component)
    #                 if var is None:
    #                     assign_to_new_var(component)
    #                 else: 
    #                     continue
    #             else: 
    #                 continue
            

# def load(path = r"src/cfg.txt"):
#     global dict_list
#     f = open(path, "r")

#     for line in f.readlines():
#         line = line.strip().split('->')
#         LHS = line[0].strip()
#         RHS = line[1:][0].split('|')

#         for expression in RHS:
#             rules = expression.split()
#             rules = [rule.strip() for rule in rules]
#             list_of_var_used = []
#             for rule in rules: 
#                 if is_terminal(rule):
#                     var = term_to_var(rule)
#                     list_of_var_used.append(var)
#                 else :
#                     list_of_var_used.append(rule)
#             temp = arr_to_string(convert_long(list_of_var_used))
#             if LHS in CFG:
#                 CFG[f"{LHS}"].append(temp)
#             else :
#                 CFG[f"{LHS}"] = [temp]
                
            # if (len(rules) == 1 and is_terminal(rules[0])):
            #     # print(0, rules[0])
            #     key = get_key(rules[0])
            #     if key is None:
            #         if LHS in CFG:
            #             CFG[f"{LHS}"].append(rules[0])
            #         else :
            #             CFG[f"{LHS}"] = [rules[0]]
            #     else :
            #         if LHS in CFG:
            #             CFG[f"{LHS}"].append(key)
            #         else :
            #             CFG[f"{LHS}"] = [key]
            # else :
            #     list_of_var_used = []
            #     for rule in rules:
            #         if is_terminal(rule):
            #             var = term_to_var(rule)
            #             list_of_var_used.append(var)
            #         else : 
            #             list_of_var_used.append(rule)
            #     temp = arr_to_string(convert_long(list_of_var_used))
            #     if LHS in CFG:
            #         CFG[f"{LHS}"].append(temp)
            #     else :
            #         CFG[f"{LHS}"] = [temp]
    # subs_unit_prod()

    # p()
    # subs_unit_prod()
    # assign_terminal()
    # for (k, v) in CFG.items():
    #     print(f"{k} : {v}")
    # print(len(CFG))
    # print(find_rhs("'COMMA'"))




