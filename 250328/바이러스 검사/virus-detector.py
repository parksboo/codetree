


def main():
    n = int(input())
    stores = list(map(int, input().split()))
    capalead, capamem = map(int, input().split())
    total = 0
    for store in stores:
        store -= capalead
        total += 1
        if store > 0:
            total += store // capamem
            if store % capamem:
                total += 1
    return total

# file=open('test.txt','r')
# input = file.readline
# tc= int(input())
tc=1
for i in range(tc):
    r = main()
    print(r)

