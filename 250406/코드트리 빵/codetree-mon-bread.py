from collections import deque
import copy
# 상 좌 우 하
dr = [-1,0,0,1]
dc = [0,-1,1,0]

class Pedestrian:
    def __init__(self, r,c,goal):
        self.r=r
        self.c=c
        self.goal=goal
    def mkpath(self,path):
        self.path = path
def in_range(r,c):
    return 0<=r<n and 0<=c<n
def bfs(start,dest):

    q = deque([(start[0],start[1],0)])
    visited=[[[] for _ in range(n)] for _ in range(n)]
    visited[start[0]][start[1]]=[-1,-1]

    while q:
        r,c,dist = q.popleft()
        for d in range(4):
            nr,nc = r+dr[d], c+dc[d]
            if in_range(nr,nc) and not mat[nr][nc]==2 and not visited[nr][nc]:
                visited[nr][nc]= [r,c]
                q.append((nr,nc,dist+1))
                if (nr,nc) == dest:
                    return dist+1, visited

def backtrack(pathmap, goal):
    path=[]
    r,c = goal
    path.append((r,c))
    while pathmap[r][c]!=[-1,-1]:
        r,c=pathmap[r][c]
        path.append((r,c))
    path.reverse()
    return path


def search_base(t):
    global maxlen
    goal=goals[t]
    min_dist = 1024
    for r in range(n):
        for c in range(n):
            if mat[r][c]==1:
                length, path_map = bfs((r,c), goal)
                if min_dist>length:
                    min_dist=length
                    min_path_map =path_map
                    minpos=(r,c)
    path = backtrack(min_path_map, goal)
    return minpos, path

def move():
    for ped in ppl:
        if ped.path:
            r,c=ped.path.popleft()
            ped.r=r
            ped.c=c
            if (r,c)==ped.goal:
                mat[r][c]=2
def new_ped(t):
    pos, path = search_base(t)
    ppl.append(Pedestrian(pos[0],pos[1], goals[t]))
    ppl[t].mkpath(deque(path[1:]))
    mat[pos[0]][pos[1]] = 2
def repath():
    for ped in ppl:
        if (ped.r,ped.c) != ped.goal:
            length, path_map = bfs((ped.r,ped.c), ped.goal)
            path = backtrack(path_map, ped.goal)
            ped.mkpath(deque(path[1:]))

# file = open('input.txt','r')
# input = file.readline
# tc = int(input())
tc=1
for _ in range(tc):
    n,m = map(int, input().split())
    mat = [list(map(int, input().split())) for _ in range(n)]
    goals = [tuple(map(lambda x: x-1, map(int,input().split()))) for _ in range(m)]
    ppl=[]
    minute=0
    for t in range(m):
        move()
        new_ped(t)
        repath()
        minute+=1
    while True:
        move()
        repath()
        cnt=0
        minute += 1
        for ped in ppl:
            cnt+=len(ped.path)
        if not cnt:
            print(minute)
            break