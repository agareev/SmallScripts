#!/usr/bin/env bash

# #
# sync infocx modules between servers
# #
source server.conf


from=${1}
to=${2}
module_name=${3}
alias getversion="unzip -q -c ${1}/${1}.jar META-INF/MANIFEST.MF|grep Build-Version|awk '{print $2}'"

if [[ ${from} == "beta" ]]; then
  donor="infocx@${beta-server}"
else
  donor="infocx@${from}"
fi

if [[ ${to} == "prod" ]]; then
  recipient="infocx@${prod-server}"
else
  recipient="infocx@${to}"
fi

if [[ ${module_name} == "" ]]; then
  module_name="All"
else
  module_name=${module_name}
fi


echo "${donor} to ${recipient} coping module ${module_name}"
#cd ${module_name}
if [[ ${module_name} != "All" ]]; then
  files=$(ssh ${donor} "find ~infocx/${module_name} -name '*.jar'")
  for i in ${files}; do
    ssh ${donor} "hostname"
    ssh ${donor} "unzip -q -c ${i} META-INF/MANIFEST.MF|grep Build-Version"
  done
else
  echo "stub"
fi
