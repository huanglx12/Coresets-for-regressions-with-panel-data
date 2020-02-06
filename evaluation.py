import time
from l2_regression import *
from coreset import *
from generate import *


#############################################
# evaluate the empirical error for coreset_glse and uniform_1
def evaluate_glse(panel,q,lam,times):
    N = panel.shape[0]
    T = panel.shape[1]
    d = panel.shape[2]
    eps = [0.1, 0.2, 0.3, 0.4, 0.5]
    
    BETA = []
    RHO = []
    for i in range(times):
        BETA.append(generate_beta(d - 1))
        RHO.append(generate_rho(q,lam))

    construction_glse = []
    construction_start = [0 for i in range(len(eps))]
    size_glse = []
    evaluate_glse = []
    evaluate_start = [[0 for i in range(times)] for j in range(len(eps))]
    all_start = [[0 for i in range(times)] for j in range(len(eps))]
    evaluate_uniform1 = []
    evaluate_uniform2 = []
    evaluate_time_glse = []
    for e in range(len(eps)):
        print(e)
        nt_sample = int(q * (d-1)*(d-1)/eps[e]/eps[e])
        construction_start[e] = time.time()
        c_glse = coreset_glse(sen_glse(panel, q, lam), nt_sample)
        construction_glse.append(time.time()-construction_start[e])
        size_glse.append(len(c_glse))
        u1_glse = uniform_1(N*T, nt_sample)
        sample = int(math.sqrt(nt_sample))
        u2_glse = coreset_nt_and_divide(T,uniform_2(N,T,sample,sample),1)

        temp_evaluate_glse = 0
        temp_evaluate_uniform1 = 0
        temp_evaluate_uniform2 = 0
        time_all = 0
        time_glse = 0
        for i in range(times):
            beta = BETA[i]
            rho = RHO[i]

            all_start[e][i] = time.time()
            all = glse_obj(panel,beta,rho)
            time_all += time.time()-all_start[e][i]
            evaluate_start[e][i] = time.time()
            glse = glse_coreset_obj(panel,beta,rho,c_glse)
            time_glse += time.time()-evaluate_start[e][i]
            uniform1 = glse_coreset_obj(panel,beta,rho,u1_glse)
            uniform2 = glse_coreset_obj(panel,beta,rho,u2_glse)
            error_glse = abs(glse-all)/all
            error_uniform1 = abs(uniform1-all)/all
            error_uniform2 = abs(uniform2 - all) / all

            if error_glse > temp_evaluate_glse:
                temp_evaluate_glse = error_glse
            if error_uniform1 > temp_evaluate_uniform1:
                temp_evaluate_uniform1 = error_uniform1
            if error_uniform2 > temp_evaluate_uniform2:
                temp_evaluate_uniform2 = error_uniform2
        evaluate_glse.append(temp_evaluate_glse)
        evaluate_uniform1.append(temp_evaluate_uniform1)
        evaluate_uniform2.append(temp_evaluate_uniform2)
        evaluate_time_glse.append(time_glse/time_all)
        construction_glse[e] /= time_all/times

    return eps, evaluate_glse, evaluate_uniform1, evaluate_uniform2, size_glse, evaluate_time_glse, construction_glse


#############################################
# evaluate the empirical error for coreset_glsek and uniform_2
def evaluate_glsek(panel,k,q,lam,times):
    N = panel.shape[0]
    T = panel.shape[1]
    d = panel.shape[2]
    eps = [0.1, 0.2, 0.3, 0.4, 0.5]

    BETA = []
    RHO = []
    for i in range(times):
        BETA.append([])
        RHO.append([])
        for l in range(k):
            BETA[i].append(generate_beta(d - 1))
            RHO[i].append(generate_rho(q,lam))

    construction_glsek = []
    construction_start = [0 for i in range(len(eps))]
    size_glsek = []
    evaluate_glsek = []
    evaluate_start = [[0 for i in range(times)] for j in range(len(eps))]
    all_start = [[0 for i in range(times)] for j in range(len(eps))]
    evaluate_uniform1 = []
    evaluate_uniform2 = []
    evaluate_time_glsek = []

    for e in range(len(eps)):
        print(e)
        n_sample = int(q * k * (d - 1) / eps[e])
        t_sample = int(q * (d - 1) / eps[e])
        construction_start[e] = time.time()
        c_glsek = coreset_glsek(panel, q, lam, n_sample, t_sample)
        construction_glsek.append(time.time()-construction_start[e])
        size = 0
        for s in range(len(c_glsek)):
            size += len(c_glsek[s])-1
        size_glsek.append(size)
        u1_glsek = coreset_nt_and_divide(T,uniform_1(N*T, n_sample*t_sample),0)
        u2_glsek = uniform_2(N, T, n_sample, t_sample)

        temp_evaluate_glsek = 0
        temp_evaluate_uniform1 = 0
        temp_evaluate_uniform2 = 0
        temp_evaluate_time_glsek = 0
        time_all = 0
        time_glsek = 0
        for i in range(times):
            beta = BETA[i]
            rho = RHO[i]
            # beta = []
            # rho = []
            # for l in range(k):
            #     beta.append(generate_beta(d - 1))
            #     rho.append(generate_rho(q,lam))

            all_start[e][i] = time.time()
            all = glsek_obj(panel,beta,rho)
            time_all += time.time()-all_start[e][i]
            evaluate_start[e][i] = time.time()
            glsek = glsek_coreset_obj(panel,beta,rho,c_glsek)
            time_glsek += time.time()-evaluate_start[e][i]
            uniform1 = glsek_coreset_obj(panel,beta,rho,u1_glsek)
            uniform2 = glsek_coreset_obj(panel,beta,rho,u2_glsek)
            error_glsek = abs(glsek-all)/all
            error_uniform1 = abs(uniform1-all)/all
            error_uniform2 = abs(uniform2-all)/all

            if error_glsek > temp_evaluate_glsek:
                temp_evaluate_glsek = error_glsek
            if error_uniform1 > temp_evaluate_uniform1:
                temp_evaluate_uniform1 = error_uniform1
            if error_uniform2 > temp_evaluate_uniform2:
                temp_evaluate_uniform2 = error_uniform2
            temp_evaluate_time_glsek += time_glsek/time_all
        evaluate_glsek.append(temp_evaluate_glsek)
        evaluate_uniform1.append(temp_evaluate_uniform1)
        evaluate_uniform2.append(temp_evaluate_uniform2)
        evaluate_time_glsek.append(time_glsek/time_all)
        construction_glsek[e] = float(construction_glsek[e]*times/time_all)

    return eps, evaluate_glsek, evaluate_uniform1, evaluate_uniform2, size_glsek, evaluate_time_glsek, construction_glsek


#############################################
#if __name__ == "__main__":
#    N = 1000
#    T = 1000
#    d = 5
#    k = 3
#    q = 1
#    lam = 0.1
#    times = 10
#    start = time.time()
#    print(evaluate_glse(generate_panel(N,T,1,q,d),q,lam,times))
#    print(evaluate_glsek(generate_panel(N, T, k, q, d), k, q,lam,times))
#    print(time.time()-start)