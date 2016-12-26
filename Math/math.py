# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import binascii
import struct

# 定义sgn函数
sgn = lambda x: 1 if x > 0 else -1 if x < 0 else 0


def dd (tup_x, tup_y):
    """
    给定插值数据点，计算牛顿插值多项式中的系数，也就是差商表并保存到m中
    :param tup_x: 数据点x
    :param tup_y: 数据点Y坐标
    :return:
    """
    #获取插值数据点个数
    n = len(tup_x)
    #生成保存差商表的数组
    m = tup_y[:]
    #迭代计算差商表
    for i in range(1, n):
        j = n - 1;
        while j >= i:
            m[j] = (m[j] - m[j - 1]) / (tup_x[j] - tup_x[j - i])
            j -= 1
            # print(m[j], i, j)
    return m


def ni (xxArray, tup_x, tup_y):
    """
    对于给定的x，本函数用牛顿插值公式计算N值。其中dd函数是生成差商表的函数
    :param xxArray: 给定x数组
    :param tup_x: 插值点x坐标值
    :param tup_y: 插值点Y坐标值
    :return:
    """
    ycs = dd(tup_x, tup_y)
    yyArray = []
    for xx in xxArray:
        j = len(ycs) - 1
        yy = ycs[j]
        j = j - 1
        while j >= 0:
            yy = yy * (xx - tup_x[j]) + ycs[j]
            j -= 1
        yyArray.append(yy)
    return yyArray


def tss (a, b, c, d, n, x):
    """
    计算三对角线方程组，系数存于数组a，b，c中
    其中a,b,c,d的具体含义
    :param a:
    :param b:
    :param c:
    :param d:
    :param n:
    :param x:
    :return:
    """
    u = [0] * n
    y = [0] * n
    l = [0] * n
    u[0] = b[0]
    y[0] = d[0]
    # 追的过程
    for k in range(1, n):
        l[k] = a[k] / u[k - 1];
        u[k] = b[k] - l[k] * c[k - 1]
        y[k] = d[k] - l[k] * y[k - 1]
    x[n - 1] = y[n - 1] / u[n - 1]
    k = n - 2
    # 赶的过程
    while k >= 0:
        x[k] = (y[k] - c[k] * x[k + 1]) / u[k]
        k -= 1
    return x


def find_k (x, _x):
    """
    用于找出_x值所在的插值区间，返回插值区间的上限对应的插值点的坐标值
    :param x: 插值点数组
    :param _x: _x要判断的x值
    :return: 返回-1说明_x点不在所有的区间内。
    """
    n = len(x)
    for i in range(0, n - 1):
        if (_x < x[i]):
            return i
    return -1



def splinem (x, y, lambda_0, d_0, u_n, d_n):
    """
    计算三次样条的参数Mi，存放于数组M中，边界参数根据不同的边界条件确定
    :param x: 插值点数据x坐标数组
    :param y: 插值点数据y坐标数组
    :param lambda_0: 边界条件
    :param d_0: 边界条件
    :param u_n: 边界条件
    :param d_n: 边界条件
    :return: 返回M的值
    """
    #获取插值点的数目
    n = len(x);
    #初始化需要计算的数组
    #因为h在函数中是从h1开始的，h0没有使用，h的值要大1
    h = [1] * (n + 1)
    a = [1] * (n)
    b = [1] * (n)
    c = [1] * (n)
    M = y[:]
    #首先计算3阶差商，行成3阶差商表
    for i in range(1, 3):
        j = n - 1
        while j >= i:
            M[j] = (M[j] - M[j - 1]) / (x[j] - x[j - i])
            j -= 1
    #计算h1
    h[1] = x[1] - x[0]
    #计算矩阵中的a，b，c
    for i in range(1, n - 1):
        h[i + 1] = x[i + 1] - x[i]
        c[i] = h[i + 1] / (h[i] + h[i + 1])
        a[i] = 1 - c[i]
        b[i] = 2
        #M对应的是边界条件d,需要根据公式调整顺序
        M[i] = 6 * M[i + 1]
    #矩阵的各个参数进行补全
    M[0] = d_0
    M[n - 1] = d_n
    c[0] = lambda_0
    b[0] = 2
    a[n - 1] = u_n
    b[n - 1] = 2
    #获取矩阵中系数b的大小
    n = len(b)
    #调用TSS算法，计算M的值
    M = tss(a, b, c, M, n, M)
    return M


