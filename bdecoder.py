import requests

"""
Augmented BNF Syntax of BEncoding, see https://hackage.haskell.org/package/bencoding-0.4.3.0/docs/Data-BEncode.html

 <DICT>  ::= "d" 1 * (<STR> <BE>) "e"
 <LIST>  ::= "l" 1 * <BE>         "e"
 <INT>   ::= "i"     <SNUM>       "e"
 <STR>   ::= <NUM> ":" n * <CHAR>; where n equals the <NUM>

 <SNUM>  ::= "-" <NUM> / <NUM>
 <NUM>   ::= 1 * <DIGIT>
 <CHAR>  ::= %
 <DIGIT> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
"""

TOKEN_DICT = b"d"
TOKEN_LIST = b"l"
TOKEN_INT = b"i"
TOKEN_SEP = b":"
TOKEN_NEG = b"-"
TOKEN_END = b"e"

def decode_int(buffer) -> int:
    """ Decode int """
    # TOKEN_INT 
    buffer.consume_token() 

    content = b''
    while (i := next(buffer.read_byte())) != TOKEN_END:
        content += i

    return int(content)

def decode_str(buffer) -> bytearray:
    """ Decode string """
    length = b'' 
    while (i := next(buffer.read_byte())) != TOKEN_SEP:
        length += i
    length = int(length)

    content = b''
    while (length := length - 1) >= 0:
        content += next(buffer.read_byte())
    
    return content

def decode_list(buffer) -> list:
    """ Decode list in format """
    # TOKEN_LIST 
    buffer.consume_token()

    lst = []
    while buffer.peek() != TOKEN_END:
        lst.append(decode(buffer))

    # TOKEN_END 
    buffer.consume_token()

    return lst
    
def decode_dict(buffer) -> dict:
    """ Decode a dictionary """
    # TOKEN_DICT
    buffer.consume_token()
   
    dic = {}
    while buffer.peek() != TOKEN_END:
        key = decode_str(buffer)
        value = decode(buffer)
        dic[key] = value

    # TOKEN_END
    buffer.consume_token()

    return dic

def decode(buffer: Buffer):
    return funcs[buffer.peek()](buffer)

funcs = {
    b'0': decode_str,
    b'1': decode_str,
    b'2': decode_str,
    b'3': decode_str,
    b'4': decode_str,
    b'5': decode_str,
    b'6': decode_str,
    b'7': decode_str,
    b'8': decode_str,
    b'9': decode_str,
    TOKEN_INT: decode_int,
    TOKEN_DICT: decode_dict,
    TOKEN_LIST: decode_list
}

class Buffer:
    """ IO Buffer"""
    def __init__(self, path):
        self.f_handler = open(path, "rb")
  
    def close_file(self) -> None:
        self.f_handler.close()
    
    def peek(self) -> bytes:
        byte = next(self.read_byte())
        self.f_handler.seek(-1, 1)
        return byte
    
    def consume_token(self) -> None:
        self.f_handler.seek(1, 1)
    
    def read_byte(self, chunks=1) -> bytes:
        """ Generator for bytes in .torrent file """
        while True:
            byte =  self.f_handler.read(chunks)
            if byte == b"":
                return None
            yield byte

if __name__ == "__main__":
    path = "a .torrent file"
    buffer = Buffer(path)
    result = decode(buffer) 
    buffer.close_file()
