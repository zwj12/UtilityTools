"""PickMaster Twin User Script Sample: UserScriptSampleNumpy.py
"""

import os
import sys
import logging
import time
import copy
import traceback
import numpy
import cv2

RTType = 1
Item_1 = {'Name': 'Item_1', 'Id': '325D3EB5-B563-4F90-B0C5-2F1E770D5C04'}
Item_2 = {'Name': 'Item_2', 'Id': '9552BEFB-480E-42B3-96D1-9EA297506540'}
Container_1 = {'Name': 'Item_2', 'Id': '9552BEFB-480E-42B3-96D1-9EA297506540'}
Container_2 = {'Name': 'Item_2', 'Id': '9552BEFB-480E-42B3-96D1-9EA297506540'}
ConveyorWorkArea_1 = {'Name': 'Item_2', 'Id': '9552BEFB-480E-42B3-96D1-9EA297506540'}
ConveyorWorkArea_2 = {'Name': 'Item_2', 'Id': '9552BEFB-480E-42B3-96D1-9EA297506540'}
IndexedWorkArea_1 = {'Name': 'Item_2', 'Id': '9552BEFB-480E-42B3-96D1-9EA297506540'}
IndexedWorkArea_2 = {'Name': 'Item_2', 'Id': '9552BEFB-480E-42B3-96D1-9EA297506540'}


logFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWUserScript.log'
PyInitializeCounter = 0
PyAdjusterCounter = 0
PyDistributionCounter = 0
PyVisionCounter = 0
logInitializeCSVFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWUserScriptInitialize.csv'
logAdjusterCSVFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWUserScriptAdjuster.csv'
logDistributionCSVFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWUserScriptDistribution.csv'
logGeomatricCSVFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWUserScriptGeomatric.csv'
logBlobCSVFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWUserScriptBlob.csv'
logInspectionCSVFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWUserScriptInspection.csv'
headerInitializeList = ['Name', 'Id']
headerAdjusterList = ['X', 'Y', 'Z', 'RX', 'RY', 'RZ', 'Tag', 'Val1', 'Val2', 'Val3', 'Val4', 'Val5', 'Level', 'Id']
headerDistributionList = ['X', 'Y', 'Z', 'q1', 'q2', 'q3', 'q4', 'Tag', 'Val1', 'Val2', 'Val3', 'Val4', 'Val5', 'Index', 'Type', 'Container', 'Layer', 'Group', 'State', 'Id']
headerGeomatricList = ['X', 'Y', 'Z', 'RZ', 'SortValue', 'ZValid', 'XImgPos', 'YImgPos', 'Val1', 'Val2', 'Val3', 'Val4', 'Val5', 'Level', 'Id', 'ModelType', 'Score', 'XScale', 'YScale', 'Contrast', 'FitError', 'Coverage', 'Clutter']
headerBlobList = ['X', 'Y', 'Z', 'RZ', 'SortValue', 'ZValid', 'XImgPos', 'YImgPos', 'Val1', 'Val2', 'Val3', 'Val4', 'Val5', 'Level', 'Id', 'ModelType', 'Area', 'Perimeter', 'Elongation', 'Circularity']
headerInspectionList = ['X', 'Y', 'Z', 'RZ', 'SortValue', 'ZValid', 'XImgPos', 'YImgPos', 'Val1', 'Val2', 'Val3', 'Val4', 'Val5', 'Level', 'Id', 'ModelType']

strTab = ','

def get_logging():
    """get_logging

    """
    archiveAboveSize = 1024 * 1024 * 10
    if os.path.exists(logFilePath):
        if os.path.getsize(logFilePath) > 1024 * 1024 * 10:
            if os.path.exists(logFilePath + '.1'):
                os.remove(logFilePath + '.1')
            os.rename(logFilePath, logFilePath + '.1')
    else:
        os.makedirs(os.path.dirname(logFilePath), exist_ok=True)
    logger = logging.getLogger('PickMasterTwin')
    if logger.hasHandlers() == False:
        logger.setLevel(logging.DEBUG)
        # logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s:%(name)s:%(levelname)s:%(message)s')
        filehandler = logging.FileHandler(logFilePath)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
    return logger

