#ifndef INTERVAL_H
#define INTERVAL_H

class interval {
    public:
        double min;
        double max;

        interval() : min(+INF), max(-INF) { } //Default interval is empty

        interval(double min, double max) : min(min), max(max) { }

        double size() const {
            return max - min;
        }

        bool contains(double x) const {
            return min <= x && x <= max;
        }

        bool surrounds(double x) const {
            return min < x && x < max;
        }

        static const interval empty; 
        static const interval universe;

};

const interval interval::empty = interval(+INF, -INF);
const interval interval::universe = interval(+INF, -INF);

#endif
