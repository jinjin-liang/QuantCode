# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 18:20:16 2023

@author: Jinjin Liang
"""

import numpy as np
from scipy.stats import norm

"""
right = 'C' or 'P'
s = Spot Price
k =  Strike Price
t = Days to expiration
rfr = Risk-free Rate
sigma = volatility
div = Annual dividend rate. Defaulted to zero.
price = Known option price. Needed for implied_volatility function
"""


def d1(s, k, t, rfr, sigma, div=0):
    """d1 calculation"""
    d_1 = (np.log(s / k) +
           (rfr - div + sigma ** 2 / 2) * t) / (sigma * np.sqrt(t))
    return d_1


def d2(s, k, t, rfr, sigma, div=0):
    """d2 calculation"""
    d_2 = d1(s, k, t, rfr, sigma, div) - sigma * np.sqrt(t)
    return d_2


def nd1(right, s, k, t, rfr, sigma, div=0):
    """nd1 calculation"""
    if right == 'C':
        nd_1 = norm.cdf(d1(s, k, t, rfr, sigma, div), 0, 1)
    elif right == 'P':
        nd_1 = norm.cdf(-d1(s, k, t, rfr, sigma, div), 0, 1)
    return nd_1


def nd2(right, s, k, t, rfr, sigma, div=0):
    """nd2 calculation"""
    if right == 'C':
        nd_2 = norm.cdf(d2(s, k, t, rfr, sigma, div), 0, 1)
    elif right == 'P':
        nd_2 = norm.cdf(-d2(s, k, t, rfr, sigma, div), 0, 1)
    return nd_2


def option_price(right, s, k, t, rfr, sigma, div=0):
    """option price"""
    right = right.upper()
    t /= 365
    if right == 'C':
        price = (s * np.exp(-div * t) *
                 nd1(right, s, k, t, rfr, sigma, div)
                 - k * np.exp(-rfr * t) *
                 nd2(right, s, k, t, rfr, sigma, div))
    elif right == 'P':
        price = (k * np.exp(-rfr * t) *
                 nd2(right, s, k, t, rfr, sigma, div)
                 - s * np.exp(-div * t) *
                 nd1(right, s, k, t, rfr, sigma, div))
    return price


def option_vega(s, k, t, rfr, sigma, div=0):
    """option vega"""
    t /= 365
    vega = (.01 * s * np.exp(-div * t) * np.sqrt(t)
            * norm.pdf(d1(s, k, t, rfr, sigma, div)))
    return vega


def implied_volatility(right, s, k, t, rfr, price, div=0):
    """implied volatility approximation"""
    epsilon = 0.00000001
    sigma = 1.0

    def newton_raphson(right, s, k, t, rfr, sigma, price, epsilon, div=0):
        diff = np.abs(option_price(right, s, k, t, rfr, sigma, div) - price)
        while diff > epsilon:
            sigma = (sigma -
                     (option_price(right, s, k, t, rfr, sigma, div) - price) /
                     (option_vega(s, k, t, rfr, sigma, div) * 100))
            diff = np.abs(
                    option_price(right, s, k, t, rfr, sigma, div) - price)
        return sigma

    iv = newton_raphson(right, s, k, t, rfr, sigma, price, epsilon, div)
    return iv

if __name__ == "__main__":
    right = 'C'
    s = 8572
    k =  8700
    t = 31
    rfr = 0
    div = 0
    price = 616.05
    print("implied vol: ", implied_volatility(right, s, k, t, rfr, price, div) )