../hotspot -c exp2cores.config -f exp2cores.flp -p ces2652.ptrace -steady_file ces2652.steady -model_type grid -grid_steady_file ces2652.grid.steady -o ces2652.ttrace
perl ../grid_thermal_map.pl exp2cores.flp ces2652.grid.steady > ces2652.svg
convert -font Helvetica svg:ces2652.svg ces2652.pdf
