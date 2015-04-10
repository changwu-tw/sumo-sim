#!/bin/bash

# cd adsc
# sh vehicle_model_generator.sh 2000
# cd ../edgelist
# python create_accusation_grpah.py
# cd ../perturbation
cd perturbation
python add_noise.py

echo 'finished'

