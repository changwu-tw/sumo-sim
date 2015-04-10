# -*- coding: utf-8 -*-

import sys

curr_dir = sys.argv[1]
sim_time = sys.argv[2]

cfg_file="""<?xml version="1.0" encoding="iso-8859-1"?>

<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.sf.net/xsd/sumoConfiguration.xsd">

    <input>
        <net-file value="{}.net.xml"/>
        <route-files value="{}.rou.xml"/>
        <additional-files value="{}.poly.xml"/>
    </input>

    <time>
        <begin value="0"/>
        <end value="{}"/>
        <step-length value="0.1"/>
    </time>

    <gui_only>
        <start value="true"/>
    </gui_only>

</configuration>
"""

filename = '{}.sumo.cfg'.format(curr_dir)

with open(filename, 'w') as f:
    f.write(cfg_file.format(curr_dir, curr_dir, curr_dir, sim_time))



