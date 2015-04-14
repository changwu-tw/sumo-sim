#!/bin/bash

curr_dir="${PWD##*/}"
sim_time=$1


netconvert --osm-files $curr_dir.osm -o $curr_dir.net.xml
polyconvert --net-file $curr_dir.net.xml --osm-files $curr_dir.osm --osm.keep-full-type --type-file ../typemap.xml -o $curr_dir.poly.xml
python /Users/user/sumo/tools/trip/randomTrips.py -n $curr_dir.net.xml -e $sim_time -l
python /Users/user/sumo/tools/trip/randomTrips.py -n $curr_dir.net.xml -r $curr_dir.rou.xml -e $sim_time -l
python ../cfg_generator.py $curr_dir $sim_time
sumo --net-file $curr_dir.net.xml --route-files $curr_dir.rou.xml --fcd-output $curr_dir.fcd.xml
python /Users/user/sumo/tools/traceExporter.py --fcd-input $curr_dir.fcd.xml --gpslane-output $curr_dir.gpslane


##### Statistics #####
# sumo --net-file $curr_dir.net.xml --route-files $curr_dir.rou.xml --netstate-dump $curr_dir.sumo.tr --tripinfo-output tripinfo.tr
# python /Users/user/sumo/tools/output/vehLanes.py adsc.sumo.tr vehLanes.xml

##### Open simulator #####
# sumo-gui $curr_dir.sumo.cfg
