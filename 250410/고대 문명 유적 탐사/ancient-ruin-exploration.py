from collections import deque
from copy import deepcopy

dr=[0,0,1,-1]
dc=[1,-1,0,0]
def in_range(r,c):
    return 0<=r<5 and 0<=c<5
def bfs(r,c, mat, visited):
    n=mat[r][c]
    q=deque([[r,c]])
    visited[r][c]=True
    same=[[r,c]]
    while q:
        r,c = q.popleft()
        for d in range(4):
            nr,nc= r+dr[d],c+dc[d]
            if in_range(nr,nc) and not visited[nr][nc] and mat[nr][nc]==n:
                q.append([nr,nc])
                visited[nr][nc]=True
                same.append([nr,nc])
    return same

def cal_score(mat,partial=1):
    ans=[]
    visited=[[False]*5 for _ in range(5)]
    for r in range(partial,5-partial):
        for c in range(partial,5-partial):
            if not visited[r][c]:
                carr = bfs(r,c, mat, visited)
                if len(carr)>2:
                    ans+=carr
                visited[r][c]=True
    return ans

def tryrotate(r,c):
    trymat = deepcopy(mat)
    maxlen=-1
    minimat = [matl[c-1:c+2] for matl in trymat[r-1:r+2]]

    for d in range(1,4):
        minimat = [x[::-1] for x in zip(*minimat)]
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                trymat[r+i][c+j]=minimat[1+i][1+j]
        carray = cal_score(trymat)
        clen = len(carray)
        if clen>maxlen:
            maxarray = carray
            maxlen=clen
            rad=d
        return maxarray, rad, maxlen
def rotate():
    global scoreloc
    maxlen = -1
    for r in range(1,4):
        for c in range(1,4):
            cans, d, clen =tryrotate(r,c)
            if clen>maxlen:
                moverc=[r,c]
                maxarray = cans
                maxlen = clen
                rad = d
            elif clen == maxlen:
                if rad>d:
                    moverc = [r, c]
                    maxarray = cans
                    rad = d
                elif rad==d:
                    if moverc[1]> c:
                        moverc = [r, c]
                        maxarray = cans
                    elif moverc[1] == c:
                        if moverc[0]> r:
                            moverc = [r, c]
                            maxarray = cans


    r, c = moverc
    minimat = [list(x)[::-1] for x in zip(*list(matl[c - 1:c + 2] for matl in mat[r - 1:r + 2]))]
    for _ in range(rad-1):
        minimat = [list(x)[::-1] for x in zip(*minimat)]
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            mat[r + i][c + j] = minimat[1+i][1+j]
    return len(maxarray)





def gain_score():
    global score, ans
    ans = cal_score(mat)
    if not ans: return True
    score+=len(ans)
    return False

def fill():
    global ans
    ans.sort(key=lambda x:(x[1], -x[0]))
    for r,c in ans:
        mat[r][c]=peices.popleft()

# file = open('input.txt', 'r')
# input = file.readline
# tc=int(input())
for _ in range(1):
    K,M = map(int, input().split())
    mat=[list(map(int, input().split()))for _ in range(5)]
    peices = deque(list(map(int, input().split())))

    for _ in range(K):
        score = 0
        lenmax = rotate()
        if lenmax:
            while True:
                fail = gain_score()
                if fail:
                    break
                fill()
        else: break
        print(score, end=' ')
    print('')

