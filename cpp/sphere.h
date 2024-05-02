#ifndef SPHERE_H
#define SPHERE_H

#include "hittable.h"

class sphere : public hittable {
    public:
        sphere(const point3& center, double radius) : center(center), radius(fmax(0, radius)) { }

        bool hit(const ray& r, interval ray_t, hit_record& rec) const override {
            vec3 origin_center = center - r.get_origin();
            double a = r.get_direction().get_length_squared();
            double h = dot_product(r.get_direction(), origin_center);
            double c = origin_center.get_length_squared() - radius * radius;

            double discriminant = h * h - a * c;
            if (discriminant < 0.0) {
                return false;
            }

            double sqrt_discriminant = std::sqrt(discriminant);

            // Find the nearest root that lies in the acceptable range
            double root = (h - sqrt_discriminant) / a;
            if (!ray_t.surrounds(root)) {
                root = (h  + sqrt_discriminant) / a;
                if (!ray_t.surrounds(root)) { 
                    return false;
                }
            }

            rec.t = root;
            rec.point = r.at(rec.t);
            vec3 outward_normal = (rec.point - center) / radius;
            rec.set_face_normal(r, outward_normal);

            return true;
        }

    private:
        point3 center;
        double radius;

};
#endif
