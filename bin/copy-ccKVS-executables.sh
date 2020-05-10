#!/usr/bin/env bash
HOSTS=(20.0.0.1 20.0.0.2 20.0.0.3)
# HOSTS=( "austin" "houston" "sanantonio")
#HOSTS=( "austin" "houston" "sanantonio")
#HOSTS=( "austin" "houston" "sanantonio" "indianapolis" "philly" )
#HOSTS=( "austin" "houston" "sanantonio" "indianapolis" "philly" "baltimore" "chicago" "atlanta" "detroit")
LOCAL_HOST=`hostname`
EXECUTABLES=("ccKVS-sc" "ccKVS-lin" "run-ccKVS.sh")
HOME_FOLDER=~/ccKVS/src/ccKVS
DEST_FOLDER=~/ccKVS/src/ccKVS

cd $HOME_FOLDER
make
cd -

# for EXEC in "${EXECUTABLES[@]}"
# do
# 	#echo "${EXEC} copied to {${HOSTS[@]/$LOCAL_HOST}}"
# 	parallel scp ${HOME_FOLDER}/${EXEC} {}:${DEST_FOLDER}/${EXEC} ::: $(echo ${HOSTS[@]/$LOCAL_HOST})
# 	echo "${EXEC} copied to {${HOSTS[@]/$LOCAL_HOST}}"
# done

for exec in "${EXECUTABLES[@]}"; do
	for host in "${HOSTS[@]}"; do
		scp -o StrictHostKeyChecking=no $HOME_FOLDER/$exec yangzhou@$host:$DEST_FOLDER/$exec
		echo "$exec copied to $host"
	done
done
