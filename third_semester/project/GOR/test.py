import sys
import numpy as np

def test(f1):
    for i in f1:
        print(i)

    return()

if __name__ == "__main__":
    f1 = np.load(sys.argv[1])
    print(test(f1))
