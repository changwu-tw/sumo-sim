#!/bin/bash


sim_time=$1

cd adsc
sh ../vehicle_model_generator.sh $sim_time
cd ../edgelist
python create_accusation_grpah.py adsc
cd ../perturbation
python addnoise.py adsc $sim_time
cd ../Champaign
sh ../vehicle_model_generator.sh $sim_time
cd ../edgelist
python create_accusation_grpah.py Champaign
cd ../perturbation
python addnoise.py Champaign $sim_time


echo 'finished'

