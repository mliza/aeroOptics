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
    f'polKerl_{wavelength_nm}nm.png'), format = 'png',
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
    plt.xticks(range(np.min(vibrational_number), (np.max(vibrational_number) + 1)))
    plt.legend()
    plt.xlabel('Vibrational number $[\;]$', fontsize=fig_config['label_size'])
    plt.ylabel('Probability of state $[\;]$', fontsize=fig_config['label_size'])

    plt.savefig(os.path.join(output_png_path,
    f'{fig_name_out}'), format = 'png',
    bbox_inches='tight', dpi=fig_config['dpi_size']) 
    plt.close()

def plot_polarizability_buldakov(**kargs):
    fig_config = kargs['fig_config']
    pol_dict = kargs['pol_dict']
    vibrational_number = kargs['vibrational_number']
    fig_name_out = kargs['fig_name_out']
    output_png_path = kargs['output_path']
    for j in pol_dict.keys():
        plt.plot(vibrational_number, pol_dict[j], 
                    linewidth=fig_config['line_width'],
                    label=f'J = {j}')
    plt.xticks(range(np.min(vibrational_number), (np.max(vibrational_number) + 1)))
    plt.legend()
    plt.xlabel('Vibrational number $[\;]$', fontsize=fig_config['label_size'])
    plt.ylabel('Polarizability $[m^3]$', fontsize=fig_config['label_size'])

    plt.savefig(os.path.join(output_png_path,
    f'{fig_name_out}'), format = 'png',
    bbox_inches='tight', dpi=fig_config['dpi_size']) 
    plt.close()


def plot_partition_function_vibrational_T(**kargs):
    fig_config = kargs['fig_config']
    part_funct_dict = kargs['part_func_dict']
    vibrational_number = kargs['vibrational_number']
    legend_name = kargs['legend_name'] 
    fig_name_out = kargs['fig_name_out']
    output_png_path = kargs['output_path']
    for t in part_funct_dict.keys():
        plt.semilogy(vibrational_number, prob_state_dict[t], 'o-', 
                    linewidth=fig_config['line_width'],
                    label=f'{legend_name}, T = {t} $[K]$')
    plt.xticks(range(np.min(vibrational_number), (np.max(vibrational_number) + 1)))
    plt.legend()
    plt.xlabel('Vibrational number $[\;]$', fontsize=fig_config['label_size'])
    plt.ylabel('Partition function $[\;]$', fontsize=fig_config['label_size'])

    plt.savefig(os.path.join(output_png_path,
    f'{fig_name_out}'), format = 'png',
    bbox_inches='tight', dpi=fig_config['dpi_size']) 
    plt.close()

