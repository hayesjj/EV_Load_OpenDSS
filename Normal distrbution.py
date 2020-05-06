# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 02:35:06 2020

@author: temp2015
"""
import numpy as np
mu, sigma = 510, 30 # mean and standard deviation 
s = np.random.normal(mu, sigma, 1000)
import matplotlib.pyplot as plt
count, bins, ignored = plt.hist(s, 30, density=True)
plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
              np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
         linewidth=2, color='g')
plt.show()