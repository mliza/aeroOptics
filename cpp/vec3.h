#ifndef VEC3_H
#define VEC3_H

class vec3 {
    public:
        double e[3];

        // Constructors
        vec3() : e{0, 0, 0} { }
        vec3(double e0, double e1, double e2) : e{e0, e1, e2} { }

        // Getters
        double get_x() const { return e[0]; }
        double get_y() const { return e[1]; }
        double get_z() const { return e[2]; }

        // Function definitions (move to an .hpp file)
        vec3 operator-() const { return vec3(-e[0], -e[1], e[2]); }
        double operator[] (int i) const { return e[i]; } 
        double& operator[] (int i) { return e[i]; }

        // Function implementations (move to a .cpp file)
        vec3& operator += (const vec3& tmp) {
            e[0] += tmp.e[0];
            e[1] += tmp.e[1];
            e[2] += tmp.e[2];
            return *this;
        }

        vec3& operator *= (double tmp) {
            e[0] *= tmp;
            e[1] *= tmp;
            e[2] *= tmp;
            return *this;
        }

        vec3& operator /= (double tmp) {
            return *this *= 1 / tmp;
        }

        double get_length() const { return std::sqrt(get_length_squared()); }
        double get_length_squared() const {
            return e[0] * e[0] + e[1] * e[1] + e[2] * e[2];
        }

        bool near_zero() {
            // Return true if the vector is close to zero in all dimensions
            double s = 1e-8;
            return (std::fabs(e[0]) < s) &&
                   (std::fabs(e[1]) < s) &&
                   (std::fabs(e[2]) < s);

        }

        static vec3 random() {
            return vec3(random_double(), random_double(), random_double());
        }

        static vec3 random(double min, double max) {
            return vec3(random_double(min, max), random_double(min, max),
                    random_double(min, max));
        } 
};

// point3 is just an alias for vec3, but useful for geometric clarity in the code
using point3 = vec3;

// Vector Utility Functions
inline std::ostream& operator << (std::ostream& out, const vec3& v) {
    return out << v.e[0] << ' ' << v.e[1] << ' ' << v.e[2];
}

inline vec3 operator+(const vec3& u, const vec3& v) {
    return vec3(u.e[0] + v.e[0], u.e[1] + v.e[1], u.e[2] + v.e[2]);
}

inline vec3 operator-(const vec3& u, const vec3& v) {
    return vec3(u.e[0] - v.e[0], u.e[1] - v.e[1], u.e[2] - v.e[2]);
}

inline vec3 operator*(const vec3& u, const vec3& v) {
    return vec3(u.e[0] * v.e[0], u.e[1] * v.e[1], u.e[2] * v.e[2]); 
}

inline vec3 operator*(double tmp, const vec3& v) {
    return vec3(tmp * v.e[0], tmp * v.e[1], tmp * v.e[2]);
}

inline vec3 operator*(const vec3& v, double tmp) {
    return tmp * v;
}

inline vec3 operator/(const vec3& v, double tmp) {
    return (1 / tmp) * v;
}

inline double dot_product(const vec3& u, const vec3& v) {
    return u.e[0] * v.e[0] +
           u.e[1] * v.e[1] +
           u.e[2] * v.e[2];
}

inline vec3 cross_product(const vec3& u, const vec3& v) {
    return vec3(u.e[1] * v.e[2] - u.e[2] * v.e[1],
                u.e[2] * v.e[0] - u.e[0] * v.e[2],
                u.e[0] * v.e[1] - u.e[1] * v.e[0]);
}

inline vec3 unit_vector(const vec3& v) {
    return v / v.get_length();
}

inline vec3 random_in_unit_sphere() {
    while (true) {
        vec3 p = vec3::random(-1, 1);
        if (p.get_length_squared() < 1) {
            return p;
        }
    }
}

inline vec3 random_unit_vector() {
    return unit_vector(random_in_unit_sphere());
}

inline vec3 random_on_hemisphere(const vec3& normal) { 
    vec3 on_unit_sphere = random_unit_vector();
    // In the same hemisphere as the normal
    if (dot_product(on_unit_sphere, normal) > 0.0) {
        return on_unit_sphere;
    }
    else {
        return -on_unit_sphere;
    }
}

inline vec3 reflect(const vec3& v, const vec3& n) {
    return v - 2 * dot_product(v, n) * n;
}


#endif
