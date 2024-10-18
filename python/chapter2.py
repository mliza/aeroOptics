#!/opt/homebrew/bin/python3.9
'''
    Date:   10/15/2024
    Author: Martin E. Liza
    File:   optics.py
    Def:

    Author          Date        Revision
    ----------------------------------------------------
    Martin E. Liza  10/15/2024  Initial version.
'''
import os 
import sys 
import pickle
import IPython
import scipy.stats
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

# My Packages 
scripts_path   = os.environ.get('SCRIPTS')
python_scripts = os.path.join(scripts_path, 'Python')
sys.path.append(python_scripts) 
import optics
import helper_functions as helper 
import aerodynamic_functions as aero

def plot_polarizability_T(**kargs):
    temperature_K = kargs['temperature_K']
    fig_config = kargs['fig_config']
    wavelength_nm = kargs['wavelength_nm']
    output_png_path = kargs['output_path']

    fig = plt.figure(figsize=(fig_config['fig_width'],
                              fig_config['fig_height']))

    for i in list(kargs.keys())[1:-3]:
        plt.plot(temperature_K, kargs[i],
                 linewidth=fig_config['line_width'],
                 label=i) 

    plt.legend()
    plt.xlabel('Temperature $[K]$', fontsize=fig_config['label_size'])
    plt.ylabel('Polarizability $[m^3]$', fontsize=fig_config['label_size'])

    plt.savefig(os.path.join(output_png_path,
    f'{wavelength_nm}nm_polarizability.png'), format = 'png',
    bbox_inches='tight', dpi=fig_config['dpi_size']) 




if __name__ == "__main__":

    # Fig Stuff
    fig_config = { }
    fig_config['line_width'] = 3
    fig_config['fig_width'] = 6 
    fig_config['fig_height'] = 5 
    fig_config['dpi_size'] = 600 
    fig_config['label_size'] = 15 
    fig_config['legend_size'] = 10 
    matplotlib.rc('xtick', labelsize=10)
    matplotlib.rc('ytick', labelsize=10)


    temperature = np.linspace(0, 2000, 100)
    wavelength_nm = 633
    pol_Kerl_N2 = optics.kerl_polarizability_temperature(temperature_K=temperature, 
                                           molecule='N2',
                                           wavelength_nm=wavelength_nm)

    pol_Kerl_O2 = optics.kerl_polarizability_temperature(temperature_K=temperature, 
                                           molecule='O2',
                                           wavelength_nm=wavelength_nm)

    pol_Kerl_Air = optics.kerl_polarizability_temperature(temperature_K=temperature, 
                                           molecule='Air',
                                           wavelength_nm=wavelength_nm)

    plot_polarizability_T(temperature_K=temperature, kerl_N2=pol_Kerl_N2,
                        kerl_O2=pol_Kerl_O2, kerl_Air=pol_Kerl_Air,
                          fig_config=fig_config, wavelength_nm=wavelength_nm,
                          output_path='tmp')
