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

for file in $SCRIPT_PATH/../parameters/*.ini ;

do

	filename=$(basename "$file")
	extension="${filename##*.}"
	filename="${filename%.ini*}"

cat <<EOF > $filename.sbatch
#!/bin/bash
#SBATCH --job-name=$filename
#SBATCH --output=0_test_chains/$filename.out
#SBATCH --error=0_test_chains/$filename.err
#SBATCH --time=36:00:00
#SBATCH --partition=broadwl
#SBATCH --account=pi-whu5
#SBATCH --ntasks=8
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --exclusive

# prepare the environment:
source ~/environment/cosmomc_18.sh

mpirun -np 8 ./cosmomc 0_test_params/parameters/$filename.ini

EOF

done;

exit