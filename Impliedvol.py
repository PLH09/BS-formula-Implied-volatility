%reset -f
import pandas as pd
import numpy as np
from scipy.stats import norm
#BS formula (no-dividend)
#bs-call
def BSC_c(S, sigma, r, T, K):    
    d1 = (np.log(S/K) + (r+sigma**2/2)*T)/(sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    BSC_ = (S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2))
    return BSC_,norm.cdf(d1),norm.cdf(d2),d1,d2
#bs-put
def BSC_p(S, sigma, r, T, K):    
    d1 = (np.log(S/K) + (r+sigma**2/2)*T)/(sigma * np.sqrt(T))
    d2 = d1- sigma * np.sqrt(T)
    BSC_ = K*np.exp(-r*T)*norm.cdf(-d2)-S*norm.cdf(-d1)
    return BSC_,norm.cdf(-d1),norm.cdf(-d2),d1,d2
#current price
S = 52
sigma = 0.3
#risk-free rate
r = 0.12
#duration
T = 0.25
#strike price
K = 50

BSC_c(S, sigma, r, T, K)
BSC_p(S, sigma, r, T, K)

#%%
#solve implied volatility(call & put)
from scipy.optimize import fsolve
import scipy.stats as si
from sympy import E

#call
def solve_call_vol(unsolved_value):
    sigma, d1, d2 = unsolved_value[0],unsolved_value[1],unsolved_value[2]
    return [
        d1*sigma*np.sqrt(t)-(np.log(s/k) + (r+sigma**2/2) * t ),
        d1-sigma*np.sqrt(t)-d2,
        option - s*si.norm.cdf(d1,0.0,1.0)+k*E**(-r*t)*si.norm.cdf(d2,0.0,1.0)
    ]

#put
def solve_put_vol(unsolved_value):
    sigma, d1, d2 = unsolved_value[0],unsolved_value[1],unsolved_value[2]
    return [
        d1*sigma*np.sqrt(t)-(np.log(s/k) + (r+sigma**2/2) * t ),
        d1-sigma*np.sqrt(t)-d2,
        option + s*si.norm.cdf(-d1,0.0,1.0) - k*E**(-r*t)*si.norm.cdf(-d2,0.0,1.0)
        ]


s = 17023.84
r = 0.01
t = 0.05952381
k = 16800
option = 217
fsolve(solve_call_vol,[0,0,0])[0]

fsolve(solve_put_vol,[0,0,0])[0]
