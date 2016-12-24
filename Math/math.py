# -*- coding: utf-8 -*-
# import numpy as np
# import matplotlib.pyplot as plt
import binascii
import struct


def dd (tup_x, tup_y):
    n = len(tup_x)
    m = [0] * n
    m = tup_y[:]
    for i in range(1, n):
        j = n - 1;
        while j >= i:
            m[j] = (m[j] - m[j - 1]) / (tup_x[j] - tup_x[j - i])
            j -= 1
            print(m[j], i, j)
    return m


def ni (xxArray, tup_x, tup_y):
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


def find_k (x, _x):
    n = len(x)
    for i in range(0, n - 1):
        if (_x < x[i]):
            return i
    return -1


def splinem (x, y, lambda_0, d_0, u_n, d_n):
    n = len(x);
    M = [1] * (n);
    h = [1] * (n + 1)
    a = [1] * (n)
    b = [1] * (n)
    c = [1] * (n)
    M = y[:]
    # for k in range(1, 3):
    #     i = n - 1;
    #     while (i >=k):
    #         M[i] = (M[i] - M[i - 1]) / (x[i] - x[i - k])
    #         i -= 1
    for i in range(1, 3):
        j = n - 1;
        while j >= i:
            M[j] = (M[j] - M[j - 1]) / (x[j] - x[j - i])
            j -= 1
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


def evaspline (xxArray, tup_x, tup_y):
    # printArrayASJson(tup_x[xx],tup_y[xx])
    # M = splinem(tup_x, tup_y, 0.5, 0, 0.5, 0)
    M = splinem(tup_x, tup_y, -2, -0.0392, -2, -0.018)
    yyArray = []
    for xx in xxArray:
        yy = 0
        k = find_k(tup_x, xx)
        h = tup_x[k] - tup_x[k - 1]
        xbar = tup_x[k] - xx
        xdian = xx - tup_x[k - 1]
        yy = (M[k - 1] * (xbar ** 3) / 6 + M[k] * (xdian ** 3) / 6 + (tup_y[k - 1] - M[k - 1] * (h ** 2) / 6) * xbar + (
        tup_y[k] - (M[k] * h ** 2) / 6) * xdian) / h

        yyArray.append(yy)
    return yyArray


def printArrayASJson (x, y):
    n = len(x)
    for i in range(0, n):
        print("[" + str(x[i]) + "," + str(y[i]) + "],")


def question1 ():
    y = [9.01, 8.96, 7.96, 7.97, 8.02, 9.05, 10.13, 11.18, 12.26, 13.28, 13.32, 12.61, 11.29, 10.22, 9.15, 7.90,
         7.95, 8.86, 9.81, 10.80, 10.93]
    x = range(0, 21)
    printArrayASJson(x, y)

    xx = 0
    xxArray = []
    while xx <= 20:
        xxArray.append(xx)
        xx += 0.01

    yyArray = evaspline(xxArray, x, y)
    printArrayASJson(xxArray, yyArray)
    yyArray2 = ni(xxArray, x, y)
    # printArrayASJson(xxArray,yyArray)
    #
    plt.figure(figsize=(8, 4))
    plt.plot(np.array(xxArray), np.array(yyArray), label="$yangtiao$", color="blue")
    plt.plot(np.array(xxArray), np.array(yyArray2), label="$duoxiangs$", color="red")
    plt.plot(np.array(x), np.array(y), '*', label="$data$", color="black")
    plt.ylim(0, 20)
    plt.legend()
    plt.show()


def lss ():
    """形成矩阵"""


def question2 ():
    x = range(0, 25)
    y = [15, 14, 14, 14, 14, 15, 16, 18, 20, 20, 23, 25, 28, 31, 34, 31, 29, 27, 25, 24, 22, 20, 18, 17, 16]
    plt.figure(figsize=(8, 4))
    plt.plot(np.array(x), np.array(y), '*', label="$data$", color="red")
    plt.ylim(10, 40)
    plt.legend()
    plt.show()


