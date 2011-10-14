import os

def clean_path(path, end_exts=[".pyc", "~", ".log", ".out", "#"]):
    for f in os.walk(path):
        for l in f[2]:
            each = os.path.abspath(f[0]+ os.sep+l)
            if os.path.isfile(each):
                for e in end_exts:
                    if each.endswith(e):
                        print each + " is a " + e
                        os.remove(each)
                        continue

if __name__ == '__main__':
    import sys
    path = '.'
    if len(sys.argv)>1:
        path = sys.argv[1]
    clean_path(path)
