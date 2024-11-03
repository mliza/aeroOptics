'''
    Date:   03/26/2023
    Author: Martin E. Liza
    File:   quantum.py
    Def:

    Author          Date        Revision
    ----------------------------------------------------
    Martin E. Liza  10/29/2024  Initial version.
'''
import pickle
import molmass
import os 
import sys 
import IPython
import constants_tables 
import numpy as np
import matplotlib.pyplot as plt 
import scipy.constants as s_consts 
from ambiance import Atmosphere #package for atmosphere properties 

# My Packages 
scripts_path   = os.environ.get('SCRIPTS')
python_scripts = os.path.join(scripts_path, 'Python')
sys.path.append(python_scripts) 
import helper_functions as helper 
import aerodynamic_functions as aero

# Kayser units
def wavenumber_to_electronvolt(wavenumber_cm):
    return wavenumber_to_joules(wavenumber_cm) / s_consts.eV #[eV]

def wavenumber_to_joules(wavenumber_cm):
    return wavenumber_cm * s_consts.c * 10**2 * s_consts.h #[J]

def wavenumber_to_meter(wavelength_cm):
    return wavelength_cm * 100

# Irikura: 10.1063/1.2436891
def zero_point_energy(spectroscopy_const_in):
    scope_var = (spectroscopy_const_in['alpha_e'] *
                 spectroscopy_const_in['omega_e'] /
                 spectroscopy_const_in['B_e'])
    tmp = spectroscopy_const_in['omega_e'] / 2
    tmp -= spectroscopy_const_in['omega_xe'] / 2
    tmp += spectroscopy_const_in['omega_ye'] / 8
    tmp += spectroscopy_const_in['B_e'] / 4
    tmp += scope_var / 12 
    tmp += scope_var**2 / (144 * spectroscopy_const_in['B_e'])

    return tmp #[1/cm] 


def vibrational_partition_function(vibrational_number, temperature_K, 
                                   molecule):
    thermal_beta = 1 / (s_consts.k * temperature_K)
    z_vib = 0.0
    for v in range(vibrational_number + 1):
        z_vib += np.exp(-thermal_beta * 
                wavenumber_to_joules(vibrational_energy_k(v, molecule)))
    return z_vib

def rotational_partition_function(rotational_number, temperature_K, molecule):
    thermal_beta = 1 / (s_consts.k * temperature_K)
    z_rot = 0.0
    for j in range(rotational_number + 1):
        degeneracy_rotation = 2 * j + 1
        tmp = np.exp(-thermal_beta * 
                  wavenumber_to_joules(rotational_energy_k(j, molecule)))
        z_rot += (degeneracy_rotation * tmp)
    return z_rot

#TODO: CITE ME
def potential_dunham_coef_012(molecule):
    spectroscopy_const = constants_tables.spectroscopy_constants(molecule)
    a_0 = (spectroscopy_const['omega_e']**2 /
           (4 * spectroscopy_const['B_e']))
    a_1 = -(spectroscopy_const['alpha_e'] * spectroscopy_const['omega_e'] /
               (6 * spectroscopy_const['B_e']**2) + 1)
    a_2 = ((5/4) * a_1**2 - (2/3) *
           (spectroscopy_const['omega_xe'] / spectroscopy_const['B_e'])) 
    return (a_0, a_1, a_2)

#TODO: CITE ME
def potential_dunham_coeff_m(a_1, a_2, m):
    tmp = (12 / a_1)**(m - 2)
    tmp *= (2**(m + 1) - 1)
    tmp *= (a_2 / 7)**(m - 1)

    for i in range(m - 2):
        tmp *= (1 / (m + 2 - i))

    return tmp

def born_oppenheimer_approximation(vibrational_number, rotational_number,
                                   molecule):
    spectroscopy_constants = constants_tables.spectroscopy_constants(molecule)
    # Denegenracy
    vib_levels = vibrational_number + 1/2
    rot_levels = rotational_number * (rotational_number + 1)

    # Harmonic vibration and rotation terms
    harmonic = spectroscopy_constants['omega_e'] * vib_levels
    harmonic += spectroscopy_constants['B_e'] * rot_levels

    # Anharmonic vibration and rotation terms 
    anharmonic = spectroscopy_constants['omega_xe'] * vib_levels**2
    anharmonic += spectroscopy_constants['D_e'] * rot_levels**2

    # Interacton between vibration and rotation modes
    interaction = spectroscopy_constants['alpha_e'] * vib_levels * rot_levels

    return harmonic - anharmonic - interaction #[cm^1]

