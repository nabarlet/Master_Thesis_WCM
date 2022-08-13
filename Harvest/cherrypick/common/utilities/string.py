import pdb
import sys
import re
import random, string

__UNK__ = 'unknown'

def join(list_to_join, char = ''):
    """
        +join(list_to_join, char = '')+

        flattens a list of strings and then joins it.
        Returns a string (the joined list)
    """
    list_1D = [item for sub_list in list_to_join for item in sub_list]
    return char.join(list_1D)

__UTF_CHARS__ = [
    'AaÀàÁáÅåÄä',
    'EeÈèÉeËë',
    'IiÌìÍíÏÏ',
    'OoÒòÓóØøŐő',
    'UuÙùÚúŰű',
    'CcÇç',
]

def is_utf_char(c):
    """
        is_utf_char(c)

        check whether the character c is included in one of the utf sets
        reported in table __UTF_CHARS__. It returns either the utf set (if
        found) or the character c
    """
    result = c
    for set in __UTF_CHARS__:
        if c in set:
            result = ("[%s]" % (set))
            break
    return result

def compare_string_length(a, b):
    """
        compare_string_length(a, b)

        returns an ordered tuple (longest, shorter) among strings a end b.
        If the length is equal, it returns (a, b)
    """
    longer  = None
    shorter = None
    la = len(a)
    lb = len(b)

    if la >= lb:
        longer = a
        shorter = b
    else:
        longer = b
        shorter = a

    return (longer, shorter)

__RE_META_CHARS__ = [ '\\', '(', ')', '[', ']', ]
def escape_re_meta(c):
    result = c
    if c in __RE_META_CHARS__:
        result = '\\' + c
    return result

def normalized_re(c):
    cond_char = is_utf_char(c)
    cond_char = escape_re_meta(cond_char)
    return re.compile(cond_char, re.I | re.UNICODE)

def string_similarity(a, b):
    """
        string_similarity(a, b)

        performs a string similarity match between a and b, assuming that one
        is a longer string than the other. It does so by running a normalized
        correlation between the two strings.
        The function returns a proportion between the number of
        matched characters and the size of the shortest name

    """
    (longer, shorter) = compare_string_length(a, b)
    possible_results = []
    pridx = 0

    for start in range(len(longer)):
        possible_results.append(0)
        running_range = min(len(longer[start:]), len(shorter))
        try:
            for c in range(running_range):
                    chr_re = normalized_re(shorter[c])
                    if chr_re.match(longer[start+c]):
                        possible_results[start] += 1
        except re.error:
            print("string_similarity: regex error while compiling \"%s\". Skipping..." % (shorter[c]), file=sys.stderr)

    result = 0
    for r in possible_results:
        if r > result:
            result = r

    result = float(result) / float(len(shorter)) 
    return result

def random_string(size = 16):
    result = ''.join(random.choice(string.ascii_letters) for _ in range(size))
    return result

def escape_quotes(string):
    qre = re.compile('"') 
    escaped = qre.sub(r'\"', string)
    return escaped

def string_shortener(string, maxlen = 20, fill = '...'):
    """
        string_shortener(string, maxlen = 20, fill = '...')

        shortens a string longer than maxlen, filling the last len(fill)
        characters with the fill string.
        It returns the shortened string.
    """
    result = string
    stringsz = len(string)
    fillsz = len(fill)
    if stringsz > maxlen:
        stringsz  = maxlen - fillsz
        if        stringsz <= fillsz: raise ArgumentError
        result    = fill + string[-stringsz:]
    return result
