TOKEN_DIC = b"d"
TOKEN_LIST = b"l"
TOKEN_INT = b"i"
TOKEN_NEG = b"-"
TOKEN_SEP = b":"
TOKEN_END = b"e"

url = "a .torrent file"

def decode_int(a):
    """ Decode int in format i<content>e """
    a.consume_token() # i token

    content = b''
    while (i := next(a.read_byte())) != TOKEN_END:
        content += i

    return int(content)

def decode_str(a):
    """ Decode string in format <length>:<content> """
    length = b'' 
    while (i := next(a.read_byte())) != TOKEN_SEP:
        length += i
    length = int(length)

    content = b''
    while (length := length - 1) >= 0:
        content += next(a.read_byte())
    
    return content

def decode_list(a):
    """ Decode list in format l<content>e """
    a.consume_token() # l token
    lst = []
    while a.peek() != TOKEN_END:
        lst.append(decode(a))

    a.consume_token() # *e* token 
    return lst
    
def decode_dic(a):
    a.consume_token()
   
    dic = {}
    while a.peek() != TOKEN_END:
        string = decode_str(a)
        content = decode(a)
        dic[string] = content

    a.consume_token()

    return dic

def decode(a):
    return FUNCS[a.peek()](a)


FUNCS = {}
FUNCS[b'0'] = decode_str
FUNCS[b'1'] = decode_str
FUNCS[b'2'] = decode_str
FUNCS[b'3'] = decode_str
FUNCS[b'4'] = decode_str
FUNCS[b'5'] = decode_str
FUNCS[b'6'] = decode_str
FUNCS[b'7'] = decode_str
FUNCS[b'8'] = decode_str
FUNCS[b'9'] = decode_str
FUNCS[TOKEN_INT] = decode_int
FUNCS[TOKEN_DIC] = decode_dic
FUNCS[TOKEN_LIST] = decode_list
  
class Decode:
    def __init__(self, url):
        self.f_handler = open(url, "rb")
  
    def close_file(self):
        self.f_handler.close()
    
    def peek(self) -> bytes:
        byte = next(self.read_byte())
        self.f_handler.seek(-1, 1)
        return byte
    
    def consume_token(self):
        self.f_handler.seek(1, 1)
    
    def read_byte(self, chunks=1) -> bytes:
        """ Generator for bytes in .torrent file """
        while True:
            byte =  self.f_handler.read(chunks)
            if byte == b"":
                return None
            yield byte
    

if __name__ == "__main__":
    a = Decode(url)
    r = decode(a)
