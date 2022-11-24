     
"""
CNF
Start symbol generating ε. For example, A → ε.
A non-terminal generating two non-terminals. For example, S → AB.
A non-terminal generating a terminal. For example, S → a.
"""


def generate_var(start_char = 'A', mod = 10):
    global count_var 
    var = chr(ord(start_char) + int(count_var/mod)) + str(count_var%mod)
    count_var += 1
    return var

def print_dictionary(dict, indent=0):
   for key, value in dict.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         print_dictionary(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

def is_terminal(string):
    return string[0] == "'" and string[len(string) - 1] == "'"

def convert_long(list):
    global dict_list

    if len(list) == 2 or len(list) == 1:
        return list[:]
    elif len(list) == 3:
        temp = list[:]
        var = generate_var()
        dict_list.append([var] + [list[1:3]])
        temp[1:3] = [var]
        return temp
    else :
        temp = list[:]
        var_used = []
        i = 0
        while (i < len(temp) - (len(temp) % 2)):
            rule_subs = temp[i:i+2]
            try :
                idx = ([i[1] for i in dict_list]).index(rule_subs)
                var_used.append(dict_list[idx][0])
            except:
                var = generate_var()
                var_used.append(var)
                dict_list.append([var] + [rule_subs])
            i += 2
        return convert_long(var_used)
        


def load(path = r"src/cfg.txt"):
    global dict_list
    f = open(path, "r")

    for line in f.readlines():
        line = line.strip().split('->')
        LHS = line[0].strip()
        RHS = line[1:][0].split('|')

        for expression in RHS:
            rules = expression.split()
            # print(rules)
            # terminal

            if (len(rules) == 1 ) and (is_terminal(rules[0])):
                dict_list.append([LHS] + [rules])
            else :
                list_of_var_used = []
                for rule in rules:
                    # print(rule)
                    if is_terminal(rule):
                        try:
                            idx = ([i[1] for i in dict_list]).index(rule)
                            list_of_var_used.append(dict_list[idx][1])
                        except:
                            var = generate_var()
                            dict_list.append([var] + [[rule]])
                            list_of_var_used.append(var)
                    else : 
                        list_of_var_used.append(rule)
                list = convert_long(list_of_var_used)
                dict_list.append([LHS] + [list])

CFG = {}  
dict_list = []
count_var = 0
if __name__ == "__main__":
    from tabulate import tabulate
    load()
    print(tabulate(dict_list))
    print(len(dict_list))




