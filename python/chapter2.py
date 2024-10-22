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
    plt.close()



def plot_probability_of_state_vibrational_T(**kargs):
    fig_config = kargs['fig_config']
    prob_state_dict = kargs['prob_state_dict']
    vibrational_number = kargs['vibrational_number']
    legend_name = kargs['legend_name']
    fig_name_out = kargs['fig_name_out']
    output_png_path = kargs['output_path']
    for t in prob_state_dict.keys():
        plt.semilogy(vibrational_number, prob_state_dict[t], 'o-', 
                    linewidth=fig_config['line_width'],
                    label=f'{legend_name}, T = {t} $[K]$')
    plt.xticks(range(np.min(vibrational_number), np.max(vibrational_number)))
    plt.legend()
    plt.xlabel('Vibrational number $[\;]$', fontsize=fig_config['label_size'])
    plt.ylabel('Probability of state $[\;]$', fontsize=fig_config['label_size'])

    plt.savefig(os.path.join(output_png_path,
    f'{fig_name_out}'), format = 'png',
    bbox_inches='tight', dpi=fig_config['dpi_size']) 
    plt.close()

def plot_partition_function_vibrational_T(**kargs):
    fig_config = kargs['fig_config']
    IPython.embed(colors = 'Linux')
    part_funct_dict = kargs['part_func_dict']
    vibrational_number = kargs['vibrational_number']
    legend_name = kargs['legend_name']
    fig_name_out = kargs['fig_name_out']
    output_png_path = kargs['output_path']
    for t in part_funct_dict.keys():
        plt.plot(vibrational_number, prob_state_dict[t], 'o-', 
                    linewidth=fig_config['line_width'],
                    label=f'{legend_name}, T = {t} $[K]$')
    plt.xticks(range(np.min(vibrational_number), np.max(vibrational_number)))
    plt.legend()
    plt.xlabel('Vibrational number $[\;]$', fontsize=fig_config['label_size'])
    plt.ylabel('Partition function $[\;]$', fontsize=fig_config['label_size'])

    plt.savefig(os.path.join(output_png_path,
    f'{fig_name_out}'), format = 'png',
    bbox_inches='tight', dpi=fig_config['dpi_size']) 
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
    matplotlib.rc('xtick', labelsize=10)
    matplotlib.rc('ytick', labelsize=10)


# Probability of State at equilibrium
    temperature_K = ['500', '1000', '2000']
    vibrational_number = np.arange(0, 21)
    molecule='N2'
    rotational_number = 1
    fig_name_prob = f'probState{molecule}_J{rotational_number}.png'
    fig_name_part = f'partFunction{molecule}_J{rotational_number}.png'
    legend_name = f'$J$ = {rotational_number}'

    prob_state_dict = { }
    partition_function_dict = { }

    for t in temperature_K:
        prob_state_dict[t] = np.zeros(21)
        partition_function_dict[t] = np.zeros(21)

    for t in temperature_K:
        for v in vibrational_number:
            prob_state_dict[t][v] = optics.probability_of_state(
                                    temperature_K=int(t),
                                    vibrational_number=v,
                                    rotational_number=rotational_number,
                                    molecule=f'{molecule}')

            partition_function_dict[t][v] = optics.partition_function(
                                    temperature_K=int(t),
                                    vibrational_number=v,
                                    rotational_number=rotational_number,
                                    molecule=f'{molecule}')

    plot_partition_function_vibrational_T(
                            part_func_dict=partition_function_dict,
                            vibrational_number=vibrational_number,
                            legend_name=legend_name,
                            fig_name_out=fig_name_part,
                            fig_config=fig_config,
                            output_path='tmp')

    plot_probability_of_state_vibrational_T(
                            prob_state_dict=prob_state_dict,
                            vibrational_number=vibrational_number,
                            legend_name=legend_name,
                            fig_name_out=fig_name_prob,
                            fig_config=fig_config,
                            output_path='tmp')



# Kerl Polarizability (function of temperature)
    temperature_K = np.linspace(0, 2000, 100)
    wavelength_nm = 633
    pol_Kerl_N2 = optics.kerl_polarizability_temperature(
                                        temperature_K=temperature_K,
                                        molecule='N2',
                                        wavelength_nm=wavelength_nm)

    pol_Kerl_O2 = optics.kerl_polarizability_temperature(
                                        temperature_K=temperature_K,
                                        molecule='O2',
                                        wavelength_nm=wavelength_nm)

    pol_Kerl_Air = optics.kerl_polarizability_temperature(
                                        temperature_K=temperature_K,
                                        molecule='Air',
                                        wavelength_nm=wavelength_nm)

    plot_polarizability_T(temperature_K=temperature_K, kerl_N2=pol_Kerl_N2,
                        kerl_O2=pol_Kerl_O2, kerl_Air=pol_Kerl_Air,
                        fig_config=fig_config, wavelength_nm=wavelength_nm,
                        output_path='tmp')
