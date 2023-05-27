#!/opt/homebrew/bin/python3.9
import sys 
import os 
import IPython 
import pickle 
import pandas as pd 
import matplotlib.pyplot as plt 


# Inputs 
'''
file_in_abs_path  = sys.argv[1] 
plots_path        = sys.argv[2]
'''

mesh = 'eyi_chem'
case = '12'

file_in_abs_path  = f'/Users/martin/Desktop/optics/simulations/mackey/{mesh}/Mackey_{case}/history.csv'
file_in_abs_path  = f'/Users/martin/Desktop/optics/simulations/eyi/{mesh}/Eyi_{case}/history.csv'
plots_path        = '/Users/martin/Desktop/results'
dict_out          = { }

# Read files 
data_in        = pd.read_csv(file_in_abs_path) 
data_variables = list(data_in.columns.values)

for i in data_variables:
    dict_out[i.strip().replace("\"","")] = data_in[i].to_numpy() 

dict_keys = list(dict_out.keys())
plot_variables = ['rms[Rho_0]', 'rms[Rho_1]', 'rms[Rho_2]', 
                  'rms[Rho_3]', 'rms[Rho_4]', 'rms[RhoE]'] 

for i in plot_variables:
    plt.plot(dict_out['Inner_Iter'], dict_out[i], 
             label=f'{i}', linewidth=2.5)

plt.legend()
plt.title(f'{mesh}_{case}')
plt.xlabel('Iterations')
plt.savefig(os.path.join(plots_path, f'{mesh}_{case}_convergence.png'),
            bbox_inches='tight', dpi=300)
plt.close() 
