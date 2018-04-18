#coding=utf-8
from __future__ import division
import math
import copy
import sys

'''
operations of vectors
row vector, r_vec: [[1,2,3,4,5]]
col vector, c_vec: [[1],[2],[3].[4],[5]]
len(r_vec) = 1, len(r_vec[0]) = n
len(c_vec) = n, len(c_vec_ = 1)
'''
def mean(vec):
	ret = 0

	m, n = shape(vec)
	if m == 1:
		for i in range(n):
			ret += vec[0][i]
		ret = ret / n
	elif n == 1:
		for i in range(m):
			ret += vec[i][0]
		ret = ret / m
	else:
		print "Input is not a vector."
		return None

	return ret

def inner(vecA, vecB):
	m1, n1 = shape(vecA)
	m2, n2 = shape(vecB)
	ret = 0

	if m1 == m2 and n1 == n2:
		ret = createMatrix(m1, n1)
		for i in range(m1):
			for j in range(n1):
				ret[i][j] = vecA[i][j] * vecB[i][j]
		return ret
	elif m1 == n2 and m2 == n1:
		return mul(vecA, vecB)
	else:
		print "WRONG format of vectors."
		return None

def outer(vecA, vecB):
	m1, n1 = shape(vecA)
	m2, n2 = shape(vecB)

	if n1 != 1 or m2 != 1:
		print "Input is not exactly vectors"
		return None

	ret = createMatrix(m1, n2)
	for i in range(m1):
		for j in range(n2):
			ret[i][j] = vecA[i][0] * vecB[0][j]

	return ret

def sum(vec):
	ret = 0
	m, n = shape(vec)

	for i in range(m):
		for j in range(n):
			ret += vec[i][j]
	return ret

'''
operations of matrix
'''
def getRow(A, row):
	m, n = shape(A)
	ret = createMatrix(1, n)
	for i in range(n):
		ret[0][i] = A[row][i]
	return ret

def getCol(A, col):
	m, n = shape(A)
	ret = createMatrix(m, 1)
	for i in range(m):
		ret[i][0] = A[i][col]
	return ret

def mul(A, B):
	m, n = shape(A)
	p, q = shape(B)

	if n != p:
		return None

	ret = createMatrix(m, q)
	for i in range(m):
		for j in range(q):
			tmp = 0
			for f in range(n):
				tmp += A[i][f] * B[f][j]
			ret[i][j] = tmp

	return ret
def mulByCol(A, B):
	m1, n1 = shape(A)
	m2, n2 = shape(B)

	if m1 != m2:
		print "WRONG format of input."
		return None
	ret = createMatrix(m1, n1)
	for i in range(m1):
		for j in range(n1):
			ret[i][j] = A[i][j] * B[i][0]
	return ret
def mulByElement(A, B):
	m1, n1 = shape(A)
	m2, n2 = shape(B)

	ret = createMatrix(m1, n1)
	for i in range(m1):
		for j in range(n1):
			ret[i][j] = A[i][j] * B[i][j]
	return ret

def eye(size):
	ret = createMatrix(size, size)
	for i in range(size):
		ret[i][i] = 1
	return ret

def cov(A, B):
	m1, n1 = shape(A)
	m2, n2 = shape(B)

	if (m1, n1) != (m2, n2):
		print "WRONG input format."
		return None

	ret = createMatrix(n1, n2)

	for i in range(n1):
		cola = getCol(A, i)
		#print "get a col from A, number: %d"%i
		#print cola
		cola = minusByNum(cola, mean(cola))
		#print cola
		for j in range(n1):
			#print "get a col from B, number: %d"%j
			colb = getCol(B, j)
			#print colb
			colb = minusByNum(colb, mean(colb))
			#print colb
			ret[i][j] = sum(inner(cola, colb))/(m1-1)
			#print ret[i][j]

	return ret

def det(A):
	m, n = shape(A)
	if m == 0 or n == 0:
		return None
	if m == 1:
		return A[0][0]
	else:
		ret = 0
		return sum([[(1)**i*A[i][0]*det(minor(A,i))for i in range(m)]])

def minor(x,i):y=x[:];del(y[i]);y=zip(*y);del(y[0]);return zip(*y)

def hangchangeone(matrix,b,m):# 用matrix第m行m列为主元，造第m列的上三角
	_c=matrix[m][m]
	L=len(matrix)
	matrix[m][m]=1
	for i in range(L):
		b[m][i]=b[m][i]/_c
	for i in range(m+1,L):
		matrix[m][i]=matrix[m][i]/_c# m行随主元变

	for i in range(m+1,L):# m行以下所有按照m减一次
		_d=matrix[i][m]
		for j in range(L):
			matrix[i][j]=matrix[i][j]-matrix[m][j]*_d
			b[i][j]=b[i][j]-b[m][j]*_d

	return matrix,b

