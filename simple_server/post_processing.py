# aim to get an input string such as `on soccer` and output as
# a mdl query e.g. `?ON "soccer"`
from utils import add_quote, text2int, month2int

keywords = ['LAST','ON','TOTAL','DATE','FROM','TO','EMAIL','MSWORD','PDF','GIF']
lower_keywords = ['all','day','days','year','years','month','months','subject','full']

def str_to_mdl(inp):
    # convert 'January 2 2019' to 01-02-2019
    # hacking...
    inp, is_date = month2int(inp)
    print(inp)
    # convert `one number` to `1 number`
    if not is_date:
        inp = text2int(inp).strip()
        print(inp)



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
