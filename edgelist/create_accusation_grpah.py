import random
import sys

import pandas as pd

def decision(probability):
    return random.random() < probability


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
                if decision(0.1):
                    bad_vid = random.choice(vids)

                    for vid in vids:
                        if vid != bad_vid and decision(0.8):
                            f.write('{} {} {}\n'.format(vid, bad_vid, t))

            curr_vids.append(tmp_vids)

        prev_vids = curr_vids

    f.close()


if __name__ == '__main__':
    main()
