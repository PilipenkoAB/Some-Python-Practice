import random
import math

from operator import itemgetter #sorting


# Creates a list containing 5 lists, each of 8 items, all set to 0
h = 1000
w = 4 + h

# radius of the circle
circle_r = h
# center of the circle (x, y)
circle_x = 0
circle_y = 0

Matrix = [[0 for x in range(w)] for y in range(h)] 

# create coordinates
for i in range(h):
    Matrix[i][0] = i

    alpha = 2 * math.pi * random.random()
    r = circle_r * math.sqrt(random.random())
    x = r * math.cos(alpha) + circle_x
    y = r * math.sin(alpha) + circle_y
    z = random.uniform(-1, 1)

    Matrix[i][1] = x
    Matrix[i][2] = y
    Matrix[i][3] = z

  #  print(  str(i)+" x = "+str(Matrix[i][1]) + "; y = "+str(Matrix[i][2])+";")

#calculate distance between all points
for i in range(h):
    for ii in range(h):
        x1 = Matrix[i][1]
        x2 = Matrix[ii][1]
        y1 = Matrix[i][2]
        y2 = Matrix[ii][2]

        distance = math.sqrt(math.pow(x1-x2,2) + math.pow(y1-y2,2))
        Matrix[ii][i+4] = distance
     #   print("["+str(ii) + "] ["+str(i)+"] - " + str(distance))


print("")


#save matrix with coordinates and distances
f = open("\\M1Way\\test.txt", "a")
for i in range(h):
    for ii in range(w):
        f.write(str(Matrix[i][ii]) + ";")
    f.write("\n")
f.close()


#final results
closepoints = 5

def sortAndGetSorted(row, dot):
    MatrixNumbers = [0 for x in range(h)] 
    for i in range(h):
        MatrixNumbers[i] = i
    MatrixValues = [0 for x in range(h)] 
    for i in range(h):
        MatrixValues[i] = Matrix[i][row]  
     #   print(" - - " + str(MatrixValues[i]))
    MatrixValuesSorted, MatrixNumbersSorted = zip(*sorted(zip(MatrixValues,MatrixNumbers),key=itemgetter(0)))
   # print(" sorted " + str(MatrixNumbersSorted[dot]))
    return MatrixNumbersSorted[dot]

#find close points 
f = open("\\M1Way\\test1.txt", "a")
for i in range(h):
    f.write(str(Matrix[i][0]) + ";")
    for ii in range(closepoints):
        f.write(str(sortAndGetSorted(i+4,ii+1)) + ";")
    f.write("\n")
f.close()



