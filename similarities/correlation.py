# -------------------------------------------------------------------------------
# Name:        Recommendations
# 
# Author:      mourad mourafiq
# -------------------------------------------------------------------------------
# !/usr/bin/env python
from __future__ import division
from math import sqrt

PEARSON_SIMILARITY_CACHE = {}


def get_commun_items(x, y):
    """
    Returns the commun items between x and y
    """
    return [i for i in x.keys() if i in y.keys()]


def pearson_correlation(x, y, commun_items):
    """
    The population correlation coefficient corr(x,y) between x and y with expected
    values m(x) and m(y) and standard deviations std(x) and std(y) is defined as:
        corr(x,y) = cov(x, y) / (std(x) * std(y)) = E((x - m(x))(y - m(y))) / (std(x) * std(y))
    
    Returns the pearson correlation for x and y for a given list of commun items 
    """
    # Find the number of elements
    n = len(commun_items)
    # if they are no ratings in common, return 0
    if n == 0: return 0
    # Add up all the preferences
    sumX = sum([x[i] for i in commun_items])
    sumY = sum([y[i] for i in commun_items])
    # Sum up the squares
    sumX2 = sum([pow(x[i], 2) for i in commun_items])
    sumY2 = sum([pow(y[i], 2) for i in commun_items])
    # Sum up the products
    prodSum = sum([x[i] * y[i] for i in commun_items])
    # Calculate Pearson score
    num = prodSum - (sumX * sumY / n)
    den = sqrt((sumX2 - pow(sumX, 2) / n) * (sumY2 - pow(sumY, 2) / n))
    if den == 0: return 0
    r = num / den
    return r


def pearson_sim(items, x, y, cache=False):
    """
    Returns the similarity between x and y based on the pearson correaltion
    """
    if cache:
        if (x, y) in PEARSON_SIMILARITY_CACHE:
            return PEARSON_SIMILARITY_CACHE[(x, y)]
        i_x = items[x]
        i_y = items[y]
        sim = pearson_correlation(i_x, i_y, get_commun_items(i_x, i_y))
        PEARSON_SIMILARITY_CACHE[(x, y)] = sim
        PEARSON_SIMILARITY_CACHE[(y, x)] = sim
        return sim
    i_x = items[x]
    i_y = items[y]
    return pearson_correlation(i_x, i_y, get_commun_items(i_x, i_y))


def mean(input_array):
    for i in range(0, (len(input_array) - 1)):
        input_array[i] = float(input_array[i])
    total_sum = 0.00
    for value in input_array:
        total_sum = total_sum + value
    return float(total_sum / len(input_array))


def standard_deviation(input_array):
    mu = mean(input_array)
    variance_numerator = 0.00
    for val in input_array:
        variance_numerator = variance_numerator + (val - mu) ** 2  # Sigma((x-mu)^2)
    variance = variance_numerator / len(input_array)
    return sqrt(variance)


def covariance(x_array, y_array):
    if len(x_array) != len(y_array):
        return False
    x_mu = mean(x_array)
    y_mu = mean(y_array)
    covariance_numerator = 0.00
    for i in range(len(x_array)):
        covariance_numerator = covariance_numerator + (x_array[i] - x_mu) * (y_array[i] - y_mu)
    return covariance_numerator / len(x_array)


def correlation(x_array, y_array):
    if covariance(x_array, y_array):
        return covariance(x_array, y_array) / ((standard_deviation(x_array)) * (standard_deviation(y_array)))
    else:
        return False


X = [1, 2, 2, 4]
Y = [2, 4, 6, 8]
print correlation(X, Y)