def WriteCSVLog(filePath, index, values):
    strLine = ''
    for value in values:
        if type(value) == float:
            strLine += f"{value:.1f}" + strTab
        else:
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

def PyInitialize(type, itemInfo):
    """PyInitialize

    Keyword arguments:
    type -- This is the runtime type. It can be either 0 (representing VRT) or 1 (representing RRT).
    itemInfo -- Item information, example:
        {
            '0': {'Name': 'Item_1', 'Id': '325D3EB5-B563-4F90-B0C5-2F1E770D5C04'}, 
            '1': {'Name': 'Item_2', 'Id': '9552BEFB-480E-42B3-96D1-9EA297506540'}
        }
    """
    kwargs = locals()
    logger = get_logging()
    logger.debug(f"Call {sys._getframe().f_code.co_name}")
    logger.debug(f'kwargs = {kwargs}')
    NumPyTest()

    if (os.path.exists(logInitializeCSVFilePath) == False):
        WriteCVSLogHeader(logInitializeCSVFilePath, headerInitializeList)
    if (os.path.exists(logAdjusterCSVFilePath) == False):
        WriteCVSLogHeader(logAdjusterCSVFilePath, headerAdjusterList)
    if (os.path.exists(logDistributionCSVFilePath) == False):
        WriteCVSLogHeader(logDistributionCSVFilePath, headerDistributionList)
    if (os.path.exists(logGeomatricCSVFilePath) == False):
        WriteCVSLogHeader(logGeomatricCSVFilePath, headerGeomatricList)
    if (os.path.exists(logBlobCSVFilePath) == False):
        WriteCVSLogHeader(logBlobCSVFilePath, headerBlobList)
    if (os.path.exists(logInspectionCSVFilePath) == False):
        WriteCVSLogHeader(logInspectionCSVFilePath, headerInspectionList)

    global PyInitializeCounter
    global RTType
    global Item_1
    global Item_2
    global Container_1
    global Container_2
    global ConveyorWorkArea_1
    global ConveyorWorkArea_2
    global IndexedWorkArea_1
    global IndexedWorkArea_2
    PyInitializeCounter += 1
    logger.debug(f'PyInitializeCounter = {PyInitializeCounter}')
    RTType = type
    logger.debug(f'RTType = {RTType}')
    index = 0
    for item in itemInfo.values():
        if item["Name"] == 'Item_1':
            Item_1 = item
            logger.debug(f'Item_1 updated = {item}')
        if item["Name"] == 'Item_2':
            Item_2 = item
            logger.debug(f'Item_2 updated = {item}')
        elif item["Name"] == 'Container_1':
            Container_1 = item
            logger.debug(f'Container_1 updated = {item}')
        elif item["Name"] == 'Container_2':
            Container_2 = item
            logger.debug(f'Container_2 updated = {item}')
        elif item["Name"] == 'ConveyorWorkArea_1':
            ConveyorWorkArea_1 = item
            logger.debug(f'ConveyorWorkArea_1 updated = {item}')
        elif item["Name"] == 'ConveyorWorkArea_2':
            ConveyorWorkArea_2 = item
            logger.debug(f'ConveyorWorkArea_2 updated = {item}')
        elif item["Name"] == 'IndexedWorkArea_1':
            IndexedWorkArea_1 = item
            logger.debug(f'IndexedWorkArea_1 updated = {item}')
        elif item["Name"] == 'IndexedWorkArea_2':
            IndexedWorkArea_2 = item
            logger.debug(f'IndexedWorkArea_2 updated = {item}')
        values = item.values()
        index = index + 1
        WriteCSVLog(logInitializeCSVFilePath, index, values)

