import re

DEFAULT_EOL_TOKEN = '@'

def text_conditioner(text, eol = DEFAULT_EOL_TOKEN):
    result = re.sub('\s*\n+', DEFAULT_EOL_TOKEN, text)
    return result
