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
optical_flag = True  # add optical properties to the dictionaries 
data_in      = helper.pickle_manager(file_in, pickle_path)

if optical_flag:
    for d in data_in:
        data_in[d].pop('optics', None)
        density_dict = { 'N'  : data_in[d]['Density_0'],
                         'O'  : data_in[d]['Density_1'],
                         'NO' : data_in[d]['Density_2'],
                         'N2' : data_in[d]['Density_3'],
                         'O2' : data_in[d]['Density_4'] } #[kg/m3]

        mass_frac_dict = { 'N'  : data_in[d]['MassFrac_0'],
                           'O'  : data_in[d]['MassFrac_1'],
                           'NO' : data_in[d]['MassFrac_2'],
                           'N2' : data_in[d]['MassFrac_3'],
                           'O2' : data_in[d]['MassFrac_4'] } #[ ]

        total_density = 0.0 
        for i in density_dict:
            total_density += density_dict[i] 

        # Optic properties dictionary 
        optics_dict         = { } 
        index_of_refraction = optics.index_of_refraction(density_dict)  
        #reflectivity        = optics.reflectivity(index_of_refraction) 
        dielectric_const_m  = optics.dielectric_material_const(
                              index_of_refraction) 
        optical_path_length = optics.optical_path_length(
                              index_of_refraction, data_in[d]['Distance'])
        optics_dict['index_of_refraction'] = index_of_refraction
        #optics_dict['reflectivity']        = reflectivity 
        optics_dict['dielectric_constant'] = dielectric_const_m 
        optics_dict['optical_path_length'] = optical_path_length 
        optics_dict['mass_fraction']       = mass_frac_dict 
        optics_dict['density']             = total_density
        # Add optics dictionary to pickle dictionary
        data_in[d]['optics'] = optics_dict 
    helper.pickle_manager(file_in, pickle_path, data_in)   



# Plot Laminar Chemistry cases comparing mach numbers
mackey_flag    = False 
plotting_axis  = 'x'
plotting_label = 'X'
plotting_axis  = 'Distance'
plotting_label = 'Normal'
if mackey_flag:
    mackey_1 = 'mackeyChem_1_stag'
    mackey_2 = 'mackeyChem_2_stag'
    mackey_3 = 'mackeyChem_3_stag'
    save_name = 'mackeyLaminarChemistry'

if not mackey_flag:
    mackey_1 = 'eyiChem_1_stag'
    mackey_2 = 'eyiChem_6_stag'
    mackey_3 = 'eyiChem_12_stag'

    mackey_1 = 'laminarChem_12_stag'
    mackey_2 = 'laminarFrozen_12_stag'
    mackey_3 = 'turbulentChem_12_stag'
    save_name = 'eyiCase12'
    mackey_1 = 'laminarChem_12_diag'
    mackey_2 = 'laminarFrozen_12_diag'
    mackey_3 = 'turbulentChem_12_diag'
    save_name = 'eyiCase12Diag'

case_a  = data_in[mackey_1] 
case_b  = data_in[mackey_2] 
case_c  = data_in[mackey_3] 

plots_path = '/Users/martin/Desktop/results'
lines = ['solid', 'dashed', 'dashdot', '--', 
         (5, (10, 3)), (0, (3,10,1,10))]
title_size=15
label_size=13

# NOTE:MACKEY 
# Plot Mass fraction 
if mackey_flag:
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14,8))
#fig.tight_layout()
    for indx, key in enumerate(case_a['optics']['mass_fraction']):
        ax1.plot(case_a['x']*1E3, 
                 case_a['optics']['mass_fraction'][key], 
                 linestyle=lines[indx], label=f'{key}', linewidth=2.5)
        ax2.plot(case_b['x']*1E3, 
                 case_b['optics']['mass_fraction'][key], 
                 linestyle=lines[indx], label=f'{key}', linewidth=2.5)
        ax3.plot(case_c['x']*1E3, 
                 case_c['optics']['mass_fraction'][key], 
                 linestyle=lines[indx], label=f'{key}', linewidth=2.5)
    ax1.set_title('M = 11.2', fontsize=title_size)
    ax2.set_title('M = 13.2', fontsize=title_size)
    ax3.set_title('M = 15.2', fontsize=title_size)
    ax1.set_xlim(-2, 0)
    ax2.set_xlim(-2, 0)
    ax3.set_xlim(-2, 0)
    ax1.set_xlabel('X $[mm]$', fontsize=label_size)
    ax1.set_ylabel('Mass Fraction', fontsize=label_size)
    ax2.set_xlabel('X $[mm]$', fontsize=label_size)
    ax2.set_ylabel('Mass Fraction', fontsize=label_size)
    ax3.set_xlabel('X $[mm]$', fontsize=label_size)
    ax3.set_ylabel('Mass Fraction', fontsize=label_size)
    ax1.legend() 
    ax2.legend() 
    ax3.legend() 
    plt.savefig(os.path.join(plots_path, f'{save_name}_massFraction.png'),
                bbox_inches='tight', dpi=300)
    plt.close() 

