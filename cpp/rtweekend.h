#ifndef RTWEEKEND_H
#define RTWEEKEND_H

#include <cmath>
#include <iostream>
#include <limits>
#include <memory>

// C++ Std Using
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

// Common Headers 
#include "color.h"
#include "interval.h"
#include "ray.h"
#include "vec3.h"

#endif
