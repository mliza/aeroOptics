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
import constants_tables as s_consts

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
    return dict_kerl  

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
        distribution_func[ti] = quantum.distribution_function(val, molecule,
                                vibrational_number_max,
                                rotational_number_max,
                                born_opp_flag=True) 

    # Sum for all states
    buldakov_polarizability = np.zeros(np.shape(temperature_K)[0])
    for ti, val in enumerate(temperature_K): 
        buldakov_polarizability[ti] = np.sum(distribution_func[ti,:,:] *
                                             buldakov_expansion)


    ### PLOT ### 
    plt.plot(temperature_K, buldakov_polarizability, 
                 linewidth=fig_config['line_width'], label=f'{molecule}')
    #plt.show()

    plt.xlabel('Temperature $[K]$', fontsize=fig_config['label_size'])
    plt.ylabel('Polarizability $[m^3]$', fontsize=fig_config['label_size'])

    ## Maybe Move this Out ##
    plt.legend(fontsize=fig_config['legend_size'])
    plt.xticks(fontsize=fig_config['ticks_size'])
    plt.yticks(fontsize=fig_config['ticks_size'])
    plt.savefig(os.path.join(fig_config['out_path'],
        f'buldakovPolarizability_{molecule}_{wavelength_nm}nm.png'), format = 'png',
                bbox_inches='tight', dpi=fig_config['dpi_size'])
    plt.close()


    return buldakov_polarizability  


def plot_buldakov_kerl(temperature_K, buldakov, kerl, molecule, fig_config):
    # Assuming pol_const, temperature_K, buldakov, kerl, fig_config, and molecule are defined
    pol_const = s_consts.polarizability()[molecule]
    # Create the main figure and first y-axis
    fig, ax1 = plt.subplots()
    # Plot Buldakov on the primary y-axis
    ax1.plot(temperature_K, kerl, linewidth=fig_config['line_width'], color='b', label=f'Kerl, {molecule}')
    ax1.axhline(y=pol_const, linestyle='--', linewidth=fig_config['line_width'], color='b', label='Const')
    # Set labels and formatting for the primary y-axis
    ax1.set_xlabel('Temperature $[K]$', fontsize=fig_config['label_size'])
    ax1.set_ylabel('Polarizability $[m^3]$', fontsize=fig_config['label_size'], color='b')
    ax1.tick_params(axis='y', labelcolor='b')  # Color ticks to match y-axis label
    # Create a secondary y-axis for the Kerl plot
    ax2 = ax1.twinx()
    ax2.plot(temperature_K, buldakov, color='r', linewidth=fig_config['line_width'], label=f'Buldakov, {molecule}')
    # Set labels and formatting for the secondary y-axis
    ax2.set_ylabel('Buldakov Values $[m^3]$', fontsize=fig_config['label_size'], color='r')  # Customize label as needed
    ax2.tick_params(axis='y', labelcolor='r')  # Color ticks to match y-axis label
    # Add legends for both y-axes
    ax1.legend(loc="upper left", fontsize=fig_config['legend_size'])
    ax2.legend(loc="upper right", fontsize=fig_config['legend_size'])
    # Set tick sizes
    ax1.tick_params(axis='x', labelsize=fig_config['ticks_size'])
    ax1.tick_params(axis='y', labelsize=fig_config['ticks_size'])
    ax2.tick_params(axis='y', labelsize=fig_config['ticks_size'])

    # Save the figure
    plt.savefig(os.path.join(fig_config['out_path'],
                f'buldakovKerlPolarizability_{molecule}_{wavelength_nm}nm.png'),
                format='png', bbox_inches='tight', dpi=fig_config['dpi_size'])

# Close the plot to free up memory
    plt.close()




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
    fig_config['out_path'] = '/Users/martin/Desktop/pola'


    temperature_K = np.linspace(200, 1500, 200)
    rotational_num_max = 7
    vibrational_num_max = 5 #3,4,5
    molecule = 'N2'
    wavelength_nm = 633

    kerl = kerl_analysis(temperature_K, wavelength_nm, fig_config) 
    buldakov = buldakov_analysis(temperature_K, vibrational_num_max, 
                      rotational_num_max, molecule) 
    plot_buldakov_kerl(temperature_K, buldakov, kerl[molecule], molecule, fig_config)


