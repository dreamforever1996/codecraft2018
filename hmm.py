#coding=utf-8
#recoding

import sys
from math import pi,sqrt,exp,pow,log
from abc import ABCMeta, abstractmethod
import random
import kmeans
from matrix_ import *

def random_pick(some_list, probabilities):
    x = random.uniform(0,1)
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability:break
    return item

def any(x=[]):
    for each in x:
        if each != 0:
            return True
    return False

def argmax(input_=[]):
    
    input_ = input_[0]
    #if len(input_) == 1:
        #print len(input_[0])
    index = 0
    max_n = 0
    for i in range(len(input_)):
        if input_[i] > max_n:
            max_n = input_[i]
            index = i
    return index

class _BaseHMM():
    '''
    elementary hmm abstract class,
    n_state: number of hidden states
    n_iter: number of iterators
    x_size: dimensions of observation
    start_prob: probability of init
    transmit_prob: probability of transmission
    '''

    __metaclass__ = ABCMeta

    def __init__(self, n_state=1, x_size=1, iter=20):
        print "Enter class _BaseHMM: "
        print "__init__(self, n_state=%d, x_size=%d, iter=%d):"%(n_state, x_size, iter)
        self.n_state = n_state
        self.x_size = x_size
        self.start_prob = [1 * 1.0 / n_state for i in range(n_state)]
        self.transmit_prob = [[1 * 1.0 / n_state for i in range(n_state)] for j in range(n_state)]
        self.trained = False
        self.n_iter = iter
        print "shape of start_prob: ", len(self.start_prob), 1
        print "shape of transmat_prob: ", shape(self.transmit_prob)

    # init param of emit
    @abstractmethod
    def _init(self, x):
        pass

    # abstract func: to return probability of emit
    @abstractmethod
    def emit_prob(self, x):
        return []

    @abstractmethod
    def generate_x(self, z):
        return []

    @abstractmethod
    def emit_prob_updated(self, x, post_state):
        pass

    def generate_seq(self, seq_length):
        x = createMatrix(seq_length, self.x_size)
        z = [0 for i in range(seq_length)]
        z_pre = [random_pick([i for i in range(self.n_state)], self.start_prob)]
        x[0] = self.generate_x(z_pre)
        z[0] = z_pre
        
        for i in range(seq_length):
            if i == 0: continue
            # P(Zn+1)=P(Zn+1|Zn)P(Zn)
            z_next = [random_pick([i for i in range(self.n_state)], self.transmit_prob[z_pre, :][0])]
            z_pre = z_next

            x[i] = self.generate_x(z_pre)
            z[i] = z_pre

        return x, z

    def X_prob(self, x, z_seq = []):
        x_length = len(x)
        #if z_seq.any
        if any(z_seq):
            z = [[0 for i in range(self.n_state)] for j in range(x_length)]
            for i in range(x_length):
                z[i][int(z_seq[i])] = 1
        else:
            z = [[1 for i in range(self.n_state)] for j in range(x_length)]

        _, c = self.forward(x, z)
        prob_x = 0.0
        for each in c:
            prob_x = prob_x + math.log(each)
        return prob_x

    def predict(self, x, x_next, z_seq=[], istrain=True):
        if self.trained == False or istrain == False:
            self.train(x)

        x_length = len(x)
        if any(z_seq):
            z = [[0 for i in range(self.n_state)] for j in range(x_length)]
            for i in range(x_length):
                z[i][int(z_seq[i])] = 1
        else:
            z = [[1 for i in range(self.n_state)] for j in range(x_length)]

        alpha, _ = self.forward(x, z)
        prob_x_next = mulByNum(self.emit_prob([x_next]), inner(alpha[x_length-1], transpose(self.transmit_prob)))
        prob_x_next = self.emit_prob(x_next) * matrixMul(alpha[x_length - 1], self.transmit_prob)

        return prob_x_next

    def decode(self, x, istrain=True):
        print ">> In decode()"
        if self.trained == False or istrain == False:
            self.train(x)

        x_length = len(x)
        state = [0 for i in range(x_length)]
        print "x_length is ", x_length
        print "shape of state is ", shape([state])

        pre_state = [[0 for i in range(self.n_state)] for j in range(x_length)]
        max_pro_state = [[0 for i in range(self.n_state)] for j in range(x_length)]
        print "shape of pre_state", shape(pre_state)
        print "shape of max_pro_state", shape(max_pro_state)

        _, c = self.forward(x, [[1 for i in range(self.n_state)] for j in range(x_length)])
        print c
        max_pro_state[0] = mulByNum(mulByElement(self.emit_prob(x[0]), [self.start_prob]), (1/c[0]))[0]
        print max_pro_state[0]



        for i in range(x_length):
            if i == 0: continue
            for k in range(self.n_state):
                #print "=================="
                #print self.emit_prob(x[i])[0][k]
                #print getCol(self.transmit_prob, k)
                #print max_pro_state[i-1]
                prob_state = mulByNum(getCol(self.transmit_prob, k), self.emit_prob(x[i])[0][k])
                #print "(***)", prob_state
                #print "(***)", max_pro_state[i-1]
                prob_state = mulByElement(transpose(prob_state), [max_pro_state[i-1]])
                #print "[***]", prob_state
                prob_state = mulByElement(transpose(mulByNum(getCol(self.transmit_prob, k),self.emit_prob(x[i])[0][k])), [max_pro_state[i-1]])
                #print prob_state
                max_n = sum(prob_state)
                #print max_n
                max_pro_state[i][k] = max_n * (1/c[i])
                pre_state[i][k] = argmax(prob_state)

        print "shape of max_pro_state is ", shape(max_pro_state)
        state[x_length - 1] = argmax(getRow(max_pro_state, x_length - 1))
        #print state[x_length - 1]
        for i in reversed(range(x_length)):
            if i == x_length - 1: continue
            state[i] = pre_state[i + 1][int(state[i+1])]
        for each in state:
            print each
        print "<< Leaving decode()"
        return state

    def train(self, x, z_seq = []):
        print "In train()"
        self.trained=True
        x_length = len(x)
        print "len of X: ", x_length
        print "Entering _init()"
        self._init(x)

        if any(z_seq):
            print "Z_seq.any() is True"
            print z_seq
            z = [[0 for i in range(self.n_state)] for j in range(x_length)]
            for i in range(x_length):
                z[i][int(z_seq[i])] = 1
            for each in z:
                print each
        else:
            print "Z_seq.any() is False, create a matrix z"
            z = [[1 for i in range(self.n_state)] for j in range(x_length)]
            print "shape of Z is: ", shape(z)

        print "EM iteration"
        for e in range(self.n_iter):
            print e, " iter"

            print "Entering forward()"
            alpha, c = self.forward(x, z)
            print "Entering backward()"
            beta = self.backward(x, z, c)

            print "shape of alpha: ", shape(alpha)
            #for each in alpha:
                #print each
            print "shape of beta: ", shape(beta)

            #print shape(alpha)
            #print shape(beta)
            post_state = mulByElement(alpha, beta)
            print "shape of post_state: ", shape(post_state)
            post_adj_state = [[0 for i in range(self.n_state)] for j in range(self.n_state)]
            print "shape of post_adj_state", shape(post_adj_state)
            for i in range(x_length):
                if i == 0: continue
                if c[i] == 0: continue
                post_adj_state = add(post_adj_state, mulByNum(mulByElement(outer(transpose([alpha[i-1]]), mulByElement([beta[i]], self.emit_prob(x[i]))),self.transmit_prob), 1/c[i]))

            a_sum = sum([post_state[0]])
            self.start_prob = mulByNum([post_state[0]], 1/a_sum)[0]
            for each in self.start_prob:
                print each
            for k in range(self.n_state):
                b_sum = 1
                for i in post_adj_state[k]:
                    b_sum += i
                self.transmit_prob[k] = mulByNum([post_adj_state[k]], 1/b_sum)[0]
            print "shape of self.transmat_prob is ", shape(self.transmit_prob)
            print "Entering emit_prob_update..."
            self.emit_prob_updated(x, post_state)

    def forward(self, x, z):
        print ">> In forward()"
        x_length = len(x)
        print "length of x: ", x_length
        alpha = createMatrix(x_length, self.n_state)
        print "creating alpha, shape of it is: ", shape(alpha)
        print "z[0] is: ", z[0]
        print "self.emit_prob(X[0]) is ", self.emit_prob(x[0])
        print "self.start_prob is ", self.start_prob
        alpha[0] = mulByElement([z[0]], mulByElement(self.emit_prob(x[0]), [self.start_prob]))[0]
        c = [0 for i in range(x_length)]
        c[0] = sum([alpha[0]])
        print "c[0] is ", c[0]
        alpha[0] = mulByNum([alpha[0]], 1/c[0])[0]
        print "alpha[0] is ", alpha[0]
        #print alpha[0]
        for i in range(x_length):
            if i == 0: continue 
            alpha[i] = mulByElement(mulByElement(self.emit_prob(x[i]), mul([alpha[i - 1]], self.transmit_prob)),[z[i]])[0]
            c[i] = sum([alpha[i]])
            if c[i] == 0: continue
            alpha[i] = mulByNum([alpha[i]], 1/c[i])[0]
        print "After a series of calculation, shape of alpha is ", shape(alpha)
        #print "And c is ", c
        print "Leaving forward()"
        return alpha, c

    def backward(self, x, z, c):
        print ">> In backward"
        x_length = len(x)
        print "x_length is ", x_length
        beta = createMatrix(x_length, self.n_state)
        print "creating beta, shape of it is ", shape(beta)
        beta[x_length - 1] = [1 for i in range(self.n_state)]
        print "last element of beta is ", beta[x_length-1]

        for i in reversed(range(x_length)):
            if i == x_length-1: continue
            beta[i] = mulByElement(mul(mulByElement([beta[i+1]], self.emit_prob(x[i+1])), transpose(self.transmit_prob)),[z[i]])[0]
            if c[i+1] == 0: continue
            beta[i] = mulByNum([beta[i]], 1/c[i+1])[0]

        print "shape of beta is ", shape(beta)
        print "<< Leaving backward()"
        return beta

