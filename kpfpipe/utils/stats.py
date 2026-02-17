import numpy as np
from scipy.optimize import least_squares


def gaussian(theta, x):
    mu, sigma, a, b = theta
    return b + a * np.exp(-(x-mu)**2/(2*sigma**2))


def gaussian_jac(theta, x):
    mu, sigma, a, b = theta
    dx = x - mu
    e = np.exp(-dx**2 / (2*sigma**2))

    J = np.empty((x.size, 4))
    J[:, 0] = a * e * dx / sigma**2
    J[:, 1] = a * e * dx**2 / sigma**3
    J[:, 2] = e
    J[:, 3] = 1.0
    
    return J


def optimize_lsq(func, theta0, x, y, jac=None):
    """
    Optimize theta for a given function using non-linear least-squares
    Wrapper function for scipy.optimize.least_squares
    """   
    def _residuals(theta, x, y):
        return func(theta, x) - y

    def _jac(theta, x, y):
        return jac(theta, x)

    result = least_squares(_residuals, theta0, jac=_jac, method='lm', args=(x,y))
    theta, rms = result.x, np.std(result.fun)
    
    return theta, rms