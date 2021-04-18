# 使用一个xls里记录的1份自动测量+3份医生测量数据，计算骨盆参数的rmse
import pandas as pd
import math
import numpy as np
from scipy import stats

def get_p_value(arrA, arrB):

    a = np.array(arrA)
    b = np.array(arrB)

    t, p = stats.ttest_ind(a,b)

    return p


def get_mse(records_real, records_predict):
    """
    均方误差 估计值与真值 偏差
    """
    if len(records_real) == len(records_predict):
        return sum([(x - y) ** 2 for x, y in zip(records_real, records_predict)]) / len(records_real)
    else:
        return None


def get_rmse(records_real, records_predict):
    """
    均方根误差：是均方误差的算术平方根
    """
    mse = get_mse(records_real, records_predict)
    if mse:
        return math.sqrt(mse)
    else:
        return None


df = pd.read_excel('pelvis-1+3.xls')
print(df)
ss_auto = []
pt_auto = []
pi_auto = []

for i in df['b']:
    ss_auto.append(i)
print(ss_auto)
for i in df['c']:
    pt_auto.append(i)
print(pt_auto)
for i in df['d']:
    pi_auto.append(i)
print(pi_auto)

ss_truth = []
pt_truth = []
pi_truth = []
for i in range(0, len(ss_auto)):
    ss_truth.append(np.average((df['e'][i] + df['h'][i] + df['k'][i]) / 3.0))
    pt_truth.append(np.average((df['f'][i] + df['i'][i] + df['l'][i]) / 3.0))
    pi_truth.append(np.average((df['g'][i] + df['j'][i] + df['m'][i]) / 3.0))

print(ss_truth)
print(pt_truth)
print(pi_truth)

all_truth=[]
all_auto=[]
for i in range(0, len(ss_auto)):
    all_truth.append((ss_truth[i]+pi_truth[i]+pt_truth[i])/3.0)
    all_auto.append((ss_auto[i]+pi_auto[i]+pt_auto[i])/3.0)

all_truth_mean=np.mean(all_truth)
all_auto_mean=np.mean(all_auto)

all_truth_std=np.std(all_truth)
all_auto_std=np.std(all_auto)

all_p=get_p_value(all_truth, all_auto)

print("all_truth_mean:",all_truth_mean)
print("all_auto_mean:",all_auto_mean)

print("all_truth_std:",all_truth_std)
print("all_auto_std:",all_auto_std)

print("all_p:",all_p)


ss_rmse = round(get_rmse(ss_truth, ss_auto), 3)
pt_rmse = round(get_rmse(pt_truth, pt_auto), 3)
pi_rmse = round(get_rmse(pi_truth, pi_auto), 3)
all_rmse = round(get_rmse(all_truth, all_auto), 3)

print('ss_rmse:', ss_rmse)
print('pt_rmse:', pt_rmse)
print('pi_rmse:', pi_rmse)
print('all_rmse:', all_rmse)
print('')

#求p值
ss_p=get_p_value(ss_truth, ss_auto)
pt_p=get_p_value(pt_truth, pt_auto)
pi_p=get_p_value(pi_truth, pi_auto)
print('ss_p:', ss_p)
print('pt_p:', pt_p)
print('pi_p:', pi_p)
print('')

#求均值
ss_auto_mean = np.mean(ss_auto)
#求标准差
ss_auto_std = np.std(ss_auto,ddof=1)
print('ss_auto_mean:', ss_auto_mean)
print('ss_auto_std :',ss_auto_std )
print('')

#求均值
pt_auto_mean = np.mean(pt_auto)
#求标准差
pt_auto_std = np.std(pt_auto,ddof=1)
print('pt_auto_mean:', pt_auto_mean)
print('pt_auto_std :',pt_auto_std )
print('')

#求均值
pi_auto_mean = np.mean(pi_auto)
#求标准差
pi_auto_std = np.std(pi_auto,ddof=1)
print('pi_auto_mean:', pi_auto_mean)
print('pi_auto_std :',pi_auto_std )
print('')

#求均值
ss_truth_mean = np.mean(ss_truth)
#求标准差
ss_truth_std = np.std(ss_truth,ddof=1)
print('ss_truth_mean:', ss_truth_mean)
print('ss_truth_std :',ss_truth_std )
print('')

#求均值
pt_truth_mean = np.mean(pt_truth)
#求标准差
pt_truth_std = np.std(pt_truth,ddof=1)
print('pt_truth_mean:', pt_truth_mean)
print('pt_truth_std :',pt_truth_std )
print('')

#求均值
pi_truth_mean = np.mean(pi_truth)
#求标准差
pi_truth_std = np.std(pi_truth,ddof=1)
print('pi_truth_mean:', pi_truth_mean)
print('pi_truth_std :',pi_truth_std )