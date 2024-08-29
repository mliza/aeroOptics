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
import os 
import sys 
import pickle
import IPython
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt 

# My Packages 
scripts_path   = os.environ.get('SCRIPTS')
python_scripts = os.path.join(scripts_path, 'Python')
sys.path.append(python_scripts) 
import optics
import helper_functions as helper 
import aerodynamic_functions as aero

def plot_fields(df_in : pd.core.frame.DataFrame, gd_const : dict,
                gds_vec : np.array, density_dict : dict,
                index_refraction : dict,
                png_path : str, csv_in :str,
                ion_dict : dict = { },
                cut_dict : dict = { },
                pickle_flag : bool = False) -> None:

    pickle_path = os.path.join(png_path, 'pickle')

    # Figure size
    line_width = 3
    fig_width  = 6
    fig_height = 5
    dpi_size   = 600
    label_size = 15
    matplotlib.rc('xtick', labelsize=10)
    matplotlib.rc('ytick', labelsize=10)
    total_density = sum(density_dict.values()) 

    if ion_dict:
        ion_density = sum(ion_dict.values()) 
        total_density += ion_density
    # Plot Density
    fig = plt.figure(figsize=(fig_width,fig_height))
    for i in density_dict.keys(): 
        plt.semilogx(df_in['time'], density_dict[i]/total_density, linewidth=line_width, label=f'${i}$')
    if cut_dict:
        plt.xlim(cut_dict['density'])
    plt.legend()
    plt.xlabel('Time $[s]$', fontsize=label_size)
    plt.ylabel('Mass fraction $[\;]$', fontsize=label_size)
    plt.savefig(os.path.join(png_path,
                f'{csv_in}_massFractionNeutralTime.png'),
                format='png', bbox_inches='tight', dpi=dpi_size)
    if pickle_flag:
        pickle.dump(fig, open(os.path.join(pickle_path,
                                f'{csv_in}_massFractionNeutralTime.pickle'), 'wb'))
    plt.close()

    # Plot Specific Gladstone-Dale constant
    fig = plt.figure(figsize=(fig_width,fig_height))
    for i in density_dict.keys(): 
        plt.semilogx(df_in['time'], gd_const[i]*1E4, linewidth=line_width, label=f'${i}$')
    if cut_dict:
        plt.xlim(cut_dict['density'])
    plt.legend()
    plt.xlabel('Time $[s]$', fontsize=label_size)
    plt.ylabel('GladstoneDale const $\\times 10^{-4}\,[m^3/kg]$',
               fontsize=label_size)
    plt.savefig(os.path.join(png_path, 
                f'{csv_in}_gladstoneSpecificNeutralTime.png'),
                format='png', bbox_inches='tight', dpi=dpi_size)
    if pickle_flag:
        pickle.dump(fig, open(os.path.join(pickle_path, 
                    f'{csv_in}_gladstoneSpecificNeutralTime.pickle'), 'wb'))
    plt.close()

    # Plot ion-Density
    if ion_dict:
        fig = plt.figure(figsize=(fig_width,fig_height))
        for i in ion_dict.keys():
            plt.semilogx(df_in['time'], (ion_dict[i]/total_density) * 1E4,
                         linewidth=line_width, label=f'${i}$')
        plt.legend()
        plt.xlabel('Time $[s]$', fontsize=label_size)
        plt.ylabel('Mass fraction $\\times 10^{-4}$ $[\;]$', fontsize=label_size)
        if cut_dict:
            plt.xlim(cut_dict['density'])
        plt.savefig(os.path.join(png_path, 
                    f'{csv_in}_massFractionIonTime.png'),
                    format='png', bbox_inches='tight', dpi=dpi_size)
        if pickle_flag:
            pickle.dump(fig, open(os.path.join(pickle_path,
                                    f'{csv_in}_massFractionIonTime.pickle'), 'wb'))
        plt.close()
        # Plot Specific Gladstone-Dale constant
        fig = plt.figure(figsize=(fig_width,fig_height))
        del ion_dict['e+']
        for i in ion_dict.keys():
            plt.semilogx(df_in['time'], gd_const[i]*1E7,
                         linewidth=line_width, label=f'${i}$')
        plt.legend()
        plt.xlabel('Time $[s]$', fontsize=label_size)
        plt.ylabel('GladstoneDale const $\\times 10^{-7}\,[m^3/kg]$',
                   fontsize=label_size)
        if cut_dict:
            plt.xlim(cut_dict['density'])
        plt.savefig(os.path.join(png_path, 
                    f'{csv_in}_gladstoneSpecificIonTime.png'),
                    format='png', bbox_inches='tight', dpi=dpi_size)
        if pickle_flag:
            pickle.dump(fig, open(os.path.join(pickle_path,
                    f'{csv_in}_gladstoneSpecificIonTime.pickle'), 'wb'))
        plt.close()

    # Plot Temperatures
    fig = plt.figure(figsize=(fig_width,fig_height))
    plt.semilogx(df_in['time'], df_in['Tt'], linewidth=line_width, label='$T_{tr}$')
    plt.semilogx(df_in['time'], df_in['Tv'], linewidth=line_width, label='$T_{vr}$')
    plt.xlabel('Time $[s]$', fontsize=label_size)
    plt.ylabel('Temperature $[K]$', fontsize=label_size)
    plt.legend()
    if cut_dict:
        plt.xlim(cut_dict['temperature'])
    plt.savefig(os.path.join(png_path, 
                f'{csv_in}_temperatureTime.png'),
                format='png', bbox_inches='tight', dpi=dpi_size)
    if pickle_flag:
        pickle.dump(fig, open(os.path.join(pickle_path, 
                    f'{csv_in}_gladstoneSpecificTime.pickle'), 'wb'))
    plt.close() 

    # Plot Index of Refraction
    fig = plt.figure(figsize=(fig_width,fig_height))
    plt.semilogx(df_in['time'], (index_refraction['dilute'] - 1) * 10**3, linewidth=line_width)
    plt.xlabel('Time $[s]$', fontsize=label_size)
    plt.ylabel('(Index of refraction - 1)$\\times 10^{-3}$ $[\;]$',
               fontsize=label_size)
    if cut_dict:
        plt.xlim(cut_dict['density'])
    plt.savefig(os.path.join(png_path, 
                f'{csv_in}_indexOfRefractionTime.png'),
                format='png', bbox_inches='tight', dpi=dpi_size)
    if pickle_flag:
        pickle.dump(fig, open(os.path.join(pickle_path, 
        f'{csv_in}_indexOfRefractionTime.pickle'), 'wb'))
    plt.close() 

    # Plot GD using density_dict and GD at sea level 
    fig = plt.figure(figsize=(fig_width,fig_height))
    plt.semilogx(df_in['time'], gd_const['gladstone_dale'] * 1E4, linewidth=line_width,
    label='flow')
    plt.plot(df_in['time'], gds_vec * 1E4, linewidth=line_width, label='atm')
    plt.legend()
    plt.xlabel('Time $[s]$', fontsize=label_size)
    plt.ylabel('GladstoneDale const $\\times 10^{-4}\,[m^3/kg]$',
               fontsize=label_size)
    if cut_dict:
        plt.xlim(cut_dict['density'])
    plt.savefig(os.path.join(png_path,
                f'{csv_in}_gladstonedaleConstTime.png'),
                format='png', bbox_inches='tight', dpi=dpi_size)
    if pickle_flag:
        pickle.dump(fig, open(os.path.join(pickle_path, 
        f'{csv_in}_gladstonedaleConstTime.pickle'), 'wb'))
    plt.close() 


