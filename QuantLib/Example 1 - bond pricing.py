# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 23:47:01 2023

@author: Jinjin
"""

import QuantLib as ql
import numpy as np

prices = {}

start_date = ql.Date(8, ql.February, 2016)
maturity_date = start_date + ql.Period(5, ql.Years)
schedule = ql.Schedule(start_date, maturity_date,
ql.Period(ql.Semiannual), ql.TARGET(),
ql.Following, ql.Following,
ql.DateGeneration.Backward, False)
coupons = [0.01]*10
bond = ql.FixedRateBond(3, 100, schedule, coupons,
ql.Thirty360(ql.Thirty360.BondBasis))

today = ql.Date(9, ql.May, 2018)
nodes = [ today + ql.Period(i, ql.Years) for i in range(11) ]
rates = [ 0.007, 0.010, 0.012, 0.013, 0.014,
0.016, 0.017, 0.018, 0.020, 0.021, 0.022 ]
discount_curve = ql.ZeroCurve(nodes, rates, ql.Actual360())

discount_handle = ql.RelinkableYieldTermStructureHandle(discount_curve)
bond.setPricingEngine(ql.DiscountingBondEngine(discount_handle))
ql.Settings.instance().evaluationDate = today
prices[today] = bond.cleanPrice()
print("quant lib price: ", prices[today])

def get_rates(rates, t):
    times = [i for i in range(11)]
    i = 0
    while i < len(times) and t >= times[i]:
        i += 1
    i -= 1
    r1, r2 = rates[i], rates[i+1]
    t1, t2 = t-times[i], times[i+1]-t
    return r1 * t2/(t1+t2) + r2 * t1/(t1+t2)

fv = 100
coupon = 1
times = [(t-today)/360 for t in schedule if t >= today]
linear_rates = [ get_rates(rates, t) for t in times]
price_local = fv * np.exp(-linear_rates[-1] * times[-1] ) + coupon * times[0] * np.exp(-linear_rates[0] * times[0]) + coupon/2 * sum(np.exp(-r*t) for r, t in zip(linear_rates[1:], times[1:]) ) 
print("local calculation: ", price_local)