# Plot Temperatures
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18,8))
#fig.tight_layout()
    ax1.plot(case_a['x']*1E3, case_a['Temperature_tr'],
             linestyle=lines[0], label='$T_{tr}$', linewidth=2.5)
    ax1.plot(case_a['x']*1E3, case_a['Temperature_ve'],
             linestyle=lines[1], label='$T_{ve}$', linewidth=2.5)

    ax2.plot(case_b['x']*1E3, case_b['Temperature_tr'],
             linestyle=lines[0], label='$T_{tr}$', linewidth=2.5)
    ax2.plot(case_b['x']*1E3, case_b['Temperature_ve'],
             linestyle=lines[1], label='$T_{ve}$', linewidth=2.5)

    ax3.plot(case_c['x']*1E3, case_c['Temperature_tr'],
             linestyle=lines[0], label='$T_{tr}$', linewidth=2.5)
    ax3.plot(case_c['x']*1E3, case_c['Temperature_ve'],
             linestyle=lines[1], label='$T_{ve}$', linewidth=2.5)

    ax1.set_title('M = 11.2', fontsize=title_size)
    ax2.set_title('M = 13.2', fontsize=title_size)
    ax3.set_title('M = 15.2', fontsize=title_size)
    ax1.set_xlim(-2, 0)
    ax2.set_xlim(-2, 0)
    ax3.set_xlim(-2, 0)
    ax1.set_ylim(0, 11000)
    ax2.set_ylim(0, 11000)
    ax3.set_ylim(0, 11000)
    ax1.set_xlabel('X $[mm]$', fontsize=label_size)
    ax1.set_ylabel('Temperature $[K]$', fontsize=label_size)
    ax2.set_xlabel('X $[mm]$', fontsize=label_size)
    ax2.set_ylabel('Temperature $[K]$', fontsize=label_size)
    ax3.set_xlabel('X $[mm]$')
    ax3.set_ylabel('Temperature $[K]$', fontsize=label_size)
    ax1.legend() 
    ax2.legend() 
    ax3.legend() 
    plt.savefig(os.path.join(plots_path, f'{save_name}_temperature.png'),
                bbox_inches='tight', dpi=300)
    plt.close() 

## Optics  
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(21,9))
#fig.tight_layout()
## Density 
    ax1.plot(case_a['x']*1E3, case_a['optics']['density'], 
             linestyle=lines[0], label='M = 11.2', linewidth=2.5)
    ax1.plot(case_b['x']*1E3, case_b['optics']['density'], 
             linestyle=lines[1], label='M = 13.2', linewidth=2.5)
    ax1.plot(case_c['x']*1E3, case_c['optics']['density'], 
             linestyle=lines[2], label='M = 15.2', linewidth=2.5)
    ax1.set_xlim(-2.3, 0)
    ax1.set_ylim(0.01, 0.2)
    ax1.set_ylabel('Density $[kg/m^3]$', fontsize=label_size)
    ax1.set_xlabel('X $[mm]$', fontsize=label_size)
    ax1.legend() 

## Index of Refraction 
    ax2.plot(case_a['x']*1E3, 
             case_a['optics']['index_of_refraction']['dilute'], 
             linestyle=lines[0], label='dilute, M = 11.2',
             linewidth=2.5)
    ax2.plot(case_a['x']*1E3, 
             case_a['optics']['index_of_refraction']['dense'], 
             linestyle=lines[1], label='dense, M = 11.2',
             linewidth=2.5)

    ax2.plot(case_b['x']*1E3, 
             case_b['optics']['index_of_refraction']['dilute'], 
             linestyle=lines[2], label='dilute, M = 13.2',
             linewidth=2.5)
    ax2.plot(case_b['x']*1E3, 
             case_b['optics']['index_of_refraction']['dense'], 
             linestyle=lines[3], label='dense, M = 13.2',
             linewidth=2.5)

    ax2.plot(case_c['x']*1E3, 
             case_c['optics']['index_of_refraction']['dilute'], 
             linestyle=lines[4], label='dilute, M = 15.2',
             linewidth=2.5)
    ax2.plot(case_c['x']*1E3, 
             case_c['optics']['index_of_refraction']['dense'], 
             linestyle=lines[5], label='dense, M = 15.2',
             linewidth=2.5)

    ax2.set_ylabel('Index of Refraction', fontsize=label_size)
    ax2.set_xlabel('X $[mm]$', fontsize=label_size)
    ax2.set_xlim(-2.3, 0)
    ax2.set_ylim(1, 1.00005)
    ax2.legend() 

