import sys, re, math, random, time
import cv2 as cv
import numpy as np

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
    Templist = []
    tempkeys = set(tkeys)
    curr = 1
    board = []

    while len(tempkeys)>0:
        #print(board)
        board+=[curr]
        tempkeys.remove(curr)
        Templist = {v:k for k,v in city_list[curr].items()}
        key = list(Templist.keys())
        key = sorted(key)
        for count in range(0,len(city_list)-1):
            #print(key[count])
            if curr ==count:
                continue
            elif Templist[key[count]] in tempkeys:
                curr = Templist[key[count]]
                break
            if curr == Templist[key[count]]:
                break

    return board

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

    leni = 100
    test = 10
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

        print(dist)
        #if (i%10 == 0):
            #print(min)
            #print(bboard)

        if dist<min:
                min = dist
                bboard = copy(board)

        if i ==leni-1:
            continue

        else:
            #count = shuffle(board,city_list,test)
                #print()
            test = random.randint(10,60)
            Temp = copy(bboard)
            for i in range(test):
                c1 = random.randint(0,len(board)-1)
                c2 = random.randint(0,len(board)-1)
                while c1==c2:
                    c2 = random.randint(0,len(board)-1)
                Temp = swap(copy(Temp),c1,c2)
            board = Temp


    print("best distance: "+str(min))
    print(bboard)
    cv.imshow("Image", showpath(bboard,dcities))
    cv.waitKey(2500)
    return bboard

def acceptp(improv,T):
    if improv/T > 150:
        return 1
    elif improv/T < -150:
        return 0
    else:
        return math.pow(2.71828,improv/T)


def annealing(city_list, board, dcities):

    Temp = 100
    Temp_min = .01
    alpha = .8

    min = totalDist(city_list,board)
    bboard = board
    count = 2
    while(Temp>Temp_min):
        #print(Temp)
        cv.imshow("Image", showpath(board,dcities))
        cv.waitKey(1)
        #print(board)
        for i in range(100):
            city1 = random.randint(1,len(board)-1)
            city2 = random.randint((city1+2)%len(board),len(board)-1)%len(board)
            while city1 == city2:
                city2 =random.randint((city1+2)%len(board),len(board)-1)%len(board)
            # improv = improvement(city1,city2,city_list,board)
            # ap = acceptp(improv,Temp)
            # if ap>float(    1.0* random.randint(0,100)/100 ):
            #     board = rswap(board, city1,city2)
            # else:
            improv = compare(city1,city2,city_list,board)
            ap = acceptp(improv,Temp)
            if ap>float(    1.0* random.randint(0,100)/100 ):
                board = swap(board, city1,city2)
        count+=1
        Temp = Temp* alpha
        if alpha<.995:
            alpha = alpha + (   (1 - alpha)/(math.exp(-1*count) +1 )    )
        else:
            alpha = .999

    return minimizer(city_list,board,dcities)
file ="tsp0734.txt"#sys.argv[1]
list_cities = open(file,'r').read().split()

num_cities = int(list_cities.pop(0))

dcities, citykey = formatlist(list_cities)
#print(dcities, citykey)
startboard = randomize(citykey)
#cv.imshow("Image",showpath(startboard,dcities))

