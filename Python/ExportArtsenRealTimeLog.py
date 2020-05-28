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
regularCorrectionLimit = regularTime + r'.*Limit correction to.*: ([0-9.-]+)'
regularCurrentR = regularTime + r'.*Current on Right.*: ([0-9]+)'
regularCurrentL = regularTime + r'.*Current on Left.*: ([0-9]+)'
regularDifference = regularTime + r'.*Difference.*: ([0-9-]+)'
regularZReference = regularTime + r'.*Z-Reference.*: ([0-9.]+)'
regularZMeasured = regularTime + r'.*Z-Measured.*: ([0-9]+)'
regularYZCorrectionLimit = regularTime + r'.*(Y|Z)-Correction.*Limit'

regularAccumulated = regularTime + r'.*Accumulated corrections'
regularTotalY = regularTime + r'.*Total Corrections Y: ([0-9.-]+)'
regularTotalZ = regularTime + r'.*Total Corrections Z: ([0-9.-]+)'
regularCalculatedZ = regularTime + r'.*Calculated Z-Reference.*: ([0-9.]+)'
regularNumberLeft = regularTime + r'.*Number of Left.*: ([0-9]+)'
regularNumberRight = regularTime + r'.*Number of right.*: ([0-9]+)'
regularNumberCenter = regularTime + r'.*Number of Center.*: ([0-9]+)'

regularActiveTrackdata = regularTime + r'.*Active trackdata'
regularTracksystem = regularTime + r'.*Tracksystem.*: ([0-9]+)'
regularSeamName = regularTime + r'.*SeamName.*: (.*)$'
regularTrackType = regularTime + r'.*TrackType.*: (.*)$'
regularGainY = regularTime + r'.*Gain_y.*: ([0-9]+)'
regularGainZ = regularTime + r'.*Gain_z.*: ([0-9]+)'
regularBias = regularTime + r'.*Bias.*: ([0-9.-]+)'
regularWeaveTime = regularTime + r'.*Weave time.*: ([0-9.]+)'


strLogFileName = "Artsen_RealTimeLog_ROB1.log"
fileLog = open(strLogFileName)
YZCorrectionList = []

