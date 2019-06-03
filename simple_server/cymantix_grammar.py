from parsimonious.grammar import Grammar
import re
import six
import parsimonious
import argparse

# sc: scope
# op: opration
grammar = Grammar(
    """
    all             = space op space sc
    sc              = sc_EMAIL_from / sc_EMAIL_attach / sc_EMAIL_piece / space
    sc_EMAIL_piece  = "EMAIL LAST" space op_LAST_piece
    sc_EMAIL_from   = "EMAIL" space op_lit_name
    sc_EMAIL_attach = "EMAIL" space sc_attach
    sc_attach       = "MSWORD" / "PDF" / "GIF"
    sc_sub          = "full" / "subject"
    op              = op_trig space op_first space
    op_first        = op_TOTAL / op_LAST / op_lit_ON / op_lit_name 
    op_lit_ON       = op_lit_name* op_ON space op_lit_topic space sc_sub* space sc_attach* space op_LAST*
    op_lit_topic    = '"' chars '"'
    op_lit_name     = ('"' (chars space)+ '"' space)+
    op_ON           = "ON"
    op_LAST         = "LAST" space (op_LAST_time / op_LAST_piece)
    op_LAST_piece   = ~"[0-9]*" 
    op_LAST_time    = ~"[0-9]*" space ~"[a-z]+"
    op_TOTAL        = "TOTAL"
    op_trig         = "?"
    space           = " "*
    chars           = ~"[A-z0-9 ]*"
    """
)


class EntryParser(parsimonious.NodeVisitor):
    """
    Recognize one command and convert it to json format
    Details:
        GRAMMAR         JSON_KEY                TYPE        NOTES         
        op_lit_topic:   "topic"                 str         
        op_lit_name:    "from"                  str         might contain multiple names
        op_TOTAL:       "total"                 bool        
        op_LAST_time:   "time"                  str         "all" or "month" or "1 month" ...
        op_LAST_piece   "piece"                 str         
        sc_attach       "attachment"            str         
 
    Example use case:
        command = '''?TOTAL '''
        print(EntryParser(grammar,command).entry)
    """
    def __init__(self, grammar, text):
        self.entry = {}
        # self.grammar = parsimonious.Grammar(grammar)
        ast = grammar.parse(text)
        self.visit(ast)
    def visit_op_lit_topic(self, node, vc):
        self.entry['topic'] = node.text

    def visit_op_lit_name(self, node, vc):
        self.entry['from'] = node.text

    def visit_op_TOTAL(self, node, vc):
        self.entry['total'] = True

    def visit_op_LAST_time(self, node, vc):
        self.entry['time'] = node.text

    def visit_op_LAST_piece(self, node, vc):
        if (node.text) == '':
            self.entry['piece'] = '1'
        else:
            self.entry['piece'] = node.text
    
    def visit_sc_attach(self, node, vc):
        self.entry['attachment'] = node.text

    def visit_sc_sub(self, node, vc):
        self.entry['sub'] = node.text

    def generic_visit(self, node, visited_children):
        pass


"""
example command:
?ON 'haha' 
?'Mike' ON 'Soccer' MSWORD LAST
?'mike' 
?'Mike' EMAIL LAST 1
?'Mike' 'Drake' 'Jim'
?LAST
?LAST 1 
?LAST 1 month EMAIL 'Drake'
?LAST EMAIL 'Drake' 'Jim'
?LAST 1 EMAIL 'Drake'
?TOTAL
"""

def c_json(inp):
    # replace single quote to double quote (bc solr only allow double quote for
    # specific string search)
    command = inp.replace("\'", '"')
    return EntryParser(grammar,command).entry


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--command', type=str, default='', help='Test grammar mode. Cymantix command eg. ?LAST all EMAIL from "Mike" ')
    args = parser.parse_args()
    # command = args.command.replace('"', "\'")
    command = args.command.replace("\'", '"')
    try:
        res = EntryParser(grammar,command).entry
        print(res)
        # print(grammar.parse(command))
    except parsimonious.exceptions.IncompleteParseError as e:
        e = re.sub("[\(\[].*?[\)\]]", "", str(e))
        print(e)
    except parsimonious.exceptions.ParseError as e:
        if '?' not in command:
            print("Missing '?' at the start of the query")
        else:
            # remove position indicated
            e = re.sub("[\(\[].*?[\)\]]", "", str(e))
            print(e)


    
