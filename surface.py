#!/opt/homebrew/bin/python3.9
'''
    Date:   04/06/2023
    Author: Martin E. Liza
    File:   main.py
    Def:

    Author		Date		Revision
    ----------------------------------------------------
    Martin E. Liza	04/06/2023	Initial version.
'''
import os  
import sys 
import pickle 
import IPython
import numpy as np 
import matplotlib.pyplot as plt 

# My packages 
scripts_path   = os.environ.get('SCRIPTS')
python_scripts = os.path.join(scripts_path, 'Python')
sys.path.append(python_scripts)
from aerodynamics_class import *
from helper_class import *
import optics 

# Loading classes 
aero   = Aero() 
helper = Helper()

pickle_path = '/Users/martin/Desktop/optics/data/pickle_data'
plots_path  = '/Users/martin/Desktop/results'
plot_out_na = 'mackeyFrozen'
files_in    = ['eyiChem_1_surface', 'eyiChem_6_surface',
               'eyiChem_12_surface'] 

files_in    = ['mackeyChem_1_surface', 'mackeyChem_2_surface',
               'mackeyChem_3_surface'] 
files_in    = ['mackeyTurbulent_1_surface', 'mackeyTurbulent_2_surface', 
               'mackeyTurbulent_3_surface'] 
files_in    = ['mackeyFrozen_1_surface', 'mackeyFrozen_2_surface', 
               'mackeyFrozen_3_surface'] 

for i in files_in:
    data_in     = helper.pickle_manager(i, pickle_path)
    case_num = i.split('_')[1] 
    plt.plot(data_in['x'], data_in['Heat_Flux'], 'o', 
             label=f'case {case_num}')

plt.legend() 
plt.xlabel('x-axis $[mm]$')
plt.ylabel('Heat')
plt.savefig(os.path.join(plots_path, f'{plot_out_na}_yPlus.png'),
                bbox_inches='tight', dpi=300)
plt.close() 
