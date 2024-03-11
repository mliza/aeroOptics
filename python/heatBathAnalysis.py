#!/opt/homebrew/bin/python3.9
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
import pandas as pd
import matplotlib.pyplot as plt 
import scipy.constants as s_consts 
import astropy.constants as a_consts
from ambiance import Atmosphere #package for atmosphere properties 

# My Packages 
scripts_path   = os.environ.get('SCRIPTS')
python_scripts = os.path.join(scripts_path, 'Python')
sys.path.append(python_scripts) 
import optics
import helper_functions as helper 
import aerodynamic_functions as aero

data_path = '/Users/martin/Documents/Research/UoA/Projects/aeroOptics/data'
file_name = 'heatBathEyiCase12.csv'

df_in = pd.read_csv(os.path.join(data_path, file_name))
dict_in = df_in.to_dict()
IPython.embed(colors ='Linux')
df_in['time'] *= 1E6

density_dict = { }
density_dict['N2'] = df_in['rhoN2'].to_numpy()
density_dict['N'] = df_in['rhoN'].to_numpy()
density_dict['O2'] = df_in['rhoO2'].to_numpy()
density_dict['O'] = df_in['rhoO'].to_numpy()
density_dict['NO'] = df_in['rhoNO'].to_numpy()
gd_const = optics.Gladstone_Dale(density_dict)
index_refraction = optics.index_of_refraction(density_dict)

plt.plot(df_in['time'], index_refraction['dilute'] - 1, linewidth=2)
plt.xlabel('Time $[\mu s]$')
plt.ylabel('Index of refraction - 1 $[\;]$')
plt.savefig('indexOfRefractionTime.eps', format='eps', bbox_inches='tight',
            dpi=1200)
plt.savefig('indexOfRefractionTime.png', format='png', bbox_inches='tight',
            dpi=1200)
plt.close() 

# Plot GD 
plt.plot(df_in['time'], gd_const['gladstone_dale'] * 1E4, linewidth=2)
plt.xlabel('Time $[\mu s]$')
plt.ylabel('GladstoneDale const $\\times 10^{-4}\,[m^3/kg]$')
plt.savefig('gladstonedaleConstTime.eps', format='eps', bbox_inches='tight',
            dpi=1200)
plt.savefig('gladstonedaleConstTime.png', format='png', bbox_inches='tight',
            dpi=1200)
plt.close() 

'''
# Plot Mass frac
plt.plot(df_in['time'], df_in['massFracN2'], linewidth=2, label='$N2$')
plt.plot(df_in['time'], df_in['massFracO2'], linewidth=2, label='$O2$')
plt.plot(df_in['time'], df_in['massFracO'], linewidth=2, label='$O$')
plt.plot(df_in['time'], df_in['massFracNO'], linewidth=2, label='$NO$')
plt.plot(df_in['time'], df_in['massFracN'], linewidth=2, label='$N$')
plt.legend()
plt.xlabel('Time $[\mu s]$')
plt.ylabel('Mass Fraction $[\;]$')
plt.savefig('massFractionTime.eps', format='eps', bbox_inches='tight',
            dpi=1200)
plt.savefig('massFractionTime.png', format='png', bbox_inches='tight',
            dpi=1200)
plt.close() 
'''





# Plot densities
'''
plt.plot(df_in['time'], df_in['rhoN2'], linewidth=2, label='$N2$')
plt.plot(df_in['time'], df_in['rhoO2'], linewidth=2, label='$O2$')
plt.plot(df_in['time'], df_in['rhoO'], linewidth=2, label='$O$')
plt.plot(df_in['time'], df_in['rhoNO'], linewidth=2, label='$NO$')
plt.plot(df_in['time'], df_in['rhoN'], linewidth=2, label='$N$')
plt.legend()
plt.xlabel('Time $[\mu s]$')
plt.ylabel('Density $[kg/m^3]$')
plt.savefig('densityTime.eps', format='eps', bbox_inches='tight',
            dpi=1200)
plt.savefig('densityTime.png', format='png', bbox_inches='tight',
            dpi=1200)
plt.close() 
'''

plt.plot(df_in['time'], df_in['Tt'], linewidth=2, label='$T_{tr}$')
plt.plot(df_in['time'], df_in['Tv'], linewidth=2, label='$T_{vr}$')
plt.ylabel('Temperature $[K]$')
plt.xlabel('Time $[\mu s]$')
plt.legend()
plt.savefig('temperatureTime.eps', format='eps', bbox_inches='tight',
            dpi=1200)
plt.savefig('temperatureTime.png', format='png', bbox_inches='tight',
            dpi=1200)
plt.close() 



