# -*- coding: utf-8 -*-
"""
Docs used:
- http://lxml.de/tutorial.html#namespaces
- http://stackoverflow.com/questions/1786476/parsing-xml-in-python-using-elementtree-example
- https://docs.python.org/3/library/xml.etree.elementtree.html
- http://pandas.pydata.org/pandas-docs/version/0.15.0/generated/pandas.Series.interpolate.html?highlight=interpolate#pandas.Series.interpolate
- http://stackoverflow.com/questions/30530001/python-pandas-time-series-interpolation-and-regularization
- http://pandas.pydata.org/pandas-docs/stable/missing_data.html

@author: David
"""
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd


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

startdir = os.getcwd()

phonefilename = os.path.join('phone', 'activity_704970907.tcx')
hrmonfilename = os.path.join('vivofit', 'activity_704996112.tcx')
outfilename = os.path.join('fused', 'uniqueStructure.tcx')

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

nohrdict = {}
for Trackpoint in root.iterfind(".//{%s}Trackpoint" % XHTML_NAMESPACE):
    time = Trackpoint.find(".//{%s}Time" % XHTML_NAMESPACE).text
    timedatetime = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.000Z')
    nohrdict[timedatetime] = np.nan

nohrSeries = pd.Series(nohrdict)
#nohrSeries.plot()

hrdict = {}
for Trackpoint in roothr.findall(".//{%s}Trackpoint" % XHTML_NAMESPACE):
    time = Trackpoint.find(".//{%s}Time" % XHTML_NAMESPACE).text
    timedatetime = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.000Z')
    heartRateBpm = Trackpoint.find(".//{%s}HeartRateBpm" % XHTML_NAMESPACE)
    if heartRateBpm is not None:
        value = heartRateBpm.find(".//{%s}Value" % XHTML_NAMESPACE).text
        hrdict[timedatetime] = int(value)

hrSeries = pd.Series(hrdict)
#hrSeries.plot()

result = pd.concat([nohrSeries,hrSeries], axis=0).sort_index()
result = result.interpolate(method='time')
result.plot()

