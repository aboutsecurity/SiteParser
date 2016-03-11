"""
Utils.py
@brad_anton

"""
import pylab 
import matplotlib.pyplot as plt
import numpy 

def graph_lines(points, filename):
    """Plots the points and creates an image
    """
    plt.plot(points, 'ro-')
    plt.savefig(filename)

def find_outliers(points, thresh=20):
    """Finds line count outliers that greatly deviate from the mean 
    which makes them suspicious
    """
    if points.size <= 1:
        print "\t[!] Don't have enough data to find outliers"
        return numpy.empty([])

    if len(points.shape) == 1:
        points = points[:,None]

    median = numpy.median(points, axis=0)
    diff = numpy.sum((points - median)**2, axis=-1)
    diff = numpy.sqrt(diff)
    med_abs_deviation = numpy.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation


    outliers = points[numpy.where(modified_z_score > thresh)]
    return outliers
