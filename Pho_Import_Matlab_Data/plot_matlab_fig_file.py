#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: pho
"""
import sys
import numpy as np
import h5py
import hdf5storage # conda install hdf5storage
# from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.pyplot import plot,figure,hold,xlabel,ylabel,show,clf,xlim,legend
from pathlib import Path


def plot_matlab_fig_file(filename,fignr=1):
    # d = loadmat(filename,squeeze_me=True, struct_as_record=False)
    d = hdf5storage.loadmat(filename, appendmat=False)
    ax1 = d['hgS_070000'].children
    if np.size(ax1) > 1:
        legs= ax1[1]
        ax1 = ax1[0]
    else:
        legs=0
    plt.figure(fignr)
    plt.clf()
    plt.hold(True)
    counter = 0    
    for line in ax1.children:
        if line.type == 'graph2d.lineseries':
            if hasattr(line.properties,'Marker'):
                mark = "%s" % line.properties.Marker
                mark = mark[0]
            else:
                mark = '.'
            if hasattr(line.properties,'LineStyle'):
                linestyle = "%s" % line.properties.LineStyle
            else:
                linestyle = '-'
            if hasattr(line.properties,'Color'):
                r,g,b =  line.properties.Color
            else:
                r = 0
                g = 0
                b = 1
            if hasattr(line.properties,'MarkerSize'):
                marker_size = line.properties.MarkerSize
            else:
                marker_size = 1                
            x = line.properties.XData
            y = line.properties.YData
            plt.plot(x,y,marker=mark,linestyle=linestyle,color=plt.color(r,g,b),markersize=marker_size)
        elif line.type == 'text':
            if counter < 1:
                plt.xlabel("%s" % line.properties.String,fontsize =16)
                counter += 1
            elif counter < 2:
                plt.ylabel("%s" % line.properties.String,fontsize = 16)
                counter += 1        
    plt.xlim(ax1.properties.XLim)
    if legs:        
        leg_entries = tuple(legs.properties.String)
        py_locs = ['upper center','lower center','right','left','upper right','upper left','lower right','lower left','best']
        MAT_locs=['North','South','East','West','NorthEast', 'NorthWest', 'SouthEast', 'SouthWest','Best']
        Mat2py = dict(zip(MAT_locs,py_locs))
        location = legs.properties.Location
        plt.legend(leg_entries,loc=Mat2py[location])
    plt.hold(False)
    plt.show()