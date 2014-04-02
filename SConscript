# -*- mode:python -*-

Import('*')

# These are the default values for verbosity and math acceleration. To use
# other values check the HotSpot Makefile and change the values in the
# following line.
env.Append(CCFLAGS=['-DVERBOSE=1', '-DMATHACCEL=0'])

Source('flp.c', Werror=False)
Source('flp_desc.c', Werror=False)
Source('npe.c', Werror=False)
Source('package.c', Werror=False)
Source('RCutil.c', Werror=False)
Source('shape.c', Werror=False)
Source('temperature_block.c', Werror=False)
Source('temperature.c', Werror=False)
Source('temperature_grid.c', Werror=False)
Source('util.c', Werror=False)
Source('wire.c', Werror=False)
Source('hotspot-glue.c')

# Import the hotspot bindings as a top-level module called 'hotspot'.
SwigSource('', 'hotspot.i')

# The following files are part of the HotSpot source-code distribution, but are
# not part of the hotspot library, i.e, they're not needed or lead to build
# errors.
#
#   Source('hotfloorplan.c', Werror=False)
#   Source('hotspot.c', Werror=False)
#   Source('sim-template.c', Werror=False)
#   Source('temperature_mobile.c', Werror=False)
