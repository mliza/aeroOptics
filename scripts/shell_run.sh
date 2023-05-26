#!/bin/bash 
shopt -s expand_aliases;
source ~/.bashrc86; 

OPTICS='/Users/martin/Desktop/optics'
SIMULATIONS=$OPTICS/simulations
MACKEYCHEM=$SIMULATIONS/mackey/mackey_chemistry
MACKEYFROZEN=$SIMULATIONS/mackey/mackey_frozen
MACKEYTURBULENT=$SIMULATIONS/mackey/mackey_turbulent
EYICHEM=$SIMULATIONS/eyi/eyi_chem
TPPATH=$OPTICS/data/tp_data
PICKPATH=$OPTICS/data/pickle_data
OZGURPATH=$SIMULATIONS/ozgur

# OZGUR PATH # 
runTec tp_data_cutter.py $OZGURPATH/laminarChemistry/flow.szplt $TPPATH/laminarChem_12_stag.dat -0.02 0.0 0.0 0.0 1000;
runTec tp_data_cutter.py $OZGURPATH/laminarFrozen/flow.szplt $TPPATH/laminarFrozen_12_stag.dat -0.02 0.0 0.0 0.0 1000;
runTec tp_data_cutter.py $OZGURPATH/turbulentChemistry/flow.szplt $TPPATH/turbulentChem_12_stag.dat -0.02 0.0 0.0 0.0 1000;

#runTec tp_data_cutter.py $OZGURPATH/laminarChemistry/flow.szplt $TPPATH/laminarChem_12_diag.dat 0.0 0.005 0.017 0.0013 1000;
#runTec tp_data_cutter.py $OZGURPATH/laminarFrozen/flow.szplt $TPPATH/laminarFrozen_12_diag.dat 0.0 0.005 0.017 0.0013 1000; 
#runTec tp_data_cutter.py $OZGURPATH/turbulentChemistry/flow.szplt $TPPATH/turbulentChem_12_diag.dat 0.0 0.005 0.017 0.0013 1000;

runTec tp_data_cutter.py $OZGURPATH/laminarChemistry/flow.szplt $TPPATH/laminarChem_12_diag.dat 0.033 0.04 0.04 0.02 1000;
runTec tp_data_cutter.py $OZGURPATH/laminarFrozen/flow.szplt $TPPATH/laminarFrozen_12_diag.dat 0.033 0.04 0.04 0.02 1000;
runTec tp_data_cutter.py $OZGURPATH/turbulentChemistry/flow.szplt $TPPATH/turbulentChem_12_diag.dat 0.033 0.04 0.04 0.02 1000;
# OZGUR PATH # 


# Mackey Chem stagnation #
runTec tp_data_cutter.py $MACKEYCHEM/Mackey_1/flow.szplt $TPPATH/mackeyChem_1_stag.dat -0.02 0.0 0.0 0.0 1000;
runTec tp_data_cutter.py $MACKEYCHEM/Mackey_2/flow.szplt $TPPATH/mackeyChem_2_stag.dat -0.02 0.0 0.0 0.0 1000;
runTec tp_data_cutter.py $MACKEYCHEM/Mackey_3/flow.szplt $TPPATH/mackeyChem_3_stag.dat -0.02 0.0 0.0 0.0 1000;
# Mackey Chem stagnation #

# Mackey Chem diagonal #
runTec tp_data_cutter.py $MACKEYCHEM/Mackey_1/flow.szplt $TPPATH/mackeyChem_1_diag.dat 0.0 0.005 0.017 0.0013 1000; 
runTec tp_data_cutter.py $MACKEYCHEM/Mackey_2/flow.szplt $TPPATH/mackeyChem_2_diag.dat 0.0 0.005 0.017 0.0013 1000;
runTec tp_data_cutter.py $MACKEYCHEM/Mackey_3/flow.szplt $TPPATH/mackeyChem_3_diag.dat 0.0 0.005 0.017 0.0013 1000;
# Mackey Chem diagonal #

# Mackey Frozen Chem stagnation #
runTec tp_data_cutter.py $MACKEYFROZEN/Mackey_1/flow.szplt $TPPATH/mackeyFrozen_1_stag.dat -0.02 0.0 0.0 0.0 1000;
runTec tp_data_cutter.py $MACKEYFROZEN/Mackey_2/flow.szplt $TPPATH/mackeyFrozen_2_stag.dat -0.02 0.0 0.0 0.0 1000;
runTec tp_data_cutter.py $MACKEYFROZEN/Mackey_3/flow.szplt $TPPATH/mackeyFrozen_3_stag.dat -0.02 0.0 0.0 0.0 1000;
# Mackey Froze Chem stagnation #

