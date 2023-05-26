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
optical_flag = False  # add optical properties to the dictionaries 
data_in      = helper.pickle_manager(file_in, pickle_path)

if optical_flag:
    for d in data_in:
        data_in[d].pop('optics', None)
        density_dict = { 'N'  : data_in[d]['Density_0'],
                         'O'  : data_in[d]['Density_1'],
                         'NO' : data_in[d]['Density_2'],
                         'N2' : data_in[d]['Density_3'],
                         'O2' : data_in[d]['Density_4'] } #[kg/m3]

        # Optic properties dictionary 
        optics_dict         = { } 
        index_of_refraction = optics.index_of_refraction(density_dict)  
        reflectivity        = optics.reflectivity(index_of_refraction) 
        dielectric_const_m  = optics.dielectric_material_const(
                              index_of_refraction) 
        optical_path_length = optics.optical_path_length(
                              index_of_refraction, data_in[d]['Distance'])
        optics_dict['index_of_refraction'] = index_of_refraction
        optics_dict['reflectivity']        = reflectivity 
        optics_dict['dielectric_constant'] = dielectric_const_m 
        optics_dict['optical_path_length'] = optical_path_length 
        optics_dict['density']             = density_dict 
        # Add optics dictionary to pickle dictionary
        data_in[d]['optics'] = optics_dict 
    helper.pickle_manager(file_in, pickle_path, data_in)   



caseT = 'mackeyTurbulent_1_stag'
caseF = 'mackeyFrozen_1_stag'
caseC = 'mackeyChem_1_stag' 
case_name = 'mackey1'

eyi_flag = True 
caseC = 'eyiChem_6_stag' 
case_name = 'eyi6'

turbulent = data_in[caseT]
frozen    = data_in[caseF]
chemistry = data_in[caseC]

# Plot Index of refraction 
if not eyi_flag:
    plt.plot(turbulent['x']*1E3, turbulent['optics']['index_of_refraction']['dilute'],
         label='$n_{turbulent}^{dilute}$')
    plt.plot(turbulent['x']*1E3, turbulent['optics']['index_of_refraction']['dense'],
         '.', label='$n_{turbulent}^{dense}$')
    plt.plot(frozen['x']*1E3, frozen['optics']['index_of_refraction']['dilute'], 
         label='$n_{frozen}^{dilute}$')
    plt.plot(frozen['x']*1E3, frozen['optics']['index_of_refraction']['dense'], 
         '.', label='$n_{frozen}^{dense}$')
plt.plot(chemistry['x']*1E3, chemistry['optics']['index_of_refraction']['dilute'], 
        label='$n_{chemistry}^{dilute}$')
plt.plot(chemistry['x']*1E3, chemistry['optics']['index_of_refraction']['dense'], 
        '.',label='$n_{chemistry}^{dense}$')
plt.legend() 
plt.xlim([-3, 0]) 
#plt.ylim([1, 1.00005]) 
plt.xlabel('X $[mm]$')
plt.ylabel('n $[\;]$')
plt.savefig(os.path.join(plots_path, 
            f'index_of_refraction_{case_name}.png'), 
            bbox_inches='tight', dpi=300)
plt.close() 

# Plot Index of refraction 
'''
if not eyi_flag:
    plt.plot(turbulent['x']*1E3, turbulent['optics']['reflectivity']['dilute'],
             label='$R_{turbulent}^{dilute}$')
    plt.plot(turbulent['x']*1E3, turbulent['optics']['reflectivity']['dense'],
             '.', label='$R_{turbulent}^{dense}$')
    plt.plot(frozen['x']*1E3, frozen['optics']['reflectivity']['dilute'], 
             label='$R_{frozen}^{dilute}$')
    plt.plot(frozen['x']*1E3, frozen['optics']['reflectivity']['dense'], 
             '.', label='$R_{frozen}^{dense}$')
plt.plot(chemistry['x']*1E3, chemistry['optics']['reflectivity']['dilute'], 
        label='$R_{chemistry}^{dilute}$')
plt.plot(chemistry['x']*1E3, chemistry['optics']['reflectivity']['dense'], 
        '.',label='$R_{chemistry}^{dense}$')
plt.legend() 
plt.xlim([-2.5, -1e-1]) 
#plt.ylim([0, 0.002]) 
plt.xlabel('X $[mm]$')
plt.ylabel('R $[\;]$')
plt.savefig(os.path.join(plots_path, 
            f'reflectivity_{case_name}.png'), 
            bbox_inches='tight', dpi=300)
plt.close() 
'''

