import pandas as pd
import random
import sys

from scipy import spatial


p_pf = 1e-7
p_mb = 0.1
radius = 20


def decision(p):
    return random.random() < p


if __name__ == '__main__':
    curr_dir = sys.argv[1]
    filepath = '../{0}/{0}.gpslane'.format(curr_dir)

    df = pd.read_csv(filepath, delimiter='\t', header=None)
    df.columns = ['id', 'x', 'y', 'lane_id', 'speed', 'angle', 'slope', 'timestep']

    # settings
    pd_vars = [0.01, 0.05, 0.1, 0.2]     # 0.3, 0.4, 0.5
    for p_pd in pd_vars:
        print p_pd

        # read adsc.gpslane
        accusation_file = '{0}_{1}_accusation_list.txt'.format(p_pd, curr_dir)

        with open(accusation_file, 'w') as f:

            timestep = list(set(df.timestep))

            for t in timestep:
                # Get vehicle information on timestep t
                dt = df[df.timestep == t]

                # Get vehicle's position
                x, y = dt.x, dt.y
                pos = zip(x.ravel(), y.ravel())
                tree = spatial.cKDTree(pos)

                for i, veh in enumerate(pos):
                    # A misbehavior vehicle exist
                    if decision(p_mb):
                        bad_vid = dt.iloc[i].id
                        # Get a list of the indices of the neighbors of vehicle
                        dt_index = tree.query_ball_point(veh, radius)
                        if dt_index:
                            for index in dt_index:
                                nearby_vid = dt.iloc[index].id
                                if bad_vid != nearby_vid and decision(p_pd):
                                    bad_loc = dt.iloc[i].x, dt.iloc[i].y
                                    nearby_loc = dt.iloc[index].x, dt.iloc[index].y
                                    f.write('{0} {1} {2} {3} {4} {5}\n'.format(nearby_vid, bad_vid, nearby_loc, bad_loc, 'T', t))
                    else:
                        good_vid = dt.iloc[i].id
                        # Get a list of the indices of the neighbors of vehicle
                        dt_index = tree.query_ball_point(veh, radius)
                        if dt_index:
                            for index in dt_index:
                                nearby_vid = dt.iloc[index].id
                                if good_vid != nearby_vid and decision(p_pf):
                                    good_loc = dt.iloc[i].x, dt.iloc[i].y
                                    nearby_loc = dt.iloc[index].x, dt.iloc[index].y
                                    f.write('{0} {1} {2} {3} {4} {5}\n'.format(nearby_vid, good_vid, nearby_loc, good_loc, 'F', t))
