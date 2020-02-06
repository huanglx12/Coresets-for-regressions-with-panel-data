import random
import numpy as np
import math
import time
import pickle

# sum of squares in a list
def square_sum(list):
    sum = 0
    for i in range(len(list)):
        sum += list[i]*list[i]
    return sum

##############################################
# generate the covariance matrix of AR(q)
def generate_cov(T,rho):
    P = np.identity(T)
    q = len(rho)
    P[0][0] = np.sqrt(1-square_sum(rho))
    for i in range(1,T):
        for j in range(max(0,i-q),i):
            P[i][j] = - rho[j+q-i]

    cov = np.linalg.inv(np.dot(P.T,P))
    return cov

##############################################
# generate panel data
def generate_panel(N,T,k,q,d,lam):
    beta = []
    rho = []
    for l in range(k):
        beta.append(generate_beta(d-1))
        temp_rho = generate_rho(q,lam)
        rho.append(temp_rho)

    panel = np.array([[[1.0 for fea in range(d)] for t in range(T)] for i in range(N)])
    mean = [0 for i in range(d-2)]
    cov = np.identity(d-2)

    # mean vector of each individual
    mean_individual = []
    cluster = np.random.randint(0,k,N)
    for i in range(N):
        temp = np.random.multivariate_normal(mean, cov, 1)[0]
        temp = temp/np.sqrt(square_sum(temp))*np.random.uniform(cluster[i],cluster[i]+1)
        mean_individual.append(temp)
    #for i in range(N):
    #    l2 = square_sum(mean_individual[i])
    #    norm = random.uniform(0, 10)
    #    for dim in range(d-1):
    #        mean_individual[i][dim] *= math.sqrt(norm / l2)
    # model of each individual
    mean_error = [0 for i in range(T)]
    for i in range(N):
        mean_i = np.random.multivariate_normal(mean_individual[i], cov*square_sum(mean_individual[i]), T)
        error_i = []
        error_basic = np.random.normal(0,1,T)
        for t in range(T):
            temp = error_basic[t]
            for tt in range(min(t,q)):
                temp += rho[tt] * error_i[tt]
            error_i.append(temp)
        for t in range(T):
            panel[i][t][0:-2] = mean_i[t]
            panel[i][t][d-1] = np.dot(panel[i][t][0:d-1],beta[cluster[i]]) + error_i[t]
    return panel

##############################################
# generate beta
def generate_beta(d):
    beta = np.random.normal(0,1,d-1)
    beta = np.append(beta,[-1])
    return beta

##############################################
# generate rho
def generate_rho(q,lam):
    rho = np.random.normal(0,1,q)
    l2 = square_sum(rho)
    norm = random.uniform(0,1-lam)
    for i in range(q):
        rho[i] *= math.sqrt(norm/l2)
    return rho


##############################################