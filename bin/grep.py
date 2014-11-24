import re
import os
from sys import argv

def grep(match):
    def _do_grep_wrapper(match):
        def _do_grep(lines):
            if match(lines):
                yield lines
        return _do_grep
    return _do_grep_wrapper(match)


def find(what, where, depth=True):
    """
    :param what: str String to search for
    :param where: str directory to start search in
    :param regexp: bool If true then 'what' is a regexp, otherwise - use simple substring search
    :return:
    """
    r = re.compile(what, re.M)
    res = []
    for root, sub_dirs, files in os.walk(where, True):
        if (not depth) and (root != where):
            continue

        for file_name in files:
            f = open(os.path.join(root, file_name), 'r')
            data = f.read()
            if r.search(data):
                res.append(os.path.join(root, file_name))
    return res

if __name__ == '__main__':
    if len(argv) > 2:
        print(list(find(argv[1], argv[2], True)))