#ifndef RTWEEKEND_H
#define RTWEEKEND_H

#include <cmath>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <memory>
#include <random>

// C++ Std Using
using std::fabs;
using std::make_shared;
using std::shared_ptr;
using std::sqrt;

// Constants
const double INF = std::numeric_limits<double>::infinity();
const double PI = 3.1415926535897932385; 

// Utility Functions
inline double deg_to_rad(double degrees) {
    return degrees * PI / 180.0;
}

/* This doesnt mach the one from the repo
inline double random_double() {
    static std::uniform_real_distribution<double> distribution(0.0, 1.0);
    static std::mt19937 generator;
    return distribution(generator);    
}
*/

inline double random_double() {
    // Returns a random real in [0,1).
    return rand() / (RAND_MAX + 1.0);
}

inline double random_double(double min, double max) {
    // Returns a random real in [min, max)
    return min + (max - min) * random_double();
}

// Common Headers 
#include "color.h"
#include "interval.h"
#include "ray.h"
#include "vec3.h"

#endif
