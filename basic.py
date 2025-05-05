##-------------------------------------- Tokens 


# digits
DIGITS = '0123456789'

TT_INT = 'TT_INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'

# Error
class Error:
    def __init__(self, error_name ,details, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details  

    def as_string(self):
        result = f'{self.error_name} : {self.details} \n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln+1}'
        return result


class IllegalCharError(Error):
    def __init__(self, details, pos_start=None, pos_end=None):
        super().__init__('Illegal Character', details, pos_start, pos_end)


# token
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.type}: {self.value}'
        return f'{self.type}'
    

#position
class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_chr):
        self.idx+=1
        self.col+=1

        if current_chr == '\n':
            self.ln += 1
            self.col = 0

        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


## Lexer

class Lexer:
    def __init__(self,fn,text):
        self.fn = fn
        self.text=text
        self.pos=Position(-1,0,-1, fn,text)
        self.current_chr=None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_chr)
        self.current_chr=self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
    
    def make_tokens(self):
        tokens = []

        while self.current_chr != None:

            if self.current_chr=="\t":
                self.advance()

            elif self.current_chr == ' ':
                self.advance() 

            elif self.current_chr in DIGITS:
                tokens.append(self.make_number())
                self.advance()

            elif self.current_chr=='+':
                tokens.append(Token(TT_PLUS))
                self.advance()

            elif self.current_chr=='-':
                tokens.append(Token(TT_MINUS))
                self.advance()

            elif self.current_chr=='*':
                tokens.append(Token(TT_MUL))
                self.advance()

            elif self.current_chr=='/':
                tokens.append(Token(TT_DIV))
                self.advance()

            elif self.current_chr=='(':
                tokens.append(Token(TT_LPAREN))
                self.advance()

            elif self.current_chr==')':
                tokens.append(Token(TT_RPAREN))
                self.advance() 

            else:
                #return error
                pos_start = self.pos.copy()
                char = self.current_chr
                self.advance()
                return [], IllegalCharError("'"+char+"'", pos_start, self.pos)
        
        return tokens, None
    

    def make_number(self):
        num_str=''
        dot_count=0

        while self.current_chr != None and self.current_chr in DIGITS + '.':
            if self.current_chr == '.':
                if dot_count == 1 : break
                dot_count+=1
                num_str+='.'
            else:
                num_str+=self.current_chr
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))
        

def run (fn, text):
    lexer = Lexer(fn ,text)
    tokens, error = lexer.make_tokens()

    return tokens, error