def PyAdjuster(items):
    """PyAdjuster

    Keyword arguments:
    items -- Item information, example:
        {'Time': 1702296806.51,
         '0': {'X': -97.5999984741211,
               'Y': -150.0,
               'Z': 0.0,
               'RX': 0.0,
               'RY': 0.0,
               'RZ': 0.0,
               'Tag': 0,
               'Val1': 0.0,
               'Val2': 0.0,
               'Val3': 0.0,
               'Val4': 0.0,
               'Val5': 0.0,
               'Level': 2,
               'Id': '5345941F-A17C-4F8A-80C8-D1CF5C7C1883'
               }
         }
    """
    kwargs = locals()
    logger = get_logging()
    logger.debug(f"Call {sys._getframe().f_code.co_name}")
    logger.debug(f'kwargs = {kwargs}')
    NumPyTest()

    global PyAdjusterCounter
    global RTType
    global Item_1
    global Item_2
    global Container_1
    global Container_2
    global ConveyorWorkArea_1
    global ConveyorWorkArea_2
    global IndexedWorkArea_1
    global IndexedWorkArea_2
    PyAdjusterCounter += 1
    logger.debug(f'PyAdjusterCounter = {PyAdjusterCounter}')

    # Modify item positions for test, can be ccommented out
    index = 0
    for key in items.keys():
        if key == 'Time':
            logger.debug(f'Time = {items[key]}')
        else:
            logger.debug(f'Input: {key} = {items[key]}')
            
            if RTType == 0:
                items[key]['Val1'] = 1
                items[key]['Val2'] = 2
                items[key]['Val3'] = 3
                items[key]['Val4'] = 4
                items[key]['Val5'] = 5
            else:
                items[key]['Val1'] = 5
                items[key]['Val2'] = 4
                items[key]['Val3'] = 3
                items[key]['Val4'] = 2
                items[key]['Val5'] = 1   

            if items[key]['Id'] == Item_1['Id']:
                items[key]['X'] = items[key]['X'] + 25
                items[key]['Y'] = items[key]['Y'] + 25
                # items[key]['Z'] = items[key]['Z'] + 25
                logger.debug(f'Adjust: {Item_1}') 
            elif items[key]['Id'] == Item_2['Id']:
                items[key]['X'] = items[key]['X'] + 25
                items[key]['Y'] = items[key]['Y'] + 25
                # items[key]['Z'] = items[key]['Z'] + 25
                logger.debug(f'Adjust: {Item_2}')

            logger.debug(f'Output: {key} = {items[key]}')

            values = items[key].values()
            index = index + 1
            WriteCSVLog(logAdjusterCSVFilePath, index, values)

    # Add a new item for test, can be commented out
    for key in items.keys():
        if key != 'Time' and items[key]['Id'] == Item_1['Id']:     
            newItem = copy.deepcopy(items[key])
            newItem['X'] = newItem['X'] + 100
            newItem['Y'] = newItem['Y'] - 100
            new_key = str(len(items) - 1)
            items[new_key] = newItem
            logger.debug(f'items = {items}')    
            break              

    # delete the first container for test, can be commented out
    # for key in items.keys():
    #     if key != 'Time' and items[key]['Id'] == Container_1['Id']:   
    #         del items[key]
    #         logger.debug(f'items = {items}')    
    #         break    

    return items

