from collections import deque
#우하좌상
dr=[0,1,0,-1]
dc=[1,0,-1,0]


def choice_attacker():
    minatk=5001
    for r in range(n):
        for c in range(m):
            if mat[r][c]:
                atk = mat[r][c]
                if minatk>atk:
                    minatk=atk
                    minpos = [r,c]
                elif minatk == atk:
                    if atkhistory[r][c] > atkhistory[minpos[0]][minpos[1]]:
                        minpos = [r, c]
                    elif atkhistory[r][c] == atkhistory[minpos[0]][minpos[1]]:
                        if sum(minpos) < r+c:
                            minpos = [r, c]
                        elif sum(minpos)==r+c:
                            if c> minpos[1]:
                                minpos = [r, c]

    return minpos, minatk+m+n

def choice_strong():
    maxatk=-1

    for r in range(n):
        for c in range(m):
            atk = mat[r][c]
            if maxatk < atk:
                maxatk = atk
                maxpos = [r, c]
            elif maxatk == atk:
                if atkhistory[r][c] < atkhistory[maxpos[0]][maxpos[1]]:
                    maxpos = [r, c]
                elif atkhistory[r][c]== atkhistory[maxpos[0]][maxpos[1]]:
                    if sum(maxpos) > r + c:
                        maxpos = [r, c]
                    elif sum(maxpos) == r + c:
                        if c < maxpos[1]:
                            maxpos = [r, c]
    return maxpos, maxatk
def up_atk(active_pos):
    for r in range(n):
        for c in range(m):
            if mat[r][c] and not attacked[r][c]:
                mat[r][c]+=1
def reset_atked():
    for r in range(n):
        for c in range(m):
            attacked[r][c]=False
def bfs(start, end):
    q= deque([start])
    track=[[[] for _ in range(m)] for _ in range(n)]
    track[start[0]][start[1]]=[-1,-1]

    while(q):
        r,c = q.popleft()
        for d in range(4):
            nr,nc = (r+dr[d])%n, (c+dc[d])%m
            if not mat[nr][nc] ==0 and not track[nr][nc]:
                track[nr][nc]=[r,c]
                q.append([nr,nc])
                if nr==end[0] and nc==end[1]:
                    return backtrack([nr,nc], track)
    return []


def backtrack(pos, track):
    r,c=pos
    route =[]

    while not (r==-1 and c==-1):
        route.append([r, c])
        r,c=track[r][c]
    route.reverse()
    return route

def drop(pos):
    r,c=pos
    mat[r][c]= max(mat[r][c] -deal, 0)
    attacked[r][c] = True
    for dr in [1,0,-1]:
        for dc in [1,0,-1]:
           nr,nc = (r+dr)%n, (c+dc)%m
           if mat[nr][nc]:
               mat[nr][nc]= max(mat[nr][nc] - (deal//2), 0)
               attacked[nr][nc]=True
def laser(route):
    for r,c in route[1:-1]:
        mat[r][c]= max(mat[r][c] - (deal//2), 0)
        attacked[r][c] = True
    r,c = strpos
    mat[r][c] = max(mat[r][c] - deal, 0)
    attacked[r][c] = True


def attack(wkpos, strpos):
    route = bfs(wkpos, strpos)
    if not route:
        drop(strpos)
    else:
        laser(route)




# file = open('input.txt','r')
# input= file.readline
# tc= int(input())
for _ in range(1):
    n,m,k = map(int, input().split())
    handi = n+m
    mat = [list(map(int, input().split()))for _ in range(n)]
    atkhistory =[[0]*m for _ in range(n)]
    attacked = [[False]*m for _ in range(n)]
    for i in range(1, k+1):
        wkpos, wkatk = choice_attacker()
        atkhistory[wkpos[0]][wkpos[1]]= i
        deal = wkatk
        strpos, stratk= choice_strong()
        mat[wkpos[0]][wkpos[1]] += n + m
        attacked[wkpos[0]][wkpos[1]]=True
        attack(wkpos, strpos)

        up_atk([wkpos, strpos])
        reset_atked()
    dump, atk = choice_strong()
    print(atk)