def gauss2D(x, mean, cov):
    x = [x]
    mean = [mean]
    #print x, mean, cov
    #z = np.dot((x-mean).T,inv(cov))
    print ">> In gauss2D"
    z1 = minus(x, mean)
    z2 = inverse(cov)
    z3 = mul(z1, z2)
    z4 = mul(z3,transpose(z1))[0][0]
    print "z1: ", z1
    print "z2: ", z2
    print "z3: ", z3
    print "z4: ", z4
    z = 0.5 * -1 * z4
    
    #z = mulByNum(mulByNum(mul(mul(minusByNum(x,mean),inverse(cov)),minusByNum(x,mean)),0.5), -1)[0][0]
    temp = pow(sqrt(2.0*pi),len(x))*sqrt(det(cov))
    print "temp: ", temp
    print "z: ", z
    print "<< Leaving gauss2D"
    return (1.0/temp)*exp(z)

class GaussianHMM(_BaseHMM):

    """docstring for Gaussi_BaseHMM"""

    def __init__(self, n_state=1, x_size=1, iter=20):
        print "Enter class GaussianHMM(_BaseHMM):"
        print "__init__(self, n_state=%d, x_size=%d, iter=%d):"%(n_state, x_size, iter)
        _BaseHMM.__init__(self, n_state=n_state, x_size=x_size, iter=iter)
        self.emit_means = createMatrix(n_state, x_size)
        self.emit_covars = [[[0 for i in range(x_size)] for j in range(x_size)] for o in range(n_state)]
        for i in range(n_state): self.emit_covars[i] = eye(x_size)
        print "shape of emit_means: ", shape(self.emit_means)
        print "shape of emit_covars: ", shape(self.emit_covars), len(self.emit_covars[0][0])

    def _init(self, x):
        print ">> _init() entered."
        print "kmeans..."
        myCentroids,clustAssing = kmeans.kMeans(x,self.n_state)
        mean_kmeans = myCentroids
        self.emit_means = mean_kmeans
        print "shape of self.emit_means: ", shape(self.emit_means)
        for each in self.emit_means:
            print each
        print "calculating self.emit_covars"
        for i in range(self.n_state):
            for each in cov(x, x):
                print each
            self.emit_covars[i] = add(cov(x, x), mulByNum(eye(len(x[0])), 0.01))
        print "shape of self.emit_covars: ", shape(self.emit_covars)
        for each in self.emit_covars:
            print each
        print "<< _init() finished."

    def emit_prob(self, x):
        prob = createMatrix(1, self.n_state)
        #print "shape of prob", shape(prob)
        for i in range(self.n_state):
            prob[0][i] = gauss2D(x, self.emit_means[i], self.emit_covars[i])

        return prob

    def generate_x(self, z):
        return random.normalvariate(self.emit_means[z][0], self.emit_covars[z][0])

    def emit_prob_updated(self, x, post_state):
        print ">> In emit_prob_updated"
        print "shape of x is ", shape(x)
        print "shape of post_state is ", shape(post_state)
        for k in range(self.n_state):
            #print k
            for j in range(self.x_size):
                self.emit_means[k][j] = sum(mulByElement(getCol(post_state, k),getCol(x, j))) / sum(getCol(post_state,k))

            #print shape(x)
            #print shape([self.emit_means[k]])
            #print self.emit_means[k]
            #print minusByRow(x, [self.emit_means[k]])
            #print transpose(minusByRow(x, self.emit_means[k]))
            #print mulByElement(getCol(post_state, k), transpose(minusByRow(x, self.emit_means[k])))
            print "1. ", shape(transpose(minusByRow(x, [self.emit_means[k]])))
            print "2. ", shape(mulByCol(minusByRow(x, [self.emit_means[k]]), getCol(post_state, k)))
            x_cov = mul(transpose(minusByRow(x, [self.emit_means[k]])), mulByCol(minusByRow(x, [self.emit_means[k]]), getCol(post_state, k)))
            print "shape of x_cov is ", shape(x_cov)
            self.emit_covars[k] = mulByNum(x_cov, 1/sum(getCol(post_state, k)))
            print "shape of self.emit_covars[k] is ", shape(self.emit_covars[k])
            #print shape(self.emit_covars[k])
            if det(self.emit_covars[k]) == 0:
                self.emit_covars[k] = add(self.emit_covars[k], mulByNum(eye(len(x[0])), 0.01))
        print "<< Leaving emit_prob_updated"
    