def get_density_dict(data_path : str, f_in : str) -> tuple[dict, object, dict]:
    """
    Load csv files and returns a dictionary with all the densities
    """
    # Loads all csv
    df_in = pd.read_csv(os.path.join(data_path, f_in), index_col=False) 

    # Keys to ignore 
    ignore_keys = ('time', 'Tt', 'Tv', 'e+')
    #gas_type = f_in.split('_')[1]
    if df_in['N2'][0] != 0 and df_in['O2'][0] == 0:
        gas_type = 'N2'
    elif df_in['O2'][0] != 0 and df_in['N2'][0] == 0:
        gas_type = 'O2'
    else:
        gas_type = 'Air'

    if gas_type in ('O2', 'N2'):
        # (false_value, true_value) [condition]
        tmp = (('N', 'N2', 'NO'),('O', 'O2', 'NO'))[gas_type == 'N2']
        ignore_keys += tmp

    density_dict = { }
    ion_dict = { }
    # Create a density dictionary
    for density_key in df_in.keys():
        if density_key in ignore_keys:
            continue
        density_dict[density_key] = df_in[density_key].to_numpy()

    if len(density_dict.keys()) == 10:
        ion_dict['N+'] = density_dict['N+']
        ion_dict['O+'] = density_dict['O+']
        ion_dict['NO+'] = density_dict['NO+']
        ion_dict['N2+'] = density_dict['N2+']
        ion_dict['O2+'] = density_dict['O2+']
        ion_dict['e+'] = df_in['e+'].to_numpy()

    return df_in, density_dict, ion_dict

