#include "camera.h"
#include "hittable.h"
#include "hittable_list.h"
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
     
    world.add(std::make_shared<sphere>(point3(0.0, 0.0, -1.0), 0.5));
    world.add(std::make_shared<sphere>(point3(0.0, -100.5, -1.0), 100.0));

    camera cam;

    cam.aspect_ratio = 16.0 / 9.0;
    cam.image_width = 400;
    cam.samples_per_pixel = 100;

    cam.render(world);
}

