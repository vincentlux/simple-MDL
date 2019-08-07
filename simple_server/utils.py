import subprocess
import datetime
def delete_core(corename):
    subprocess.run(["bash", "delete_core.sh", str(corename)])
    print(f'successfully deleted {corename}')
    return 'succeed'

def add_quote(inp):
    try:
        return int(inp)
    except:
        return "'" + inp + "'"

def is_number(x):
    if type(x) == str:
        x = x.replace(',', '')
    try:
        float(x)
    except:
        return False
    return True

def text2int (textnum, numwords={}):
    # https://stackoverflow.com/a/53400669/10394324
    units = [
        'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
        'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
        'sixteen', 'seventeen', 'eighteen', 'nineteen',
    ]
    tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    scales = ['hundred', 'thousand', 'million', 'billion', 'trillion']
    ordinal_words = {'first':1, 'second':2, 'third':3, 'fifth':5, 'eighth':8, 'ninth':9, 'twelfth':12}
    

    if not numwords:
        numwords['and'] = (1, 0)
        for idx, word in enumerate(units): numwords[word] = (1, idx)
        for idx, word in enumerate(tens): numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)

    textnum = textnum.replace('-', ' ')

    current = result = 0
    curstring = ''
    onnumber = False
    lastunit = False
    lastscale = False

    def is_numword(x):
        if is_number(x):
            return True
        if word in numwords:
            return True
        return False

    def from_numword(x):
        if is_number(x):
            scale = 0
            increment = int(x.replace(',', ''))
            return scale, increment
        return numwords[x]

    for word in textnum.split():
        if word in ordinal_words:
            scale, increment = (1, ordinal_words[word])
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0
            onnumber = True
            lastunit = False
            lastscale = False
        else:
            # for ending, replacement in ordinal_endings:
            #     if word.endswith(ending) and word[0].isdigit():
            #         word = "%s%s" % (word[:-len(ending)], replacement)

            if (not is_numword(word)) or (word == 'and' and not lastscale):
                if onnumber:
                    # Flush the current number we are building
                    curstring += repr(result + current) + " "
                curstring += word + " "
                result = current = 0
                onnumber = False
                lastunit = False
                lastscale = False
            else:
                scale, increment = from_numword(word)
                onnumber = True

                if lastunit and (word not in scales):                                                                                                                                                                                                                                         
                    # Assume this is part of a string of individual numbers to                                                                                                                                                                                                                
                    # be flushed, such as a zipcode "one two three four five"                                                                                                                                                                                                                 
                    curstring += repr(result + current)                                                                                                                                                                                                                                       
                    result = current = 0                                                                                                                                                                                                                                                      

                if scale > 1:                                                                                                                                                                                                                                                                 
                    current = max(1, current)                                                                                                                                                                                                                                                 

                current = current * scale + increment                                                                                                                                                                                                                                         
                if scale > 100:                                                                                                                                                                                                                                                               
                    result += current                                                                                                                                                                                                                                                         
                    current = 0                                                                                                                                                                                                                                                               

                lastscale = False                                                                                                                                                                                                              
                lastunit = False                                                                                                                                                
                if word in scales:                                                                                                                                                                                                             
                    lastscale = True                                                                                                                                                                                                         
                elif word in units:                                                                                                                                                                                                             
                    lastunit = True

    if onnumber:
        curstring += repr(result + current)

    return curstring


def month2int(date_time_str):

    if not date_time_str.startswith('date'):
        return date_time_str, False


    # 1. remove potential date endings
    ordinal_endings = [('st', ''), ('nd', ''), ('rd', ''), ('th', '')]

    date_time_list = date_time_str.split()
    for i in range(len(date_time_list)):
        for ending, replacement in ordinal_endings:
            if date_time_list[i].endswith(ending) and date_time_list[i][0].isdigit():
                date_time_list[i] = "%s%s" % (date_time_list[i][:-len(ending)], replacement)
    
    date_time_str = ' '.join(date_time_list)
    print(date_time_str)
    
    if date_time_str.startswith('date from'):
        # date range
        # split into two strings in order to parse time
        try:
            time_a, time_b = date_time_str.split(' to ')
            time_a_obj = datetime.datetime.strptime(time_a, 'date from %B %d %Y')
            time_a = time_a_obj.date().strftime('%m-%d-%Y')
            time_b_obj = datetime.datetime.strptime(time_b, '%B %d %Y')
            time_b = time_b_obj.date().strftime('%m-%d-%Y')
            print(time_a)
            print(time_b)
            return 'date from ' + time_a + ' to ' + time_b, True
        except Exception as e:
            print(e)

    else:
        # only one date
        try:
            time_obj = datetime.datetime.strptime(date_time_str, 'date %B %d %Y')
            time = time_obj.date().strftime('%m-%d-%Y')
            print(time)
            return 'date ' + time, True
        except Exception as e:
            print(e)