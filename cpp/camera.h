#ifndef CAMERA_H
#define CAMERA_H

#include "rtweekend.h"
#include "hittable.h"

class camera {
    public:
        /* Public Camera Parameters Here */
        double aspect_ratio = 1.0; // Ratio of image width over height
        int image_width = 100; // Rendered image width in pixel count

        void render(const hittable& world) {
            initialize();

            std::cout << "P3\n" << image_width << ' '
                << image_height << "\n255\n";

            for (int j = 0; j < image_height; j++) {
                std::clog << "\rScanlines remaining: " << (image_height - j) <<
                    ' ' << std::flush;
                for (int i = 0; i < image_width; i++) {
                    vec3 pixel_center = pixel00_loc + (i * pixel_delta_u) +
                                            (j * pixel_delta_v);
                    vec3 ray_direction = pixel_center - center;
                    ray r(center, ray_direction);

                    color pixel_color = ray_color(r, world);
                    write_color(std::cout, pixel_color);
                }
            }

            std::clog << "\rDone.           \n";
        }

    private:
        /* Private Camera Variables Here */
        int image_height; // Rendered image height
        point3 center; // Camera center
        point3 pixel00_loc; // Location of pixel (0,0)
        vec3 pixel_delta_u; // Offset pixel from left to right
        vec3 pixel_delta_v; // Offset pixel from top to bottom

        void initialize() {
            image_height = static_cast<int>(image_width / aspect_ratio);
            image_height = (image_height < 1) ? 1 : image_height;

            center = point3(0.0, 0.0, 0.0);

            // Determine viewport dimensions
            double focal_length = 1.0;
            double viewport_height = 2.0;
            double viewport_width = viewport_height *
                    static_cast<double>(image_width) / image_height;

            // Calculate the vectors across the horizontal
            // and vertical viewport edges
            vec3 viewport_u = vec3(viewport_width, 0.0, 0.0);
            vec3 viewport_v = vec3(0.0, -viewport_height, 0.0);

            // Calculate the horizontal and vertical delta vectors from
            // pixel to pixel
            pixel_delta_u = viewport_u / image_width;
            pixel_delta_v = viewport_v / image_height;

            // Calculate the location of the origin pixel (top, left)
            vec3 viewport_origin_edge = center - vec3(0.0, 0.0, focal_length)
                    - 0.5 * (viewport_u + viewport_v);
            pixel00_loc = viewport_origin_edge
                    + 0.5 * (pixel_delta_u + pixel_delta_v);
        }

        color ray_color(const ray& ray, const hittable& world) const {
            hit_record record;

            if (world.hit(ray, interval(0, INF), record)) {
                return 0.5 * (record.normal_vec + color(1.0, 1.0, 1.0));
            }

            vec3 unit_direction = unit_vector(ray.get_direction());
            double a = 0.5 * (unit_direction.get_y() + 1.0);
            return (1.0 - a) * color(1.0, 1.0, 1.0) + a * color(0.5, 0.7, 1.0); 
        }
};

#endif
