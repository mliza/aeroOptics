#ifndef COLOR_H
#define COLOR_H

#include "interval.h"
#include "vec3.h"

using color = vec3;

inline double linear_to_gamma(double linear_component) {
    if (linear_component > 0.0) {
        return sqrt(linear_component);
    }

    return 0;
}

void write_color(std::ostream& out, const color& pixel_color) {
    double red   = pixel_color.get_x();
    double green = pixel_color.get_y();
    double blue  = pixel_color.get_z();

    // Apply a linear to gamma transform for gamma 2
    red   = linear_to_gamma(red);
    green = linear_to_gamma(green);
    blue  = linear_to_gamma(blue);

    // Translate the [0,1] component values to the byte range [0,255]
    static const interval intensity(0.000, 0.999);
    int red_byte   = static_cast<int>(256 * intensity.clamp(red));
    int green_byte = static_cast<int>(256 * intensity.clamp(green));
    int blue_byte  = static_cast<int>(256 * intensity.clamp(blue));


    // Write out the pixel color components
    out << red_byte << ' ' << green_byte << ' ' << blue_byte << '\n';
}

#endif
