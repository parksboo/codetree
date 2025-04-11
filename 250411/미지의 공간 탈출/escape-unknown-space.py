from collections import deque
from copy import deepcopy
#동서남북
dr=[0,0,1,-1]
dc=[1,-1,0,0]
def printmat(mat):
    for matl in mat:
        print(*matl)
    print('')
def in_range1(r,c):
    return 0<=r<3*M and 0<=c<3*M
def bfs1(r,c):
    visited=deepcopy(wallmat)
    q = deque([[r,c,0]])

    while q:
        r,c,p=q.popleft()
        for d in range(4):
            nr,nc=r+dr[d],c+dc[d]
            if in_range1(nr,nc):
                if visited[nr][nc]==-1:
                    # 동
                    if d==0:
                        # 북 - 동
                        if r<M:
                            tmp=M-r
                            nr,nc=M,2*M-1+tmp
                        # 남 - 동
                        else:
                            nr, nc = c, r
                    # 서
                    elif d==1:
                        # 북 - 서
                        if r < M:
                            nr, nc = c, r
                        # 남 - 서
                        else:
                            tmp = r-2*M+1
                            nr, nc = 2*M-1,tmp
                    # 남
                    elif d==2:
                        # 서 남
                        if c<M:
                            tmp= M-c
                            nr,nc = 2*M-1+tmp,M
                        # 동 남
                        else:
                            nr, nc = c, r
                    #북
                    else:
                        # 서 북
                        if c<M:
                            nr,nc=c,r
                        # 동북
                        else:
                            nr,nc=3*M-c-1,2*M-1
                if visited[nr][nc]==0:
                    visited[nr][nc]=p+1
                    q.append([nr,nc,p+1])
                elif wallmat[nr][nc]==3:
                    visited[nr][nc]=p+1
                    return p+1
    return -1



class Timemachine:
    def __init__(self):
        for r in range(M,2*M):
            for c in range(M,2*M):
                if wallmat[r][c]==2:
                    self.r=r
                    self.c=c
                    break

class Strange:
    def __init__(self, r,c ,d, v):
        self.r=r
        self.c=c
        self.d=d
        self.v=v
        self.curr=0
        self.dead=False

# file = open('input.txt','r')
# input= file.readline
# tc= int(input())
def findexit():
    for r in range(N):
        for c in range(N):
            if mat[r][c]==3:
                for i in range(r,r+M):
                    for j in range(c,c+M):
                        for d in range(4):
                            ni,nj = i+dr[d],j+dc[d]
                            if mat[ni][nj]==0:
                                walls[d][i-r][j-c]=3
                                return [ni,nj]
def in_range(r,c):
    return 0<=r<N and 0<=c<N
def makemap():
    visited = deepcopy(mat)
    deadcnt=0
    for obj in stranges:
        visited[obj.r][obj.c]=-1
    while True:
        for obj in stranges:
            if not obj.dead:
                nr,nc=obj.r+dr[obj.d],obj.c+dc[obj.d]
                if in_range(nr,nc) and mat[nr][nc]<1:
                    obj.curr += obj.v
                    if visited[nr][nc]==0:
                        visited[nr][nc]=obj.curr
                    obj.r,obj.c=nr,nc
                else:
                    obj.dead=True
                    deadcnt+=1
        if len(stranges)==deadcnt:
            break

    return visited
def bfs(r,c, time):
    visited=deepcopy(mat)
    if time<visited[r][c]:
        return -1
    q=deque([[r,c, time+1]])
    visited[r][c] = 1
    while q:
        r,c,time = q.popleft()
        for d in range(4):
            nr,nc= r+dr[d],c+dc[d]
            if in_range(nr,nc):
                if not visited[nr][nc] and (smat[nr][nc]>time+1 or smat[nr][nc]==0):
                    q.append([nr,nc, time+1])
                    visited[nr][nc]=1

                elif mat[nr][nc]==4:
                    return time+1

    return -1




for _ in range(1):
    N,M,F = map(int, input().split())
    wallrange = [[M, 2*M, 3], [M, 0, 1], [2*M,M,0],[0,M,2],[M,M,0]]
    # 3:시간의벽 탈출구 1개, 1:벽, 0:통로, 4:탈출구
    mat= [list(map(int, input().split())) for _ in range(N)]
    # 동서남북, 타임머신:2
    wallmat = [[-1] * 3 * M for _ in range(3 * M)]
    walls=[]
    for i in range(5):
        wall =[list(map(int, input().split()))for _ in range(M)]
        r,c,d= wallrange[i]
        for _ in range(d):
            wall = [list(x)[::-1] for x in zip(*wall)]
        walls.append(wall)
    # r,c 시작점, v 배수마다 이, d방향으로 증식, 장애물&탈출구x 빈공간 확산
    stranges=[]
    for _ in range(F):
        r,c,d,v= map(int, input().split())
        stranges.append(Strange(r,c,d,v))
    # find 먼저
    start2 = findexit()
    for i in range(5):
        r,c,d= wallrange[i]
        wall=walls[i]
        for i in range(M):
            for j in range(M):
                wallmat[r+i][c+j] = wall[i][j]
    machine= Timemachine()
    escapetime1=bfs1(machine.r,machine.c)
    smat=makemap()
    r=bfs(start2[0],start2[1], escapetime1)
    print(r)