def evaspline (xxArray, tup_x, tup_y):
    # printArrayASJson(tup_x[xx],tup_y[xx])
    # M = splinem(tup_x, tup_y, 0.5, 0, 0.5, 0)
    #利用SPLINEM算法计算M系数的值
    """
    利用数据点tup_x,tup_y做三次插值样条函数，然后求相应的函数值
    :param xxArray: 待计算的x
    :param tup_x: 数据点x坐标
    :param tup_y: 数据点y坐标
    :return:
    """
    M = splinem(tup_x, tup_y, -2, -0.0392, -2, -0.018)
    #ss = []
    yyArray = []
    l = [0] * (len(xxArray) + 1)
    for xx in xxArray:
        yy = 0
        k = find_k(tup_x, xx)
        h = tup_x[k] - tup_x[k - 1]
        xbar = tup_x[k] - xx
        xdian = xx - tup_x[k - 1]
        # 样条插值公式计算对应的y值
        yy = (M[k - 1] * (xbar ** 3) / 6 + M[k] * (xdian ** 3) / 6 + (tup_y[k - 1] - M[k - 1] * (h ** 2) / 6) * xbar + (
            tup_y[k] - (M[k] * h ** 2) / 6) * xdian) / h
        yyArray.append(yy)
        #ss.append(-M[k - 1] * (xbar ** 2) / (2 * h) + M[k] * (xdian ** 2) / (2 * h) + (tup_y[k] - tup_y[k - 1]) / h - (
        #M[k] - M[k - 1]) * h / 6)
    # 利用曲线积分公式计算曲线的长度，求出电缆的长度
    #for j in range(len(xxArray)):
        # l[j + 1] += (1 + ss[j] ** 2) ** 0.5 * (20 / len(xxArray))
    #print(l[len(xxArray)])
    return yyArray


def printArrayASJson (x, y):
    n = len(x)
    for i in range(0, n):
        print("[" + str(x[i]) + "," + str(y[i]) + "],")


def initG (x, y, n):
    g = [[] for i in range(len(x))]
    for i in range(len(x)):
        for j in range(n + 1):
            g[i].append(x[i] ** j)
        g[i].append(y[i])
    for xxx in g:
        print(xxx)
    return g


def printDataInfo (path):
    print("文件路径", path)
    f = open(path, "rb")
    m = 8
    # 矩阵文件头的个数
    # 读取文件头
    fhead = f.read(4 * 5)
    # hexstr = binascii.b2a_hex(fhead)  #得到一个16进制的数
    a = struct.unpack("IIIII", fhead)
    id = hex(a[0])
    version = hex(a[1])
    n = a[2]
    q = a[3]
    p = a[4]
    print("文件标识部分-------------")
    print("文件标识符", id)
    print("数据文件版本号", version)
    print("矩阵描述部分-------------")
    print("方程阶数", n)
    print("带状矩阵上带宽", q)
    print("带状矩阵下带宽", p)
    print("------------------")
    # f.seek(0,3)
    if (version == '0x102'):
        print("矩阵为未压缩带状矩阵")
        count = 0
        ma = [[] for i in range(a[2])]
        j = k = 0
        while j <= (n - 1):
            fbody = f.read(4)
            count += 1
            s = struct.unpack("f", fbody)
            ma[j].append(s[0])
            k += 1
            if (k == (a[2])):
                k = 0
                j += 1
        if (count == n ** 2):
            print("矩阵数据正确")
        j = 0
        b = [0] * a[2]
        while j < (a[2]):
            fbody2 = f.read(4)
            s = struct.unpack("f", fbody2)
            b[j] = s[0]
            j += 1
        if (f.read(4)):
            print("数据没有用完")
        else:
            print("数据已经用完")
            # gaussPP(ma,b,p,q,version)
            # choleskyb(ma,n,q,p,b)
    if (version == "0x202"):
        print("矩阵为压缩带状矩阵")
        count = 0
        ma = [[] for i in range(a[2])]
        j = k = 0
        while j <= (n - 1):
            fbody = f.read(4)
            count += 1
            s = struct.unpack("f", fbody)
            ma[j].append(s[0])
            k += 1
            if (k == (p + q + 1)):
                k = 0
                j += 1
        if (count == n * (p + q + 1)):
            print("矩阵数据正确")
        j = 0
        b = [0] * a[2]
        while j < (a[2]):
            fbody2 = f.read(4)
            s = struct.unpack("f", fbody2)
            b[j] = s[0]
            j += 1
        if (f.read(4)):
            print("数据没有用完")
        else:
            print("数据已经用完")
        gaussPP2(ma, b, p, q)


