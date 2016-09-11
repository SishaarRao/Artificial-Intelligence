import sys, re, math, random, time


def showpath(board, dcities):
    image = 255-np.zeros((650,650))
    maxx = 0
    minx = math.inf
    maxy = 0
    miny = math.inf
    for d in dcities.keys():
        x, y = dcities[d]
        if x>maxx:
            maxx = x
        if x<minx:
            minx = x
        if y>maxy:
            maxy = y
        if y<miny:
            miny = y
    for i in range(len(dcities)-1):

        col1, row1 = dcities[board[i]]
        col1 = 650-int((col1-minx)/(maxx - minx)*600)
        row1 = int((row1-miny)/(maxy - miny)*600)
        col2, row2 = dcities[board[i+1]]
        col2 = 650-int((col2-minx)/(maxx - minx)*600)
        row2 = int((row2-miny)/(maxy - miny)*600)
        cv.circle(image, ((col1),(row1)), 2, [0,0,0],-1)
        cv.line(image, ((col1),(row1)), (int(col2),int(row2)),[0,0,0], 2)


    col1, row1 = dcities[board[len(dcities)-1]]
    col1 = 650-int((col1-minx)/(maxx - minx)*600)
    row1 = int((row1-miny)/(maxy - miny)*600)
    col2, row2 = dcities[board[0]]
    col2 = 650-int((col2-minx)/(maxx - minx)*600)
    row2 = int((row2-miny)/(maxy - miny)*600)
    cv.circle(image, ((col1),(row1)), 2, [0,0,0],-1)
    cv.line(image, ((col1),(row1)), (int(col2),int(row2)),[0,0,0],2)
    return image.astype(np.uint8)


def copy(board):
    tb = []
    for b in range(len(board)):
        tb.append(board[b])
    return tb

def swap(board,s1,s2):
    '''minim = min(s1,s2)
    maxim = max(s1,s2)
    sboard = board[0:minim]+board[maxim:]+board[minim:maxim]
    return sboard'''
    temp = board[s2]
    board[s2] = board[s1]
    board[s1] = temp
    return board

def totalDist(city_list,config):
    dist = 0
    #print(len(config))
    for city in range(len(config)-1):
        dist+=city_list[config[city]][config[city+1]]
    dist+=city_list[config[len(city_list)-1]][config[0]]
    return dist

def formatlist(city_list):
    dictcities = {}
    citylook = {}
    count = 1

    for i in range(0,len(city_list),2):
        dictcities[count] =(    float(city_list[i])   ,   float(city_list[i+1])   )
        citylook[count] = {}
        count+=1

    for city1 in citylook:
        for city2 in citylook:
            if city1 == city2:
                continue
            else:
                if city2 in citylook[city1]:
                    continue
                else:
                    dist = math.sqrt(   (dictcities[city1][0]-dictcities[city2][0])*(dictcities[city1][0]-dictcities[city2][0]) +   (dictcities[city1][1]-dictcities[city2][1])*(dictcities[city1][1]-dictcities[city2][1]) )
                    citylook[city1][city2] = dist
                    citylook[city2][city1] = dist

    return (dictcities, citylook)

def rswap(board,s1,s2):
    minim = min(s1,s2)
    maxim = max(s1,s2)
    sboard = board[0:minim]+board[minim:maxim+1][::-1]+board[maxim+1:]
    return sboard

def randomize(city_list):
    tkeys = list(city_list.keys())
    random.shuffle(tkeys)
    return tkeys

def improvement(c1,c2,dist, board):
    mini = min(c1,c2)
    maxi = max(c1,c2)
    c1 = mini
    c2 = maxi
    prev = c1-1
    next = (c2+1)%len(board)

    curr = dist[   board[c1]   ][  board[prev]  ] + dist[  board[c2]   ][  board[next]   ]
    reverse = dist[ board[c2]   ][  board[prev] ] + dist[   board[c1]   ][  board[next] ]
    return curr - reverse

def compare(c1,c2,dist,board):
    mini = min(c1,c2)
    maxi = max(c1,c2)
    c1 = mini
    c2 = maxi

    pc1 = c1-1
    pc2 = c2-1

    nc1 = (c1+1)%len(board)
    nc2 = (c2+1)%len(board)

    if pc1 == c2 or c2==nc1 or pc2 == c1 or nc2 == c1:
        return -1*math.inf

    curr = dist[ board[pc1] ][  board[c1]   ]   +   dist[   board[c1]   ][  board[nc1]  ]   +   dist[  board[pc2]   ][  board[c2]   ]   +   dist[   board[c2]   ][  board[nc2]  ]
    reverse = dist[ board[pc1] ][  board[c2]   ]   +   dist[   board[c2]   ][  board[nc1]  ]   +   dist[  board[pc2]   ][  board[c1]   ]   +   dist[   board[c1]   ][  board[nc2]  ]

    return curr-reverse

def shuffle(board,city_list,test):
    count = 0
    for c1 in range (1, len(board)-1):
        for c2 in range(c1+2, len(board)):
            if compare(c1,c2,city_list,board) > -50:
                count+=1
                board = swap(board,c1,c2)
                if count == test:
                    return count
    return count

