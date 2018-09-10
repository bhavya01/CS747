#!/bin/bash


#To run this script put it outside just outside extras folder where encodeGambler.sh and planner.sh are present
ph=( 0.2 0.4 0.6 0.8 )
outputfile='gambler.txt'
for i in "${ph[@]}"
do
    echo $i
	cmd="./encodeGambler.sh $i"
    $cmd > $outputfile
    cmd="./planner.sh --mdp gambler.txt --algorithm hpi"
    $cmd
done

cmd="python extras/plot.py"
$cmd
