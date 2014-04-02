/* Make the hotspot module a top-level module. */
%module(package="") hotspot

%{
#if defined __cplusplus
extern "C" {
#endif
#include "hotspot-iface.h"
#include "hotspot-glue.h"
#if defined __cplusplus
}
#endif
%}

%include "hotspot-iface.h"
%include "hotspot-glue.h"