## Dielectric constants 
    ax3.plot(case_a['x']*1E3, 
             case_a['optics']['dielectric_constant']['dilute'], 
             linestyle=lines[0], label='dilute, M = 11.2',
             linewidth=2.5)
    ax3.plot(case_a['x']*1E3, 
             case_a['optics']['dielectric_constant']['dense'], 
             linestyle=lines[1], label='dense, M = 11.2',
             linewidth=2.5)

    ax3.plot(case_b['x']*1E3, 
             case_b['optics']['dielectric_constant']['dilute'], 
             linestyle=lines[2], label='dilute, M = 13.2',
             linewidth=2.5)
    ax3.plot(case_b['x']*1E3, 
             case_b['optics']['dielectric_constant']['dense'], 
             linestyle=lines[3], label='dense, M = 13.2',
             linewidth=2.5)

    ax3.plot(case_c['x']*1E3, 
             case_c['optics']['dielectric_constant']['dilute'], 
             linestyle=lines[4], label='dilute, M = 15.2',
             linewidth=2.5)
    ax3.plot(case_c['x']*1E3, 
             case_c['optics']['dielectric_constant']['dense'], 
             linestyle=lines[5], label='dense, M = 15.2',
             linewidth=2.5)

    ax3.set_ylabel('Dielectric constant $[Fm^{-1}]$', fontsize=label_size)
    ax3.set_xlabel('X $[mm]$', fontsize=label_size)
    ax3.set_xlim(-2.3, 0)
    ax3.set_ylim(8.8542E-12, 8.855E-12) 
    ax3.legend() 
    plt.savefig(os.path.join(plots_path, f'{save_name}_Optics.png'),
                bbox_inches='tight', dpi=300)
    plt.close() 

# NOTE: EYI # 
if not mackey_flag:
# Plot Mass fraction 
    #fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14,8))
    fig, (ax1, ax3) = plt.subplots(1, 2, figsize=(14,8))
    #fig.tight_layout()
    for indx, key in enumerate(case_a['optics']['mass_fraction']):
        ax1.plot(case_a[plotting_axis]*1E3, 
                 case_a['optics']['mass_fraction'][key], 
                 linestyle=lines[indx], label=f'{key}', linewidth=2.5)
        '''
        ax2.plot(case_b[plotting_axis]*1E3, 
                 case_b['optics']['mass_fraction'][key], 
                 linestyle=lines[indx], label=f'{key}', linewidth=2.5)
        '''
        ax3.plot(case_c[plotting_axis]*1E3, 
                 case_c['optics']['mass_fraction'][key], 
                 linestyle=lines[indx], label=f'{key}', linewidth=2.5)
    '''
    ax1.set_title('P = 8.18 $[Pa]$', fontsize=title_size)
    ax2.set_title('P = 445  $[Pa]$', fontsize=title_size)
    ax3.set_title('P = 3519 $[Pa]$', fontsize=title_size)
    '''
    ax1.set_title('Laminar Chemistry', fontsize=title_size)
    #ax2.set_title('Laminar Frozen', fontsize=title_size)
    ax3.set_title('Turbulent Chemistry', fontsize=title_size)
    # Comment for diagonal plots 
    '''
    ax1.set_xlim(-2, 0)
    #ax2.set_xlim(-2, 0)
    ax3.set_xlim(-2, 0)
    '''
    # Comment for diagonal plots 
    ax1.set_xlabel(f'{plotting_label} $[mm]$', fontsize=label_size)
    ax1.set_ylabel('Mass Fraction', fontsize=label_size)
    #ax2.set_xlabel(f'{plotting_label} $[mm]$', fontsize=label_size)
    #ax2.set_ylabel('Mass Fraction', fontsize=label_size)
    ax3.set_xlabel(f'{plotting_label} $[mm]$', fontsize=label_size)
    ax3.set_ylabel('Mass Fraction', fontsize=label_size)
    ax1.legend() 
    #ax2.legend() 
    ax3.legend() 
    plt.savefig(os.path.join(plots_path, f'{save_name}_massFraction.png'),
                bbox_inches='tight', dpi=300)
    plt.close() 

