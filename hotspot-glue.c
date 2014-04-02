#include <stdio.h>
#include <string.h>

#include "hotspot-glue.h"

double
double_array_get(double *arr, unsigned idx)
{
    return arr[idx];
}

void
double_array_set(double *arr, unsigned idx, double value)
{
    arr[idx] = value;
}

unit_t *
unit_array_get(unit_t *arr, unsigned idx)
{
    return &arr[idx];
}

void
unit_array_set(unit_t *arr, unsigned idx, const unit_t *value)
{
    arr[idx] = *value;
}

FILE *
load_floorplan_from_string(const char *str)
{
    /*
     * fmemopen operates on a non-const pointer, but we're opening it
     * read-only, thus we can be sure that nothing ever writes into the buffer.
     */
    FILE *f = fmemopen((void *)str, strlen(str), "r");

    if (!f)
        fprintf(stderr, "Warning: loading floorplan from memory failed!\n");

    return f;
}
