# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 22:35:36 2021

@author: Jinjin
"""

import pandas as pd, numpy as np
from datetime import datetime
import tvm, price_bond
import matplotlib.pyplot as plt

bonds = pd.read_csv('gilts_2012_09_19.csv', index_col=None, parse_dates=['maturity'])

current_date = datetime(2012, 9, 19)
ttm = [(maturity - current_date).days / 360 for maturity in bonds['maturity']]
bonds['time to maturity'] = ttm

# benchmark: compute yield to maturity using tvm
tr, yr = [], []
current_date = datetime(2012, 9, 19)
for i, bond in bonds.iterrows():
    ttm = bond['time to maturity']
    price = (bond['bid'] + bond['ask']) / 2
    freq = 2 # semiannually
    ytm = tvm.TVM(n=ttm * freq, pv=-price, pmt=bond['coupon'] / freq, fv=100).calc_r() * freq
    tr.append(ttm)
    yr.append(ytm)
    
bonds['npv_bench'] = yr

# compute yield to maturity using newton
bonds['ytm_newton'] = bonds.apply(lambda row: price_bond.calc_r( (row['bid'] + row['ask']) / 2, 100, row['coupon'], row['time to maturity'], 0.05, 0.0001, 100), axis = 1)
             
plt.xlabel('Time to maturity'), plt.ylabel('Yield to maturity'), plt.grid(True)
plt.plot(tr, np.array(yr)*100, marker='^', label='Original Yield Curve')
plt.plot(tr, np.array(bonds['ytm_newton'])*100, marker='*', label='Newton')
plt.legend(loc=4)
plt.show()

if __name__ == "__main__":
    ytm = price_bond.calc_r(pv = 1038.01, fv = 1000, coupon = 70, T = 7, r0 = 0.05, min_err = 0.00001, max_iter = 100)
    print("ytm = %s" %ytm)
    
    pv = price_bond.calc_pv(fv = 1000, coupon = 80, T = 20, r = 0.09)
    print("bond price = %s" %pv)    
              