#!/bin/bash


cd adsc
sh ../vehicle_model_generator.sh 3600
cd ../edgelist
python create_accusation_grpah.py adsc

# cd ../perturbation
# python add_noise.py Champaign 2000


cd Champaign
sh ../vehicle_model_generator.sh 3600
cd ../edgelist
python create_accusation_grpah.py Champaign

# cd ../perturbation
# python add_noise.py Champaign 2000


echo 'finished'