def PyVision(imageData, calibData, items):
    """PyVision

    Keyword arguments:
    imageData -- Image data, example:
        {'Width': 481,
         'Height': 409,
         'IsColor': 0,
         'Grey': [56,…,67],
         }

        {'Width': 481,
         'Height': 409,
         'IsColor': 1,
         'Blue': [56,…,67],
         'Green': [56,…,67],
         'Red': [56,…,67],
         }

    calibData -- Calibration data, example:
        {'UpperLeftX': -313,
         'UpperLeftY': -265,
         'LowerRightX': 168,
         'LowerRightY': 144,
         'XScale': 0.415,
         'YScale': 0.415
         }

    items -- Item information, example:
        Geomatric model:
        {'Time': 1702296806.51,
         '0': {'X': -97.5999984741211,
               'Y': -150.0,
               'Z': 0.0,
               'RZ': 0.0,
               'SortValue': 0.976,
               'ZValid': 0,
               'XImgPos': -80.1,
               'YImgPos': -77.2,
               'Val1': 0.0,
               'Val2': 0.0,
               'Val3': 0.0,
               'Val4': 0.0,
               'Val5': 0.0,
               'Level': 2,
               'Id': '5345941F-A17C-4F8A-80C8-D1CF5C7C1883',
               'ModelType': 1,
               'Score': 0.747174859046936,
               'XScale': 0.9995959997177124,
               'YScale': 0.9995959997177124,
               'Contrast': 12.289325714111328,
               'FitError': 0.36996814608573914,
               'Coverage': 0.747174859046936,
               'Clutter': 0.10466811060905457,               
               }
         }

        Blob model:
        {'Time': 1702296806.51,
         '0': {'X': -97.5999984741211,
               'Y': -150.0,
               'Z': 0.0,
               'RZ': 0.0,
               'SortValue': 0.976,
               'ZValid': 0,
               'XImgPos': -80.1,
               'YImgPos': -77.2,
               'Val1': 0.0,
               'Val2': 0.0,
               'Val3': 0.0,
               'Val4': 0.0,
               'Val5': 0.0,
               'Level': 2,
               'Id': '5345941F-A17C-4F8A-80C8-D1CF5C7C1883',
               'ModelType': 2,
               'Area': 0,
               'Perimeter': 0,
               'Elongation': 0,
               'Circularity': 0        
               }
         }

        Inspection model:
        {'Time': 1702296806.51,
         '0': {'X': -97.5999984741211,
               'Y': -150.0,
               'Z': 0.0,
               'RZ': 0.0,
               'SortValue': 0.976,
               'ZValid': 0,
               'XImgPos': -80.1,
               'YImgPos': -77.2,
               'Val1': 0.0,
               'Val2': 0.0,
               'Val3': 0.0,
               'Val4': 0.0,
               'Val5': 0.0,
               'Level': 2,
               'Id': '5345941F-A17C-4F8A-80C8-D1CF5C7C1883',
               'ModelType': 3   
               }
         }
    """
    kwargs = locals()
    logger = get_logging()
    logger.debug(f"Call {sys._getframe().f_code.co_name}")
    # logger.debug(f'kwargs = {kwargs}')

    global PyVisionCounter
    global RTType
    global Item_1
    global Item_2
    global Container_1
    global Container_2
    global ConveyorWorkArea_1
    global ConveyorWorkArea_2
    global IndexedWorkArea_1
    global IndexedWorkArea_2
    PyVisionCounter += 1
    logger.debug(f'PyVisionCounter = {PyVisionCounter}')

    imageDataTemp = copy.deepcopy(imageData)
    if imageDataTemp['IsColor'] == 0:
         imageDataTemp['Grey'] = len(imageData['Grey'])
    else:   
        imageDataTemp['Blue'] = len(imageData['Blue'])
        imageDataTemp['Green'] = len(imageData['Green'])  
        imageDataTemp['Red'] = len(imageData['Red'])

    logger.debug(f'imageData = {imageDataTemp}')
    logger.debug(f'calibData = {calibData}')

    index = 0
    keys = items.keys()
    for key in keys:
        if key == 'Time':
            logger.debug(f'Time = {items[key]}')
        else:
            logger.debug(f'Input: {key} = {items[key]}')

            if items[key]['ModelType'] == 1:
                # Geometric model
                if items[key]["Score"] < 0.7 :
                    items[key]['Level'] = 0
                    logger.debug(f'Adjust: {items[key]}')
            elif items[key]['ModelType'] == 2:
                # Blob model
                if items[key]["Perimeter"] < 1000:
                    items[key]['Level'] = 0
                    logger.debug(f'Adjust: {items[key]}')
            else:
                # Inspection model
                if items[key]['Id'] == Item_1['Id']:
                    items[key]['X'] = items[key]['X'] + 25
                    items[key]['Y'] = items[key]['Y'] + 25
                    # items[key]['Z'] = items[key]['Z'] + 25
                    logger.debug(f'Adjust: {items[key]}')

            logger.debug(f'Output: {key} = {items[key]}')

            values = items[key].values()
            index = index + 1
            if items[key]['ModelType'] == 1:
                WriteCSVLog(logGeomatricCSVFilePath, index, values)
            elif items[key]['ModelType'] == 2:
                WriteCSVLog(logBlobCSVFilePath, index, values)
            elif items[key]['ModelType'] == 3:
                WriteCSVLog(logInspectionCSVFilePath, index, values)

    return items