def printDataInfo (path):
    print ("文件路径", path)
    f = open(path, "rb")
    m = 8
    # 矩阵文件头的个数
    # 读取文件头
    fhead = f.read(4 * 5)
    # hexstr = binascii.b2a_hex(fhead)  #得到一个16进制的数
    a = struct.unpack("IIIII", fhead)
    id=hex(a[0])
    version=hex(a[1])
    n=a[2]
    q=a[3]
    p=a[4]
    print ("文件标识部分-------------")
    print ("文件标识符", id)
    print ("数据文件版本号",version)
    print ("矩阵描述部分-------------")
    print ("方程阶数", n)
    print ("带状矩阵上带宽", q)
    print ("带状矩阵下带宽", p)
    print ("------------------")
    # f.seek(0,3)



    if(version=='0x102'):
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
        print (count)
        j=0
        b=[0]*a[2]
        while j<(a[2]):
            fbody2 =f.read(4)
            s=struct.unpack("f",fbody2)
            b[j]=s[0]
            j+=1
        if(f.read(4)):
            print ("数据没有用完")
        else:
            print ("数据已经用完")
        #gaussPP(ma,b,p,q,version)
        #choleskyb(ma,n,q,p,b)
    if(version=="0x202"):
        print ("矩阵为压缩带状矩阵")
        count = 0
        ma = [[] for i in range(a[2])]
        j = k = 0
        while j <= (n - 1):
            fbody = f.read(4)
            count += 1
            s = struct.unpack("f", fbody)
            ma[j].append(s[0])
            k += 1
            if (k == (p+q+1)):
                k = 0
                j += 1
        print (count)
        j=0
        b=[0]*a[2]
        while j<(a[2]):
            fbody2 =f.read(4)
            s=struct.unpack("f",fbody2)
            b[j]=s[0]
            j+=1
        if(f.read(4)):
            print ("数据没有用完")
        else:
            print ("数据已经用完")
        for aaa in ma:
            print (aaa)
        gaussPP2(ma,b,p,q,version)
def choleskyb(aa,n,q,p,b):
    """
    本函数针对给定带宽为p的对称正定矩阵A计算其Cholesky矩阵G，其元存放于A的相应位置
    :param aa: 对阵正定带状矩阵
    :param n: 矩阵的阶数
    :param p: 矩阵的带宽
    """
    a=aa[:]
    u=[[0 for i in range(n)] for i in range(n)]
    l=[[0 for i in range(n)] for i in range(n)]
    for i in range(0,n):
        temp1=n
        if(i+q<temp1):
            temp1=i+q+1
        for j in range(i,temp1):
            temp2=0
            if(i-p>0):
                temp2=i-p
            if(j-q>i-p):
                temp2=j-q
            sum=0
            for t in range(temp2,i):
                sum+=l[i][t]*u[t][j]
            u[i][j]=a[i][j]-sum
            temp2=0
            if(j-p>temp2):
                temp2=j-p
            if(i-q>temp2):
                temp2=i-q
            for t in range(temp2,i):
                sum+=l[i][t]*u[t][j]
            l[j][i]=(a[j][i]-sum)/u[i][i]
    print("a矩阵")
    for aaa in a:
        print(aaa)
    print("l矩阵")
    for lll in l:
        print(lll)
    print("u矩阵")
    for uuu in u:
        print(uuu)


    #回代的过程
    y=[0]*n
    x=[0]*n
    y[0]=b[0]
    for k in range(1,n):
        sum=0
        temp=0
        if(k-p>0):
            temp=k-p
        for j in range(temp,k):
            sum+=y[j]*l[k][j]
        y[k]=b[k]-sum

    print (y)
    x[n-1]=y[n-1]/u[n-1][n-1]
    k=n-2
    while k>=0:
        sum=0
        temp=n
        if(k-p<n-1):
            temp=k-p+1
        for j in range(k+1,temp):
            temp+=l[j][k]*x[j]
        x[k]=(y[k]-temp)/u[k][k]
        k-=1
    print (x)


