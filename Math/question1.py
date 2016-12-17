def dd(tup_x,tup_y):
    n = len(tup_x)
    for i in range(1, n):
        j=n-1;
        while j >= i:
            tup_y[j] = (tup_y[j] - tup_y[j - 1]) / (tup_x[j] - tup_x[j - i])
            j = j - 1
    print(tup_y)
    return tup_y

def ni():
    tup_y = [9.01, 8.96, 7.96, 7.97, 8.02, 9.05, 10.13, 11.18, 12.26, 13.28, 13.32, 12.61, 11.29, 13.22, 9.15, 7.90,
             7.95, 8.86, 9.81, 10.80, 10.93];
    tup_x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    ycs=dd(tup_x,tup_y)
    j=len(ycs)-1
    yy=ycs[j]
    while j>=0:
        yy=yy*(11.2-tup_x[j])+ycs[j]
        j=j-1
    print(yy)