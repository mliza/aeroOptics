#!/opt/homebrew/bin/python3
'''
    Date:   03/26/2023
    Author: Martin E. Liza
    File:   constant_tables.py
    Def:

    Author          Date        Revision
    ----------------------------------------------------
    Martin E. Liza  03/26/2023  Initial version.
'''

# Gladstone-Dale constants 
def karl_2003(): #follows SU2 MutationPP format 
# https://arc.aiaa.org/doi/pdf/10.2514/6.2003-4252
    dict_out = { 'N'  : 0.301E-3,
                 'O'  : 0.182E-3,
                 'NO' : 0.221E-3,
                 'N2' : 0.238E-3,
                 'O2' : 0.190E-3 } #[m3/kg]
    return dict_out

# Polarizability
def polarizability(): #follows SU2 MutationPP format
    dict_out = { #'e-'  : 0.0, 
                 'N+'   : 0.559E-24,
                 'O+'   : 0.345E-24,
                 'NO+'  : 1.021E-24,
                 'N2+'  : 2.386E-24,
                 'O2+'  : 0.238E-24,
                 'N'    : 1.100E-24,
                 'O'    : 0.802E-24,
                 'NO'   : 1.700E-24,
                 'N2'   : 1.740E-24,
                 'O2'   : 1.581E-24 } # [cm^3]  
    return dict_out 


