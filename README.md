############################
Environment: python 3.7

############################
# Command

python main_realworld.py/main_synthetic.py int(times)

a) python main_realworld.py 100
Input: realworld.npy (realworld dataset)
Output: result1_realworld.csv emp1_realworld.csv

b) python main_synthetic.py 100
Output: synthetic_gaussian.npy (synthetic dataset with Gaussian errors) 
        result1_synthetic_gaussian.csv (statistics)
        synthetic_cauchy.npy (synthetic dataset with Cauchy errors) 
        result1_synthetic_cauchy.csv (statistics)
        emp1_synthetic.csv (all empirical errors)

% Due to privacy issue, we do not provide the real-world dataset. 
You can change the input dataset to be your own panel dataset "XXX.npy" 
in which the ((iT-T+t)-th row is (x_{it}, y_{it}), i.e., 
the observation of i-th individual at t-th time period. 

############################

