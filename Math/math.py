# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

def dd(tup_x, tup_y):
    n = len(tup_x)
    m=[0]*n
    for i in range(0, n):
        m[i] = tup_y[i];
    for i in range(1, n):
        j = n - 1;
        while j >= i:
            m[j] = (m[j] - m[j - 1]) / (tup_x[j] - tup_x[j - i])
            j -= 1
    return m


def ni(xxArray,tup_x,tup_y):
    ycs = dd(tup_x, tup_y)
    yyArray=[]
    for xx in xxArray:
        j = len(ycs)-1
        yy = ycs[j]
        j=j-1
        while j >= 0:
            yy = yy * (xx - tup_x[j]) + ycs[j]
            j -= 1
        yyArray.append(yy)
    return yyArray

def tss(a, b, c, d, n, x):

    u = [0] * n
    y = [0] * n
    l = [0] * n
    u[0] = b[0]
    y[0] = d[0]
    for k in range(1, n):
        l[k] = a[k] / u[k - 1];
        u[k] = b[k] - l[k] * c[k - 1]
        y[k] = d[k] - l[k] * y[k - 1]
    x[n - 1] = y[n - 1] / u[n - 1]
    k = n - 2
    while k >= 0:
        x[k] = (y[k] - c[k] * x[k + 1]) / u[k]
        k -= 1
    return x


def find_k(x, _x):

    n = len(x)
    for i in range(0, n - 1):
        if (_x <= x[i]):
            return i
    return -1


def splinem(x, y, lambda_0, d_0, u_n, d_n):

    n = len(x);
    M = [0] * (n);
    h = [0] * (n + 1)
    a = [0] * (n)
    b = [0] * (n)
    c = [0] * (n)
    for i in range(0, n):
        M[i] = y[i];
    for k in range(1, 3):
        i = n - 1;
        while (i > (k-1)):
            M[i] = (M[i] - M[i - 1]) / (x[i] - x[i - 1])
            i -= 1
    h[1] = x[1] - x[0]
    for i in range(1, n - 1):
        h[i + 1] = x[i + 1] - x[i]
        c[i] = h[i + 1] / (h[i] + h[i + 1])
        a[i] = 1 - c[i]
        b[i] = 2
        M[i] = 6 * M[i + 1]
    M[0] = d_0
    M[n - 1] = d_n
    c[0] = lambda_0
    b[0] = 2
    a[n - 1] = u_n
    b[n - 1] = 2
    n = len(b)
    M = tss(a, b, c, M, n, M)
    return M


def evaspline(xxArray,tup_x,tup_y):
    # printArrayASJson(tup_x[xx],tup_y[xx])
    M = splinem(tup_x, tup_y, 0.5, 0, 0.5, 0)
    # M = splinem(tup_x, tup_y, -2, 4.02, -2, -1.8)
    yyArray=[]
    for xx in xxArray:
        yy=0
        k = find_k(tup_x, xx)
        h = tup_x[k] - tup_x[k - 1]
        xbar = tup_x[k] - xx
        xdian = xx - tup_x[k - 1]
        yy = (M[k - 1] * (xbar ** 3) / 6 + M[k] * (xdian ** 3)/6 + (tup_y[k - 1] * M[k - 1] * (h ** 2) / 6) * xbar + (
        tup_y[k] - (M[k] * h ** 2 )/ 6) * xdian) / h

        yyArray.append(yy)
    return yyArray


def printArrayASJson(x, y):
    n = len(x)
    for i in range(0,n):
        print("[" + str(x[i]) + "," + str(y[i]) + "],")

def question1():

    y = [9.01, 8.96, 7.96, 7.97, 8.02, 9.05, 10.13, 11.18, 12.26, 13.28, 13.32, 12.61, 11.29, 10.22, 9.15, 7.90,
                 7.95, 8.86, 9.81, 10.80, 10.93]
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    printArrayASJson(x,y)

    xx=0
    xxArray =[]
    while xx<=20:
        xxArray.append(xx)
        xx+=0.01

    yyArray = evaspline(xxArray,x,y)

    yyArray = ni(xxArray,x,y)
    #printArrayASJson(xxArray,yyArray)

    plt.figure(figsize=(8,4))
    plt.plot(np.array(xxArray),np.array(yyArray),label="$ni$",color="green")
    plt.plot(np.array(x),np.array(y),'*',label="$data$",color="red")
    plt.ylim(0,20)
    plt.legend()
    plt.show()

def question2():
    x=range(0,25)
    y=[15,14,14,14,14,15,16,18,20,20,23,25,28,31,34,31,29,27,25,24,22,20,18,17,16]
    plt.figure(figsize=(8,4))
    plt.plot(np.array(x),np.array(y),'*',label="$data$",color="red")
    plt.ylim(10,40)
    plt.legend()
    plt.show()


def lss():
    """形成矩阵"""


# question1()
question2()