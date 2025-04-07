#상하좌우
dr=[-1,1,0,0]
dc=[0,0,-1,1]
def in_range(r,c):
    return 0<=r<n and 0<=c<n
def cal_dist(r1,c1, r2,c2):
    return abs(r1-r2)+ abs(c1-c2)


class Participant:
    def __init__(self,r,c):
        self.r=r
        self.c =c
        self.dist=0
        self.escape=False
        self.moved=False
def move():
    moved=False
    for p in ppl:
        if not p.escape:
            default=cal_dist(p.r,p.c, goal[0],goal[1])
            for d in range(4):
                nr,nc=p.r+dr[d],p.c+dc[d]
                if in_range(nr,nc) and mat[nr][nc]==0 and cal_dist(nr,nc, goal[0],goal[1])< default:
                    moved=True
                    p.r=nr
                    p.c =nc
                    p.dist+=1
                    if [nr,nc]==goal:
                        p.escape=True
                    break
    return moved
def det_sqr():
    minlen=n
    for r in range(n):
        for c in range(n):
            for l in range(1,n):
                if r<=goal[0]<=r+l and c<=goal[1]<=c+l:
                    if minlen<=l:
                        break
                    for p in ppl:
                        if not p.escape and r<=p.r<=r+l and c<=p.c<=c+l and minlen>l:
                            minlen=l
                            minrc=[r,c]
                            break


    return minrc, minlen
def rotate():
    global goal
    # find sqr
    min_pos,min_len = det_sqr()

    tmp=[[0]*n for _ in range(n)]
    mc = min_pos[1] + min_len
    goalmoved=False
    for r in range(min_pos[0], min_pos[0]+min_len+1):
        mr = min_pos[0]
        for c in range(min_pos[1], min_pos[1]+min_len+1):
            tmp[mr][mc]=max(mat[r][c]-1,0)
            if not goalmoved and r==goal[0] and c==goal[1]:
                goal=[mr,mc]
                goalmoved=True
            for p in ppl:
                if not p.moved and p.r ==r and p.c ==c:
                    p.r, p.c = mr,mc
                    p.moved=True
            mr+=1
        mc-=1
    for r in range(min_pos[0], min_pos[0]+min_len+1):
        for c in range(min_pos[1], min_pos[1]+min_len+1):
            mat[r][c]= tmp[r][c]
    for p in ppl:
        p.moved=False


# file = open('input.txt', 'r')
# input = file.readline
# tc=int(input())
tc=1
for _ in range(tc):
    n,m,k = map(int, input().split())
    mat = [list(map(int, input().split())) for _ in range(n)]
    ppl=[]
    for _ in range(m):
        r,c = map(int, input().split())
        ppl.append(Participant(r-1,c-1))
    goal= list(map(lambda x: x-1, map(int, input().split())))

    for i in range(k):
        moved=move()
        all_es=True
        for p in ppl:
            if not p.escape:
                all_es=False
        if all_es: break
        rotate()
    score=0
    for p in ppl:
        score+=p.dist
    print(score)
    print(*map(lambda x:x+1,goal))

