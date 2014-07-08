#!/usr/bin/python

import csv
from copy import deepcopy
from math import *

# Define defaults

# Order is followed, though it shouldn't actually affect results
SORT_ORDER = [
    'Age',
    'd18O',
    'Pb',
    'Sr',
    'DeathYr',
    'Sex',
    'Race'
]
ERROR_RANGES = {
    'Age': 0.25, # proportion
    'd18O': 0.40, # proportion
    'DeathYr': 4, # range
    'Pb': 0.03**0.5, # log proportion
    'Sr': 0.01**0.5 # log proportion
}

ERROR_FUNCTIONS = {
    'Age': "x * 0.25", # proportion
    'd18O': "x * 0.40", # proportion
    'DeathYr': "4", # range
    'Pb': "x * 0.03**0.5", # log proportion
    'Sr': "x * 0.01**0.5" # log proportion
}

# This list includes user-accessible functions for the error functions
safe_list = ['math','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'de grees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']

def matcher(sortOrder=SORT_ORDER, errorFunctions=ERROR_FUNCTIONS, outDir="./"):

    # Use the list to filter the local namespace
    safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ])
    # Add any needed builtins back in
    safe_dict['abs'] = abs
    
    
    acceptableCategories = {
        'Race': {'C','B','H'},
        'Sex': {'M','F'} 
    }

    # Record anomalous data that needs to be handled or cleaned up
    log_fp = open('anomaly_log.csv', 'w')
    anomalyLog = csv.writer(log_fp)

    # return True when record is outside of acceptable range
    def isPoorFit(skel, record, key):
        # this function will record uninterpretable data
        def logAnomaly():
            for arg in [skel, record, key]:
                anomalyLog.writerow([key,skel[key],record[key]])        

        # skip if empty data, note that skeleton could be checked
        # before loop outside to improve speed
        if type(skel[key]) is str:
            if not skel[key]:
                return False

        # skip if empty data
        if type(record[key]) is str:
            if not record[key]:
                return False

        # Use error functions
        if (key in ['Age','d18O','Pb','Sr','DeathYr']):
            safe_dict['x'] = float(skel[key])
            delta = abs(float(eval(errorFunctions[key],{"__builtins__":None},safe_dict)))

        # Check if the skel and record data are in the acceptable values
        elif ({skel[key], record[key]} <= acceptableCategories[key]):
            # Any difference in category is a bad fit
            return skel[key] != record[key]
        
        else:
            # record unhandled data and don't reject the record
            logAnomaly()
            return False

        return (abs(float(skel[key]) - float(record[key])) > delta)
    
    # Input data filenames
    skeletonDataName = "skeleton-list.csv"
    patientDataName = "patient-list.csv"

    # Initialize dict lists
    skeletonData = []
    patientData = []

    class Skeleton:
        def __init__(self):
            self.data = {}
            self.records = []
            self.removed = {}
            self.remaining = {}

    def populate_lod(lod, csv_fp): # lod is "list of dicts"
        rdr = csv.DictReader(csv_fp)
        lod.extend(rdr)

    populate_lod(patientData, open(patientDataName))
    populate_lod(skeletonData, open(skeletonDataName))

    Closet = []
    numTotalRecords = len(patientData)

    for skelRow in skeletonData:
        numRemainingRecords = deepcopy(numTotalRecords)
        sk = Skeleton()
        sk.data = skelRow
        sk.records = deepcopy(patientData)
        # Now eliminate records one by one
        for label in sortOrder:
            popcount = 0
            i = 0
            while (i < len(sk.records)):
                if (isPoorFit(sk.data, sk.records[i], label)):
                    sk.records.pop(i)
                    i = i - 1
                    popcount = popcount + 1
                i = i + 1
            sk.removed[label] = popcount
            numRemainingRecords = numRemainingRecords - popcount
            sk.remaining[label] = deepcopy(numRemainingRecords)
        Closet.append(sk)

    # Generate counts table
    counts_fp = open(outDir + '/Counts_Table.csv', 'w')
    csvCounts = csv.writer(counts_fp)
    header = ['Grave ID']
    for label in sortOrder:
        header.extend([label, 'NoRecs'])
    csvCounts.writerow(header)

    for skeleton in Closet:
        row = [skeleton.data['OurNo']]
        for label in sortOrder:
            row.append(skeleton.data[label])
            row.append(skeleton.remaining[label])
        csvCounts.writerow(row)
    
    # Generate table of remaining records
    remain_fp = open(outDir + '/Remaining_Table.csv', 'w')
    csvRemain = csv.writer(remain_fp)
    for skeleton in Closet:
        csvRemain.writerow(skeleton.data.keys())
        csvRemain.writerow(skeleton.data.values())
        for recordNum, record in enumerate(skeleton.records):
            if (recordNum == 0):
                csvRemain.writerow(record.keys())
            csvRemain.writerow(record.values())