def minimizer(city_list, board,dcities):

    leni = 1
    test = 2
    threshold = 1000
    bboard = []

    min = totalDist(city_list,board)

    for i in range(leni):

        checked = True
        while(checked):

            checked = False

            start = time.clock()

            checker = True
            while(checker):

                checker = False

                for city1 in range(1,len(board)-1):

                    for city2 in range(city1+1,len(board)):

                        if city1 == city2:
                            continue
                        else:
                            improv = improvement(city1,city2,city_list,board)
                            if improv>0:
                                board = rswap(board, city1,city2)
                                checker = True
                                checked = True

            #print(str(  time.clock()-start))

            start = time.clock()
            checker = True

            while(checker):

                checker = False
                best = 0
                bswap = (0,0)

                for city1 in range(1,len(board)-1):
                    for city2 in range(city1+2,len(board)):
                        if city1 == city2:
                            continue
                        else:
                            comp = compare(city1,city2,city_list,board)
                            if comp>best:
                                checker = True
                                checked = True
                                best = comp
                                bswap = (city1,city2)

                board = swap(board,bswap[0],bswap[1])

            #print(str(  time.clock() - start))

        dist = totalDist(city_list,board)

        #print(dist)


        if dist<min:
                min = dist
                bboard = copy(board)

        if i ==leni-1:
            continue

        else:
            #count = shuffle(board,city_list,test)
                #print()
            for i in range(test):
                c1 = random.randint(0,len(board)-1)
                c2 = random.randint(0,len(board)-1)
                while c1==c2:
                    c2 = random.randint(0,len(board)-1)
                board = swap((board),c1,c2)


    print("best distance: "+str(min))
    print(bboard)
    #cv.imshow("Image", showpath(bboard,dcities))
    #cv.waitKey(2500)
    return bboard

def acceptp(improv,T):
    if improv/T > 150:
        return 1
    elif improv/T < -150:
        return 0
    else:
        return math.pow(2.71828,improv/T)

def randt(list):
    random.shuffle(list)
    return list
def annealing(city_list, board, dcities):

    Temp = 100
    Temp_min = .01
    alpha = .85

    min = totalDist(city_list,board)
    count = 2
    while(Temp>Temp_min):
        #cv.imshow("Image", showpath(board,dcities))
        #cv.waitKey(1)
        #print(Temp)
        checker  = True
        for i in range(10):

            checker = False

            for city1 in randt(list(range(1,len(board)-1))):
                for city2 in randt(list(range(city1+1,len(board)))):

                    improv = improvement(city1,city2,city_list,board)
                    ap = acceptp(improv,Temp)
                    if ap>float(    1.0* random.randint(0,100)/100 ):
                        board = rswap(board, city1,city2)
                        checker = True

                    else:
                        improv = compare(city1,city2,city_list,board)
                        ap = acceptp(improv,Temp)
                        if ap>float(    1.0* random.randint(0,100)/100 ):
                            board = swap(board, city1,city2)
                            checker = True
                            break
                    break
                break

        count+=1
        Temp = Temp* alpha
        if alpha<.995:
            alpha = alpha + (   (1 - alpha)/(math.exp(-1*count) +1 )    )
        else:
            alpha = .99

    return minimizer(city_list,board,dcities)
def makeBaby(b1, b2,pivot):
    baby = []
    tempb2 = b2[pivot:]
    tempb2 = tempb2[::-1]
    baby+=tempb2
    tempb1 = b1[::-1]
    for city in tempb1:
        if city not in baby:
            baby.append(city)
    #print(len(baby))
    return baby[::-1]
def genetic(city_list,dcitites):
    maxgen = 300
    numrents = 100
    currgen = []
    newgen = []
    multiplier = 10
    mini = 100000000
    best = []
    for i in range(numrents):
        randt = randomize(city_list)
        while randt in currgen:
            randt = randomize(city_list)
        currgen.append(randt)

    newgen = currgen

    for i in range(maxgen):
        print(mini)
        currgen = newgen
        dict_length = {}

        for i in range(numrents):

            city1 = random.randint(0,numrents-1)

            while not (totalDist(city_list,currgen[city1]))<multiplier*mini:
                city1  = random.randint(0,numrents-1)

            city2 = random.randint(0,numrents-1)

            while not (city1 != city2 or (totalDist(city_list,currgen[city1])<multiplier*mini)):
                city2 = random.randint(0,numrents-1)

            pivot = random.randint(int(len(currgen[0])/1.3),len(currgen[0]))

            board1 = currgen[city1]
            board2 = currgen[city2]
            #print(board1==board2)
            baby1 = makeBaby(board1,board2,pivot)
            baby2 = makeBaby(board2,board1,pivot)

            if random.randint(0,10)>10:
                rand1 = random.randint(0,len(board1)-1)
                rand2 = random.randint(0,len(board1)-1)
                while rand1 == rand2:
                    rand2 = random.randint(0,len(board1)-1)
                if random.randint(0,10)<5:
                    baby1 = swap(baby1,rand1,rand2)
                else:
                    baby2 = swap(baby2,rand1,rand2)

            bump = 0
            better = []
            #print("b")
            tot1 = totalDist(city_list,baby1)
            tot2 = totalDist(city_list,baby2)
            #print(tot1,tot2)
            bump = min(tot1,tot2)
            if bump == tot2:
                better = baby2
            else:
                better = baby1

            if bump<mini:
                mini = bump
                best = better

    return minimizer(city_list,best,dcities)
file ="tsp0734.txt"#sys.argv[1]
list_cities = open(file,'r').read().split()

num_cities = int(list_cities.pop(0))

dcities, citykey = formatlist(list_cities)
#print(dcities, citykey)
startboard = randomize(citykey)
#cv.imshow("Image",showpath(startboard,dcities))

#print(startboard)
start = time.clock()
bb = genetic(citykey,dcities)
print(str(time.clock()-start))
#cv.imshow("Image", showpath(bb,dcities))
#cv.waitKey(0)
