'''
    Date:   03/26/2023
    Author: Martin E. Liza
    File:   quantum.py
    Def:

    Author          Date        Revision
    ----------------------------------------------------
    Martin E. Liza  10/29/2024  Initial version.
'''
import os 
import sys 
import IPython
import molmass
import constants_tables 
import numpy as np
import scipy.constants as s_consts 

# My Packages 
scripts_path   = os.environ.get('SCRIPTS')
python_scripts = os.path.join(scripts_path, 'Python')
sys.path.append(python_scripts) 
import helper_functions as helper 
import aerodynamic_functions as aero

# Unit Conversions
def wavenumber_to_electronvolt(wavenumber_cm):
    """Convert wavenumber [cm^-1] to energy in Joules [J]."""
    return wavenumber_to_joules(wavenumber_cm) / s_consts.eV #[eV]

def wavenumber_to_joules(wavenumber_cm):
    """Convert wavenumber [cm^-1] to energy in electron volts [eV]."""
    return wavenumber_cm * s_consts.c * 100 * s_consts.h #[J]

def molarmass_to_kilogram(molarmass_gmol):
    """Convert molar mass [g/mol] to [kg]."""
    return molarmass_gmol * 1E-3 / s_consts.N_A

def zero_point_energy(molecule):
    """Calculate zero-point energy based on spectroscopy constants. 
    (Ref: Irikura https://doi.org/10.1063/1.2436891)"""
    spectroscopy_const = constants_tables.spectroscopy_constants(molecule)
    scope_var = (spectroscopy_const['alpha_e'] *
                 spectroscopy_const['omega_e'] /
                 spectroscopy_const['B_e'])
    zpe = spectroscopy_const['omega_e'] / 2
    zpe -= spectroscopy_const['omega_xe'] / 2
    zpe += spectroscopy_const['omega_ye'] / 8
    zpe += spectroscopy_const['B_e'] / 4
    zpe += scope_var / 12 
    zpe += scope_var**2 / (144 * spectroscopy_const['B_e'])
    return zpe #[1/cm] 

def vibrational_partition_function(vibrational_number, temperature_K, molecule):
    """Calculates the vibrational partition function, (harmonic terms only)"""
    z_vib = 0.0
    for v in range(vibrational_number + 1):
        z_vib += boltzman_factor(temperature_K, molecule, vibrational_number=v)
    return z_vib

def rotational_partition_function(rotational_number, temperature_K, molecule):
    """Calculates the rotational partition function, (harmonic terms only)"""
    z_rot = 0.0
    for j in range(rotational_number + 1):
        z_rot += boltzman_factor(temperature_K, molecule, rotational_number=j)
    return z_rot

def born_oppenheimer_partition_function(vibrational_number,
                                        rotational_number,
                                        temperature_K,
                                        molecule):
    """Calculates the partition function using the Born-Oppenheimer
    approximation"""
    z_bo = 0.0
    for j in range(rotational_number + 1):
        for v in range(vibrational_number + 1):
            z_bo += boltzman_factor(temperature_K, molecule,
                                    vibrational_number=v,
                                    rotational_number=j,
                                    born_opp_flag=True)
    return z_bo


def potential_dunham_coef_012(molecule):
    """Calculates the 0th, 1st, and 2nd Dunham potential coefficients.
    Using: Ogilvie (https://doi.org/10.1016/0022-2852(76)90323-4)
    and Herschbach (https://doi.org/10.1063/1.1731952)."""
    spectroscopy_const = constants_tables.spectroscopy_constants(molecule)
    a_0 = (spectroscopy_const['omega_e']**2 /
           (4 * spectroscopy_const['B_e']))
    a_1 = -(spectroscopy_const['alpha_e'] * spectroscopy_const['omega_e'] /
               (6 * spectroscopy_const['B_e']**2) + 1)
    a_2 = ((5/4) * a_1**2 - (2/3) *
           (spectroscopy_const['omega_xe'] / spectroscopy_const['B_e'])) 
    return (a_0, a_1, a_2)

def potential_dunham_coeff_m(a_1, a_2, m):
    """Calculates the higher order Dunham potential coefficients, using
    Morizadeh work (https://doi.org/10.1016/j.theochem.2003.12.003)."""
    tmp = (12 / a_1)**(m - 2)
    tmp *= (2**(m + 1) - 1)
    tmp *= (a_2 / 7)**(m - 1)
    for i in range(m - 2):
        tmp *= (1 / (m + 2 - i))

    #tmp2 = a_1**3 * 0.25 - 0.5 * a_1**2 + 1/6 * a_1
    return tmp


