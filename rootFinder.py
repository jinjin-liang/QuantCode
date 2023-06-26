# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 23:33:50 2023

@author: Jinjin
"""
import numpy as np
from scipy import optimize

def fun(x):
    coupon = 3/4
    v = coupon * np.exp(-0.01995 * 0.25) + coupon * np.exp(-0.02188*0.5)+coupon*np.exp(-0.0232865*0.75)+coupon*np.exp(-0.024693*1)\
        +coupon*np.exp(-(0.024693 + (x-0.024693)*0.25) * 1.25) +coupon*np.exp(-(0.024693 + (x-0.024693)*0.5) * 1.5) + coupon*np.exp(-(0.024693 + (x-0.024693)*0.75) * 1.75)\
            + (100+coupon)*np.exp(-x * 2) - 100
    return v

sol = optimize.root(fun, 0.02, method='hybr')

print(sol.x)