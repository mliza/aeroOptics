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
from matplotlib import cm
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

# My Packages 
scripts_path   = os.environ.get('SCRIPTS')
python_scripts = os.path.join(scripts_path, 'Python')
sys.path.append(python_scripts) 
import optics
import quantum
import helper_functions as helper 
import aerodynamic_functions as aero

def kerl_analysis(temperature_K, wavelength_nm, fig_config): 
    # Calculations #
    keys = ['N2', 'O2', 'Air']
    dict_kerl = { }
    for k in keys:
        dict_kerl[k] = np.zeros(np.shape(temperature_K)[0])
        for i, val in enumerate(temperature_K):
            dict_kerl[k][i] = optics.kerl_polarizability_temperature(val, k,
                                                                wavelength_nm)
    # Calculations #

    # Plot #
    fig = plt.figure(figsize=(fig_config['fig_width'],
                               fig_config['fig_height']))
    for k in keys:
        plt.plot(temperature_K, dict_kerl[k],
                 linewidth=fig_config['line_width'], label=k)

    plt.xlabel('Temperature $[K]$', fontsize=fig_config['label_size'])
    plt.ylabel('Polarizability $[m^3]$', fontsize=fig_config['label_size'])

    ## Maybe Move this Out ##
    plt.legend(fontsize=fig_config['legend_size'])
    plt.xticks(fontsize=fig_config['ticks_size'])
    plt.yticks(fontsize=fig_config['ticks_size'])
    plt.savefig(os.path.join(fig_config['out_path'],
        f'kerlPolarizability_{wavelength_nm}nm.png'), format = 'png',
                bbox_inches='tight', dpi=fig_config['dpi_size'])
    plt.close()
    # Plot #

def buldakov_analysis(temperature_K, vibrational_number_max,
                      rotational_number_max, molecule):
    # [vibrational, rotational]
    buldakov_expansion = np.zeros([vibrational_number_max + 1,
                                   rotational_number_max + 1])

    # [temperature, vibrational, rotational]
    distribution_func = np.zeros([np.shape(temperature_K)[0],
                                  vibrational_number_max + 1,
                                  rotational_number_max + 1])

    for j in range(rotational_number_max + 1):
        for v in range(vibrational_number_max + 1):
            buldakov_expansion[v][j] = optics.buldakov_expansion(v, j, molecule)

    for ti, val in enumerate(temperature_K):
        distribution_func[ti] = quantum.distribution_function(
                vibrational_number_max, rotational_number_max, val, molecule)

    # Matrix multiplication
    """
    polarizability_T_vib = np.dot(buldakov_expansion[:,2],
                                  distribution_func[:,:,2])
        distribution_func[:,0] * buldakov_expansion[0]
    """


    ### PLOT ### 
    IPython.embed(colors = 'Linux')
    polarizability_T_vib = buldakov_expansion[:,1] * distribution_func[:,:,1]
    T_mesh, v_mesh = np.meshgrid(temperature_K,
                                 range(vibrational_number_max + 1))
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(7, 6))
    surf = ax.plot_surface(T_mesh, v_mesh, polarizability_T_vib.transpose(),
                           cmap='plasma', linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=10, pad=0.07)
    ax.set_yticklabels(ax.get_yticks().astype(int))
    ax.set_xlabel('Temperature $[K]$')
    ax.set_ylabel('Vibrational number $[\;]$')
    ax.set_zlabel('Polarizability $[m^3]$')
    ax.grid(False)
    #plt.show()



    ### PLOT ###





if __name__ == "__main__":

    # Fig Stuff
    fig_config = { }
    fig_config['line_width'] = 3
    fig_config['fig_width'] = 6
    fig_config['fig_height'] = 5
    fig_config['dpi_size'] = 600
    fig_config['label_size'] = 15
    fig_config['legend_size'] = 10
    fig_config['ticks_size'] = 10
    fig_config['out_path'] = '/Users/martin/Desktop'


    temperature_K = np.linspace(300, 2000, 100)
    rotational_num_max = 0
    vibrational_num_max = 1 #3,4,5
    molecule = 'O2'
    wavelength_nm = 633


    kerl_analysis(temperature_K, wavelength_nm, fig_config) 
    buldakov_analysis(temperature_K, vibrational_num_max, 
                      rotational_num_max, molecule) 

