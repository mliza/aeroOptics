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

pickle_path  = '/Users/martin/Desktop/optics/data/pickle_data'
plots_path   = '/Users/martin/Desktop/results'
file_in      = 'data_out' 
data_in      = helper.pickle_manager(file_in, pickle_path)

# Plot Eyi Mass Fraction 
stagL = data_in['laminarChem_12_stag']
stagT = data_in['turbulentChem_12_stag']
diagL = data_in['laminarChem_12_diag']
diagT = data_in['turbulentChem_12_diag']
save_name = 'eyiCase12'

lines = ['solid', 'dashed', 'dashdot', '--', 
         (5, (10, 3)), (0, (3,10,1,10))]
colors = ['b', 'g', 'r', 'c', 'm']
title_size=15
label_size=13

# Plot Mass fraction 
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,8))
    #fig.tight_layout()
for indx, key in enumerate(stagL['optics']['mass_fraction']):
    ax1.plot(stagL['x']*1E3, 
             stagL['optics']['mass_fraction'][key], color=colors[indx],
             linestyle='-', label=f'{key}, Laminar Chemistry', 
             linewidth=2.5)

    ax1.plot(stagT['x']*1E3, 
             stagT['optics']['mass_fraction'][key], color=colors[indx], 
             linestyle='--', label=f'{key}, Turbulent Chemistry', 
             linewidth=2.5)

    ax2.plot(diagL['Distance']*1E3, 
             diagL['optics']['mass_fraction'][key], color=colors[indx], 
             linestyle='-', label=f'{key}, Laminar Chemistry', 
             linewidth=2.5)

    ax2.plot(diagT['Distance']*1E3, 
             diagT['optics']['mass_fraction'][key], color=colors[indx], 
             linestyle='--', label=f'{key}, Turbulent Chemistry', 
             linewidth=2.5)

ax1.set_title('Stagnation', fontsize=title_size)
ax2.set_title('Diagonal', fontsize=title_size)
ax1.set_xlim([-0.025, 0]) 

# Comment for diagonal plots 
ax1.set_xlabel(f'X $[mm]$', fontsize=label_size)
ax1.set_ylabel('Mass Fraction', fontsize=label_size)
ax2.set_xlabel(f'Normal $[mm]$', fontsize=label_size)
ax2.set_ylabel('Mass Fraction', fontsize=label_size)
ax1.legend() 
ax2.legend() 

plt.savefig(os.path.join(plots_path, f'{save_name}_massFraction.png'),
            bbox_inches='tight', dpi=300)
plt.close() 
