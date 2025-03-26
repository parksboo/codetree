REVERSE=1
EMPTY =0
HEAD =1
REST=2
TAIL =3
TRAIL =4
dr =[0,-1,0,1]
dc =[1,0,-1,0]

def in_range(r,c):
    return 0<=r<n and 0<=c<n

class HumanAndTrack:
    def __init__(self, r, c, role, is_human):
        self.r = r
        self.c = c
        self.role= role
        self.is_human=is_human
        self.score=0
    def is_track(self):
        self.role =4
        self.is_human =False
        self.score=0
def dfs(r,c,n):
    for d in range(4):
        nr,nc = r+dr[d], c+dc[d]
        if in_range(nr,nc) and 1<mat[nr][nc]<=4 and not visited[nr][nc]:
            visited[nr][nc]=True
            if mat[nr][nc]==4:
                is_human =False
            else:
                is_human =True
                n += 1
            humanline.append(HumanAndTrack(nr,nc,mat[nr][nc], is_human))
            n= dfs(nr,nc, n)
    return n
def cal_score(linenum):
    line = humanlines[linenum]
    head, tail, length = metadata[linenum]
    if not line[(head + 1)%len(line)].is_human:
        dir = -1
    else:
        dir = 1
    curr = head
    num = 1

    while line[curr].is_human:
        line[curr].score = num ** 2
        num += 1
        curr = (curr + dir) % len(line)
def reverse_line(linenum):
    line = humanlines[linenum]
    head,tail, length=metadata[linenum]
    line[head].role = TAIL
    line[tail].role = HEAD
    metadata[linenum]=[tail, head, length]
    cal_score(linenum)


def move_line():
    for i,line in enumerate(humanlines):
        head,tail, length=metadata[i]
        n = len(line)
        line[tail].is_track()
        line[head].role = 2
        if not line[(head + 1)%n].is_human:
            dir = 1

        else:
            dir = -1





        head=(head+dir)%n
        tail=(tail+dir)%n
        line[head].role = HEAD
        line[tail].role = TAIL
        line[head].is_human = True
        line[tail].is_human = True
        metadata[i] = [head, tail, length]
        cal_score(i)






def throw_ball(round):
    global score
    modround = round%(4*n)
    d,p=divmod(modround, n)
    r,c = startpos[d]
    r+=p*dr[(d-1)%4]
    c+=p*dc[(d-1)%4]
    for k in range(n):
        nr,nc = r+k*dr[d],c+k*dc[d]
        if mat[nr][nc]:
            for i,line in enumerate(humanlines):
                for human in line:
                    if human.is_human and human.r== nr and human.c==nc:
                        score+=human.score
                        reverse_line(i)
                        return


# file = open('input.txt', 'r')
# input = file.readline
# tc = int(input())
tc=1
for _ in range(tc):
    n,m,k = map(int, input().split())
    mat = []
    for _ in range(n):
        mat.append(list(map(int, input().split())))
    humanlines=[]
    metadata=[]
    length=[]
    visited = [[False]*n for _ in range(n)]
    startpos = [(0, 0), (n - 1, 0), (n-1,n-1), (0,n-1)]
    score=0
    for r in range(n):
        for c in range(n):
            if mat[r][c] == HEAD and not visited[r][c]:
                visited[r][c]=True
                humanline = []
                humanline.append(HumanAndTrack(r, c, HEAD, True))
                length.append(dfs(r,c,1))
                humanlines.append(humanline)
    for idx1 in range(len(humanlines)):
        line =humanlines[idx1]
        tmp=[0,0,0]
        for idx in range(len(line)):
            if line[idx].role == 1:
                tmp[0] = idx
            elif line[idx].role == 3:
                tmp[1] = idx
        tmp[2] = length[idx1]
        metadata.append(tmp)
        cal_score(idx1)

    for round in range(k):
        move_line()
        throw_ball(round)
    print(score)

        # print(round)
        # k=1
        # for line in humanlines:
        #     print(f'line : {k}')
        #     print(metadata[k-1])
        #     k+=1
        #     for human in line:
        #         print(f'{human.r} {human.c} : {human.role} , {human.score}')



