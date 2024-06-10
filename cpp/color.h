#ifndef COLOR_H
#define COLOR_H

#include "interval.h"
#include "vec3.h"

using color = vec3;

void write_color(std::ostream& out, const color& pixel_color) {
    double red = pixel_color.get_x();
    double green = pixel_color.get_y();
    double blue = pixel_color.get_z();

    // Translate the [0,1] component values to the byte range [0,255]
    static const interval intensity(0.000, 0.999);
    int red_byte = static_cast<int>(256 * intensity.clamp(red));
    int green_byte = static_cast<int>(256 * intensity.clamp(green));
    int blue_byte = static_cast<int>(256 * intensity.clamp(blue));

    // Write out the pixel color components
    out << red_byte << ' ' << green_byte << ' ' << blue_byte << '\n';
}

#endif
