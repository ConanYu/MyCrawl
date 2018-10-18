import os
def chPathToThis(f=None):
    f = __file__ if f is None else f
    os.chdir(os.path.dirname(f))
