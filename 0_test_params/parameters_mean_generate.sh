#!/bin/bash

# get the path of the script:
SCRIPT_PATH="`dirname \"$0\"`"                  # relative
SCRIPT_PATH="`( cd \"$SCRIPT_PATH\" && pwd )`"  # absolutized and normalized
if [ -z "$SCRIPT_PATH" ] ; then
  exit 1
fi

# definitions:
OUT_FOLDER=$SCRIPT_PATH/parameters_mean
IN_FOLDER=$SCRIPT_PATH/parameters

# go to the script folder:
cd $SCRIPT_PATH

# cycle
for file in $IN_FOLDER/*.ini ;
do

	filename=$(basename "$file")
	extension="${filename##*.}"
	filename="${filename%.ini*}"

cat <<EOF > $OUT_FOLDER/$filename.ini

# output name:
test_output_root=5_SN_data/$filename
# mean parameters:
DEFAULT(5_SN_params/parameters_mean_inputrange/$filename.mean_inputrange)
# settings:
DEFAULT(5_SN_params/common_parameters/mean.ini)
DEFAULT(5_SN_params/parameters/$filename.ini)

EOF

done;
exit

#
