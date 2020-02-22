# -*- coding: utf-8 -*-

"""
This file contains global settings and module imports.

Author: Marco Raveri (mraveri@uchicago.edu)

"""

################################################################################
# import matplotlib discriminating clusters:
################################################################################

import os
has_display = os.system('python -c "import matplotlib.pyplot as plt;plt.figure()" &> /dev/null')
import matplotlib
if has_display != 0:
    matplotlib.use('Agg')
import matplotlib.pyplot     as plt
import matplotlib.cm         as cm
import matplotlib.mlab       as mlab
import matplotlib.gridspec   as gridspec
import matplotlib.lines      as mlines
import matplotlib.patches    as mpatches
import matplotlib.ticker     as ticker
import matplotlib.transforms as transform
from matplotlib.colors import LinearSegmentedColormap

################################################################################
# other imports:
################################################################################

import numpy as np
import argparse
import math
import sys
import ctypes
import time
import re
import itertools

import scipy as scipy
from scipy.interpolate import RectBivariateSpline
from scipy.interpolate import UnivariateSpline
from scipy.interpolate import interp1d
import scipy as scipy
import scipy.special   as sp
import scipy.stats     as scs
import scipy.integrate as integrate

import copy
import itertools as it
import ConfigParser

# Try to import cPickle, which is faster but not default.
try:
    import cPickle as plk
except:
    import Pickle as plk
from sklearn.externals import joblib

# Color print:
from color_utilities import *
color_print = bash_colors()

# ignore future warnings:
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
# also ignore all warnings:
warnings.filterwarnings("ignore")

################################################################################
# parallelism:
################################################################################

import multiprocessing

from functools import partial
from tqdm import tqdm
import contextlib
# number of threads available:
if os.environ.has_key('OMP_NUM_THREADS'):
    n_threads = int(os.environ['OMP_NUM_THREADS'])
else:
    n_threads = multiprocessing.cpu_count()

################################################################################
# path structure:
################################################################################

here = os.path.dirname(os.path.abspath(__file__))

results_dir = here+'/results'
if not os.path.exists(results_dir): os.mkdir(results_dir)

################################################################################
# path dependent imports:
################################################################################

# import getdist:
getdist_python_path = here+'/../python/'
sys.path.insert(0, os.path.normpath(getdist_python_path))
import getdist.plots             as gplot
import getdist.paramnames        as gpar
import getdist.mcsamples         as gsamp
import getdist.types             as gtypes
import getdist.gaussian_mixtures as ggaussian
import getdist

# import MC evidence:
import MCEvidence as MCE

################################################################################
# global plot settings:
################################################################################

# 1- size of figures (PRD optimized):
x_size        = 15.4  # in cm
y_size        = 10.0  # in cm
# 2- font size:
main_fontsize = 10.0
# 3- LateX rendering:
if has_display == 0:
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rc('text', usetex=True)
# 4- running on cluster:
on_cluster = not has_display

################################################################################

# exit if the file is directly called:
if __name__ == "__main__":
    exit()