def gaussPP (aa,bb,p,q,version):

    a=aa[:][:]
    b=bb[:][:]
    n = len(a)
    for k in range(0, n):
        max = abs(a[k][k])
        maxi=k
        # for s in range(k+1,n):
        #     if(abs(a[s][k])>max):
        #         max=abs(a[s][k])
        #         maxi=s
        if(max==0):
            print ("主元为零")
        if(k!=maxi):
            temp =a[k][:]
            a[k]=a[maxi][:]
            a[maxi]=temp[:]
            tempb=b[k]
            b[k]=b[maxi]
            b[maxi]=tempb
            print ("进行主元交换")
            print ("该",k,"迭代的主元是",max,"位于第",maxi,"行")
        temp=n
        if(k+p<n):
            temp=k+p+1
        for i in range(k+1,temp):
            a[i][k]=a[i][k]/a[k][k]
            temp2=n
            if(temp2>k+q):
                temp2=k+q+1
            for m in range(k+1,temp2):
                a[i][m]=a[i][m]-a[i][k]*a[k][m]
            b[i]=b[i]-a[i][k]*b[k]
    #回代的过程
    print ("开始回带")
    x=[0]*n
    x[n-1]=b[n-1]/a[n-1][n-1]
    k=n-2
    while k>=0:
        temp=0
        for j in range(k+1,n):
            temp+=a[k][j]*x[j]
        x[k]=(b[k]-temp)/a[k][k]
        k-=1
    print (x)
    print ("x的个数",len(x))

def gaussPP2(aa,bb,p,q,version):
    a=aa[:][:]
    b=bb[:][:]
    m = len(a)
    n= len(a[0])
    for k in range(0, m):
        max = abs(a[k][0])
        maxi=k
        # for s in range(k+1,n):
        #     if(abs(a[s][k])>max):
        #         max=abs(a[s][k])
        #         maxi=s
        if(max==0):
            print ("主元为零")
        if(k!=maxi):
            temp =a[k][:]
            a[k]=a[maxi][:]
            a[maxi]=temp[:]
            tempb=b[k]
            b[k]=b[maxi]
            b[maxi]=tempb
            print ("进行主元交换")
            print ("该",k,"迭代的主元是",max,"位于第",maxi,"行")
        temp=n
        if(k+p<n):
            temp=k+p+1
        for i in range(k+1,temp):
            a[i][k+p-i]=a[i][k+p-i]/a[k][p]
            temp2=n
            if(temp2>k+q):
                temp2=k+q+1
            for m in range(k+1,temp2):
                a[i][m+p-i]=a[i][m+p-i]-a[i][k+p-i]*a[k][m+p-k]
            b[i]=b[i]-a[i][+p-i]*b[k]
    #回代的过程
    print ("开始回带")
    x=[0]*n
    x[n-1]=b[n-1]/a[n-1][p]
    k=n-2
    while k>=0:
        temp=0
        for j in range(k+1,n):
            temp+=a[k][j]*x[j]
        x[k]=(b[k]-temp)/a[k][k]
        k-=1
    print (x)
    print ("x的个数",len(x))


def question3 ():
    # 选择数据文件
    pathArray = ["dat62.dat"]
    for path in pathArray:
        printDataInfo(path)

        # 读取数据文件

        # a = fh.read()
        # print 'raw: ',`a`,type(a)
        # hexstr = binascii.b2a_hex(a)  #得到一个16进制的数
        # print ('hex: ',hexstr, type(hexstr))
        # bsstr = bin(int(hexstr,16))[2:]
        # print('bin: ',bsstr, type(bsstr))


# question1()
# question2()
question3()