# Plot Temperatures
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18,8))
#fig.tight_layout()
    ax1.plot(case_a[plotting_axis]*1E3, case_a['Temperature_tr'],
             linestyle=lines[0], label='$T_{tr}$', linewidth=2.5)
    ax1.plot(case_a[plotting_axis]*1E3, case_a['Temperature_ve'],
             linestyle=lines[1], label='$T_{ve}$', linewidth=2.5)

    ax2.plot(case_b[plotting_axis]*1E3, case_b['Temperature_tr'],
             linestyle=lines[0], label='$T_{tr}$', linewidth=2.5)
    ax2.plot(case_b[plotting_axis]*1E3, case_b['Temperature_ve'],
             linestyle=lines[1], label='$T_{ve}$', linewidth=2.5)

    ax3.plot(case_c[plotting_axis]*1E3, case_c['Temperature_tr'],
             linestyle=lines[0], label='$T_{tr}$', linewidth=2.5)
    ax3.plot(case_c[plotting_axis]*1E3, case_c['Temperature_ve'],
             linestyle=lines[1], label='$T_{ve}$', linewidth=2.5)

    '''
    ax1.set_title('P = 8.18 $[Pa]$', fontsize=title_size)
    ax2.set_title('P = 445  $[Pa]$', fontsize=title_size)
    ax3.set_title('P = 3519 $[Pa]$', fontsize=title_size)
    '''
    ax1.set_title('Laminar Chemistry', fontsize=title_size)
    ax2.set_title('Laminar Frozen', fontsize=title_size)
    ax3.set_title('Turbulent Chemistry', fontsize=title_size)
    # Comment for diagonal plots 
    '''
    ax1.set_xlim(-2, 0)
    ax2.set_xlim(-2, 0)
    ax3.set_xlim(-2, 0)
    '''
    ax1.set_ylim(0, 15000)
    ax2.set_ylim(0, 15000)
    ax3.set_ylim(0, 15000)
    ax1.set_ylim(0, 8000)
    ax2.set_ylim(0, 8000)
    ax3.set_ylim(0, 8000)
    # Comment for diagonal plots 
    ax1.set_xlabel(f'{plotting_label} $[mm]$')
    ax1.set_ylabel('Temperature $[K]$', fontsize=label_size)
    ax2.set_xlabel(f'{plotting_label} $[mm]$')
    ax2.set_ylabel('Temperature $[K]$', fontsize=label_size)
    ax3.set_xlabel(f'{plotting_label} $[mm]$')
    ax3.set_ylabel('Temperature $[K]$', fontsize=label_size)
    ax1.legend() 
    ax2.legend() 
    ax3.legend() 
    plt.savefig(os.path.join(plots_path, f'{save_name}_temperature.png'),
                bbox_inches='tight', dpi=300)
    plt.close() 

## Optics  
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(23,9))
#fig.tight_layout()
## Density 
    ax1.plot(case_a[plotting_axis]*1E3, case_a['optics']['density'], 
             #linestyle=lines[0], label='P = 8.18', linewidth=2.5)
             linestyle=lines[0], label='Laminar Chemistry', linewidth=2.5)
    ax1.plot(case_b[plotting_axis]*1E3, case_b['optics']['density'], 
             #linestyle=lines[1], label='P = 445 $[Pa]$', linewidth=2.5)
             linestyle=lines[1], label='Laminar Frozen', linewidth=2.5)
    ax1.plot(case_c[plotting_axis]*1E3, case_c['optics']['density'], 
             #linestyle=lines[2], label='P = 3519 $[Pa]$', linewidth=2.5)
             linestyle=lines[2], label='Turbulent Chemistry', linewidth=2.5)
    # Comment for diagonal plots 
    '''
    ax1.set_xlim(-2, 0)
    ax1.set_ylim(0.05, 0.8)
    '''
    # Comment for diagonal plots 
    ax1.set_ylabel('Density $[kg/m^3]$', fontsize=label_size)
    ax1.set_xlabel(f'{plotting_label} $[mm]$', fontsize=label_size)
    ax1.legend() 

