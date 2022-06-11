import sys

def error_message(text):
    print(text, file=sys.stderr)
    sys.stderr.flush()
