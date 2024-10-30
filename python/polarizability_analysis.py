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

def kerl_analysis(temperature_K, wavelength_nm): 
    # Calculations #
    kerl_N2 = np.zeros(np.shape(temperature_K)[0])
    kerl_O2 = np.zeros(np.shape(temperature_K)[0])
    kerl_Air = np.zeros(np.shape(temperature_K)[0])

    for i, val in enumerate(temperature_K):
        kerl_N2[i] = optics.kerl_polarizability_temperature(val, 'N2',
                                                         wavelength_nm)

        kerl_O2[i] = optics.kerl_polarizability_temperature(val, 'O2',
                                                         wavelength_nm)

        kerl_Air[i] = optics.kerl_polarizability_temperature(val, 'Air',
                                                         wavelength_nm)
    # Calculations #

    # Plot #
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

    # Matix multiplication  
    """
    polarizability_T_vib = np.dot(buldakov_expansion[:,2],
                                  distribution_func[:,:,2]) 
    """

    ### PLOT ### 
    polarizability_T_vib = buldakov_expansion[:,2] * distribution_func[:,:,2] 
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
    IPython.embed(colors = 'Linux')
    plt.show()



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
    output_path = 'tmp'
    matplotlib.rc('xtick', labelsize=10)
    matplotlib.rc('ytick', labelsize=10)


    temperature_K = np.linspace(300, 20000, 100)
    rotational_num_max = 2
    vibrational_num_max = 3
    molecule = 'N2'
    wavelength_nm = 633


    kerl_analysis(temperature_K, wavelength_nm) 
    buldakov_analysis(temperature_K, vibrational_num_max, 
                      rotational_num_max, molecule) 

