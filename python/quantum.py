'''
    Date:   03/26/2023
    Author: Martin E. Liza
    File:   optics.py
    Def:

    Author          Date        Revision
    ----------------------------------------------------
    Martin E. Liza  03/26/2023  Initial version.
'''
import pickle
import molmass
import os 
import sys 
import IPython
import constants_tables 
import numpy as np
import matplotlib.pyplot as plt 
import scipy.constants as s_consts 
from ambiance import Atmosphere #package for atmosphere properties 

# My Packages 
scripts_path   = os.environ.get('SCRIPTS')
python_scripts = os.path.join(scripts_path, 'Python')
sys.path.append(python_scripts) 
import helper_functions as helper 
import aerodynamic_functions as aero