def plot_polarizability_buldakov_surface(**kargs):
    fig_config = kargs['fig_config']
    vib_mesh = kargs['x_mesh']
    rot_mesh = kargs['y_mesh']
    fig_name_out = kargs['fig_name_out']
    output_png_path = kargs['output_path']
    buldakov_polarizability_2D = kargs['z_func']
    legend_name = kargs['legend_name']

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(7, 6))
    ax.view_init(elev=17, azim=-125, roll=0.0)
    surf = ax.plot_surface(vib_mesh, rot_mesh,
                           buldakov_polarizability_2D, label=f'{legend_name}',
                           cmap='plasma', linewidth=0, antialiased=False)
    """
    ax.contourf(vib_mesh, rot_mesh, buldakov_polarizability_2D,
                zdir='z', offset=1.5E30, cmap='plasma')
    """
    fig.colorbar(surf, shrink=0.5, aspect=10, pad=0.07)
    ax.set_xticklabels(ax.get_xticks().astype(int))
    ax.set_yticklabels(ax.get_yticks().astype(int))
    #ax.set_zticks([])
    ax.set_xlabel('Vibrational number $[\;]$', fontsize=fig_config['label_size'])
    ax.set_ylabel('Rotational number $[\;]$', fontsize=fig_config['label_size'])
    ax.set_zlabel('Polarizability $[m^3]$', fontsize=fig_config['label_size'])
    ax.grid(False)
    #ax.legend()

    plt.savefig(os.path.join(output_png_path,
    f'{fig_name_out}'), format = 'png',
    dpi=fig_config['dpi_size'], pad_inches=0.01) 
    #bbox_inches='tight', dpi=fig_config['dpi_size'], pad_ines=0) 
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
    vibrational_num_max = 21
    rotational_num_max = 30
    vibrational_number = np.arange(0, vibrational_num_max)
    molecule='O2'
    fig_name_prob = f'probState{molecule}_J{rotational_num_max}.png'
    fig_name_part = f'partFunction{molecule}_J{rotational_num_max}.png'
    fig_name_pol  = f'polBuldakov{molecule}.png'
    legend_name = f'$J$ = {rotational_num_max}'

    prob_state_dict = { }
    partition_function_dict = { }
    buldakov_polarizability = { }

    for t in temperature_K:
        prob_state_dict[t] = np.zeros(vibrational_num_max)
        partition_function_dict[t] = np.zeros(vibrational_num_max)

    for t in temperature_K:
        for v in vibrational_number:
            prob_state_dict[t][v] = optics.probability_of_state(
                                    temperature_K=int(t),
                                    vibrational_number=v,
                                    rotational_number=rotational_num_max,
                                    molecule=f'{molecule}')

            partition_function_dict[t][v] = optics.partition_function(
                                    temperature_K=int(t),
                                    vibrational_number=v,
                                    rotational_number=rotational_num_max,
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

    rotational_number = ['1', '10', '20'] 
    legend_name = f'$J$ = {rotational_number}'
    for j in rotational_number:
        buldakov_polarizability[j] = np.zeros(vibrational_num_max)
        for v in vibrational_number:
            # Buldakov Polarizability (function of rotational and vibrational numbers)
            buldakov_polarizability[j][v] = optics.buldakov_polarizability(
                                        vibrational_number=v, 
                                        rotational_number=int(j),
                                        molecule=f'{molecule}')

    plot_polarizability_buldakov(pol_dict=buldakov_polarizability,
                            vibrational_number=vibrational_number,
                            fig_name_out=fig_name_pol,
                            fig_config=fig_config,
                            output_path='tmp')


    
    # Polarizability Buldakov function of rotational and vibrational
    vibrational_numbers = np.arange(0, vibrational_num_max)
    rotational_numbers = np.arange(0, rotational_num_max)
    vib_mesh, rot_mesh = np.meshgrid(vibrational_numbers, rotational_numbers)
    buldakov_polarizability_2D = np.zeros([rotational_num_max,
                                           vibrational_num_max])
    fig_name_out = f'surfacePolBuldakov{molecule}.png'
    for v in vibrational_numbers:
        for j in rotational_numbers:
            buldakov_polarizability_2D[j][v] = optics.buldakov_polarizability(
                                        vibrational_number=v, 
                                        rotational_number=j,
                                        molecule=f'{molecule}')

    plot_polarizability_buldakov_surface(x_mesh=vib_mesh,
                                         y_mesh=rot_mesh,
                                         z_func=buldakov_polarizability_2D,
                                         fig_name_out=fig_name_out,
                                         fig_config=fig_config,
                                         legend_name=f'{molecule}',
                                         output_path='tmp')


    temperature_K_max = 2000
    vibrational_number = np.arange(0, vibrational_num_max)
    temperature_K = np.arange(100, 2550, 50)
    buldakov_expectation_value = np.zeros([vibrational_num_max])

    prob_state = np.zeros([vibrational_num_max, np.shape(temperature_K)[0]])
    vib_mesh, temp_mesh = np.meshgrid(temperature_K, vibrational_number)
    for v in vibrational_numbers: 
        buldakov_expectation_value[v] = optics.buldakov_polarizability(
                                        vibrational_number=v, 
                                        rotational_number=rotational_num_max,
                                        molecule=f'{molecule}')
        for indx, val in enumerate(temperature_K):
            prob_state[v][indx] = optics.probability_of_state(
                                    temperature_K=val,
                                    vibrational_number=v,
                                    rotational_number=rotational_num_max,
                                    molecule=f'{molecule}')
    np.expand_dims(buldakov_expectation_value,1)
    tot_pol = prob_state.transpose() * buldakov_expectation_value

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(7, 6))
    ax.view_init(elev=17, azim=-125, roll=0.0)
    surf = ax.plot_surface(vib_mesh, temp_mesh,
                           tot_pol.transpose(), #label=f'{legend_name}',
                           cmap='plasma', linewidth=0, antialiased=False)
    plt.show()


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
