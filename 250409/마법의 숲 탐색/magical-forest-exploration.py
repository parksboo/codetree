from collections import deque
# 상우하좌
dr=[-1,0,1,0]
dc=[0,1,0,-1]
checkl=[[-1,-1],[0,-2],[1,-1],[2,-1],[1,-2]]
checkr=[[-1,1],[0,2],[1,1],[2,1],[1,2]]
checkd=[[2,0],[1,1],[1,-1]]

def in_range(r,c):
    return 0<=r<R+1 and 0<=c<C

def reset():
    global mat
    mat = [[0]*C for _ in range(R+1)]

class Golem:
    def __init__(self,c,d, n):
        self.c=c
        self.r=0
        self.d=d
        self.n=n
    def godown(self):
        fail = False
        for r,c in checkd:
            nr,nc=self.r+r,self.c+c
            if not in_range(nr,nc) or mat[nr][nc]:
                fail=True
        if not fail:
            self.r+=1
        return fail

    def insert(self):
        fail = False
        if mat[self.r + 1][self.c] or self.c>C-2 or self.c<1:
            fail = self.gol(1)
            if fail:
                fail = self.gor(1)
        else:
            while self.r<2 and not fail:
                if self.godown():
                    fail = self.gol(1)
                    if fail:
                        fail = self.gor(1)

        return fail

    def move(self):
        global prevr,prevc
        fail = self.insert()
        if fail:
            reset()
            return True
        else:
            while not fail:
                fail = self.godown()
                if fail:
                    fail = self.gol(0)
                    if fail:
                        fail = self.gor(0)
        exits[self.n]=self.d
        return False

    def gol(self, start):
        fail = False
        for r,c in checkl[start:]:
            nr,nc=r+self.r, c+self.c
            if not in_range(nr,nc) or mat[nr][nc]:
                fail=True
        if not fail:
            self.r+=1
            self.c-=1
            self.d= (self.d-1)%4
        return fail
    def gor(self, start):
        fail = False
        for r, c in checkr[start:]:
            nr, nc = r + self.r, c + self.c
            if not in_range(nr, nc) or mat[nr][nc]:
                fail = True
        if not fail:
            self.r += 1
            self.c += 1
            self.d = (self.d + 1) % 4
        return fail


    def fill(self):
        mat[self.r][self.c]=self.n
        for d in range(4):
            nr,nc= self.r+dr[d], self.c+dc[d]
            mat[nr][nc]=self.n
        return self.bfs()


    def bfs(self):
        r,c= self.r,self.c
        maxr=r
        visited=[[False]*C for _ in range(R+1)]
        visited[r][c] = True
        n= self.n
        exit= self.d
        q = deque([[r,c,n, exit]])
        while q:
            r,c,n,exit = q.popleft()
            for d in range(4):
                nr,nc = r+dr[d],c+dc[d]
                if d==exit:
                    if in_range(nr,nc) and not visited[nr][nc] and mat[nr][nc]:
                        q.append([nr, nc, mat[nr][nc], exits[mat[nr][nc]]])
                        visited[nr][nc]=True
                        maxr = max(maxr,nr)
                    continue

                if in_range(nr,nc) and not visited[nr][nc] and mat[nr][nc]==n:
                    q.append([nr,nc,n, exit])
                    visited[nr][nc] = True
                    maxr = max(maxr, nr)
        return maxr

def printmat():
    for matl in mat:
        print(*matl)
    print('')

# file = open('input.txt','r')
# input= file.readline
# tc= int(input())
for _ in range(1):
    R,C,K = map(int, input().split())
    golems=deque([])
    exits={}
    score =0
    for n in range(1,K+1):
        c,d = map(int, input().split())
        golems.append(Golem(c-1,d,n))
    mat = [[0]*C for _ in range(R+1)]
    while(golems):
        golem=golems.popleft()
        fail = golem.move()
        if not fail:
            score +=golem.fill()
        # printmat()

    print(score)

