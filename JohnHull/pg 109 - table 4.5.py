# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 23:33:50 2023

@author: Jinjin Liang

bootstrap OIS zero rate using OIS rate

This code is the solution code to Table 4.5 of pg 109
"""
import numpy as np
from scipy import optimize

ois_data = [(1, 1.8), (3, 2.0), (6, 2.2), (12, 2.5), (24, 3.0), (60, 4.0)]
ois_zero = {}
for i, (term, coupon) in enumerate(ois_data):
    if term <= 12:
        zero = np.log( 1+coupon/100*term/12 )*12/term
        ois_zero[term] = zero
    else:
        t0 = ois_data[i-1][0]
        r0 = ois_zero[t0]
        old_dates = list( range(3, t0+1, 3) )
        new_dates = list( range(t0+3, term+1, 3) )
        def obj(r):
            c = coupon/4
            v = -100 + 100*np.exp(-r*term/12)
            for d in old_dates:
                if d not in ois_zero:
                    # special handling on 9m
                    ois_zero[d] = 0.5 * (ois_zero[d+3]+ois_zero[d-3])
                v += c * np.exp(-ois_zero[d] * d/12)
            for d in new_dates:
                v += c * np.exp(- (r0+(r-r0)*(d-t0)/(term-t0)) * d/12 )
            return v
        sol = optimize.root(obj, 0.03, method='hybr')
        r = sol.x[0]
        for d in new_dates:
            ois_zero[d] = r0+(r-r0)*(d-t0)/(term-t0)
print(ois_zero)