#!/bin/bash

filepath=$2
algorithm=$4

cmd="python extras/mdp.py $filepath $algorithm"

$cmd
