'''
Incomplete Python emulator.
'''
import sys
import path_helpers as ph


if __name__ == '__main__':
    __filepath__ = ph.path(sys.argv[1]).realpath()
    __file__ = str(__filepath__)
    sys.path.insert(0, __filepath__.parent)
    exec(__filepath__.text())
