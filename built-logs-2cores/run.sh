#/bin/bash

run() {
	FILE=$1
	CONFIG=$2
	FLP=$3 
	(
	../hotspot -c ${CONFIG} -f ${FLP} -p ${FILE}.ptrace -steady_file ${FILE}.steady -model_type grid -grid_steady_file ${FILE}.grid.steady -o ${FILE}.ttrace
	perl ../grid_thermal_map.pl ${FLP} ${FILE}.grid.steady 64 64 320 352 > ${FILE}.svg
	convert -density 288 ${FILE}.svg ${FILE}.png
	)
}

#run basket_2cores exp2cores.config exp2cores.flp
run $1 $2 $3
