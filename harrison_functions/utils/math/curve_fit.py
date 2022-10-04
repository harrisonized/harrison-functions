import numpy as np
import datetime as dt
import matplotlib.dates as mdates
from scipy.optimize import curve_fit

 
# Functions included in this file:
# # logistic_func
# # curve_fit_new_grades


def logistic_func(x, a, b, c, d):
    return a * np.log(b * x + c) + d


def curve_fit_new_grades(df, p0=None):
    new_grades_df = df[df.grade_ - df.grade_.shift().fillna(0) > 0]
    popt, pcov = curve_fit(
        logistic_func,
        new_grades_df.date_.map(lambda x: dt.datetime.strptime(x, "%Y-%m-%d")).map(lambda x: mdates.date2num(x)),
        new_grades_df.grade_,
        p0=p0)
    return popt
