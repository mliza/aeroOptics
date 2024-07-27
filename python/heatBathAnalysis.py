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
import matplotlib.pyplot as plt 

# My Packages 
scripts_path   = os.environ.get('SCRIPTS')
python_scripts = os.path.join(scripts_path, 'Python')
sys.path.append(python_scripts) 
import optics
import helper_functions as helper 
import aerodynamic_functions as aero


def plot_fields(df_in, gd_const, gds_vec, density_dict, 
                index_refraction, png_path, csv_in, pickle_flag=False):

    pickle_path = os.path.join(png_path, 'pickle') 
    # Plot Density
    fig = plt.figure()
    for i in density_dict.keys(): 
        plt.semilogx(df_in['time'], density_dict[i], linewidth=2, label=f'${i}$')
    plt.legend()
    plt.xlabel('Time $[s]$')
    plt.ylabel('Density $[kg/m^3]$')
    plt.savefig(os.path.join(png_path, 
                f'{csv_in}_densityTime.png'),
                format='png', bbox_inches='tight', dpi=1200)
    if pickle_flag:
        pickle.dump(fig, open(os.path.join(pickle_path,
                                f'{csv_in}_densityTime.pickle'), 'wb'))
    plt.close() 


    # Plot Specific Gladstone-Dale constant
    fig = plt.figure()
    for i in density_dict.keys(): 
        plt.semilogx(df_in['time'], gd_const[i]*1E4, linewidth=2, label=f'${i}$')
    plt.legend()
    plt.xlabel('Time $[s]$')
    plt.ylabel('GladstoneDale const $\\times 10^{-4}\,[m^3/kg]$')
    plt.savefig(os.path.join(png_path, 
                f'{csv_in}_gladstoneSpecificTime.png'),
                format='png', bbox_inches='tight', dpi=1200)
    if pickle_flag:
        pickle.dump(fig, open(os.path.join(pickle_path, 
                            f'{csv_in}_gladstoneSpecificTime.pickle'), 'wb'))
    plt.close()

    # Plot Temperatures
    fig = plt.figure()
    plt.semilogx(df_in['time'], df_in['Tt'], linewidth=2, label='$T_{tr}$')
    plt.semilogx(df_in['time'], df_in['Tv'], linewidth=2, label='$T_{vr}$')
    plt.ylabel('Temperature $[K]$')
    plt.xlabel('Time $[s]$')
    plt.legend()
    plt.savefig(os.path.join(png_path, 
                f'{csv_in}_temperatureTime.png'),
                format='png', bbox_inches='tight', dpi=1200)
    if pickle_flag:
        pickle.dump(fig, open(os.path.join(pickle_path, 
                    f'{csv_in}_gladstoneSpecificTime.pickle'), 'wb'))
    plt.close() 

    # Plot Index of Refraction
    fig = plt.figure()
    plt.semilogx(df_in['time'], index_refraction['dilute'], linewidth=2)
    plt.xlabel('Time $[s]$')
    plt.ylabel('Index of refraction $[\;]$')
    plt.savefig(os.path.join(png_path, 
                f'{csv_in}_indexOfRefractionTime.png'),
                format='png', bbox_inches='tight', dpi=1200)
    if pickle_flag:
        pickle.dump(fig, open(os.path.join(pickle_path, 
        f'{csv_in}_indexOfRefractionTime.pickle'), 'wb'))
    plt.close() 

    # Plot GD using density_dict and GD at sea level 
    fig = plt.figure()
    plt.semilogx(df_in['time'], gd_const['gladstone_dale'] * 1E4, linewidth=2,
    label='flow')
    plt.plot(df_in['time'], gds_vec * 1E4, linewidth=2, label='atm')
    plt.xlabel('Time $[s]$')
    plt.ylabel('GladstoneDale const $\\times 10^{-4}\,[m^3/kg]$')
    plt.legend()
    plt.savefig(os.path.join(png_path,
                f'{csv_in}_gladstonedaleConstTime.png'),
                format='png', bbox_inches='tight', dpi=1200)
    if pickle_flag:
        pickle.dump(fig, open(os.path.join(pickle_path, 
        f'{csv_in}_gladstonedaleConstTime.pickle'), 'wb'))
    plt.close() 


def main():
    data_path = '/Users/martin/Documents/Research/UoA/Projects/aeroOptics/data'
    data_out = 'outputFigures'

    files_in = os.listdir(data_path)
    for i in files_in: 
        df_in = pd.read_csv(os.path.join(data_path, i), index_col=False) 

        # Create a density dictionary
        density_dict = { }
        density_dict['N2'] = df_in['rhoN2'].to_numpy()
        density_dict['N'] = df_in['rhoN'].to_numpy()
        density_dict['O2'] = df_in['rhoO2'].to_numpy()
        density_dict['O'] = df_in['rhoO'].to_numpy()
        density_dict['NO'] = df_in['rhoNO'].to_numpy()

        # Add ions to the dictionary 
        # TODO: fix string and 
        if i.split('_')[0] == '11Air':
            density_dict['N2+'] = df_in['rhoN2+'].to_numpy()
            density_dict['N+'] = df_in['rhoN+'].to_numpy()
            density_dict['O2+'] = df_in['rhoO2+'].to_numpy()
            density_dict['O+'] = df_in['rhoO+'].to_numpy()
            density_dict['NO+'] = df_in['rhoNO+'].to_numpy()
            #density_dict['e+'] = df_in['rhoE'].to_numpy()

        # Gladstone-Dale constants and index of refraction using heath bath data
        gd_const = optics.Gladstone_Dale(density_dict)
        index_refraction = optics.index_of_refraction(density_dict)

        # Gladstone-Dale constant and index of refraction at sea level
        gd = optics.Gladstone_Dale()
        gds = optics.atmospheric_gladstoneDaleConstant(0.0) #[m]
        gds_vec = gds * np.ones(np.shape(df_in['time'])) 

        # Plot data fields 
        plot_fields(df_in, gd_const, gds_vec,
                    density_dict, index_refraction, data_out, i.split('.')[0],
                    pickle_flag=True)

if __name__=="__main__":
    main()
