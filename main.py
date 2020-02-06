from l2_regression import *
from coreset import *
from generate import *
import pandas as pd
import time
from evaluation import *
import pickle

##########################################
# output an excel
def arrays_write_to_excel(eps, evaluate_glse, evaluate_uniform1, evaluate_uniform2, size_glsek, evaluate_time_glse, construction_glse, k):
    l = []
    for v in [eps, evaluate_glse, evaluate_uniform1, evaluate_uniform2, size_glsek, evaluate_time_glse, construction_glse]:
        l.append(v)

    arr = np.asarray(l).transpose()
    df = pd.DataFrame(arr, columns=['eps',  'emp_c', 'emp_u1', 'emp_u2', 'size', 'T_S/T_X', 'T_C/T_X'])
    df.to_csv('result_'+str(k)+'.csv')
    return df

#####################################
if __name__ == "__main__":
# glse
    N = 500
    T = 500
    d = 11
    q = 1
    lam = 0.2

    start = time.time()
    panel = generate_panel(N, T, 1, q, d, lam)
    with open("panel", "wb") as f:
        pickle.dump(panel, f)

    times = 200

    # with open("panel", "rb") as f:
    #     panel = pickle.load(f)

    eps, evaluate_glse, evaluate_uniform1, evaluate_uniform2, size_glse, evaluate_time_glse, construction_glse = evaluate_glse(
        panel, q, lam, times)
    arrays_write_to_excel(eps, evaluate_glse, evaluate_uniform1, evaluate_uniform2, size_glse, evaluate_time_glse,
                          construction_glse, 1)

    print(time.time() - start)


##############################
# glsek
    N = 500
    T = 500
    d = 11
    k = 3
    q = 1
    lam = 0.2

    start = time.time()
    panelk = generate_panel(N, T, k, q, d, lam)
    with open("panelk", "wb") as f:
        pickle.dump(panelk, f)

    times = 200

    # with open("panelk", "rb") as f:
    #    panelk = pickle.load(f)
    eps, evaluate_glse, evaluate_uniform1, evaluate_uniform2, size_glsek, evaluate_time_glse, construction_glse = evaluate_glsek(panelk, k, q, lam, times)
    arrays_write_to_excel(eps, evaluate_glse, evaluate_uniform1, evaluate_uniform2, size_glsek, evaluate_time_glse, construction_glse, k)
    print(time.time() - start)