def PyDistribution(WaId, items):
    """PyDistribution

    Keyword arguments:
    WaId -- Workarea ID, exaple: '3F8AE17B-C16C-4FE9-9DF5-C2D14ED1BC07'
    items -- Item information, example:
        {'Time': 1702301071.989,
         '0': {'X': -72.5999984741211,
               'Y': -125.0,
               'Z': 5.0,
               'q1': 0.0,
               'q2': 1.0,
               'q3': 0.0,
               'q4': 0.0,
               'Tag': 0,
               'Val1': 0.0,
               'Val2': 0.0,
               'Val3': 0.0,
               'Val4': 0.0,
               'Val5': 0.0,
               'Index': 26,
               'Type': 0,
               'Container': 0,
               'Layer': 0,
               'Group': 0,
               'State': 0,
               'Id': '346563A7-F607-4D65-8DFD-D53AB615EDA8'
               }
         }
    """
    kwargs = locals()
    logger = get_logging()
    logger.debug(f"Call {sys._getframe().f_code.co_name}")
    logger.debug(f'kwargs = {kwargs}')
    NumPyTest()

    global PyDistributionCounter
    global RTType
    global Item_1
    global Item_2
    global Container_1
    global Container_2
    global ConveyorWorkArea_1
    global ConveyorWorkArea_2
    global IndexedWorkArea_1
    global IndexedWorkArea_2
    PyDistributionCounter += 1
    logger.debug(f'PyDistributionCounter = {PyDistributionCounter}')

    logger.debug(f'WaId = {WaId}')

    index = 0
    keys = items.keys()
    for key in keys:
        if key == 'Time':
            logger.debug(f'Time = {items[key]}')
        else:
            logger.debug(f'Input: {key} = {items[key]}')

            if RTType == 0:
                if items[key]['Id'] == Item_1['Id']:
                    items[key]['X'] = items[key]['X'] + 25
                    items[key]['Y'] = items[key]['Y'] + 25
                    # items[key]['Z'] = items[key]['Z'] + 25
                    logger.debug(f'Adjust: {Item_1}')
            else:
                if items[key]['Id'] == Item_2['Id']:
                    items[key]['X'] = items[key]['X'] + 25
                    items[key]['Y'] = items[key]['Y'] + 25
                    # items[key]['Z'] = items[key]['Z'] + 25
                    logger.debug(f'Adjust: {Item_2}')

            logger.debug(f'Output: {key} = {items[key]}')

            values = items[key].values()
            index = index + 1
            WriteCSVLog(logDistributionCSVFilePath, index, values)

    return items

def multiply(a,b):
    print("Will compute", a, "times", b)
    NumPyTest()
    c = 0
    for i in range(0, a):
        c = c + b
    return c


def NumPyTest():
    a = numpy.array([[1,1],[0,1]])
    b = numpy.array([[2,0],[3,4]])
    c = a * b
    logger = get_logging()
    logger.debug(f'Call numpy: a * b = {c}')
    logger.debug(cv2.__name__)


