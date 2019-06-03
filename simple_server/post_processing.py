# aim to get an input string such as `on soccer` and output as
# a mdl query e.g. `?ON "soccer"`
from utils import add_quote, text2int

keywords = ['LAST','ON','TOTAL','EMAIL','MSWORD','PDF','GIF']
lower_keywords = ['all','day','year','month','subject','full']

def str_to_mdl(inp):
    # convert `one number` to `1 number`
    inp = text2int(inp)
    # strip leading and ending spaces
    inp = inp.upper().strip()
    # convert to list
    inp_list = inp.split(' ')
    # add quote other then keyword
    for i in range(len(inp_list)):
        if inp_list[i] not in keywords:
            inp_list[i] = inp_list[i].lower()
            if inp_list[i] not in lower_keywords:
                inp_list[i] = add_quote(inp_list[i])
            else:
                pass
        else:
            pass
    
    # list to str
    outp = " ".join(str(x) for x in inp_list)
    return '?' + outp

# if __name__ == '__main__':
#     print(str_to_mdl("Mike ON picnic LAST"))