def choleskyb (aa, n, q, p, b):
    """
    本函数针对给定带宽为p的对称正定矩阵A计算其Cholesky矩阵G，其元存放于A的相应位置
    :param aa: 对阵正定带状矩阵
    :param n: 矩阵的阶数
    :param p: 矩阵的带宽
    """
    a = aa[:]
    u = [[0 for i in range(n)] for i in range(n)]
    l = [[0 for i in range(n)] for i in range(n)]
    for i in range(0, n):
        temp1 = n
        if (i + q < temp1):
            temp1 = i + q + 1
        for j in range(i, temp1):
            temp2 = 0
            if (i - p > 0):
                temp2 = i - p
            if (j - q > i - p):
                temp2 = j - q
            sum = 0
            for t in range(temp2, i):
                sum += l[i][t] * u[t][j]
            u[i][j] = a[i][j] - sum
            temp2 = 0
            if (j - p > temp2):
                temp2 = j - p
            if (i - q > temp2):
                temp2 = i - q
            for t in range(temp2, i):
                sum += l[i][t] * u[t][j]
            l[j][i] = (a[j][i] - sum) / u[i][i]
    print("a矩阵")
    for aaa in a:
        print(aaa)
    print("l矩阵")
    for lll in l:
        print(lll)
    print("u矩阵")
    for uuu in u:
        print(uuu)

    # 回代的过程
    y = [0] * n
    x = [0] * n
    y[0] = b[0]
    for k in range(1, n):
        sum = 0
        temp = 0
        if (k - p > 0):
            temp = k - p
        for j in range(temp, k):
            sum += y[j] * l[k][j]
        y[k] = b[k] - sum

    print(y)
    x[n - 1] = y[n - 1] / u[n - 1][n - 1]
    k = n - 2
    while k >= 0:
        sum = 0
        temp = n
        if (k - p < n - 1):
            temp = k - p + 1
        for j in range(k + 1, temp):
            temp += l[j][k] * x[j]
        x[k] = (y[k] - temp) / u[k][k]
        k -= 1
    print(x)


def gaussPP (aa, bb):
    a = aa[:][:]
    b = bb[:][:]
    n = len(a)
    for k in range(0, n):
        max = abs(a[k][k])
        maxi = k
        # for s in range(k+1,n):
        #     if(abs(a[s][k])>max):
        #         max=abs(a[s][k])
        #         maxi=s
        if (max == 0):
            print("主元为零")
        if (k != maxi):
            temp = a[k][:]
            a[k] = a[maxi][:]
            a[maxi] = temp[:]
            tempb = b[k]
            b[k] = b[maxi]
            b[maxi] = tempb
            print("进行主元交换")
            print("该", k, "迭代的主元是", max, "位于第", maxi, "行")
        for i in range(k + 1, n):
            a[i][k] = a[i][k] / a[k][k]
            for m in range(k + 1, n):
                a[i][m] = a[i][m] - a[i][k] * a[k][m]
            b[i] = b[i] - a[i][k] * b[k]
    # 回代的过程
    print("开始回带")
    x = [0] * n
    x[n - 1] = b[n - 1] / a[n - 1][n - 1]
    k = n - 2
    while k >= 0:
        temp = 0
        for j in range(k + 1, n):
            temp += a[k][j] * x[j]
        x[k] = (b[k] - temp) / a[k][k]
        k -= 1
    print(x)
    print("x的个数", len(x))


