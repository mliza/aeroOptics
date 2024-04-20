#include "color.h"
#include "ray.h"
#include "vec3.h"

#include <iostream>

// https://raytracing.github.io/books/RayTracingInOneWeekend.html#overview
// https://github.com/RayTracing/raytracing.github.io/tree/release

// Return color for a given ray
// Linearly blends white and blue (lerp linear interpolation)
// blendValue = (1 - alpha) * startValue + alpha * endValue
color ray_color(const ray& ray){
    vec3 unit_diction = unit_vector(ray.get_direction());
    // alpha = 0.0 => white, alpha = 1.0 => blue
    double alpha = 0.5 * (unit_diction.get_y() + 1.0); 
    return (1 - alpha) * color(1.0, 1.0, 1.0) + alpha * color(0.5, 0.7, 1.0);
}


int main(){

    // Image
    double aspect_ratio = 16.0 / 9.0;
    int image_width = 400;

    // Calculate the image height, and ensure that it's at least 1
    int image_height = static_cast<int>(image_width / aspect_ratio);
    image_height = (image_height < 1) ? 1 : image_height;

    // Camera (right handed coordinate)
    double focal_lenght = 1.0;
    double viewport_height = 2.0;
    double viewport_width = viewport_height * static_cast<double>(image_width)  
                            / static_cast<double>(image_height);
    auto camera_center = point3(0.0, 0.0, 0.0);

    // Calculate vectors across the view port space grid
    // origin define on top-left, moves from left-to-right (u) and from top-to-bottom (v)
    vec3 viewport_u = vec3(viewport_width, 0.0, 0.0);
    vec3 viewport_v = vec3(0.0, -viewport_height, 0.0);

    // Calculate displacement vectors across the view port space grid from pixel to pixel
    vec3 pixel_delta_u = viewport_u / image_width;
    vec3 pixel_delta_v = viewport_v / image_height;

    // Calculate pixel-origin, top-left pixel
    vec3 viewport_top_left = camera_center - 
                            vec3(0.0, 0.0, focal_lenght)
                            - 0.5 * (viewport_u + viewport_v); 
    vec3 origin_pixel = viewport_top_left + 0.5 * (pixel_delta_u + pixel_delta_v);
                                
    // Render
    std::cout << "P3\n" << image_width << ' ' << image_height << "\n255\n";

    for (int j = 0; j < image_height; j++){
        std::clog << "\rScanlines remaining: " << (image_height - j) << 
            ' ' << std::flush;
        for (int i = 0; i < image_width; i++){
            vec3 pixel_center = origin_pixel + (i * pixel_delta_u) + (j * pixel_delta_v);
            vec3 ray_direction = pixel_center - camera_center;
            ray r(camera_center, ray_direction);
            color pixel_color = ray_color(r);
            write_color(std::cout, pixel_color);
                                   
        }
    }

    std::clog << "\rDone.                   \n";
}

