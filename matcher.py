#!/usr/bin/python

import csv
from copy import deepcopy

# Define defaults

SORT_ORDER = ['Age','d18O','Pb','Sr','DeathYr','Sex','Race']
ERROR_RANGES = {
    'Age': 0.2, # percentage
    'd18O': 0.1, # percentage
    'DeathYr': 2, # range
    'Pb': 0.03, # percentage
    'Sr': 0.01 # percentage
}

def matcher(sortOrder=SORT_ORDER, errorRanges=ERROR_RANGES):

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

        # For percentage range
        if (key in ['Age','d18O','Pb','Sr']):
            delta = float(skel[key]) * errorRanges[key]
        # For absolute range
        elif (key in ['DeathYr']):
            delta = errorRanges[key]
        # Check if the skel and record data are in the acceptable values
        elif ({skel[key], record[key]} <= acceptableCategories[key]):
            # Any difference in category is a bad fit
            return skel[key] != record[key]
        else:
            # record unhandled data and don't reject the record
            logAnomaly()
            return False
        return (abs(float(skel[key]) - float(record[key])) > delta)
        
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
            for (i, row) in enumerate(sk.records):
                if (isPoorFit(sk.data, row, label)):
                    sk.records.pop(i)
                    popcount = popcount + 1
            sk.removed[label] = popcount
            numRemainingRecords = numRemainingRecords - popcount
            sk.remaining[label] = deepcopy(numRemainingRecords)
        Closet.append(sk)

    # Generate counts table
    counts_fp = open('Counts_Table.csv', 'w')
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
    remain_fp = open('Remaining_Table.csv', 'w')
    csvRemain = csv.writer(remain_fp)
    for skeleton in Closet:
        csvRemain.writerow(['Grave Id',skeleton.data['OurNo']])
        header = skeleton.records[0].keys()
        csvRemain.writerow(header)
        for record in skeleton.records:
            csvRemain.writerow(record.values())
