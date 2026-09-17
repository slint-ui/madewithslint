"""Fail if assets/css/gallery.css has unbalanced braces.

A stray } is not a harmless typo in CSS: the parser folds it into the next
rule's selector and drops that rule. #19 left one behind and it took out the
gallery's column layout. generate_html.py runs this before inlining the file.
"""
import re
import sys


def check(css, name='gallery.css'):
    depth = 0
    line = 1
    for ch in re.sub(r'/\*.*?\*/', lambda m: '\n' * m.group(0).count('\n'), css, flags=re.S):
        if ch == '\n':
            line += 1
        elif ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth < 0:
                sys.exit(f'{name}:{line}: unmatched closing brace')
    if depth:
        sys.exit(f'{name}: {depth} unclosed brace(s)')
