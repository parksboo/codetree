#상우하좌
dr=[-1,0,1,0]
dc=[0,1,0,-1]
def in_range(r,c):
    return 0<=r<L and 0<=c<L
class Knight:
    def __init__(self,n, r,c,h,w,k):
        self.n=n
        self.r=r
        self.c=c
        self.h=h
        self.w=w
        self.k=k
        self.dmg=0

    def fill(self, mat):
        for r in range(self.r, self.r + self.h + 1):
            for c in range(self.c, self.c + self.w + 1):
                mat[r][c] = self.n
    def scan(self,d):
        global enable
        if mat_k[self.r][self.c] not in scanmove:
            scanmove.append(mat_k[self.r][self.c])
        if not enable:
            return
        for r in range(self.r +dr[d], self.r + self.h+dr[d] + 1):
            for c in range(self.c+dc[d], self.c + self.w +dc[d] + 1):
                if not in_range(r,c) or mat[r][c]==2:
                    enable= False
                    return
                elif mat_k[r][c]==0 or mat_k[r][c]==self.n:
                    continue
                else:
                    knights[mat_k[r][c]].scan(d)

    def move(self,d):
        global mat_nk, mat_k,enable
        mat_nk = [[0] * L for _ in range(L)]
        if not in_range(self.r,self.c) or mat[self.r][self.c] == 2:
            enable = False
        else:
            self.scan(d)
        if enable:
            self.r+=dr[d]
            self.c+=dc[d]
            for numi in scanmove[1:]:
                if knights[numi].k>0:
                    knights[numi].realmove(d)
            for k in knights:
                if k.k>0:
                    k.fill(mat_nk)
            mat_k = mat_nk


    def realmove(self, d):
        self.r+=dr[d]
        self.c+=dc[d]
        for r in range(self.r, self.r+self.h+1):
            for c in range(self.c, self.c+self.w+1):
                trap=mat[r][c]
                if trap and self.k>0:
                    self.k-=1
                    self.dmg+=1




# file = open('input.txt','r')
# input = file.readline
# tc= int(input())
for _ in range(1):
    L,N,Q = map(int, input().split())
    knights=[Knight(0,0,0,0,0,0)]
    mat = [list(map(int, input().split())) for _ in range(L)]
    for n in range(1,N+1):
        r,c,h,w,k = map(lambda x: x-1, map(int, input().split()))
        knights.append(Knight(n,r,c,h,w,k))
    cmds = [list((map(int, input().split()))) for _ in range(Q)]
    mat_k =[[0]*L for _ in range(L)]
    mat_nk= [[0]*L for _ in range(L)]
    for k in knights:
        k.k+=1
        k.fill(mat_k)


    for cmd in cmds:

        knum, d = cmd
        cmdknight= knights[knum]
        if cmdknight.k>0:
            enable = True
            scanmove=[]
            cmdknight.move(d)
    score=0
    for k in knights:
        if k.k>0:
            score+=k.dmg
    print(score)
