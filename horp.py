
class HorpError(Exception):
    """Exception for parser errors"""
    def __init__(self, message):
        self.message = message



class Program:
    """Class Program contain program data

    public:
        open()
        get_next_token()
    """
    # programm text data
    prog_text = {}

    # programm control symbols
    ctrl_sym = ('(', ')', '{', '}', '[', ']', '+', '-', '*', '/', 
                 '.', ',', '|', '&', '~', '^', '!', '>', '<', '=',
                 ';', '\n')

    # ANSI C two bytes oparators
    operators = ('--', '-=', '->',
                 '++', '+=',
                 '&&', '&=',
                 '||', '|=',
                 '/=',
                 '*=',
                 '==',
                 '>=',
                 '<=',
                 '!=')

    def __init__(self, filename):
        """Create program object from filename

        args:
            filename - program file
        """
        self.open(filename);

    def open(self, filename):
        """Open program text file

        args:
            filename - program file
        """
        f = open(filename, 'r')
        self.prog_text['text'] = f.read()
        self.prog_text['idx'] = 0
        self.prog_text['len'] = len(self.prog_text['text'])
        f.close()

    def _next_ch(self):
        """Get next programm text symbol"""
        self.prog_text['idx'] += 1
        ch = self.prog_text['text'][self.prog_text['idx']]
        return ch

    def _curr_ch(self, count = 1):
        """Get current programm text symbol

        args:
            count - count sumbols returned
        """
        return self.prog_text['text'][self.prog_text['idx'] : 
                                      self.prog_text['idx'] + count]

    def _get_string(self):
        """Find and return string in quotes"""
        ch = self._curr_ch()
        # find start string
        while ch not in ('"', "'"):
            ch = self.__next_ch()
        # store type of quotes " or '
        quotes_type = ch

        string = quotes_type
        ch = self._next_ch()
        while ch not in (quotes_type, 0):
            string += ch
            ch = self._next_ch()
        
        if (ch == 0):
            raise HorpError('end quotes not found\n')

        string += quotes_type
        self._next_ch()
        return string

    def _get_word(self):
        """Find and return word"""
        word = ''
        ch = self._curr_ch()

        # find start word
        while not ch.isalnum():
            ch = self._next_ch()
        
        # find end word
        while (ch not in self.ctrl_sym) and (not ch.isspace()):
            word += ch
            ch = self._next_ch()

        return word

    def _get_symbol(self):
        """Find and return symbol or operator"""
        ch = self._curr_ch()

        # find start symbol
        while ch not in self.ctrl_sym:
            ch = self._next_ch()

        # get two bytes for math with operators
        str = self._curr_ch(2)
        if str in self.operators:
            # increase internal programm text counter 
            self._next_ch()
            self._next_ch()
            return str

        self._next_ch()
        return ch


    def get_next_token(self):
        """Get next token form program"""
        try:
            ch = self._curr_ch()
            while True:
                if ch.isspace():
                    ch = self._next_ch()
                elif ch in self.ctrl_sym:
                    return self._get_symbol()
                elif ch in ('"', "'"):
                    return self._get_string()
                elif ch.isalnum():
                    return self._get_word()
                elif ch == '\0':
                    return None
                else:
                    raise HorpError('Undefined symbol "' + ch + '"')
        except IndexError:
            return None



class Compiler:
    """compile program"""
    
    # program token tree
    tree = []

    def __init__(self, prog):
        """Create parser object. 

        args:
            prog - object of class Program
        """
        list_tokens = []
        token = []
        while token is not None:
            token = prog.get_next_token()
            list_tokens.append(token)
        self.tree = self._get_tree(enumerate(list_tokens))
        
    def _get_tree(self, prog):
        """Return tree of sources.

        args:
            prog - object of class Program
        """
        block = []
        expr = []
        for idx, token in prog:
            if token == ';':
                expr.append(token)
                block.append({'expr': expr})
                expr = []
            elif token == '{':
                block.append({'expr': expr,
                              'block': self._get_tree(prog)})
                expr = []
            elif token in ('}', None):
                if len(expr):
                    block.append({'expr': expr})
                    expr = []
                return block
            else:
                expr.append(token)

    def _compile_expr(self, expr):
        """Basic compiler expression"""
        text = ''
        for token in expr:
            text += ' ' + token
        return text + '\n'

    def _compiler(self, block):
        """Basic recursive compiler function"""
        text = ''
        for node in block:
            if node.has_key('block'):
                text += self._compile_expr(node['expr'])                
                text += '{\n' + self._compiler(node['block']) + '}\n'
            else:
                text += self._compile_expr(node['expr'])                
        return text

    def compile(self):
        """Compile Horp code"""
        return self._compiler(self.tree)




