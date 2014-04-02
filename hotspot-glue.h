/**
 * This header defines some SWIG glueing function, that allow access to C
 * arrays from Python code.
 */

#ifndef HOTSPOT_GLUE_H
#define HOTSPOT_GLUE_H 1

#include "hotspot-iface.h"

double double_array_get(double *arr, unsigned idx);
void double_array_set(double *arr, unsigned idx, double value);

unit_t * unit_array_get(unit_t *arr, unsigned idx);

void unit_array_set(unit_t *arr, unsigned idx, const unit_t *value);

FILE * load_floorplan_from_string(const char *str);

#endif /* HOTSPOT_GLUE_H */
