#ifndef HITTABLE_H
#define HITTABLE_H

#include "rtweekend.h"
class material;

class hit_record {
    public:
        point3 point;
        vec3 normal_vec;
        shared_ptr<material> mat;
        double t;
        bool front_face;

    void set_face_normal(const ray& ray, const vec3& outward_normal) {
        // Sets the hit record normal vector
        // NOTE: the parameter outward_normal is assume to be unit length

        front_face = dot_product(ray.get_direction(), outward_normal) < 0.0;
        normal_vec = front_face ? outward_normal : -outward_normal;
    }

};

class hittable {
    public:
        virtual ~hittable() = default;

        virtual bool hit(const ray& ray, interval ray_t, hit_record& rec) const = 0;
};

#endif
