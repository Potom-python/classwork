import copy
a = int(input())
papa = [list(map(int, input().split())) for _ in range(a)]
cock = int(input())
pro = copy.deepcopy(papa)

for k in range(cock - 1):
    tvar = [[0] * a for _ in range(a)]
    for u in range(a):
        for i in range(a):
            kal = 0
            for j in range(a):
                kal += papa[i][j] * pro[j][u]
            tvar[i][u] = kal
    papa = tvar.copy()
for d in tvar:
    print(*d)