from collections import deque
from copy import deepcopy

# 메두사는 항상 도로(0)만, 집 - 공원 최단 경로
# 전사 도로아니어도 ㄱㅊ, 메두사까지 최단경로, 집에서는 x

#상하좌우
dr=[-1,1,0,0]
dc=[0,0,-1,1]


def dist(r1,c1,r2,c2):
    return abs(r1-r2)+ abs(c1-c2)

def printmat(mat):
    for matl in mat:
        print(*matl)
    print('')
class Warrior:
    def __init__(self,r,c):
        self.r=r
        self.c=c
        self.stone=False
    def move(self):
        moved=False
        mindist=dist(self.r,self.c ,r,c)
        bestr,bestc = self.r, self.c
        for d in range(4):
            nr,nc=self.r+dr[d],self.c+dc[d]
            if in_range(nr,nc) and not seen[nr][nc]:
                currdist= dist(nr,nc,r,c)
                if currdist<mindist:
                    mindist=currdist
                    bestr, bestc = nr,nc
                    moved=True
        self.r=bestr
        self.c=bestc
        return moved



def in_range(r,c):
    return 0<=r<N and 0<=c<N
def bfs():
    q=deque([[sr,sc]])
    visited=deepcopy(mat)
    visited[sr][sc]=1
    track=[[[] for _ in range(N)]for _ in range(N)]
    while q:
        r,c = q.popleft()
        for d in range(4):
            nr,nc = r+dr[d],c+dc[d]
            if in_range(nr,nc) and not visited[nr][nc]:
                track[nr][nc]=[r,c]
                visited[nr][nc]=1
                if [nr,nc]==[er,ec]:
                    return track
                q.append([nr,nc])
    return -1
def backtrack():
    nr,nc=er,ec
    route=[[nr,nc]]
    while([nr,nc]!=[sr,sc]):
        nr, nc = track[nr][nc]
        route.append([nr,nc])
    route.reverse()
    deque(route)
    return route
def mkblocklr(r,c,maind, subd, blocked):
    while True:
        r+=subd
        c+=maind
        if not in_range(r,c):
            break
        blocked[r][c]=True
def mkblockud(r,c,maind, subd, blocked):
    while True:
        r+=maind
        c+=subd
        if not in_range(r,c):
            break
        blocked[r][c]=True


def golr(r,c,maind, seen, blocked, subd):
    nr, nc = r, c
    while in_range(nr,nc):
        if not blocked[r][nc]:
            for w in warriors:
                if w.r == r and w.c == nc:
                    if in_range(r,nc+maind):
                        blocked[r][nc+maind] = True
            if in_range(r,nc+maind) and blocked[r][nc+maind] and subd:
                mkblocklr(r, nc, maind, subd, blocked)
            seen[r][nc] = True
        else:
            break
        nc += maind
def goud(r,c,maind, seen, blocked, subd):
    nr, nc = r, c
    while in_range(nr,nc):
        if not blocked[nr][c]:
            for w in warriors:
                if w.r == nr and w.c == c:
                    if in_range(nr+maind, c):
                        blocked[nr+maind][c] = True
            if in_range(nr+maind,c) and blocked[nr+maind][c] and subd:
                mkblockud(nr, nc, maind, subd, blocked)
            seen[nr][c] = True
        else:
            break
        nr += maind

def scan(r,c,d, update=False):
    seen=[[False]*N for _ in range(N)]
    blocked=[[False]*N for _ in range(N)]

    nw=0
    if d<2:
        maind = dr[d]
        sided = [dc[2], dc[3]]
        if d==1:
            length = N-r
        else:
            length = r+1
        nr, nc = r, c
        goud(r+maind, c, maind, seen, blocked,0)
        for i in range(1,length):
            # 직선
            nr=nr+maind
            # 좌
            nc = c + i * sided[0]
            if in_range(nr,nc):
                goud(nr,nc,maind, seen, blocked, sided[0])
            # 우
            nc = c + i * sided[1]
            if in_range(nr, nc):
                goud(nr, nc, maind, seen, blocked, sided[1])
    else:
        sided=[dr[0],dr[1]]
        maind=dc[d]
        if d==3:
            length = N-c
        else:
            length = c+1
        golr(r, c+maind, maind, seen, blocked,0)
        nr, nc = r, c
        for i in range(1,length):
            nc = nc + maind
            # 상
            nr = r + i * sided[0]
            if in_range(nr, nc):
                golr(nr, nc, maind, seen, blocked,sided[0])
            # 하
            nr = r + i * sided[1]
            if in_range(nr, nc):
                golr(nr, nc, maind, seen, blocked, sided[1])
    for w in warriors:
        if seen[w.r][w.c]:
            if update:
                w.stone=True
            nw+=1
    return nw,seen



# file=open('input.txt','r')
# input=file.readline
# tc=int(input())
for _ in range(1):
    N,M = map(int, input().split())
    sr,sc,er,ec = map(int, input().split())
    tmp=list(map(int,input().split()))
    warriors=[]
    for i in range(0,2*M,2):
        r,c = tmp[i],tmp[i+1]
        warriors.append(Warrior(r,c))
    mat=[list(map(int, input().split())) for _ in range(N)]
    track = bfs()
    # 공원까지 도로 x: -1
    if track==-1:
        print(-1)
        continue
    route= backtrack()
    # 1 메두사 이동
    # 1칸, 집 - 공원 최단경로, 전사있으면 죽이기, 상하좌우(dr,dc), 경로 x 가능
    for r,c in route[1:-1]:
        warriors = [w for w in warriors if [w.r,w.c]!=[r,c]]
        # 2 메두사 시선
        # 상하좌우 선택, 다른 전사에 시야 가리기 가능 - 8방향 중 하나 골라 동일 방향 x
        # 해당 칸 바라보는 모두 전사 1턴 돌, 가장 많은 전사 돌만드는 방향 선택
        maxnumw=-1
        for d in range(4):
            numw,_ = scan(r,c,d)
            if numw>maxnumw:
                maxnumw=numw
                maxd=d
        _,seen = scan(r,c,maxd,True)

        # 3 전사 이동
        # 돌 x 전사 이동, 2칸 이동, 중복가능
        # 3-1. 메두사와 거리 좁히는 방향 선택, 상하좌우, 시야 내로 이동 x, 격자 나가기 x
        # 3-2. 동일
        move =0
        for w in warriors:
            if not w.stone:
                moved = w.move()
                if moved:
                    move+=1
                moved = w.move()
                if moved:
                    move+=1
        # 4 전사 공격
        # 메두사 같은 칸일 때 공격, 소멸
        prevw=len(warriors)
        warriors = [w for w in warriors if [w.r,w.c]!=[r,c]]
        atks=prevw-len(warriors)
        stone=0
        # 출력
        # 턴마다
        # (모든 전사 이동거리 합) (돌전사 수) (공격한 전사 수)
        for w in warriors:
            if w.stone:
                stone+=1
                w.stone=False
        print(f"{move} {stone} {atks}")
    print(0)
    # 메두사 도착 시 0





