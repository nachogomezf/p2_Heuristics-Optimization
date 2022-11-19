f = open("test16siblings.txt", 'w')
for i in range(1,17):
    f.write(str(i) +"," + str(1+(i % 2)) + ",X,X," + str((abs(16+i))) + '\n')
for i in range(17,33):
        f.write(str(i) +"," + str(1+(i % 2)) + ",X,X," + str((abs(i-16))) + '\n')
f.close()