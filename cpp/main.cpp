#include "camera.h"
#include "hittable.h"
#include "hittable_list.h"
#include "material.h"
#include "rtweekend.h"
#include "sphere.h"

// https://raytracing.github.io/books/RayTracingInOneWeekend.html#overview
// https://github.com/RayTracing/raytracing.github.io/tree/release



// Return color for a given ray
// Linearly blends white and blue (lerp linear interpolation)
// blendValue = (1 - alpha) * startValue + alpha * endValue

int main() {
    // World
    hittable_list world;
    /*
    double R = cos(PI/4);
    shared_ptr<material> material_left = make_shared<lambertian>(color(0, 0, 1));
    shared_ptr<material> material_right = make_shared<lambertian>(color(1, 0, 0));

    world.add(make_shared<sphere>(point3(-R, 0, -1), R, material_left));
    world.add(make_shared<sphere>(point3(R, 0, -1), R, material_right));
    */

    std::shared_ptr<material> material_ground = std::make_shared<lambertian>
                                                (color(0.8, 0.8, 0.0));
    std::shared_ptr<material> material_center = std::make_shared<lambertian>
                                                (color(0.1, 0.2, 0.5));
    std::shared_ptr<material> material_left   = std::make_shared<dielectric>(1.50);
    std::shared_ptr<material> material_buble  = std::make_shared<dielectric>(1.0/1.50);

    std::shared_ptr<material> material_right  = std::make_shared<metal>
                                                (color(0.8, 0.6, 0.2), 1.0);

    world.add(std::make_shared<sphere>(point3( 0.0, -100.5, -1.0), 100.0, material_ground));
    world.add(std::make_shared<sphere>(point3( 0.0, 0.0, -1.2), 0.5, material_center));
    world.add(std::make_shared<sphere>(point3(-1.0, 0.0, -1.0), 0.5, material_left));
    world.add(std::make_shared<sphere>(point3(-1.0, 0.0, -1.0), 0.4, material_buble));
    world.add(std::make_shared<sphere>(point3( 1.0, 0.0, -1.0), 0.5, material_right));

    camera cam;

    // Camera Properties
    cam.aspect_ratio = 16.0 / 9.0;
    cam.image_width = 400;
    cam.samples_per_pixel = 100;
    cam.max_depth = 50;
    cam.vfov = 20.0;
    cam.lookfrom = point3(-2, 2, 1);
    cam.lookat = point3(0, 0, -1);
    cam.vup = vec3(0, 1, 0);
    cam.defocus_angle = 10.0;
    cam.focus_dist = 3.4;

    cam.render(world);
}
