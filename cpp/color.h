#ifndef COLOR_H
#define COLOR_H

#include "vec3.h"
#include <iostream>

using color = vec3;

void write_color(std::ostream& out, const color& pixel_color) {
    double red = pixel_color.get_x();
    double green = pixel_color.get_y();
    double blue = pixel_color.get_z();

    // Translate the [0,1] component values to the byte range [0,255]
    int red_byte = static_cast<int>(255.999 * red);
    int green_byte = static_cast<int>(255.999 * green);
    int blue_byte = static_cast<int>(255.999 * blue);

    // Write out the pixel color components
    out << red_byte << ' ' << green_byte << ' ' << blue_byte << '\n';
}

#endif