def gaussPP1 (aa, bb, p, q):
    a = aa[:][:]
    b = bb[:][:]
    n = len(a)
    for k in range(0, n):
        max = abs(a[k][k])
        maxi = k
        # for s in range(k+1,n):
        #     if(abs(a[s][k])>max):
        #         max=abs(a[s][k])
        #         maxi=s
        if (max == 0):
            print("主元为零")
        if (k != maxi):
            temp = a[k][:]
            a[k] = a[maxi][:]
            a[maxi] = temp[:]
            tempb = b[k]
            b[k] = b[maxi]
            b[maxi] = tempb
            print("进行主元交换")
            print("该", k, "迭代的主元是", max, "位于第", maxi, "行")
        temp = n
        if (k + p < n):
            temp = k + p + 1
        for i in range(k + 1, temp):
            a[i][k] = a[i][k] / a[k][k]
            temp2 = n
            if (temp2 > k + q):
                temp2 = k + q + 1
            for m in range(k + 1, temp2):
                a[i][m] = a[i][m] - a[i][k] * a[k][m]
            b[i] = b[i] - a[i][k] * b[k]
    # 回代的过程
    print("开始回带")
    x = [0] * n
    x[n - 1] = b[n - 1] / a[n - 1][n - 1]
    k = n - 2
    while k >= 0:
        temp = 0
        for j in range(k + 1, n):
            temp += a[k][j] * x[j]
        x[k] = (b[k] - temp) / a[k][k]
        k -= 1
    print(x)
    print("x的个数", len(x))


def gaussPP2 (aa, bb, p, q):
    """
    对带状压缩矩阵进行高斯消去法
    :param aa:系数矩阵A
    :param bb:矩阵b
    :param p:带宽p
    :param q:带宽q
    :param version:
    """
    a = aa[:][:]
    b = bb[:][:]
    m = len(a)
    n = len(a[0])
    for k in range(0, m):
        max = abs(a[k][p])
        maxi = k
        # for s in range(k+1,n):
        #     if(abs(a[s][k])>max):
        #         max=abs(a[s][k])
        #         maxi=s
        if (max == 0):
            print("主元为零")
        if (k != maxi):
            temp = a[k][:]
            a[k] = a[maxi][:]
            a[maxi] = temp[:]
            tempb = b[k]
            b[k] = b[maxi]
            b[maxi] = tempb
            print("进行主元交换")
            print("该", k, "迭代的主元是", max, "位于第", maxi, "行")
        temp = m
        if ((k + p) < temp):
            temp = k + p + 1
        for i in range(k + 1, temp):
            a[i][k + p - i] = a[i][k + p - i] / a[k][p]
            for j in range(k + 1, k + q + 1):
                a[i][j + p - i] = a[i][j + p - i] - a[i][k + p - i] * a[k][j + p - k]
            b[i] = b[i] - a[i][k + p - i] * b[k]
    # 回代的过程
    print("开始回带")
    x = [0] * m
    x[m - 1] = b[m - 1] / a[m - 1][p]
    k = m - 2
    while k >= 0:
        temp = b[k]
        st2 = m
        if ((k + q) < st2):
            st2 = k + q + 1
        for j in range(k + 1, st2):
            temp -= a[k][j + p - k] * x[j]
        x[k] = temp / a[k][p]
        k -= 1
    print(x)
    print("x的个数", len(x))


