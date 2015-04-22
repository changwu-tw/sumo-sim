import random
import sys

import pandas as pd
from random import randint


def decision(probability):
    return random.random() < probability


# print randint(0, 10000000)
# p_pd = 0.01
# p_pf = 1e-7
p_pd = 0.5
p_pf = 1e-4
p_mb = 0.1


def main():
    curr_dir = sys.argv[1]
    filepath = '../{}/{}.gpslane'.format(curr_dir, curr_dir)

    df = pd.read_csv(filepath, delimiter='\t', header=None)
    df.columns = ['id', 'x', 'y', 'lane_id', 'speed', 'angle', 'slope', 'timestep']

    # read adsc.gpslane
    accusation_file = '{}_accusation_list.txt'.format(curr_dir)
    f = open(accusation_file, 'w')

    timestep = list(set(df.timestep))

    prev_vids = []
    for t in timestep:
        # Get vehicle information on timestep t
        dt = df[df['timestep'] == t]

        # Check whether there is any vehicle on the same lane?
        d = dict(dt['lane_id'].value_counts())

        curr_vids = []
        for k, v in d.iteritems():
            if v == 1: continue

            # Get the nearby vehicle ids
            vids = dt[dt['lane_id'] == k].id.values
            tmp_vids = ', '.join(str(v) for v in vids)

            if tmp_vids not in prev_vids:
                # Exist a misbehavior vehicle and is detected
                if decision(p_mb):
                    bad_vid = random.choice(vids)

                    for vid in vids:
                        if vid != bad_vid and decision(p_pd):
                            f.write('{} {} {}\n'.format(vid, bad_vid, t))
                else:
                    good_vid = random.choice(vids)

                    for vid in vids:
                        if vid != good_vid and decision(p_pf):
                            f.write('{} {} {}\n'.format(vid, good_vid, t))

            curr_vids.append(tmp_vids)

        prev_vids = curr_vids

    f.close()


if __name__ == '__main__':
    main()
