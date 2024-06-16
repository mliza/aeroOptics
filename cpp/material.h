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
        metal(const color& albedo, double fuzz) : albedo(albedo), fuzz(fuzz < 1 ? fuzz : 1) {}

        bool scatter(const ray& r_in, const hit_record& rec,
                    color& attenuation, ray& scattered) const override {
            vec3 reflected = reflect(r_in.get_direction(), rec.normal_vec);
            reflected = unit_vector(reflected) + (fuzz * random_unit_vector());
            scattered = ray(rec.point, reflected);
            attenuation = albedo;
            return (dot_product(scattered.get_direction(), rec.normal_vec) > 0); 
        }

    private:
        color albedo;
        double fuzz;
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

class dielectric : public material {
    public:
        dielectric(double refraction_index) : refraction_index(refraction_index) {}
        
        bool scatter(const ray& r_in, const hit_record& rec, 
                    color& attenuation, ray& scattered) const override {
            attenuation = color(1.0, 1.0, 1.0);
            double ri = rec.front_face ? (1.0 / refraction_index) : refraction_index;

            vec3 unit_direction = unit_vector(r_in.get_direction());
            double cos_theta = fmin(dot_product(-unit_direction, rec.normal_vec),
                                    1.0);
            double sin_theta = sqrt(1.0 - cos_theta * cos_theta);
            bool cannot_refract = ri * sin_theta > 1.0;

            vec3 direction;

            if (cannot_refract || reflectance(cos_theta, ri) > random_double()) {
                direction = reflect(unit_direction, rec.normal_vec);
            } else {
                direction = refract(unit_direction, rec.normal_vec, ri);
            }

            scattered = ray(rec.point, direction);
            return true;
        }

    private:
        // Refractive index in vacuum or air, or the ratio of the material's
        // refractive index over the refractive index of the enclosing media
        double refraction_index;
        static double reflectance(double cosine, double refraction_index) {
            // Use Schlick's approximation for reflectance
            double r0 = (1.0 - refraction_index) / (1 + refraction_index);
            r0 = r0 * r0;
            return r0 + (1 - r0) * pow((1 - cosine), 5);
        }

};

#endif
