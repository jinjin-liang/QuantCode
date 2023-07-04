# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 20:32:15 2023

@author: Jinjin Liang
"""

import numpy as np

alpha = np.array([4000, 3000, 1000, 2000])

C = np.array([[0.000275, 0.000094, 0.000177, 0.00008],\
     [0.000094, 0.000187, 0.000138, 0.000102],\
     [0.000177, 0.000138, 0.000237, 0.000097],\
     [0.00008, 0.000102, 0.000097, 0.000173]])

print( "variance of the portfolio: ", np.dot( np.dot(alpha, C), alpha.T) )