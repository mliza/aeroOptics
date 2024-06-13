#ifndef MATERIAL_H
#define MATERIAL_H

#include "rtweekend.h"

class hit_record;

class material {
    public:
        virtual ~material() = default;

        virtual bool scatter(const ray& r_in, const hit_record& rec,
                            color& attenuation, ray& scattered) const {
            return false;
        }

};

class metal : public material {
    public:
        metal(const color& albedo) : albedo(albedo) { }

        bool scatter(const ray& r_in, const hit_record& rec,
                    color& attenuation, ray& scattered) const override {
            vec3 reflected = reflect(r_in.get_direction(), rec.normal_vec);
            scattered = ray(rec.point, reflected);
            attenuation = albedo;
            return true;
        }

    private:
        color albedo;
};

class lambertian : public material {
    public:
        lambertian(const color& albedo) : albedo(albedo) { }

        bool scatter(const ray& r_in, const hit_record& rec,
                color& attenuation, ray& scattered) const override {
            vec3 scatter_direction = rec.normal_vec + random_unit_vector();

            // Catch degenerate scatter direction
            if (scatter_direction.near_zero()) {
                scatter_direction = rec.normal_vec;
            }

            scattered = ray(rec.point, scatter_direction);
            attenuation = albedo;
            return true;
        }

    private:
        color albedo;
};

#endif