def hangchangetwo(matrix,b,L):# 把上三角对角化
	if L is 1:
		return matrix,b
	else:
		for i in range(L-1,0,-1):
			for j in range(i-1,-1,-1):
				for k in range(L):
					b[j][k]=b[j][k]-b[i][k]*matrix[j][i]
				matrix[j][i]=0
	return matrix,b

def getfirstone(matrix,m):# 寻找matrix矩阵第m列中，包括m行以下第一个非零行，没有则返回-1
	L=len(matrix)
	for i in range(m,L):
		if matrix[i][m]!=0:
			return i
	return -1

def inverse(matrix):# 初等行变换法
	matrixnew=copy.deepcopy(matrix)
	_m=len(matrix)
	result=eye(_m)
	for i in range(_m):
		hang=getfirstone(matrixnew,i)
		if hang is -1:
			print('抱歉，这个矩阵'+str(matrix)+'行列式为零，没有逆')
			sys.exit(0)
		elif hang is not i:
			matrixnew[i]=[matrixnew[i][j]+matrixnew[hang][j] for j in range(_m)]
			result[i]=[result[i][j]+result[hang][j] for j in range(_m)]
		_c=matrixnew[i][i]
		matrixnew,result=hangchangeone(matrixnew,result,i)# 上三角化
	matrixnew,result=hangchangetwo(matrixnew,result,_m)# 对角化
	return result

'''
Common operations
'''

def shape(A):
	m = len(A)
	n = len(A[0])
	return m,n

def createMatrix(m,n):
	#print "Creating Matrix with %d rows and %d columns..."%(m,n)
	ret = [[0] * n for i in range(m)]
	return ret

def transpose(A):
	#print "Transposing: "
	#print A
	m, n = shape(A)
	ret = createMatrix(n, m)
	for i in range(m):
		for j in range(n):
			ret[j][i] = A[i][j]
	return ret

def mulByNum(A, num):
	m, n = shape(A)
	ret = createMatrix(m, n)
	for i in range(m):
		for j in range(n):
			ret[i][j] = A[i][j] * num
	return ret

def divideByNum(A, num):
	m, n = shape(A)
	ret = createMatrix(m, n)
	for i in range(m):
		for j in range(n):
			ret[i][j] = A[i][j] / num
	return ret

def minusByNum(A, num):
	m, n = shape(A)
	ret = createMatrix(m, n)
	for i in range(m):
		for j in range(n):
			ret[i][j] = A[i][j] - num
	return ret

def addByNum(A, num):
	m, n = shape(A)
	ret = createMatrix(m, n)
	for i in range(m):
		for j in range(n):
			ret = A[i][j] + num
	return ret	

def add(A, B):
	m1, n1 = shape(A)
	m2, n2 = shape(B)
	if m1 != m2 or n1 != n2:
		print "WRONG format of input."
		return None
	ret = createMatrix(m1, n1)

	for i in range(m1):
		for j in range(n1):
			ret[i][j] = A[i][j] + B[i][j]

	return ret

def minus(A, B):
	m1, n1 = shape(A)
	m2, n2 = shape(B)
	if m1 != m2 or n1 != n2:
		print "WRONG format of input."
		return None
	ret = createMatrix(m1, n1)

	for i in range(m1):
		for j in range(n1):
			ret[i][j] = A[i][j] - B[i][j]

	return ret

def minusByRow(A, B):
	m1, n1 = shape(A)
	m2, n2 = shape(B)
	if n1 != n2:
		print "WRONG format of input."
		return None
	ret = createMatrix(m1, n1)

	for i in range(m1):
		for j in range(n1):
			ret[i][j] = A[i][j] - B[0][j]
	return ret

if __name__=="__main__":
	print "hello world!"

	row_vec = [[1,1,1,1,1]]
	col_vec = [[1],[1],[1],[1],[1]]
	matrix = [[1,1,1,1],
			[0,0,0,0],
			[1,0,1,0],
			[0,1,0,1]]
	a = [[1,5,6],
		[4,3,9],
		[4,2,9],
		[4,7,2]]
	b = [[1,5,6],
		[4,3,9],
		[4,2,9]]
	print row_vec
	print col_vec
	print matrix
	for each in inverse(b):
		print each
