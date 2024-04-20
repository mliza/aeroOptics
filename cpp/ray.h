#ifndef RAY_H
#define RAY_H

#include "vec3.h"

class ray{
    public:
        // Constructor
        ray () { }
        ray(const point3& origin, const vec3 direction) : orig(origin), dir(direction) { }

        // Getters
        const point3& get_origin() const { return orig;}
        const vec3& get_direction() const { return dir;}

        // position(x) = origin + displacement * direction
        point3 at(double displacement) const{ 
            return orig + displacement * dir;
        }

    private:
        point3 orig;
        vec3 dir;
};

#endif
