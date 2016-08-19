#!/usr/bin/python3
# -*- coding: utf-8 -*-

__appname__ = "fusefit"
__author__  = "David Bradway (dpb6 @ duke)"
__version__ = "1"
__license__ = "MIT"

import os, sys, math
from datetime import datetime
#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    from lxml import etree
    print("running with lxml.etree")
except ImportError:
    print("failed to import etree, requires Python3")


def parseLaps(roothr, XHTML_NAMESPACE):
    # Initialize Time Series
    averageHeartRateBpm_value = []
    maximumHeartRateBpm_value = []
    for Lap in roothr.iterfind(".//{{{}}}Lap".format(XHTML_NAMESPACE)): # 3.1+ only
        averageHeartRateBpm = Lap.find(".//{{{}}}AverageHeartRateBpm".format(XHTML_NAMESPACE)) # 3.1+ only
        if averageHeartRateBpm is not None:
            value = averageHeartRateBpm.find(".//{{{}}}Value".format(XHTML_NAMESPACE))
            averageHeartRateBpm_value.append(value.text)

        maximumHeartRateBpm = Lap.find(".//{{{}}}MaximumHeartRateBpm".format(XHTML_NAMESPACE)) # 3.1+ only
        if maximumHeartRateBpm is not None:
            value = maximumHeartRateBpm.find(".//{{{}}}Value".format(XHTML_NAMESPACE))
            maximumHeartRateBpm_value.append(value.text)
    return {'averageHeartRateBpm_value':averageHeartRateBpm_value,'maximumHeartRateBpm_value':maximumHeartRateBpm_value}


def parseTimes(root, XHTML_NAMESPACE):
    # Initialize Time Series
    nohrdict = {}
    for Trackpoint in root.iterfind(".//{{{}}}Trackpoint".format(XHTML_NAMESPACE)): # 3.1+ only
        time = Trackpoint.find(".//{{{}}}Time".format(XHTML_NAMESPACE)) # 3.1+ only
        timedatetime = datetime.strptime(time.text, '%Y-%m-%dT%H:%M:%S.000Z')
        nohrdict[timedatetime] = np.nan
    return nohrdict


def parseHRs(roothr, hrSeries, XHTML_NAMESPACE):
    # Update and add HR timepoints
    for Trackpoint in roothr.findall(".//{{{}}}Trackpoint".format(XHTML_NAMESPACE)): # 3.1+ only
        time = Trackpoint.find(".//{{{}}}Time".format(XHTML_NAMESPACE)) # 3.1+ only
        timedatetime = datetime.strptime(time.text, '%Y-%m-%dT%H:%M:%S.000Z')
        heartRateBpm = Trackpoint.find(".//{{{}}}HeartRateBpm".format(XHTML_NAMESPACE)) # 3.1+ only
        if heartRateBpm is not None:
            value = heartRateBpm.find(".//{{{}}}Value".format(XHTML_NAMESPACE))
            hrSeries[timedatetime] = int(value.text)
    return hrSeries


def appendHRs(tree,root, hrSeries, outfilename, XHTML_NAMESPACE, dump=False):
    for Trackpoint in root.iterfind(".//{{{}}}Trackpoint".format(XHTML_NAMESPACE)): # 3.1+ only
        time = Trackpoint.find(".//{{{}}}Time".format(XHTML_NAMESPACE)) # 3.1+ only
        timedatetime = datetime.strptime(time.text, '%Y-%m-%dT%H:%M:%S.000Z')
        temp = hrSeries.loc[timedatetime]
        if math.isnan(temp) == False:
            heartRateBpm = etree.SubElement(Trackpoint,'HeartRateBpm')
            value = etree.SubElement(heartRateBpm,'Value')
            value.text = str(temp)
    if dump:
        etree.dump(root)
    tree.write(outfilename)


def mergeUploaded(folder,filename):
    XHTML_NAMESPACE = "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"

    filewohr = os.path.join(folder,filename[0])
    filewhr = os.path.join(folder,filename[1])
    outfilename = os.path.join(folder,'fused.tcx')

    tree = etree.parse(filewohr)
    root = tree.getroot()

    treehr = etree.parse(filewhr)
    roothr = treehr.getroot()

    result = parseLaps(roothr, XHTML_NAMESPACE)
    averageHeartRateBpm_value = result['averageHeartRateBpm_value']
    maximumHeartRateBpm_value = result['maximumHeartRateBpm_value']
    # TODO: Need to use the Above values!

    # Make a Pandas Series from the Dict
    hrSeries = parseHRs(roothr, pd.Series(parseTimes(root, XHTML_NAMESPACE)), XHTML_NAMESPACE)
    hrSeries.sort_index(inplace=True)
    hrSeries = hrSeries.interpolate(method='time')

    appendHRs(tree, root, hrSeries, outfilename, XHTML_NAMESPACE)

def main():

    # try:
        # import tkinter as tk
        # from tkinter import filedialog
        # print("running tkinter")
        # root = tk.Tk()
        # root.withdraw()
        # filename = tk.filedialog.askopenfilename()
    # except ImportError:
        # print("Failed to import tkinter, requires Python3")

    XHTML_NAMESPACE = "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"

    startdir = os.getcwd()

    phonefilename = os.path.join(startdir,'samplefiles','phone', 'activity_704970907.tcx')
    hrmonfilename = os.path.join(startdir,'samplefiles','vivofit', 'activity_704996112.tcx')
    outfilename = os.path.join(startdir,'samplefiles','fused.tcx')

    tree = etree.parse(phonefilename)
    root = tree.getroot()

    treehr = etree.parse(hrmonfilename)
    roothr = treehr.getroot()

    """
    find_trainingCenterDatabase = etree.ETXPath("//{{{}}}TrainingCenterDatabase".format(XHTML_NAMESPACE)) # 3.1+ only
    TrainingCenterDatabase = find_trainingCenterDatabase(root)
    find_activities = etree.ETXPath("//{{{}}}Activities".format(XHTML_NAMESPACE)) # 3.1+ only
    Activities = find_activities(root)
    find_activity = etree.ETXPath("//{{{}}}Activity".format(XHTML_NAMESPACE)) # 3.1+ only
    Activity = find_activity(root)
    find_lap = etree.ETXPath("//{{{}}}Lap".format(XHTML_NAMESPACE)) # 3.1+ only
    Lap = find_lap(root)
    find_track = etree.ETXPath("//{{{}}}Track".format(XHTML_NAMESPACE)) # 3.1+ only
    Track = find_track(root)
    find_trackpoint = etree.ETXPath("//{{{}}}Trackpoint".format(XHTML_NAMESPACE)) # 3.1+ only
    Trackpoint = find_trackpoint(root)
    """

    result = parseLaps(roothr, XHTML_NAMESPACE)
    averageHeartRateBpm_value = result['averageHeartRateBpm_value']
    maximumHeartRateBpm_value = result['maximumHeartRateBpm_value']
    # TODO: Need to use the Above values!

    nohrdict = parseTimes(root, XHTML_NAMESPACE)

    # Make a Pandas Series from the Dict
    hrSeries = pd.Series(nohrdict)

    hrSeries = parseHRs(roothr, hrSeries, XHTML_NAMESPACE)

    hrSeries.sort_index(inplace=True)
    hrSeries = hrSeries.interpolate(method='time')
    # hrSeries.plot()

    appendHRs(tree, root, hrSeries, outfilename, XHTML_NAMESPACE)

if __name__ == "__main__": main()
