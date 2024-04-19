#! /usr/bin/env bash
if [[ $# -eq 0 ]]  
then  
	echo "JOBID argument not supplied"
	exit 1
else
	echo $1
	declare -a zzJobID=$1
	declare -a zzTempDir=/gws/nopw/j04/htap2/ptg21/${zzJobID}/pp_files_ox_eval_py/
	mkdir -p ${zzTempDir}
	cp call_template_oxeval ${zzTempDir}/
	cd ${zzTempDir}
	/opt/moose/external-client-version-wrapper/bin/moo select -f call_template_oxeval moose:crum/${zzJobID}/apy.pp ./
fi



