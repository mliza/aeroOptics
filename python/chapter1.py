import os
import numpy as np
import matplotlib.pyplot as plt
from haot import optics
from ambiance import Atmosphere

import IPython

def plot_index(blue_sky, rain, altitude, output_png_path,  fig_config):
    atm = Atmosphere(altitude)
    layers = atm.layer_name
    layer_index = np.unique(layers, return_index=True)
    color_layers = 'mediumorchid'
    color_atm = 'black'

    plt.plot(blue_sky - 1, altitude * 1E-3,
             linewidth=fig_config['line_width'], label='blue-sky',
             color=color_atm)
    """
    plt.plot(rain, altitude * 1E-3,
             linewidth=fig_config['line_width'], label='rain')
    """

    for k, val in enumerate(layer_index[0]):
        plt.axhline(y=altitude[layer_index[1][k]]*1E-3,
                    linestyle='--', color=color_layers)

        x_min, x_max = plt.xlim() 
        x_pos_left = x_min + 0.05 * (x_max - x_min)  # Set text position as 5% from the left
        x_pos_right = x_max - 0.05 * (x_max - x_min)  # Set text position as 5% from the left
        if (val == layer_index[0][-1]):
            plt.text(
                x=x_pos_left,  #[x_pos_left, x_pos_right]
                y=altitude[layer_index[1][k]] * 1E-3,  # Altitude for the text
                s=val,  # Layer name
                color=color_layers,
                fontsize=10,
                ha='left',  #[right,left] 
                va='bottom'  # Align text below the line
            )
        else:
            plt.text(
                x=x_pos_right,  #[x_pos_left, x_pos_right]
                y=altitude[layer_index[1][k]] * 1E-3,  # Altitude for the text
                s=val,  # Layer name
                color=color_layers,
                fontsize=10,
                ha='right',  #[right,left] 
                va='bottom'  # Align text below the line
            )

    plt.xlabel('(Refractive Index - 1) $[\;]$', fontsize=fig_config['axis_label_size'])
    plt.ylabel('Altitude $[km]$', fontsize=fig_config['axis_label_size'])
    #plt.legend(fontsize=fig_config['legend_size'])

    plt.savefig(os.path.join(output_png_path, 'atmosphericOptics.png'),
                format = 'png', bbox_inches='tight',
                dpi=fig_config['dpi_size'])
    plt.close()

if __name__ == "__main__":
    fig_config = { }
    fig_config['line_width'] = 3
    fig_config['fig_width'] = 6 
    fig_config['fig_height'] = 5 
    fig_config['dpi_size'] = 600 
    fig_config['ticks_size'] = 12
    fig_config['legend_size'] = 14 
    fig_config['axis_label_size'] = 16 
    fig_config['title_size'] = 18
    output_png = '/Users/martin/Documents/Schools/UoA/Dissertation/figures/chapter1'

    altitude = np.linspace(0, 81E3, 1000)
    blue_sky = optics.atmospheric_index_of_refraction(altitude)
    rain = optics.atmospheric_index_of_refraction(altitude, 1)
    plot_index(blue_sky, rain, altitude, output_png, fig_config)

