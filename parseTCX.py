# -*- coding: utf-8 -*-
"""
Docs used:
- http://lxml.de/tutorial.html#namespaces
- http://stackoverflow.com/questions/1786476/parsing-xml-in-python-using-elementtree-example
- https://docs.python.org/3/library/xml.etree.elementtree.html

@author: David
"""
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

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

try:
    # python 2
    import Tkinter as tk
    print("running Tkinter")
except ImportError:
    try:
        # python 3
        import tkinter as tk
        from tkinter import filedialog
        print("running tkinter")
    except ImportError:
        print("Failed to import tkinter")


root = tk.Tk()
root.withdraw()
filename = filedialog.askopenfilename()

XHTML_NAMESPACE = "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"
XHTML = "{%s}" % XHTML_NAMESPACE

phonefilename = r'C:\Users\David\Downloads\fusefit\phone\activity_704970907.tcx'
hrmonfilename = r'C:\Users\David\Downloads\fusefit\vivofit\activity_704996112.tcx'
outfilename = r'fused\uniqueStructure.tcx'

tree = etree.parse(phonefilename)
root = tree.getroot()

treehr = etree.parse(hrmonfilename)
roothr = treehr.getroot()

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

times = []
for Trackpoint in root.iterfind(".//{%s}Trackpoint" % XHTML_NAMESPACE):
    for child in Trackpoint:
        #print(child.tag, child.attrib)
        if 'Time' in child.tag:
            print(child.text)
            times.append(datetime.strptime(child.text, '%Y-%m-%dT%H:%M:%S.000Z'))

timeshr = []
hr = []
hrdict = {}
for Trackpoint in roothr.iterfind(".//{%s}Trackpoint" % XHTML_NAMESPACE):
    for child in Trackpoint:
        #print(child.tag)
        if 'Time' in child.tag:
            #print(child.text)
            timeshr.append(datetime.strptime(child.text, '%Y-%m-%dT%H:%M:%S.000Z'))
        if 'HeartRateBpm' in child.tag:
            Values = child.getchildren()
            for value in Values:
                #print(value.text)
                hr.append(int(value.text))
                hrdict[timeshr[-1]] = hr[-1]
print(hrdict)

print(len(timeshr))
print(len(hrdict))

print(times[23:28])

print(timeshr[:5])

#plt.plot(range(len(hrdict)), list(hrdict.values()))
#plt.xticks(range(len(hrdict)),list(hrdict.keys()))
#plt.show()
