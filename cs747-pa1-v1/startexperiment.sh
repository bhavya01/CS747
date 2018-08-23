#!/bin/bash

PWD=`pwd`


port=$3
nRuns=100
hostname="localhost"

# Allowed values for algorithm parameter(case-sensitive)
# 1. epsilon-greedy
# 2. UCB
# 3. KL-UCB
# 4. Thompson-Sampling
# 5. rr


algorithm=$1
horizon=1000
epsilon=$2
numArms=25
randomSeed=3

banditFile="$PWD/data/instance-histogram-25.txt"


SERVERDIR=./server
CLIENTDIR=./client

for NUM in {1..100};
do
OUTPUTFILE=$PWD/serverlog.txt
CLIENTFILE=$PWD/output/clientlog$NUM.txt
randomSeed=$((1 + RANDOM % 1000))
echo $randomSeed
pushd $SERVERDIR
cmd="./startserver.sh $numArms $horizon $port $banditFile $randomSeed $OUTPUTFILE &"
# echo $cmd
$cmd
popd

sleep 1

pushd $CLIENTDIR
cmd="./startclient.sh $numArms $horizon $hostname $port $randomSeed $algorithm $epsilon $CLIENTFILE &"
$cmd
popd

sleep 1

done
