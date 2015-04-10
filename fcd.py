from lxml import etree


with open('xml.txt', 'w') as f:
    for event, element in etree.iterparse('adsc/adsc.fcd.xml', events=('end', ), tag='timestep'):
        f.write(str(element.attrib) + '\n')

        for info in element.iter():
            if info.tag in ('vehicle'):
                f.write(str(info.attrib) + '\n')

        f.write('-----------\n')
        # element.close()
        element.clear()
