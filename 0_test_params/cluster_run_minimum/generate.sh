#!/bin/bash

# get the path of the script:
SCRIPT_PATH="`dirname \"$0\"`"                  # relative
SCRIPT_PATH="`( cd \"$SCRIPT_PATH\" && pwd )`"  # absolutized and normalized
if [ -z "$SCRIPT_PATH" ] ; then
  exit 1
fi

# go to the script folder:
cd $SCRIPT_PATH

# parameters directories:

for file in $SCRIPT_PATH/../parameters_minimum/*.ini ;

do

	filename=$(basename "$file")
	extension="${filename##*.}"
	filename="${filename%.ini*}"

cat <<EOF > $filename.sbatch
#!/bin/bash
#SBATCH --job-name=$filename.minimum
#SBATCH --output=0_test_chains/$filename.minimum.out
#SBATCH --error=0_test_chains/$filename.minimum.err
#SBATCH --time=36:00:00
#SBATCH --partition=kicp
#SBATCH --account=kicp
###SBATCH --ntasks=1
#SBATCH --nodes=1
###SBATCH --ntasks-per-node=1
#SBATCH --exclusive

# prepare the environment:
source ~/environment/cosmomc.sh

mpirun -np 1 ./cosmomc 0_test_params/parameters_minimum/$filename.ini

EOF

done;

exit
