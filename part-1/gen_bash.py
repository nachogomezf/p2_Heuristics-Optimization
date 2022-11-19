import sys
import os
f = open('calls.sh', 'w')
for i, elem in enumerate(os.listdir("CSP-tests")):
    if elem.endswith(".txt"):
        f.write("python3 CSPBusSeats.py " + "CSP-tests/" + elem)
        if i != len(elem): f.write('\n')
f.close()