# Dielectric Constants #
if not eyi_flag:
    plt.plot(turbulent['x']*1E3, turbulent['optics']['dielectric_constant']['dilute'],
             label='$\epsilon_{turbulent}^{dilute}$')
    plt.plot(turbulent['x']*1E3, turbulent['optics']['dielectric_constant']['dense'],
             '.', label='$\epsilon_{turbulent}^{dense}$')
    plt.plot(frozen['x']*1E3, frozen['optics']['dielectric_constant']['dilute'], 
             label='$\epsilon_{frozen}^{dilute}$')
    plt.plot(frozen['x']*1E3, frozen['optics']['dielectric_constant']['dense'], 
             '.', label='$\epsilon_{frozen}^{dense}$')
plt.plot(chemistry['x']*1E3, chemistry['optics']['dielectric_constant']['dilute'], 
        label='$\epsilon_{chemistry}^{dilute}$')
plt.plot(chemistry['x']*1E3, chemistry['optics']['dielectric_constant']['dense'], 
        '.',label='$\epsilon_{chemistry}^{dense}$')
plt.legend() 
plt.xlim([-2.5, 0]) 
plt.ylim([8.8542E-12, 8.855E-12]) 
plt.xlabel('X $[mm]$')
plt.ylabel('$\epsilon$ $[Fm^{-1}]$')
plt.savefig(os.path.join(plots_path, 
            f'dielectric_constant_{case_name}.png'), 
            bbox_inches='tight', dpi=300)
plt.close() 

# Plot Temperatures #
if not eyi_flag:
    plt.plot(turbulent['x']*1E3, turbulent['Temperature_tr'],
             label='$T_{tr}^{turbulent}$')
    plt.plot(turbulent['x']*1E3, turbulent['Temperature_ve'], '.',
             label='$T_{ve}^{turbulent}$')
    plt.plot(frozen['x']*1E3, frozen['Temperature_tr'],
             label='$T_{tr}^{frozen}$')
    plt.plot(frozen['x']*1E3, frozen['Temperature_ve'], '.',
             label='$T_{ve}^{frozen}$')
plt.plot(chemistry['x']*1E3, chemistry['Temperature_tr'],
         label='$T_{tr}^{chemistry}$')
plt.plot(chemistry['x']*1E3, chemistry['Temperature_ve'], '.',
         label='$T_{ve}^{chemistry}$')
plt.legend() 
plt.xlim([-2.5, 0]) 
#plt.ylim([8.8542E-12, 8.855E-12]) 
plt.xlabel('X $[mm]$')
plt.ylabel('T $[K]$')
plt.savefig(os.path.join(plots_path, 
            f'Temperature_{case_name}.png'), 
            bbox_inches='tight', dpi=300)
plt.close() 

# Plot Densities #
if not eyi_flag:
    for i in turbulent['optics']['density']:
        if i == 'N':
            line = '-'
        elif i == 'O':
            line = '-.'
        elif i == 'NO':
            line ='--'
        elif i == 'N2':
            line = '.'
        elif i == 'O2':
            line = '.-'

        plt.plot(turbulent['x']*1E3, turbulent['optics']['density'][i], 
                 line, label=f'{i}')
        
    plt.legend() 
    plt.xlabel('X $[mm]$')
    plt.ylabel('$\\rho$ $[kg/m^3]$')
    plt.xlim([-0.25, 0]) 
    plt.ylim([0, 0.1])
    plt.savefig(os.path.join(plots_path, 
                f'Density_turbulent_{case_name}.png'), 
                bbox_inches='tight', dpi=300)
    plt.close() 

# Plot Densities #
for i in chemistry['optics']['density']:
    if i == 'N':
        line = '-'
    elif i == 'O':
        line = '-.'
    elif i == 'NO':
        line ='--'
    elif i == 'N2':
        line = '.'
    elif i == 'O2':
        line = '.-'

    plt.plot(chemistry['x']*1E3, chemistry['optics']['density'][i], 
             line, label=f'{i}')
    
plt.legend() 
plt.xlabel('X $[mm]$')
plt.ylabel('$\\rho$ $[kg/m^3]$')
plt.xlim([-0.25, 0]) 
plt.ylim([0, 0.1])
plt.savefig(os.path.join(plots_path, 
            f'Density_chemistry_{case_name}.png'), 
            bbox_inches='tight', dpi=300)
plt.close() 

# Plot Frozen #
if not eyi_flag:
    for i in frozen['optics']['density']:
        if i == 'N':
            line = '-'
        elif i == 'O':
            line = '-.'
        elif i == 'NO':
            line ='--'
        elif i == 'N2':
            line = '.'
        elif i == 'O2':
            line = '.-'

        plt.plot(frozen['x']*1E3, frozen['optics']['density'][i], 
                 line, label=f'{i}')
        
    plt.legend() 
    plt.xlabel('X $[mm]$')
    plt.ylabel('$\\rho$ $[kg/m^3]$')
    plt.xlim([-0.25, 0]) 
    plt.ylim([0, 0.1])
    plt.savefig(os.path.join(plots_path, 
                f'Density_frozen_{case_name}.png'), 
                bbox_inches='tight', dpi=300)
    plt.close() 
