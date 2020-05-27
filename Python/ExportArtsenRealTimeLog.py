#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020-4-15
# @Author  : Michael

import re

regularTime = r'([0-9]{2}:[0-9]{2}:[0-9]{2})'
regularYZCorrection = regularTime + r'.*(Y|Z)-Correction'
regularTrap = regularTime + r' Trap on ((left)|(right)) side'
regularMeasurements = regularTime + r'.*Measurements.*: ([0-9]+)'
regularCorrection = regularTime + r'.*correction.*: ([0-9.-]+)'
regularCurrentR = regularTime + r'.*Current on Right.*: ([0-9]+)'
regularCurrentL = regularTime + r'.*Current on Left.*: ([0-9]+)'
regularDifference = regularTime + r'.*Difference.*: ([0-9-]+)'
regularZReference = regularTime + r'.*Z-Reference.*: ([0-9]+)'
regularZMeasured = regularTime + r'.*Z-Measured.*: ([0-9]+)'

strLogFileName = "Artsen_RealTimeLog_ROB1.log"
fileLog = open(strLogFileName)
YZCorrectionList = []

while True:
    strLine = fileLog.readline()
    if not strLine:
        break
    
    matchYZCorrection = re.search(regularYZCorrection, strLine, re.I)
    if matchYZCorrection:
        YZCorrection = {}
        YZCorrection["time"] = matchYZCorrection.group(1)
        YZCorrection["YZ"] = matchYZCorrection.group(2)

        if YZCorrection["YZ"] == "Y":
            strLineTrap = fileLog.readline()
            strLineMeasurements = fileLog.readline()
            strLineCorrection = fileLog.readline()
            strLineCurrentR = fileLog.readline()
            strLineCurrentL = fileLog.readline()
            strLineDifference = fileLog.readline()
##            print (strLineTrap)
##            print (strLineMeasurements)
##            print (strLineCorrection)
##            print (strLineCurrentR)
##            print (strLineCurrentL)
##            print (strLineDifference)
            
            matchTrap = re.search(regularTrap, strLineTrap, re.I)
            matchMeasurements = re.search(regularMeasurements, strLineMeasurements, re.I)
            matchCorrection = re.search(regularCorrection, strLineCorrection, re.I)
            matchCurrentR = re.search(regularCurrentR, strLineCurrentR, re.I)
            matchCurrentL = re.search(regularCurrentL, strLineCurrentL, re.I)
            matchDifference = re.search(regularDifference, strLineDifference, re.I)

            if matchTrap and matchMeasurements and matchCorrection and matchCurrentR and matchCurrentL and matchDifference:
                YZCorrection["Trap"] = matchTrap.group(2)
                YZCorrection["Measurements"] = matchMeasurements.group(2)
                YZCorrection["Correction"] = matchCorrection.group(2)
                YZCorrection["CurrentR"] = matchCurrentR.group(2)
                YZCorrection["CurrentL"] = matchCurrentL.group(2)
                YZCorrection["Difference"] = matchDifference.group(2)
                YZCorrection["ZReference"] = "0"
                YZCorrection["ZMeasured"] = "0"
                
                YZCorrectionList.append(YZCorrection)
                
        elif YZCorrection["YZ"] == "Z":
            strLineMeasurements = fileLog.readline()
            strLineCorrection = fileLog.readline()
            strLineZReference = fileLog.readline()
            strLineZMeasured = fileLog.readline()
            strLineDifference = fileLog.readline()
##            print (strLineMeasurements)
##            print (strLineCorrection)
##            print (strLineZReference)
##            print (strLineZMeasured)
##            print (strLineDifference)
            
            matchMeasurements = re.search(regularMeasurements, strLineMeasurements, re.I)
            matchCorrection = re.search(regularCorrection, strLineCorrection, re.I)
            matchZReference = re.search(regularZReference, strLineZReference, re.I)
            matchZMeasured = re.search(regularZMeasured, strLineZMeasured, re.I)
            matchDifference = re.search(regularDifference, strLineDifference, re.I)

            if matchMeasurements and matchCorrection and matchZReference and matchZMeasured and matchDifference:
                YZCorrection["Measurements"] = matchMeasurements.group(2)
                YZCorrection["Correction"] = matchCorrection.group(2)
                YZCorrection["ZReference"] = matchZReference.group(2)
                YZCorrection["ZMeasured"] = matchZMeasured.group(2)
                YZCorrection["Difference"] = matchDifference.group(2)
                YZCorrection["Trap"] = ""
                YZCorrection["CurrentR"] = "0"
                YZCorrection["CurrentL"] = "0"
                
                YZCorrectionList.append(YZCorrection)       

        
fileLog.close()

fileLogCSV = open('Artsen_RealTimeLog_ROB1.csv', 'w')
strLine = 'time,index,YZ,Trap,Measurements,Correction,CurrentR,CurrentL,ZReference,ZMeasured,Difference\n'
fileLogCSV.write(strLine)

index = 0
for YZCorrection in YZCorrectionList:
##    print (YZCorrection)
    index = index + 1
    if YZCorrection["YZ"] == "Y":
        strLine = YZCorrection["time"] + ',' + str(index) + ',' + YZCorrection["YZ"] + ',' + YZCorrection["Trap"] + ',' + YZCorrection["Measurements"]
        strLine = strLine + ',' + YZCorrection["Correction"] + ',' + YZCorrection["CurrentR"] + ',' + YZCorrection["CurrentL"]
        strLine = strLine + ',' + YZCorrection["ZReference"] + ',' + YZCorrection["ZMeasured"] + ',' + YZCorrection["Difference"]
        fileLogCSV.write(strLine + "\n")
        
    elif YZCorrection["YZ"] == "Z":
        strLine = YZCorrection["time"] + ',' + str(index) + ',' + YZCorrection["YZ"] + ',' + YZCorrection["Trap"] + ',' + YZCorrection["Measurements"]
        strLine = strLine + ',' + YZCorrection["Correction"] + ',' + YZCorrection["CurrentR"] + ',' + YZCorrection["CurrentL"]
        strLine = strLine + ',' + YZCorrection["ZReference"] + ',' + YZCorrection["ZMeasured"] + ',' + YZCorrection["Difference"]
        fileLogCSV.write(strLine + "\n")        

fileLogCSV.close()

input("Press any key to exit")
