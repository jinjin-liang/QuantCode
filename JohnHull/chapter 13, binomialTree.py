# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 19:58:12 2023

This code is used to check calculations within Chapter 13 of John Hull's book.

The code was taken from the blow page.

I have modified the u/d to match the volatility.
    - u = exp(sigma * sqrt(delta t))
    - d = exp(-sigma * sqrt(delta t))

https://github.com/jamesmawm/mastering-python-for-finance-second-edition/blob/master/Chapter%2004%20-%20Numerical%20Methods%20for%20Pricing%20Options.ipynb

@author: Jinjin Liang
"""

# Writing the StockOption base class

import math
import numpy as np
from decimal import Decimal

""" 
Stores common attributes of a stock option 
"""
class StockOption(object):
    def __init__(
        self, S0, K, r=0.05, T=1, N=2, pu=0, pd=0, 
        div=0, sigma=0, is_put=False, is_am=False):
        """
        Initialize the stock option base class.
        Defaults to European call unless specified.

        :param S0: initial stock price
        :param K: strike price
        :param r: risk-free interest rate
        :param T: time to maturity
        :param N: number of time steps
        :param pu: probability at up state
        :param pd: probability at down state
        :param div: Dividend yield
        :param is_put: True for a put option,
                False for a call option
        :param is_am: True for an American option,
                False for a European option
        """
        self.S0 = S0
        self.K = K
        self.r = r
        self.T = T
        self.N = max(1, N)
        self.STs = [] # Declare the stock prices tree

        """ Optional parameters used by derived classes """
        self.pu, self.pd = pu, pd
        self.div = div
        self.sigma = sigma
        self.is_call = not is_put
        self.is_european = not is_am

    @property
    def dt(self):
        """ Single time step, in years """
        return self.T/float(self.N)

    @property
    def df(self):
        """ The discount factor """
        return math.exp(-(self.r-self.div)*self.dt)  
    
# A class for European options using a binomial tree


""" 
    Price a European option by the binomial tree model 
    """
class BinomialEuropeanOption(StockOption):

    def setup_parameters(self):
        # Required calculations for the model
        self.M = self.N+1  # Number of terminal nodes of tree
        # self.u = 1+self.pu  # Expected value in the up state
        # self.d = 1-self.pd  # Expected value in the down state
        self.u = np.exp(self.sigma * np.sqrt(self.dt) )
        self.d = np.exp(-self.sigma * np.sqrt(self.dt) )
        self.qu = (math.exp(
            (self.r-self.div)*self.dt)-self.d)/(self.u-self.d)
        self.qd = 1-self.qu

    def init_stock_price_tree(self):
        # Initialize terminal price nodes to zeros
        self.STs = np.zeros(self.M)

        # Calculate expected stock prices for each node
        for i in range(self.M):
            self.STs[i] = self.S0 * \
                (self.u**(self.N-i)) * (self.d**i)

    def init_payoffs_tree(self):
        """
        Returns the payoffs when the option 
        expires at terminal nodes
        """ 
        if self.is_call:
            return np.maximum(0, self.STs-self.K)
        else:
            return np.maximum(0, self.K-self.STs)

    def traverse_tree(self, payoffs):
        """
        Starting from the time the option expires, traverse
        backwards and calculate discounted payoffs at each node
        """
        for i in range(self.N):
            payoffs = (payoffs[:-1]*self.qu + 
                       payoffs[1:]*self.qd)*self.df

        return payoffs

    def begin_tree_traversal(self):
        payoffs = self.init_payoffs_tree()
        return self.traverse_tree(payoffs)

    def price(self):
        """ Entry point of the pricing implementation """
        self.setup_parameters()
        self.init_stock_price_tree()
        payoffs = self.begin_tree_traversal()
        
        # Option value converges to first node
        return payoffs[0]
    
if __name__ == '__main__':
    s0 = 50
    K = 52
    r = 0.05
    T = 2
    N = 500
    div = 0
    sigma = 0.3
    is_put = True
    
    option = BinomialEuropeanOption(s0, K, r=r, T=T, N=N, div=div, sigma=sigma, is_put=is_put)
    
    print('European option price is:', option.price())