# Mackey Frozen Chem diagonal #
runTec tp_data_cutter.py $MACKEYFROZEN/Mackey_1/flow.szplt $TPPATH/mackeyFrozen_1_diag.dat 0.0 0.005 0.017 0.0013 1000; 
runTec tp_data_cutter.py $MACKEYFROZEN/Mackey_2/flow.szplt $TPPATH/mackeyFrozen_2_diag.dat 0.0 0.005 0.017 0.0013 1000;
runTec tp_data_cutter.py $MACKEYFROZEN/Mackey_3/flow.szplt $TPPATH/mackeyFrozen_3_diag.dat 0.0 0.005 0.017 0.0013 1000;
# Mackey Frozen Chem diagonal #
#
#
# Mackey Turbulent stagnation #
runTec tp_data_cutter.py $MACKEYTURBULENT/Mackey_1/flow.szplt $TPPATH/mackeyTurbulent_1_stag.dat -0.02 0.0 0.0 0.0 1000;
runTec tp_data_cutter.py $MACKEYTURBULENT/Mackey_2/flow.szplt $TPPATH/mackeyTurbulent_2_stag.dat -0.02 0.0 0.0 0.0 1000;
runTec tp_data_cutter.py $MACKEYTURBULENT/Mackey_3/flow.szplt $TPPATH/mackeyTurbulent_3_stag.dat -0.02 0.0 0.0 0.0 1000;
# Mackey Turbulent stagnation #

# Mackey Turbulent diagonal #
runTec tp_data_cutter.py $MACKEYTURBULENT/Mackey_1/flow.szplt $TPPATH/mackeyTurbulent_1_diag.dat 0.0 0.005 0.017 0.0013 1000; 
runTec tp_data_cutter.py $MACKEYTURBULENT/Mackey_2/flow.szplt $TPPATH/mackeyTurbulent_2_diag.dat 0.0 0.005 0.017 0.0013 1000;
runTec tp_data_cutter.py $MACKEYTURBULENT/Mackey_3/flow.szplt $TPPATH/mackeyTurbulent_3_diag.dat 0.0 0.005 0.017 0.0013 1000;
# Mackey Turbulent diagonal #
#
#
# Eyi Cases  
runTec tp_data_cutter.py $EYICHEM/Eyi_1/flow.szplt $TPPATH/eyiChem_1_stag.dat -0.02 0.0 0.0 0.0 1000;
runTec tp_data_cutter.py $EYICHEM/Eyi_6/flow.szplt $TPPATH/eyiChem_6_stag.dat -0.02 0.0 0.0 0.0 1000;
runTec tp_data_cutter.py $EYICHEM/Eyi_12/flow.szplt $TPPATH/eyiChem_12_stag.dat -0.02 0.0 0.0 0.0 1000;
runTec tp_surface_to_pickle.py $EYICHEM/Eyi_1/surface_flow.szplt $PICKPATH/eyiChem_1_surface.pickle;
runTec tp_surface_to_pickle.py $EYICHEM/Eyi_6/surface_flow.szplt $PICKPATH/eyiChem_6_surface.pickle;
runTec tp_surface_to_pickle.py $EYICHEM/Eyi_12/surface_flow.szplt $PICKPATH/eyiChem_12_surface.pickle;
# Case 12

# Flow cut pickle tecplot # 
runTec tp_to_pickle.py $TPPATH $PICKPATH/data_out.pickle;
# Flow cut pickle tecplot # 

# Mackey Chem Surface#
runTec tp_surface_to_pickle.py $MACKEYCHEM/Mackey_1/surface_flow.szplt $PICKPATH/mackeyChem_1_surface.pickle;
runTec tp_surface_to_pickle.py $MACKEYCHEM/Mackey_2/surface_flow.szplt $PICKPATH/mackeyChem_2_surface.pickle;
runTec tp_surface_to_pickle.py $MACKEYCHEM/Mackey_3/surface_flow.szplt $PICKPATH/mackeyChem_3_surface.pickle;
# Mackey Chem Surface#
#
# Mackey Frozen Surface#
runTec tp_surface_to_pickle.py $MACKEYFROZEN/Mackey_1/surface_flow.szplt $PICKPATH/mackeyFrozen_1_surface.pickle;
runTec tp_surface_to_pickle.py $MACKEYFROZEN/Mackey_2/surface_flow.szplt $PICKPATH/mackeyFrozen_2_surface.pickle;
runTec tp_surface_to_pickle.py $MACKEYFROZEN/Mackey_3/surface_flow.szplt $PICKPATH/mackeyFrozen_3_surface.pickle;
# Mackey  Frozen Surface#
#
# Mackey Turbulent Surface#
runTec tp_surface_to_pickle.py $MACKEYTURBULENT/Mackey_1/surface_flow.szplt $PICKPATH/mackeyTurbulent_1_surface.pickle;
runTec tp_surface_to_pickle.py $MACKEYTURBULENT/Mackey_2/surface_flow.szplt $PICKPATH/mackeyTurbulent_2_surface.pickle;
runTec tp_surface_to_pickle.py $MACKEYTURBULENT/Mackey_3/surface_flow.szplt $PICKPATH/mackeyTurbulent_3_surface.pickle;
# Mackey Turbulent Surface#
