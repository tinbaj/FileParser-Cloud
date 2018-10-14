"""import lxml.etree as etree


x = etree.parse(r"C:/Users/Public/Documents/Python Scripts/text_file.xml")
print(etree.tostring(x, pretty_print=True))
"""

"""import xml.etree.ElementTree as ET
tree = ET.parse(r"C:/Users/Public/Documents/Python Scripts/text_file.xml")
root = tree.getroot()
print(root)
for child in root.iter('*'):
    print(child.tag, child.attrib,child.text)
"""

import os
import sys

print((os.path.join(os.path.abspath('.'),'\lib')))
for k in sys.path:
    print(k)


"""
from lxml import etree

for word in etree.parse(r"C:/Users/Public/Documents/Python Scripts/text_file.xml").xpath("///TestOrders"):
    print(word)
    print('--------------------------------------------------')
    for items in word:
        print(items)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print(type(items))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        for t in items:

            for t1 in t:
                print(t1)

"""