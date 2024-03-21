import sys
import os
import time

logInitializeCSVFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWUserScriptInitialize.csv'
logAdjusterCSVFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWUserScriptAdjuster.csv'
logDistributionCSVFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWUserScriptDistribution.csv'
headerInitializeList = ['Name', 'Id']
headerAdjusterList = ['X', 'Y', 'Z', 'RX', 'RY', 'RZ', 'Tag', 'Val1', 'Val2', 'Val3', 'Val4', 'Val5', 'Level', 'Id']
headerDistributionList = ['X', 'Y', 'Z', 'q1', 'q2', 'q3', 'q4', 'Tag', 'Val1', 'Val2', 'Val3', 'Val4', 'Val5'
                          , 'Index', 'Type', 'Container', 'Layer', 'Group', 'State', 'Id']
strTab = ','

def WriteCSVLog(filePath, index, values):
    strLine = ''
    for value in values:
        strLine += str(value) + strTab
    strLine += time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()) + strTab + str(index)
    f = open(filePath, 'a')
    f.write(strLine + '\n')
    f.close()

def WriteCVSLogHeader(filePath, headerList):
    strLine = ''
    for key in headerList:
        strLine += key + strTab
    f = open(filePath,'a')
    f.write(strLine + 'Time,Index' + '\n')
    f.close()

def main(argv):
    """main

    """
    print("Run from main: ", argv)
    try:
        if (os.path.exists(logInitializeCSVFilePath) == False):
            WriteCVSLogHeader(logInitializeCSVFilePath, headerInitializeList)
        if (os.path.exists(logAdjusterCSVFilePath) == False):
            WriteCVSLogHeader(logAdjusterCSVFilePath, headerAdjusterList)
        if (os.path.exists(logDistributionCSVFilePath) == False):
            WriteCVSLogHeader(logDistributionCSVFilePath, headerDistributionList)
        values = ['Item_1', '3FB6A38A-967A-4370-ABF1-1FF69F99C6C0']
        WriteCSVLog(logInitializeCSVFilePath, 1, values)
        values = [1, 2, 3, 4, 5, 6, -1, 0, 0, 0, 0, 0, 2, '3FB6A38A-967A-4370-ABF1-1FF69F99C6C0']
        WriteCSVLog(logAdjusterCSVFilePath, 1, values)
        WriteCSVLog(logAdjusterCSVFilePath, 2, values)
        values = [1, 2, 3, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, '3FB6A38A-967A-4370-ABF1-1FF69F99C6C0']
        WriteCSVLog(logDistributionCSVFilePath, 1, values)

    except Exception:
        print("Error: ", sys.exc_info()[0])
        pass
    finally:
        print("Finally")
        pass
    

if __name__ == "__main__":
    main(sys.argv)
else:
    pass