def get_cut_Thesis():
    cut_dict = { } 
    cut_dict['5H']  = { 'density' : [1E-8, 1E-5], 
                        'index'   : [1E-8, 5E-5],
                        'temperature':[0, 1E-5] }

    cut_dict['3H'] = { 'density' : [1E-9, 1E-7], 
                       'index'   : [1E-9, 5E-7],
                       'temperature':[0, 1E-6] }

    cut_dict['4H'] = { 'density' : [0, 2E-7], 
                        'index'   : [0, 2E-7],
                        'temperature':[0, 5E-7] }

    cut_dict['1H'] = { 'density' : [1E-9, 4E-6], 
                       'index'   : [1E-9, 4E-6],
                       'temperature':[0, 4E-6] }

    cut_dict['2H'] = { 'density' : [1E-9, 1E-6], 
                       'index'   : [1E-9, 1E-6],
                       'temperature':[0, 1E-6] }

    cut_dict['5I'] = { 'density' : [1E-8, 1E-5], 
                       'index'   : [1E-8, 2E-5],
                       'temperature':[0, 1E-5] }

    cut_dict['3I'] = { 'density' : [1E-9, 5E-7], 
                       'index'   : [1E-9, 1E-6],
                       'temperature':[0, 5E-7] }
    return cut_dict

def get_cut_dict():
    cut_dict = { } 
    cut_dict['5_Air_Eyi12'] = { 'density' : [1E-8, 1E-5], 
                                'index'   : [1E-8, 5E-5],
                                'temperature':[0, 1E-5] }

    cut_dict['5_Air_TC2'] = { 'density' : [1E-9, 1E-7], 
                              'index'   : [1E-9, 5E-7],
                              'temperature':[0, 1E-6] }

    cut_dict['5_Air_TC3'] = { 'density' : [0, 2E-7], 
                               'index'   : [0, 2E-7],
                               'temperature':[0, 5E-7] }

    cut_dict['5_N2_TC1A1'] = { 'density' : [1E-9, 4E-6], 
                               'index'   : [1E-9, 4E-6],
                               'temperature':[0, 4E-6] }

    cut_dict['5_O2_TC1A2'] = { 'density' : [1E-9, 1E-6], 
                               'index'   : [1E-9, 1E-6],
                               'temperature':[0, 1E-6] }

    cut_dict['11_Air_Eyi12'] = { 'density' : [1E-8, 1E-5], 
                                 'index'   : [1E-8, 2E-5],
                                 'temperature':[0, 1E-5] }

    cut_dict['11_Air_TC2'] = { 'density' : [1E-9, 5E-7], 
                               'index'   : [1E-9, 1E-6],
                               'temperature':[0, 5E-7] }
    return cut_dict

def main():
    data_path = '/Users/martin/Documents/Research/UoA/Projects/aeroOptics/data'
    data_path = '/Users/martin/Documents/Schools/UoA/Dissertation/CFD/heatBath/outputs'
    data_path = '/Users/martin/Documents/Schools/UoA/Dissertation/CFD/ionization/outputs'

    data_out = 'outputFigures'
    data_out = '/Users/martin/Documents/Schools/UoA/Dissertation/figures/chapter5/heatBath'
    data_out = '/Users/martin/Documents/Schools/UoA/Dissertation/figures/chapter5/ionization'
    files_in = os.listdir(data_path)
    name_in  = [x.split('.')[0] for x in files_in]
    #cut_dict = get_cut_dict()
    cut_dict = get_cut_Thesis()

    for f_in in name_in: 
        df_in, density_dict, ion_dict = get_density_dict(data_path,
                                                        f'{f_in}.csv')

        # Gladstone-Dale constants and index of refraction using heath bath data
        gd_const = optics.Gladstone_Dale(density_dict)
        index_refraction = optics.index_of_refraction(density_dict)

        # Gladstone-Dale constant and index of refraction at sea level
        gd = optics.Gladstone_Dale()
        gds = optics.atmospheric_gladstoneDaleConstant(0.0) #[m]
        gds_vec = gds * np.ones(np.shape(df_in['time'])) 

        # Clean up density dictionary
        if ion_dict:
            del density_dict['N+']
            del density_dict['O+']
            del density_dict['NO+']
            del density_dict['N2+']
            del density_dict['O2+']

        # Plot data fields 
        plot_fields(df_in, gd_const, gds_vec,
                    density_dict, index_refraction, data_out,
                    f_in, ion_dict, cut_dict[f_in],
                    pickle_flag=False)

if __name__=="__main__":
    main()