def main(argv):
    """main

    """
    print("Run from main: ", argv)
    multiply(2,3)
    try:
        logger = get_logging()
        logger.debug(argv)
        type = 0
        Item1_Id = '325D3EB5-B563-4F90-B0C5-2F1E770D5C04'
        Item2_Id = '9552BEFB-480E-42B3-96D1-9EA297506540'
        itemsInitialize = {
            '0': {'Name': 'Item_1', 'Id': Item1_Id},
            '1': {'Name': 'Item_2', 'Id': Item2_Id},
        }
        PyInitialize(type, itemsInitialize)

        itemsAdjuster = {'Time': 1702296806.51,
                 '0': {'X': -97.5999984741211,
                       'Y': -150.0,
                       'Z': 0.0,
                       'RX': 0.0,
                       'RY': 0.0,
                       'RZ': 0.0,
                       'Tag': 0,
                       'Val1': 0.0,
                       'Val2': 0.0,
                       'Val3': 0.0,
                       'Val4': 0.0,
                       'Val5': 0.0,
                       'Level': 2,
                       'Id': Item1_Id
                       }
                 }
        PyAdjuster(itemsAdjuster)

        imageDataGreyVision = {'Width': 481,
                           'Height': 409,
                           'IsColor': 0,
                           'Grey': [56,57,67],
                           }        
        imageDataColorVision = {'Width': 481,
                                'Height': 409,
                                'IsColor': 1,
                                'Blue': [56,57,67],
                                'Green': [56,57,67],
                                'Red': [56,57,67],
                                }
        calibDataVision = {'UpperLeftX': -313,
                           'UpperLeftY': -265,
                           'LowerRightX': 168,
                           'LowerRightY': 144,
                           'XScale': 0.415,
                           'YScale': 0.415,
                           }        
        itemsGeometricVision = {'Time': 1702301071.989,
                                 '0' : {'X': -97.5999984741211,
                                        'Y': -150.0,
                                        'Z': 0.0,
                                        'RZ': 0.0,
                                        'SortValue': 0.976,
                                        'ZValid': 0,
                                        'XImgPos': -80.1,
                                        'YImgPos': -77.2,
                                        'Val1': 0.0,
                                        'Val2': 0.0,
                                        'Val3': 0.0,
                                        'Val4': 0.0,
                                        'Val5': 0.0,
                                        'Level': 2,
                                        'Id': Item1_Id,
                                        'ModelType': 1,
                                        'Score': 0.747174859046936,
                                        'XScale': 0.9995959997177124,
                                        'YScale': 0.9995959997177124,
                                        'Contrast': 12.289325714111328,
                                        'FitError': 0.36996814608573914,
                                        'Coverage': 0.747174859046936,
                                        'Clutter': 0.10466811060905457,
                                        },
                                    }
        itemsBlobVision = {'Time': 1702301071.989,
                                 '0' : {'X': -97.5999984741211,
                                        'Y': -150.0,
                                        'Z': 0.0,
                                        'RZ': 0.0,
                                        'SortValue': 0.976,
                                        'ZValid': 0,
                                        'XImgPos': -80.1,
                                        'YImgPos': -77.2,
                                        'Val1': 0.0,
                                        'Val2': 0.0,
                                        'Val3': 0.0,
                                        'Val4': 0.0,
                                        'Val5': 0.0,
                                        'Level': 2,
                                        'Id': Item1_Id,
                                        'ModelType': 2,
                                        'Area': 0,
                                        'Perimeter': 0,
                                        'Elongation': 0,
                                        'Circularity': 0  
                                        },
                                    } 
        itemsInspectionVision = {'Time': 1702301071.989,
                                 '0' : {'X': -97.5999984741211,
                                        'Y': -150.0,
                                        'Z': 0.0,
                                        'RZ': 0.0,
                                        'SortValue': 0.976,
                                        'ZValid': 0,
                                        'XImgPos': -80.1,
                                        'YImgPos': -77.2,
                                        'Val1': 0.0,
                                        'Val2': 0.0,
                                        'Val3': 0.0,
                                        'Val4': 0.0,
                                        'Val5': 0.0,
                                        'Level': 2,
                                        'Id': Item1_Id,
                                        'ModelType': 3,
                                        },
                                    } 
        PyVision(imageDataGreyVision,calibDataVision,itemsGeometricVision)
        PyVision(imageDataGreyVision,calibDataVision,itemsBlobVision)
        PyVision(imageDataGreyVision,calibDataVision,itemsInspectionVision)
        PyVision(imageDataColorVision,calibDataVision,itemsGeometricVision)
        PyVision(imageDataColorVision,calibDataVision,itemsBlobVision)
        PyVision(imageDataColorVision,calibDataVision,itemsInspectionVision)

        logger.debug("PyDistribution in main")
        WaId = '3F8AE17B-C16C-4FE9-9DF5-C2D14ED1BC07'
        itemsDistribution = {'Time': 1702301071.989,
                             '0': {'X': -72.5999984741211,
                                   'Y': -125.0,
                                   'Z': 5.0,
                                   'q1': 0.0,
                                   'q2': 1.0,
                                   'q3': 0.0,
                                   'q4': 0.0,
                                   'Tag': 0,
                                   'Val1': 0.0,
                                   'Val2': 0.0,
                                   'Val3': 0.0,
                                   'Val4': 0.0,
                                   'Val5': 0.0,
                                   'Index': 26,
                                   'Type': 0,
                                   'Container': 0,
                                   'Layer': 0,
                                   'Group': 0,
                                   'State': 0,
                                   'Id': Item1_Id
                                   }
                             }
        PyDistribution(WaId, itemsDistribution)

    except Exception:
        print("Error: ", sys.exc_info()[0])
        traceback.print_exc()
        pass
    finally:
        print("Finally")
        pass


if __name__ == "__main__":
    main(sys.argv)
else:
    pass
