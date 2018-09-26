#!/usr/bin/python3
#Generate a dictionary of options from a command line
#Takes the output of sys.argv[1:] as input

def check_type(option):
    #Checks if option string is key or value
    
    if option.startswith("-"):
        type = "key"
    else:
        type = "value"
    
    return type
    

def get_key_name(option_key):
    #Returns the name of an option by dropping preceding hyphens
    while option_key.startswith("-"):
        option_key = option_key[1:]
    
    return option_key



def get_options(cmd):
    
    options = dict()  
    
    #Check if cmd is given as list (sys.argv output)
    if not type(cmd) is list:
        print("Unexpected argument type (expected 'list').")
        return options
    
    del cmd[0] #drop the command itself from list of options
    
    for index in range(len(cmd)):
        if check_type(cmd[index]) == "key":
            if index + 1 < len(cmd) and check_type(cmd[index+1]) == "value":
                options[get_key_name(cmd[index])] = cmd[index+1]
            else:
                options[get_key_name(cmd[index])] = True
    
    
    
    
    return options


if __name__ == "__main__":
    import sys
    my_options = get_options(sys.argv)
    print(my_options)