def question1 ():
    """
    计算题目1
    """
    y = [9.01, 8.96, 7.96, 7.97, 8.02, 9.05, 10.13, 11.18, 12.26, 13.28, 13.32, 12.61, 11.29, 10.22, 9.15, 7.90,
         7.95, 8.86, 9.81, 10.80, 10.93]
    x = range(0, 21)
    printArrayASJson(x, y)

    xx = 0
    xxArray = []
    while xx <= 20:
        xxArray.append(xx)
        xx += 0.01
    # 利用三次样条差值计算
    yyArray = evaspline(xxArray, x, y)
    l = 0
    # 利用两点之间的距离公式近似计算曲线的长度
    for i in range(1, len(xxArray)):
        l += ((yyArray[i] - yyArray[i - 1]) ** 2 + (xxArray[i] - xxArray[i - 1]) ** 2) ** 0.5

    printArrayASJson(xxArray, yyArray)
    # 利用牛顿插值多项式计算
    yyArray2 = ni(xxArray, x, y)
    printArrayASJson(xxArray,yyArray)

    # 绘制函数图像
    plt.figure(figsize=(8, 4))
    plt.plot(np.array(xxArray), np.array(yyArray), label="$spline$", color="blue")
    plt.plot(np.array(xxArray), np.array(yyArray2), label="$newton$", color="red")
    plt.plot(np.array(x), np.array(y), '*', label="$orignData$", color="black")
    plt.ylim(0, 20)
    plt.legend()
    # 显示函数图像
    plt.show()
    print("电缆的长度", l)


def question2 ():
    x = range(25)
    y = [15, 14, 14, 14, 14, 15, 16, 18, 20, 20, 23, 25, 28, 31, 34, 31, 29, 27, 25, 24, 22, 20, 18, 17, 16]
    # plt.figure(figsize=(8, 4))
    # plt.plot(np.array(x), np.array(y), '*', label="$data$", color="red")
    # plt.ylim(10, 40)
    # plt.legend()
    # plt.show()
    print(x)
    m = len(x)

    w = [0] * m
    n = 4
    g = initG(x, y, n)
    c = [0] * (n + 1)
    a = [0] * (n + 1)
    b = [0] * m
    # 建立矩阵Qk
    for k in range(0, n + 1):
        for i in range(k, m):
            c[k] = g[i][k] ** 2 + c[k]
        c[k] = -sgn(g[k][k]) * (c[k] ** 0.5)
        w[k] = g[k][k] - c[k]
        for j in range(k + 1, m):
            w[j] = g[j][k]
        b[k] = c[k] * w[k]
        # 变化G
        g[k][k] = c[k]
        for j in range(k + 1, n + 2):
            sum = 0
            for i in range(k, m):
                sum += w[i] * g[i][j]
            t = sum / b[k]
            for i in range(k, m):
                g[i][j] = g[i][j] + t * w[i]
    # 解三角方程组
    a[n] = g[n][n + 1] / g[n][n]
    i = n - 1
    while i >= 0:
        sum = 0
        for j in range(i + 1, n + 1):
            sum += g[i][j] * a[j]
        a[i] = (g[i][n + 1] - sum) / g[i][i]
        i -= 1
    e2 = 0
    for t in range(n + 1, m):
        e2 += g[t][n + 1] ** 2
    e2 = e2 ** 0.5
    print(e2)


def question3 ():
    # 选择数据文件
    print("选择进行计算的数据文件")
    print("1    dat61.dat")
    print("2    dat62.dat")
    print("3    dat63.dat")
    print("4    dat64.dat")
    str = input()
    path = "dat6" + str + ".dat"
    print("您选择的数据文件", path)
    printDataInfo(path)


def main ():
    str = input("选择进行计算第几题: ")
    print("您选择的题目", str)
    if (str == "1"):
        question1()
    if (str == "2"):
        question2()
    if (str == "3"):
        question3()


if __name__ == '__main__':
    main()