#print(startboard)
start = time.clock()
#bb = minimizer(citykey,startboard,dcities)#annealing(citykey,startboard,dcities)
#print(str(time.clock()-start))
#print(startboard)
#path = [692, 712, 723, 734, 724, 693, 679, 661, 668, 683, 694, 675, 653, 676, 656, 670, 684, 680, 689, 662, 673, 677, 686, 699, 711, 716, 722, 725, 726, 727, 732, 733, 729, 728, 730, 731, 721, 715, 709, 708, 720, 719, 718, 717, 714, 713, 710, 702, 703, 707, 706, 700, 698, 690, 682, 674, 681, 669, 657, 660, 654, 672, 678, 685, 688, 701, 704, 705, 695, 696, 697, 691, 687, 666, 651, 658, 655, 646, 645, 644, 631, 640, 643, 663, 659, 671, 665, 664, 650, 642, 637, 607, 577, 581, 562, 571, 578, 560, 556, 542, 557, 600, 601, 611, 579, 575, 584, 589, 617, 612, 580, 590, 621, 602, 630, 613, 618, 622, 632, 633, 623, 614, 591, 559, 551, 543, 539, 544, 527, 518, 509, 513, 519, 522, 520, 515, 501, 481, 483, 473, 463, 472, 460, 455, 449, 421, 379, 357, 314, 326, 325, 322, 337, 338, 348, 353, 374, 375, 402, 412, 443, 426, 419, 384, 387, 372, 401, 395, 381, 352, 331, 365, 343, 312, 306, 294, 266, 265, 261, 252, 236, 234, 208, 123, 124, 121, 126, 120, 100, 95, 66, 41, 56, 53, 50, 44, 54, 63, 67, 58, 68, 76, 75, 74, 73, 72, 105, 162, 180, 165, 169, 170, 171, 184, 196, 187, 195, 191, 190, 245, 292, 253, 237, 212, 215, 263, 270, 262, 269, 295, 296, 317, 313, 289, 281, 246, 256, 247, 257, 271, 248, 242, 240, 229, 209, 182, 213, 192, 181, 127, 115, 91, 86, 81, 80, 79, 85, 84, 93, 133, 118, 110, 109, 77, 45, 36, 46, 47, 27, 18, 16, 1, 3, 6, 11, 22, 25, 21, 19, 17, 7, 2, 5, 4, 8, 10, 15, 12, 13, 9, 14, 23, 24, 26, 28, 34, 40, 39, 43, 51, 69, 83, 98, 92, 60, 55, 38, 31, 29, 20, 42, 49, 71, 65, 62, 70, 90, 89, 57, 52, 48, 37, 35, 33, 30, 32, 59, 61, 88, 107, 112, 119, 108, 104, 113, 125, 132, 134, 140, 151, 143, 147, 205, 268, 272, 280, 301, 305, 277, 267, 274, 284, 300, 321, 324, 342, 351, 355, 341, 334, 316, 298, 291, 310, 323, 344, 304, 276, 264, 230, 207, 199, 186, 200, 233, 235, 251, 243, 244, 239, 224, 231, 227, 220, 179, 168, 163, 142, 137, 131, 156, 160, 157, 161, 167, 178, 176, 159, 150, 111, 114, 117, 97, 82, 64, 78, 87, 106, 94, 101, 102, 116, 128, 129, 152, 148, 145, 141, 138, 122, 103, 99, 96, 130, 139, 155, 175, 189, 203, 166, 149, 135, 154, 153, 146, 174, 183, 194, 226, 241, 260, 273, 238, 232, 225, 219, 223, 218, 217, 211, 202, 173, 177, 201, 198, 136, 144, 164, 158, 172, 185, 188, 197, 193, 206, 216, 222, 228, 214, 204, 210, 221, 249, 279, 278, 285, 293, 297, 302, 318, 309, 303, 315, 327, 319, 358, 361, 388, 403, 415, 440, 452, 464, 461, 468, 467, 495, 549, 545, 546, 593, 608, 594, 595, 565, 553, 540, 531, 516, 482, 466, 427, 404, 394, 391, 399, 382, 398, 407, 397, 396, 393, 385, 362, 349, 366, 367, 354, 350, 320, 308, 307, 282, 250, 254, 258, 275, 283, 286, 290, 287, 259, 255, 288, 299, 311, 333, 347, 363, 359, 373, 406, 405, 383, 380, 377, 376, 356, 389, 409, 420, 429, 428, 445, 425, 444, 456, 471, 469, 474, 441, 417, 430, 433, 431, 437, 457, 477, 487, 502, 505, 491, 484, 450, 434, 432, 423, 413, 414, 386, 400, 435, 475, 486, 507, 497, 478, 458, 442, 436, 422, 416, 418, 408, 371, 378, 370, 369, 360, 329, 328, 339, 345, 346, 335, 330, 336, 332, 340, 364, 368, 410, 392, 390, 438, 439, 448, 451, 446, 447, 411, 424, 459, 453, 479, 498, 499, 508, 493, 485, 480, 470, 465, 454, 462, 476, 490, 500, 494, 523, 536, 504, 512, 517, 526, 558, 576, 585, 572, 567, 537, 535, 514, 489, 492, 488, 503, 511, 548, 564, 586, 588, 604, 610, 616, 624, 619, 615, 609, 606, 599, 592, 573, 552, 541, 534, 533, 530, 538, 555, 570, 605, 629, 628, 627, 625, 638, 620, 574, 563, 529, 510, 506, 521, 525, 550, 561, 583, 587, 598, 626, 647, 649, 648, 636, 635, 639, 597, 582, 641, 603, 569, 596, 568, 554, 547, 528, 496, 532, 524, 566, 634, 667, 652]
bb = minimizer(citykey,startboard,dcities)
cv.imshow("Image", showpath(bb,dcities))
cv.waitKey(0)
