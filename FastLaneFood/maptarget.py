# Fall, 2019, CSc 32200, Professor Jie Wei
# FoodProject
#This is the final project for csc 322 (Software Engineering Course)  

#Project Team MEMBER:
#                    Shahan Rahman,
#                    Hasibul Islam,
#                    Eftekher Husain,
#                    Daniel Lee
from random import randint
import pandas

def initial_map_stat():
    map = [[0 for i in range(25)] for j in range(25)]
    map[0][1] = 2
    map[1][2] = 2
    map[2][3] = 2
    map[3][4] = 2
    map[0][5] = 2
    map[1][6] = 2
    map[3][8] = 2
    map[4][9] = 2
    map[5][6] = 2
    map[6][7] = 2
    map[7][8] = 2
    map[8][9] = 2
    map[5][10] = 2
    map[6][11] = 2
    map[7][12] = 2
    map[8][13] = 2
    map[9][14] = 2
    map[11][12] = 2
    map[12][13] = 2
    map[10][15] = 2
    map[11][16] = 2
    map[12][17] = 2
    map[13][18] = 2
    map[14][19] = 2
    map[15][16] = 2
    map[16][17] = 2
    map[17][18] = 2
    map[18][19] = 2
    map[15][20] = 2
    map[16][21] = 2
    map[18][23] = 2
    map[19][24] = 2
    map[20][21] = 2
    map[21][22] = 2
    map[22][23] = 2
    map[23][24] = 2
    map[1][0] = 2
    map[2][1] = 2
    map[3][2] = 2
    map[4][3] = 2
    map[5][0] = 2
    map[6][1] = 2
    map[8][3] = 2
    map[9][4] = 2
    map[6][5] = 2
    map[7][6] = 2
    map[8][7] = 2
    map[9][8] = 2
    map[10][5] = 2
    map[11][6] = 2
    map[12][7] = 2
    map[13][8] = 2
    map[14][9] = 2
    map[12][11] = 2
    map[13][12] = 2
    map[15][10] = 2
    map[16][11] = 2
    map[17][12] = 2
    map[18][13] = 2
    map[19][14] = 2
    map[16][15] = 2
    map[17][16] = 2
    map[18][17] = 2
    map[19][18] = 2
    map[20][15] = 2
    map[21][16] = 2
    map[23][18] = 2
    map[24][19] = 2
    map[21][20] = 2
    map[22][21] = 2
    map[23][22] = 2
    map[24][23] = 2
    return map

def rand_situation():
    map = initial_map_stat()
    choice1 = [[7,12], [11,12], [17,12], [13,12]]
    del choice1[randint(0,3)]
    for e in choice1:
        map[e[0]][e[1]] = 0
        map[e[1]][e[0]] = 0
    choice2 = [[1,6], [5,6], [3,8], [9,8], [15,16], [21,16], [19,18], [23,18]]
    i = randint(0,3)
    choice2 = [choice2[2*i], choice2[2*i+1]]
    for e in choice2:
        map[e[0]][e[1]] = 0
        map[e[1]][e[0]] = 0
    choice3 = [[5,10], [15,10], [1,2], [3,2], [9,14], [19,14], [21,22], [23,22]]
    i = randint(0,7)
    i2 = randint(0,7)
    while i == i2:
        i = randint(0,7)
        i2 = randint(0,7)
    choice3 = [choice3[i], choice3[i2]]
    for e in choice3:
        map[e[0]][e[1]] = 1
        map[e[1]][e[0]] = 1
    choice4 = [[6,7], [8,7], [6,11], [16,11], [16,17], [18,17], [8,13], [18,13]]
    i = randint(0,7)
    i2 = randint(0,7)
    while i == i2:
        i = randint(0,7)
        i2 = randint(0,7)
    choice4 = [choice4[i], choice4[i2]]
    for e in choice4:
        map[e[0]][e[1]] = 1
        map[e[1]][e[0]] = 1
    return map

def solution(tree, destination, ans, cur_loc):
    if tree[destination] == -1:
        ans.append(cur_loc)
        return ans
    else:
        ans.append(destination)
        return solution(tree, tree[destination], ans, cur_loc)

def find_path(map, destination, cur_loc):
    tree = [-1]*25
    distance = [111]*25
    distance[cur_loc] = 0
    temp = []
    for i in range(25):
        temp.append(i)
    while len(temp)!=0:
        min_distance = 111
        node = -1
        for i in range(len(distance)):
            if distance[i] < min_distance and i in temp:
                min_distance = distance[i]
                node = i
        temp.remove(node)
        for i in range(25):
            if map[node][i] and (i in temp) and (distance[node] + map[node][i] < distance[i]):
                tree[i]=node
                distance[i]=distance[node]+map[node][i]
    ans = []
    return solution(tree, destination, ans, cur_loc)

def get_destination(ddid):
    read = pandas.read_csv("data/order.csv")
    return read.loc[read["ddid"]==int(ddid)]["destination"].values[0]