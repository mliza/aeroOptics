import os
import sys
import IPython
import numpy as np

# My Packages 
scripts_path   = os.environ.get('SCRIPTS')
python_scripts = os.path.join(scripts_path, 'Python')
sys.path.append(python_scripts) 
import helper_functions as helper 
import aerodynamic_functions as aero


if __name__ == "__main__":
    abs_path_to_csv = "/Users/martin/Desktop/LES/converged_RANS"
    file_in = "solution_flow.csv"
    data_in = helper.flow_loader(file_in, abs_path_to_csv)
    noise_data = helper.add_noise(data_in)
    IPython.embed(colors = 'Linux') 
#    helper.plot_flow_noise(data_in, noise_data)