while True:
    strLine = fileLog.readline()
    if not strLine:
        break

    matchYZCorrection = re.search(regularYZCorrectionLimit, strLine, re.I)
    if matchYZCorrection:
        YZCorrection = {}
        YZCorrection["time"] = matchYZCorrection.group(1)
        YZCorrection["YZ"] = matchYZCorrection.group(2) + ' Limit'

        if YZCorrection["YZ"] == "Y Limit":
            strLineTrap = fileLog.readline()
            strLineMeasurements = fileLog.readline()            
            strLineCorrection = fileLog.readline()
            strLineCorrectionLimit = fileLog.readline()
            strLineDifference = fileLog.readline()
            strLineCurrentR = fileLog.readline()
            strLineCurrentL = fileLog.readline()
                        
            matchTrap = re.search(regularTrap, strLineTrap, re.I)
            matchMeasurements = re.search(regularMeasurements, strLineMeasurements, re.I)
            matchCorrection = re.search(regularCorrection, strLineCorrection, re.I)
            matchCorrectionLimit = re.search(regularCorrectionLimit, strLineCorrectionLimit, re.I)
            matchCurrentR = re.search(regularCurrentR, strLineCurrentR, re.I)
            matchCurrentL = re.search(regularCurrentL, strLineCurrentL, re.I)
            matchDifference = re.search(regularDifference, strLineDifference, re.I)

            if matchTrap and matchMeasurements and matchCorrection and matchCorrectionLimit and matchCurrentR and matchCurrentL and matchDifference:
                YZCorrection["Trap"] = matchTrap.group(2)
                YZCorrection["Measurements"] = matchMeasurements.group(2)
                YZCorrection["Correction"] = matchCorrection.group(2)
                YZCorrection["CorrectionLimit"] = matchCorrectionLimit.group(2)
                YZCorrection["CurrentR"] = matchCurrentR.group(2)
                YZCorrection["CurrentL"] = matchCurrentL.group(2)
                YZCorrection["Difference"] = matchDifference.group(2)
                YZCorrection["ZReference"] = "0"
                YZCorrection["ZMeasured"] = "0"
                
                YZCorrectionList.append(YZCorrection)
                
        elif YZCorrection["YZ"] == "Z Limit":
            strLineMeasurements = fileLog.readline()
            strLineCorrection = fileLog.readline()
            strLineCorrectionLimit = fileLog.readline()
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
            matchCorrectionLimit = re.search(regularCorrectionLimit, strLineCorrectionLimit, re.I)
            matchZReference = re.search(regularZReference, strLineZReference, re.I)
            matchZMeasured = re.search(regularZMeasured, strLineZMeasured, re.I)
            matchDifference = re.search(regularDifference, strLineDifference, re.I)

            if matchMeasurements and matchCorrection and matchCorrectionLimit and matchZReference and matchZMeasured and matchDifference:
                YZCorrection["Measurements"] = matchMeasurements.group(2)
                YZCorrection["Correction"] = matchCorrection.group(2)
                YZCorrection["CorrectionLimit"] = matchCorrectionLimit.group(2)
                YZCorrection["ZReference"] = matchZReference.group(2)
                YZCorrection["ZMeasured"] = matchZMeasured.group(2)
                YZCorrection["Difference"] = matchDifference.group(2)
                YZCorrection["Trap"] = ""
                YZCorrection["CurrentR"] = "0"
                YZCorrection["CurrentL"] = "0"
                
                YZCorrectionList.append(YZCorrection)
        continue

                
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
                YZCorrection["CorrectionLimit"] = "0"
                
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
                YZCorrection["CorrectionLimit"] = "0"
                
                YZCorrectionList.append(YZCorrection)      

        continue

    matchYZCorrection = re.search(regularAccumulated, strLine, re.I)
    if matchYZCorrection:
        YZCorrection = {}
        YZCorrection["time"] = matchYZCorrection.group(1)
        YZCorrection["YZ"] = "Accumulated"
        strLineTotalY = fileLog.readline()
        strLineTotalZ = fileLog.readline()
        strLineEmpty = fileLog.readline()
        strLineCalculatedZ = fileLog.readline()
        strLineNumberLeft = fileLog.readline()
        strLineNumberRight = fileLog.readline()
        strLineNumberCenter = fileLog.readline()
        
        matchTotalY = re.search(regularTotalY, strLineTotalY, re.I)
        matchTotalZ = re.search(regularTotalZ, strLineTotalZ, re.I)
        matchCalculatedZ = re.search(regularCalculatedZ, strLineCalculatedZ, re.I)
        matchNumberLeft = re.search(regularNumberLeft, strLineNumberLeft, re.I)
        matchNumberRight = re.search(regularNumberRight, strLineNumberRight, re.I)
        matchNumberCenter = re.search(regularNumberCenter, strLineNumberCenter, re.I)

        if matchTotalY and matchTotalZ and matchCalculatedZ and matchNumberLeft and matchNumberRight and matchNumberCenter:
            YZCorrection["TotalY"] = matchTotalY.group(2)
            YZCorrection["TotalZ"] = matchTotalZ.group(2)
            YZCorrection["CalculatedZ"] = matchCalculatedZ.group(2)
            YZCorrection["NumberLeft"] = matchNumberLeft.group(2)
            YZCorrection["NumberRight"] = matchNumberRight.group(2)
            YZCorrection["NumberCenter"] = matchNumberCenter.group(2)
            
            YZCorrectionList.append(YZCorrection)   
        continue

    matchYZCorrection = re.search(regularActiveTrackdata, strLine, re.I)
    if matchYZCorrection:        
        YZCorrection = {}
        YZCorrection["time"] = matchYZCorrection.group(1)
        YZCorrection["YZ"] = "ActiveTrackdata"
        strLineTracksystem = fileLog.readline()
        strLineSeamName = fileLog.readline()
        strLineTrackType = fileLog.readline()
        strLineGainY = fileLog.readline()
        strLineGainZ = fileLog.readline()
        strLineBias = fileLog.readline()
        strLineZReference = fileLog.readline()
        strLineWeaveTime = fileLog.readline()
        
        matchTracksystem = re.search(regularTracksystem, strLineTracksystem, re.I)
        matchSeamName = re.search(regularSeamName, strLineSeamName, re.I)
        matchTrackType = re.search(regularTrackType, strLineTrackType, re.I)
        matchGainY = re.search(regularGainY, strLineGainY, re.I)
        matchGainZ = re.search(regularGainZ, strLineGainZ, re.I)
        matchBias = re.search(regularBias, strLineBias, re.I)
        matchZReference = re.search(regularZReference, strLineZReference, re.I)
        matchWeaveTime = re.search(regularWeaveTime, strLineWeaveTime, re.I)
                    
        if matchTracksystem and matchSeamName and matchTrackType and matchGainY and matchGainZ and matchBias and matchZReference and matchWeaveTime:

            YZCorrection["Tracksystem"] = matchTracksystem.group(2)
            YZCorrection["SeamName"] = matchSeamName.group(2)
            YZCorrection["TrackType"] = matchTrackType.group(2)
            YZCorrection["GainY"] = matchGainY.group(2)
            YZCorrection["GainZ"] = matchGainZ.group(2)
            YZCorrection["Bias"] = matchBias.group(2)
            YZCorrection["ZReference"] = matchZReference.group(2)
            YZCorrection["WeaveTime"] = matchWeaveTime.group(2)
            
            YZCorrectionList.append(YZCorrection)   
        continue
    

