from l2_regression import *
from coreset import *
from generate import *
import pandas as pd
import time
import evaluation as eva
import pickle
import sys

##########################################
# output an excel
def arrays_write_to_excel(eps, evaluate_glsek, evaluate_uniform1, size_glsek, construction_time_glsek, opt_time_glsek, opt_time, k):
    l = []
    for i in range(len(eps)):
        l.append([eps[i], evaluate_glsek[i][0], evaluate_uniform1[i][0], evaluate_glsek[i][1], evaluate_glsek[i][2], evaluate_uniform1[i][1], \
                  evaluate_uniform1[i][2], size_glsek[i], construction_time_glsek[i], opt_time_glsek[i], opt_time[i]])

    arr = np.asarray(l)
    df = pd.DataFrame(arr, columns=['eps', 'max emp_c', 'max emp_u1', 'avg emp_c', 'std emp_c', 'avg emp_u1',
                                    'std emp_u1', 'size', 'T_C', 'T_C+T_S', 'T_X'])
    df.to_csv('result_realworld_'+str(k)+'.csv')
    return df

#####################################
if __name__ == "__main__":
    times = int(sys.argv[1])

# glse
    k = 1
    q = 1
    lam = 0.2

    start = time.time()
    panel = np.load('realworld.npy')

    eps, evaluate_glse, evaluate_uniform1, size_glse, construction_time_glse, opt_time_glse, opt_time = eva.evaluate_glse(panel, q, lam, times)
    arrays_write_to_excel(eps, evaluate_glse, evaluate_uniform1, size_glse, construction_time_glse, opt_time_glse, opt_time, k)

    print(time.time() - start)


# ##############################
# # glsek
#     k = 3
#     q = 1
#     lam = 0.2
#
#     start = time.time()
#     panelk = np.load('realworld.npy')
#
#     eps, evaluate_glsek, evaluate_uniform1, size_glsek, construction_time_glsek, opt_time_glsek, opt_time = eva.evaluate_glsek(panelk, k, q, lam, times)
#     arrays_write_to_excel(eps, evaluate_glsek, evaluate_uniform1, size_glsek, construction_time_glsek, opt_time_glsek, opt_time, k)
#
#     print(time.time() - start)



