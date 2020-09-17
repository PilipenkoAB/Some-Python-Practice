Matrix = [[0 for y in range(6)] for x in range(1000)] 

f = open("\\M1Way\\test2.txt", "r")
i = 0
for x in f:
    #print(x)
    xx = x.split(";")

    Matrix[i][0] = xx[0]
    Matrix[i][1] = xx[1]
    Matrix[i][2] = xx[2]
    Matrix[i][3] = xx[3]
    Matrix[i][4] = xx[4]
    Matrix[i][5] = xx[5]
    i += 1
f.close()

# matrix loaded correctly

#for i in range(1000):
 #   print(Matrix[i][5])

# [rows][columns]
row = 1000
for i in range(row):
    for ii in range(5):
        exist = 0
        for iii in range(5):
            if(int(Matrix[int(Matrix[i][ii+1])][iii+1]) == i):
                exist = 1
        if (exist == 0):
            Matrix[i][ii+1] = -1

#test results
for i in range(1000):
    print(str(Matrix[i][0]) + ";" + str(Matrix[i][1]) + ";" + str(Matrix[i][2]) + ";" + str(Matrix[i][3]) + ";" + str(Matrix[i][4]) + ";" + str(Matrix[i][5]))

# save the results
f = open("\\M1Way\\test3.txt", "a")
for i in range(row):
    f.write(str(Matrix[i][0]) + ";" + str(Matrix[i][1]) + ";" + str(Matrix[i][2]) + ";" + str(Matrix[i][3]) + ";" + str(Matrix[i][4]) + ";" + str(Matrix[i][5]))
    f.write("\n")
f.close()