fileLog.close()

fileLogCSV_Y = open('Artsen_RealTimeLog_ROB1_Y.csv', 'w')
fileLogCSV_Z = open('Artsen_RealTimeLog_ROB1_Z.csv', 'w')
strLine = 'time,index,YZ,Trap,Measurements,Correction,CorrectionLimit,CurrentR,CurrentL,ZReference,ZMeasured,Difference\n'
fileLogCSV_Y.write(strLine)
fileLogCSV_Z.write(strLine)

index = 0
for YZCorrection in YZCorrectionList:
##    print (YZCorrection)
    index = index + 1
    if YZCorrection["YZ"] == "Y" or YZCorrection["YZ"] == "Y Limit":
        strLine = YZCorrection["time"] + ',' + str(index) + ',' + YZCorrection["YZ"] + ',' + YZCorrection["Trap"] + ',' + YZCorrection["Measurements"]
        strLine = strLine + ',' + YZCorrection["Correction"]+ ',' + YZCorrection["CorrectionLimit"] + ',' + YZCorrection["CurrentR"] + ',' + YZCorrection["CurrentL"]
        strLine = strLine + ',' + YZCorrection["ZReference"] + ',' + YZCorrection["ZMeasured"] + ',' + YZCorrection["Difference"]
        fileLogCSV_Y.write(strLine + "\n")
        
    elif YZCorrection["YZ"] == "Z" or YZCorrection["YZ"] == "Z Limit":
        strLine = YZCorrection["time"] + ',' + str(index) + ',' + YZCorrection["YZ"] + ',' + YZCorrection["Trap"] + ',' + YZCorrection["Measurements"]
        strLine = strLine + ',' + YZCorrection["Correction"]+ ',' + YZCorrection["CorrectionLimit"] + ',' + YZCorrection["CurrentR"] + ',' + YZCorrection["CurrentL"]
        strLine = strLine + ',' + YZCorrection["ZReference"] + ',' + YZCorrection["ZMeasured"] + ',' + YZCorrection["Difference"]
        fileLogCSV_Z.write(strLine + "\n")        

    elif YZCorrection["YZ"] == "ActiveTrackdata":
        index = 0
        strLine = YZCorrection["time"] + ',' + '' + ',' + YZCorrection["YZ"]+ "\n"
        strLine =strLine+ ',,SeamName,,,' + YZCorrection["SeamName"]+ "\n"
        strLine =strLine+ ',,TrackType,,,' + YZCorrection["TrackType"]+ "\n"
        strLine =strLine+ ',,Gain_y,,,' + YZCorrection["GainY"]+ "\n"
        strLine =strLine+ ',,Gain_z,,,' + YZCorrection["GainZ"]+ "\n"
        strLine =strLine+ ',,Bias,,,' + YZCorrection["Bias"]+ "\n"
        strLine =strLine+ ',,Z-Reference,,,' + YZCorrection["ZReference"]+ "\n"
        strLine =strLine+ ',,WeaveTime,,,' + YZCorrection["WeaveTime"]+ "\n"
        fileLogCSV_Y.write( strLine)
        fileLogCSV_Z.write(strLine)  
        
    elif YZCorrection["YZ"] == "Accumulated":
        strLine = YZCorrection["time"] + ',' + '' + ',' + YZCorrection["YZ"]+ "\n"
        strLine =strLine+ ',,TotalY,,,' + YZCorrection["TotalY"]+ "\n"
        strLine =strLine+ ',,TotalZ,,,' + YZCorrection["TotalZ"]+ "\n"
        strLine =strLine+ ',,CalculatedZ,,,' + YZCorrection["CalculatedZ"]+ "\n"
        strLine =strLine+ ',,NumberLeft,,,' + YZCorrection["NumberLeft"]+ "\n"
        strLine =strLine+ ',,NumberRight,,,' + YZCorrection["NumberRight"]+ "\n"
        strLine =strLine+ ',,NumberCenter,,,' + YZCorrection["NumberCenter"]+ "\n"
        fileLogCSV_Y.write( strLine)
        fileLogCSV_Z.write(strLine)  


            
fileLogCSV_Y.close()
fileLogCSV_Z.close()

input("Press any key to exit")
