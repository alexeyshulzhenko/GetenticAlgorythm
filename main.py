#!/usr/bin/python3
# -*- coding: utf-8 -*-

from deap import base
from deap import creator
from deap import tools
import xlsxwriter
import numpy as np
import random
import os

print('current directory', os.getcwd())  # Getting current directory to avoid fucking mistake in future.


L_arr = [10, 20, 30, 40, 50, 100, 500, 1000]
N = [10 * L_arr[], 100 * L_arr[]]