def boltzman_factor(temperature_K, molecule, vibrational_number=None, rotational_number=None, born_opp_flag=False):
    """Calculates the Boltzman factor at a given vibrational_number and/or
    rotational_number. If the born_opp_flag is provided, it will calculate the
    total energy using the Born-Oppenheimer approximation"""
    # Initialize energy terms, degeneracy and thermal beta
    energy_vib_k = 0
    energy_rot_k = 0
    degeneracy_rotation = 1
    thermal_beta = 1 / (s_consts.k * temperature_K)

    # Calculates Energy levels
    if not born_opp_flag:
        if vibrational_number is not None:
            energy_vib_k = vibrational_energy_k(vibrational_number, molecule)
        if rotational_number is not None:
            energy_rot_k = rotational_energy_k(rotational_number, molecule)
            degeneracy_rotation = 2 * rotational_number + 1
        tot_energy = wavenumber_to_joules(energy_vib_k + energy_rot_k)
    else:
        degeneracy_rotation = 2 * rotational_number + 1
        tot_energy = wavenumber_to_joules(born_oppenheimer_approximation(vibrational_number,
                                                        rotational_number,molecule))
    return degeneracy_rotation * np.exp(-tot_energy * thermal_beta)


def distribution_function(temperature_K, molecule, vibrational_number=None,
                    rotational_number=None, born_opp_flag=False):
    """Compute the population distribution function."""
    # Calculates partition functions if vibrational or rotational numbers are provided
    if not born_opp_flag:
        z_rot = 1
        z_vib = 1
        if vibrational_number is not None:
            z_vib = vibrational_partition_function(vibrational_number, temperature_K,
                                          molecule)
        if rotational_number is not None:
            z_rot = rotational_partition_function(rotational_number, temperature_K,
                                         molecule)
        z_tot = z_rot * z_vib
    else:
        z_tot = born_oppenheimer_partition_function(vibrational_number,
                                       rotational_number, temperature_K,
                                       molecule)

    # Create the distribution array based on the inputs provided
    if vibrational_number and rotational_number:
        tmp = np.zeros([vibrational_number + 1, rotational_number + 1])
        for j in range(rotational_number + 1):
            for v in range(vibrational_number + 1):
                tmp[v][j] = boltzman_factor(temperature_K=temperature_K,
                                            molecule=molecule,
                                            vibrational_number=v,
                                            rotational_number=j,
                                            born_opp_flag=born_opp_flag)
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

def born_oppenheimer_approximation(vibrational_number, rotational_number,
                                   molecule):
    """Calculates the energy at a rotational and vibrational quantum number,
    using the Born-Oppenheimer approximation."""
    spectroscopy_constants = constants_tables.spectroscopy_constants(molecule)

    vib_levels = vibrational_number + 1/2
    rot_levels = rotational_number * (rotational_number + 1)

    # Harmonic vibration and rotation terms
    harmonic = spectroscopy_constants['omega_e'] * vib_levels
    harmonic += spectroscopy_constants['B_e'] * rot_levels

    # Anharmonic vibration and rotation terms 
    anharmonic = spectroscopy_constants['omega_xe'] * vib_levels**2
    anharmonic += spectroscopy_constants['D_e'] * rot_levels**2

    # Interaction between vibration and rotation modes
    interaction = spectroscopy_constants['alpha_e'] * vib_levels * rot_levels

    return harmonic - anharmonic - interaction #[cm^1]

def vibrational_energy_k(vibrational_number, molecule):
    """Calculates the vibrational energy at a given vibrational quantum number,
    using for the harmonic terms"""
    spectroscopy_constants = constants_tables.spectroscopy_constants(molecule)
    # Calculates the vibrational energy in units of wave number
    vib_levels = vibrational_number + 1/2
    return spectroscopy_constants['omega_e'] * vib_levels #[cm^-1]

def rotational_energy_k(rotational_number, molecule):
    """Calculates the rotational energy at a given rotational quantum number,
    using for the harmonic terms"""
    spectroscopy_constants = constants_tables.spectroscopy_constants(molecule)
    # Calculates the rotational energy in units of wave number
    rot_levels = rotational_number * (rotational_number + 1)
    return spectroscopy_constants['B_e'] * rot_levels #[cm^-1]

def reduced_mass_kg(molecule_1, molecule_2):
    """Calculates the molar reduced mass and returns it in kg of two
    elements"""
    m_1 = molmass.Formula(molecule_1).mass
    m_2 = molmass.Formula(molecule_2).mass
    mu = m_1 * m_2 / (m_1 + m_2)

    return molarmass_to_kilogram(mu)

# TODO: Missing Translational Energy
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
    BO = distribution_function(temperature_K, molecule, vibrational_number,
                    rotational_number, born_opp_flag=True)

    energy_bo = born_oppenheimer_approximation(vibrational_number=vibrational_number,
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
    z_bo = born_oppenheimer_partition_function(rotational_number,
                                                vibrational_number,
                                                temperature_K, molecule)
    IPython.embed(colors='Linux')

    """
    Molecule = ['NO+', 'N2+', 'O2+', 'NO', 'N2', 'O2'] 
    for i in Molecule:
        print( f'{i} = {zero_point_energy(i):0.3f}')
    """
    
    dict_mu = { }
    dict_mu['NO+'] = reduced_mass_kg('N+', 'O+')
    dict_mu['N2+'] = reduced_mass_kg('N+', 'N+')
    dict_mu['O2+'] = reduced_mass_kg('O+', 'O+')
    dict_mu['NO'] = reduced_mass_kg('N', 'O')
    dict_mu['N2'] = reduced_mass_kg('N', 'N')
    dict_mu['O2'] = reduced_mass_kg('O', 'O')
    for k, v in dict_mu.items():
        print(f'{k} = {v}')


