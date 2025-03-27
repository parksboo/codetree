dr = [-1,0,1,0]
dc = [0,1,0,-1]

def in_range(r,c):
    return 0<=r<n and 0<=c<n
def crash(player1, player2):
    force1 = player1.s+player1.gun
    force2 = player2.s+player2.gun
    if force1>force2:
        player1.point += force1 - force2
        player2.move_2()
        player1.grab()
    elif force2>force1:
        player2.point += force2 - force1
        player1.move_2()
        player2.grab()
    else:
        if player1.s>player2.s:
            player2.move_2()
            player1.grab()
        else:
            player1.move_2()
            player2.grab()



class Player:
    def __init__(self,r,c,d,s):
        self.r= r
        self.c=c
        self.d=d
        self.s=s
        self.gun = 0
        self.point =0

    def grab(self):
        r= self.r
        c=self.c
        tmp_rc = []
        for n in mat[r][c]:
            if n==0:
                continue
            if self.gun < n:
                if self.gun:
                    tmp_rc.append(self.gun)
                self.gun = n
            else:
                tmp_rc.append(n)
        mat[r][c] = tmp_rc

    def move(self):
        nr,nc = self.r+dr[self.d],self.c+dc[self.d]
        if not in_range(nr,nc):
            self.d = (self.d + 2) % 4
            nr,nc = self.r+dr[self.d],self.c+dc[self.d]

        for p in players:
            # crash
            if nr == p.r and nc == p.c:
                self.r = nr
                self.c = nc
                crash(p, self)
                return
        self.r = nr
        self.c = nc
        self.grab()


    def move_2(self):
        prevr, prevc= self.r, self.c
        if self.gun:
            mat[self.r][self.c].append(self.gun)
            self.gun =0
        for k in range(4):
            d = (k+self.d)%4
            nr, nc = self.r + dr[d], self.c + dc[d]
            is_pass=False
            if in_range(nr,nc):
                for p in players:
                    # crash
                    if nr == p.r and nc == p.c:
                        is_pass = True
                        continue
                if is_pass:
                    continue
                self.r = nr
                self.c = nc
                self.d = d
                self.grab()
                return










# file = open('input.txt','r')
# input = file.readline

# tc = int(input())
tc=1
for _ in range(tc):
    n,m,k = map(int, input().split())
    mat =[list(map(int, input().split())) for _ in range(n)]
    for r in range(n):
        for c in range(n):
            num = mat[r][c]
            mat[r][c]= [num]

    players=[]
    for _ in range(m):
        r,c,d,s = map(int, input().split())
        players.append(Player(r-1,c-1,d,s))

    result =[]
    for _ in range(k):
        for player in players:

            # for p in players:
            #     print(f'pos r:{p.r} c:{p.c} d:{p.d} gun:{p.gun}')
            # for matl in mat:
            #     print(*matl)
            player.move()
            # except:
            #     print(player.r, player.c)
            #     for m in mat:
            #         print(m)


    for player in players:
        result.append(player.point)
    print(*result)