## Index of Refraction 
    ax2.plot(case_a[plotting_axis]*1E3, 
             case_a['optics']['index_of_refraction']['dilute'], 
             #linestyle=lines[0], label='dilute, P = 8.18 $[Pa]$',
             linestyle=lines[0], label='dilute, Laminar Chemistry',
             linewidth=2.5)
    ax2.plot(case_a[plotting_axis]*1E3, 
             case_a['optics']['index_of_refraction']['dense'], 
             #linestyle=lines[1], label='dense, P = 8.18 $[Pa]$',
             linestyle=lines[1], label='dense, Laminar Chemistry',
             linewidth=2.5)

    ax2.plot(case_b[plotting_axis]*1E3, 
             case_b['optics']['index_of_refraction']['dilute'], 
             #linestyle=lines[2], label='dilute, P = 445 $[Pa]$',
             linestyle=lines[2], label='dilute, Laminar Frozen',
             linewidth=2.5)
    ax2.plot(case_b[plotting_axis]*1E3, 
             case_b['optics']['index_of_refraction']['dense'], 
             #linestyle=lines[3], label='dense, P = 445 $[Pa]$',
             linestyle=lines[3], label='dense, Laminar Frozen',
             linewidth=2.5)

    ax2.plot(case_c[plotting_axis]*1E3, 
             case_c['optics']['index_of_refraction']['dilute'], 
             #linestyle=lines[4], label='dilute, P = 3519 $[Pa]$',
             linestyle=lines[4], label='dilute, Turbulent Chemistry',
             linewidth=2.5)
    ax2.plot(case_c[plotting_axis]*1E3, 
             case_c['optics']['index_of_refraction']['dense'], 
             #linestyle=lines[5], label='dense, P = 3519 $[Pa]$',
             linestyle=lines[5], label='dense, Turbulent Chemistry',
             linewidth=2.5)

    ax2.set_ylabel('Index of Refraction', fontsize=label_size)
    ax2.set_xlabel(f'{plotting_label} $[mm]$', fontsize=label_size)
    # Comment for diagonal plots 
    '''
    ax2.set_xlim(-2, 0)
    ax2.set_ylim(1.00001, 1.0002)
    '''
    # Comment for diagonal plots 
    ax2.legend() 

## Dielectric constants 
    ax3.plot(case_a[plotting_axis]*1E3, 
             case_a['optics']['dielectric_constant']['dilute'], 
             #linestyle=lines[0], label='dilute, P = 8.18 $[Pa]$',
             linestyle=lines[0], label='dilute, Laminar Chemistry',
             linewidth=2.5)
    ax3.plot(case_a[plotting_axis]*1E3, 
             case_a['optics']['dielectric_constant']['dense'], 
             #linestyle=lines[1], label='dense, P = 8.18 $[Pa]$',
             linestyle=lines[1], label='dense, Laminar Chemistry',
             linewidth=2.5)

    ax3.plot(case_b[plotting_axis]*1E3, 
             case_b['optics']['dielectric_constant']['dilute'], 
             #linestyle=lines[2], label='dilute, P = 445 $[Pa]$',
             linestyle=lines[2], label='dilute, Laminar Frozen',
             linewidth=2.5)
    ax3.plot(case_b[plotting_axis]*1E3, 
             case_b['optics']['dielectric_constant']['dense'], 
             #linestyle=lines[3], label='dense, P = 445 $[Pa]$',
             linestyle=lines[3], label='dense, Laminar Frozen',
             linewidth=2.5)

    ax3.plot(case_c[plotting_axis]*1E3, 
             case_c['optics']['dielectric_constant']['dilute'], 
             #linestyle=lines[4], label='dilute, P = 3519 $[Pa]$',
             linestyle=lines[4], label='dilute, Turbulent Chemistry',
             linewidth=2.5)
    ax3.plot(case_c[plotting_axis]*1E3, 
             case_c['optics']['dielectric_constant']['dense'], 
             #linestyle=lines[5], label='dense, P = 3519 $[Pa]$',
             linestyle=lines[5], label='dense, Turbulent Chemistry',
             linewidth=2.5)

    ax3.set_ylabel('Dielectric constant $[Fm^{-1}]$', fontsize=label_size)
    ax3.set_xlabel(f'{plotting_label} $[mm]$', fontsize=label_size)
    # Comment for diagonal plots 
    '''
    ax3.set_xlim(-2, 0)
    ax3.set_ylim(8.8544E-12, 8.8575E-12) 
    '''
    # Comment for diagonal plots 
    ax3.legend() 
    plt.savefig(os.path.join(plots_path, f'{save_name}_Optics.png'),
                bbox_inches='tight', dpi=300)
    plt.close() 




