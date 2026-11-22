import json, os
import eng_to_ipa as ipa

os.chdir(os.path.dirname(os.path.abspath(__file__)))

debug_mode: bool = False

en_ni_file_name: str = "en_ni.json"
en_ni_file = open(en_ni_file_name, 'r')
en_ni: dict = json.load(en_ni_file)
en_ni_unique_symbols: dict = {
    "i": "aj",
    "j": "q",
    "ch": "c",
    "y": "j",
    "oo": "u",
    "w": "v",
    "th": "z",
    "h": "x",
    "ph": "f",
    "x": "ks",
}
en_ni_file.close()

class Token:
    text = ""
    is_word = False
    def __init__(self, text, is_word = False):
        self.text = text
        self.is_word = is_word
    def __repr__(self):
        return f"\"{self.text}\"" + ("-w" if self.is_word else "")
    def __str__(self):
        return self.text
    def __iadd__(self, other):
        self.text += other
        return self
def get_tokens(text: str) -> list[str]:
    if not len(text):
        return []
    tokens: list[Token] = []
    
    token_text: str = ""
    is_token_a_word: bool = text[0].isalpha()
    for char in text:
        if is_token_a_word:
            if char.isalpha():
                token_text += char
            else:
                tokens.append(Token(token_text, True))
                token_text = char
                is_token_a_word = False
        else:
            if not char.isalpha():
                token_text += char
            else:
                tokens.append(Token(token_text))
                token_text = char
                is_token_a_word = True
    tokens.append(Token(token_text, is_token_a_word))
    return tokens

def is_word_plural(word: str) -> bool:
    word = word.lower()
    return (word.endswith("s") and word[:-1] in en_ni)\
        or (word.endswith("ies") and (word[:-3] + "y") in en_ni)
def remove_plural(word: str) -> str:
    singular_word: str = word
    if word.endswith("s") and word[:-1] in en_ni:
        singular_word = word[:-1]
    elif word.endswith("ies") and (word[:-3] + "y") in en_ni:
        singular_word = word[:-3] + "y"
    return singular_word
def is_word_translatable(word: str) -> bool:
    is_plural: bool = is_word_plural(word)
    word = word.lower()
    return word in en_ni or is_plural
def translate_word(word: str) -> str:
    is_upper: bool = word.isupper() and len(word) > 1
    is_capitalized: bool = word[0].isupper()

    word = word.lower()
    is_plural: bool = is_word_plural(word)
    
    translated_word: str = ""
    if word in en_ni:
        translated_word = en_ni[word][0]
    elif is_plural:
        translated_word = "ty " + en_ni[remove_plural(word)][0]
    else:
        translated_word = transliterate(word)

    if is_upper:
        translated_word = translated_word.upper()
    elif is_capitalized:
        translated_word = translated_word.capitalize()
    
    return translated_word
def translate_token_buffer(token_buffer: list[Token], debug: bool = False) -> str:
    if not len(token_buffer):
        return ""
    
    # Starts at the length of the token buffer and goes down.
    # This way larger words such as "bullet train" will be translated first,
    # before reaching word "bullet" by itself and translating it seperately.
    max_buffer_index = len(token_buffer)

    if debug_mode or debug:
        print(token_buffer, end="")
        print(f" - len({max_buffer_index})")
    
    buffer_text: str = ""
    while max_buffer_index > 0:
        # get the current buffer text
        buffer_text = ""
        for add_index in range(max_buffer_index):
            buffer_text += token_buffer[add_index].text
        
        if is_word_translatable(buffer_text):
            break
        max_buffer_index -= 1

    # translate the given word(-s)
    if max_buffer_index == 0:
        buffer_text = token_buffer[0].text
        max_buffer_index += 1
    result: str = translate_word(buffer_text)
    # translate the remaining tokens
    result += translate_token_buffer(token_buffer[max_buffer_index:], debug)

    return result
def translate(text: str, debug: bool = False) -> str:
    token_buffer: list[Token] = get_tokens(text)
    if debug_mode or debug:
        print(f"Starting tokens: {token_buffer}")
    return translate_token_buffer(token_buffer, debug)

def transliterate(text: str) -> str:
    result: str = ""
    text_length: int = len(text)
    symbol_index: int = 0
    while symbol_index < text_length:
        symbol: str = text[symbol_index]
        next_symbol: str = ""
        symbols_combo: str = symbol
        if symbol_index + 1 < text_length:
            next_symbol = text[symbol_index + 1]
            symbols_combo += next_symbol
        double_letter: bool = symbol == next_symbol and symbol.isalpha()
        
        if symbol in en_ni_unique_symbols:
            result += en_ni_unique_symbols[symbol]
        elif symbols_combo in en_ni_unique_symbols:
            result += en_ni_unique_symbols[symbols_combo]
            symbol_index += 1
        elif double_letter:
            result += symbol + '\''
            symbol_index += 1
        else:
            result += symbol

        symbol_index += 1
    return result

def ipa_convert(text: str) -> str:
    return ipa.convert(text)