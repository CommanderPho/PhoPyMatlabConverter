#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: pho
"""
import sys
import numpy as np
import pandas as pd
from scipy.stats import kde
import h5py
import hdf5storage # conda install hdf5storage
from pathlib import Path

# Include using: from Pho_Import_Matlab_Data import import_mat_file, load_mat_file, print_variables

from Pho_Import_Matlab_Data.plot_matlab_fig_file import plot_matlab_fig_file

# See https://docs.h5py.org/en/stable/quick.html#quick for more info
## In short, An HDF5 file is a container for two kinds of objects: datasets, which are array-like collections of data, and groups, which are folder-like containers that hold datasets and other groups. The most fundamental thing to remember when using h5py is:
#### Groups work like dictionaries, and datasets work like NumPy arrays

enable_print_type_values = True

def printname(name):
    print(name)

def print_attrs(name, obj):
    # Create indent
    shift = name.count('/') * '    '
    item_name = name.split("/")[-1] # Get only the last suffix of the path (the variable name)
    if name.startswith("#refs#"):
        # Exclude top level '#refs#' Group
        # print('Skipping #refs# group and its children...')
        # return -1 # Apparently returning a non-None value stops enumeration
        pass
    else:
        if isinstance(obj, h5py.Dataset):
            # obj node is a dataset
            print('<dataset>: ' + shift + item_name)
        else:
            # obj node is a group
            print('<group>: ' + shift + item_name)
        if enable_print_type_values:
            try:
                for key, val in obj.attrs.items():
                    print(shift + '    ' + f"{key}: {val}")
            except:
                pass


## Import Function Definitions:

def import_mat_file(mat_file_path):
    print('opening .mat file at {}'.format(mat_file_path))
    f = h5py.File(mat_file_path,'r')
    return f
    # print(f.keys())
    # data_position = f.get(active_variables)

    
def build_tree_entries(mat_file):
    data = [
        {'level': 0, 'dbID': 77, 'parent_ID': 6, 'short_name': '{}'.format(mat_file), 'long_name': '', 'order': 1, 'pos': 0} ,
    ]
    # f.keys()
    return data


def print_variables(h5pyFile, recurrsively=False):
    # Get the list of keys for the file
    # h5pyFile.keys()
    # h5pyFile.visit(printname)
    h5pyFile.visititems(print_attrs)

def load_mat_file(mat_file_path):
    out = hdf5storage.loadmat(mat_file_path) # Load all variables by default
    return out

#end
