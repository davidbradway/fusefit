# -*- coding: utf-8 -*-
"""
Docs used:
- http://lxml.de/tutorial.html#namespaces
- http://stackoverflow.com/questions/1786476/parsing-xml-in-python-using-elementtree-example
- https://docs.python.org/3/library/xml.etree.elementtree.html

@author: David
"""

try:
    from lxml import etree
    print("running with lxml.etree")
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree
        print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree
            print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree
                print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree
                    print("running with ElementTree")
                except ImportError:
                    print("Failed to import ElementTree from any known place")

XHTML_NAMESPACE = "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"
XHTML = "{%s}" % XHTML_NAMESPACE

phonefilename = r'C:\Users\dpb6\Documents\GitHub\fusefit\phone\activity_704970907.tcx'
hrmonfilename = r'C:\Users\dpb6\Documents\GitHub\fusefit\vivofit\activity_704996112.tcx'
outfilename = r'fused\uniqueStructure.tcx'

# python 2
#import Tkinter as tk
# python 3
import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()
filename = filedialog.askopenfilename()


tree = etree.parse(phonefilename)
root = tree.getroot()

"""
find_trainingCenterDatabase = etree.ETXPath("//{%s}TrainingCenterDatabase" % XHTML_NAMESPACE)
TrainingCenterDatabase = find_trainingCenterDatabase(root)
find_activities = etree.ETXPath("//{%s}Activities" % XHTML_NAMESPACE)
Activities = find_activities(root)
find_activity = etree.ETXPath("//{%s}Activity" % XHTML_NAMESPACE)
Activity = find_activity(root)
find_lap = etree.ETXPath("//{%s}Lap" % XHTML_NAMESPACE)
Lap = find_lap(root)
find_track = etree.ETXPath("//{%s}Track" % XHTML_NAMESPACE)
Track = find_track(root)
find_trackpoint = etree.ETXPath("//{%s}Trackpoint" % XHTML_NAMESPACE)
Trackpoint = find_trackpoint(root)
"""

for Trackpoint in root.iterfind(".//{%s}Trackpoint" % XHTML_NAMESPACE):
    for child in Trackpoint:
        print child.tag
    
# Dictionary of children and their parents
"""
parent_map = dict((c, p) for p in tree.getiterator() for c in p)
"""

"""
for rank in root.iter('rank'):
    new_rank = int(rank.text) + 1
    rank.text = str(new_rank)
    rank.set('updated', 'yes')

tree.write('output.xml')
"""

# in-place prettyprint formatter
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
