from glob import glob


def outputToHTML():
    pics = zip(glob('pic/*_initial.png'), glob('pic/*_linkage.png'), glob('pic/*_perturb.png'))

    with open('demo.html', 'w') as f:
        f.write('<table border="1">')
        f.write('<tbody>')

        for i, j, k in pics:
            f.write('<tr>')
            f.write('<td><img src="{0}" /></td><td><img src="{1}" /></td><td><img src="{2}" /></td>'.format(i, j, k))
            f.write('</tr>')

        f.write('</tbody>')
        f.write('</table>')