def boltzman_factor(temperature_K, molecule, vibrational_number=None,
                    rotational_number=None):
    # Initialize energy terms, degeneracy and thermal beta
    energy_vib_k = 0
    energy_rot_k = 0
    degeneracy_rotation = 1
    thermal_beta = 1 / (s_consts.k * temperature_K)

    # Calculates Energy levels
    if vibrational_number is not None:
        energy_vib_k = vibrational_energy_k(vibrational_number, molecule)
    if rotational_number is not None:
        energy_rot_k = rotational_energy_k(rotational_number, molecule)
        degeneracy_rotation = 2 * rotational_number + 1

    tot_energy = wavenumber_to_joules(energy_vib_k + energy_rot_k)

    return degeneracy_rotation * np.exp(-tot_energy * thermal_beta)
    
def distribution_function(temperature_K, molecule, vibrational_number=None,
                    rotational_number=None):
    # Check if they exist
    z_rot = 1
    z_vib = 1

    # Calculate partition functions if vibrational or rotational numbers are provided
    if vibrational_number is not None:
        z_vib = vibrational_partition_function(vibrational_number, temperature_K,
                                          molecule)
    if rotational_number is not None:
        z_rot = rotational_partition_function(rotational_number, temperature_K,
                                          molecule)

    # Calculate total partition function as the product 
    # of rotational and vibrational partition functions
    z_tot = z_rot * z_vib
    
    # Create the distribution array based on the inputs provided
    if vibrational_number and rotational_number:
        tmp = np.zeros([vibrational_number + 1, rotational_number + 1])
        for j in range(rotational_number + 1):
            for v in range(vibrational_number + 1):
                tmp[v][j] = boltzman_factor(temperature_K=temperature_K,
                                            molecule=molecule,
                                            vibrational_number=v,
                                            rotational_number=j)
                #print(f'{v},{j} = {tmp[v][j]}')

    elif vibrational_number:
        tmp = np.zeros(vibrational_number + 1)
        for v in range(vibrational_number + 1):
            tmp[v] = boltzman_factor(temperature_K=temperature_K,
                                        molecule=molecule,
                                        vibrational_number=v)

    elif rotational_number:
        tmp = np.zeros(rotational_number + 1)
        for j in range(rotational_number + 1):
            tmp[j] = boltzman_factor(temperature_K=temperature_K,
                                        molecule=molecule,
                                        rotational_number=j)
    return tmp / z_tot


def vibrational_energy_k(vibrational_number, molecule):
    spectroscopy_constants = constants_tables.spectroscopy_constants(molecule)
    # Calculates the vibrational energy in units of wave number
    vib_levels = vibrational_number + 1/2

    return spectroscopy_constants['omega_e'] * vib_levels #[cm^-1]

def rotational_energy_k(rotational_number, molecule):
    spectroscopy_constants = constants_tables.spectroscopy_constants(molecule)
    # Calculates the rotational energy in units of wave number
    rot_levels = rotational_number * (rotational_number + 1)

    return spectroscopy_constants['B_e'] * rot_levels #[cm^-1]

# TODO
def tranlational_energy(principal_number_x, principal_number_y,
                        principal_number_z):
    A = 5


if __name__ == "__main__":
    molecule = 'N2'
    temperature_K = 2000
    vibrational_number = 3
    rotational_number = 5

    V = distribution_function(temperature_K, molecule,
                          vibrational_number=vibrational_number)
    J = distribution_function(temperature_K, molecule,
                          rotational_number=rotational_number)

    VJ = distribution_function(temperature_K, molecule,
                          vibrational_number=vibrational_number,
                          rotational_number=rotational_number)
    IPython.embed(colors = 'Linux')

    b_o = born_oppenheimer_approximation(vibrational_number=vibrational_number,
                                        rotational_number=rotational_number,
                                        molecule=molecule)

    energy_vib = vibrational_energy_k(vibrational_number=vibrational_number,
                                      molecule=molecule)

    energy_rot = rotational_energy_k(rotational_number=rotational_number,
                                   molecule=molecule)

    z_vib = vibrational_partition_function(vibrational_number=vibrational_number, 
                                   temperature_K=temperature_K,
                                   molecule=molecule)

    z_rot = rotational_partition_function(rotational_number=rotational_number, 
                                   temperature_K=temperature_K,
                                   molecule=molecule)




