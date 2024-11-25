import os
import IPython
import tecplot_tools as tp_tools


if __name__ == "__main__":
    chemistry_reaction_path = '/Users/martin/Documents/Schools/UoA/Dissertation/resultsCFD/chemistryReaction'
    su2_output_path = os.path.join(chemistry_reaction_path, 'outputs')
    folders_in = os.listdir(su2_output_path)
    data_output_path = os.path.join(chemistry_reaction_path, 'tecOutData')

    struct_in = { }
    struct_in['x1'] = -0.01
    struct_in['x2'] = 0.01
    struct_in['y1'] = 0.0
    struct_in['y2'] = 0.0
    struct_in['n'] = 200
    
    # Creates stagnation data
    for i in folders_in:
        struct_in['f_in'] = os.path.join(su2_output_path, i, 'flow.szplt')
        struct_in['f_out'] = os.path.join(data_output_path, f'{i}_stagnation.dat')
        tp_tools.data_cutter(struct_in)

    # Converts stagnation data to pickle files
    tp_tools.tp_to_pickle(data_output_path,
                os.path.join(data_output_path,'stagnation.pickle'))






