"""PickMaster Twin User Script Sample: UserScriptSample.py
"""

import os
import sys
import logging


RTType = 1
itemA = {'Name': 'Item_1', 'Id': '325D3EB5-B563-4F90-B0C5-2F1E770D5C04'}
itemB = {'Name': 'Item_2', 'Id': '9552BEFB-480E-42B3-96D1-9EA297506540'}
logFilePath = r'C:\ProgramData\ABB\PickMaster Twin 2\PickMaster Twin Runtime 2\PickMaster Runtime\Log\PMTWUserScript.log'
PyInitializeCounter = 0
PyAdjusterCounter = 0
PyDistributionCounter = 0
PyVisionCounter = 0

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

    global PyInitializeCounter
    global RTType
    global itemA
    global itemB
    PyInitializeCounter += 1
    logger.debug(f'PyInitializeCounter = {PyInitializeCounter}')
    RTType = type
    logger.debug(f'RTType = {RTType}')
    items_list = list(itemInfo.items())
    if len(items_list) > 0:
        itemA = items_list[0][1]
        logger.debug(f'itemA = {itemA}')
    if len(items_list) > 1:
        itemB = items_list[1][1]
        logger.debug(f'itemB = {itemB}')    


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

    global PyAdjusterCounter
    global RTType
    global itemA
    global itemB
    PyAdjusterCounter += 1
    logger.debug(f'PyAdjusterCounter = {PyAdjusterCounter}')

    for key in items.keys():
        if key == 'Time':
            logger.debug(f'Time = {items[key]}')
        else:
            logger.debug(f'Input: {key} = {items[key]}')

            if RTType == 0:
                if items[key]['Id'] == itemA['Id']:
                    items[key]['X'] = items[key]['X'] + 25
                    items[key]['Y'] = items[key]['Y'] + 25
                    # items[key]['Z'] = items[key]['Z'] + 25
                    logger.debug(f'Adjust: {itemA}')
            else:
                if items[key]['Id'] == itemB['Id']:
                    items[key]['X'] = items[key]['X'] + 25
                    items[key]['Y'] = items[key]['Y'] + 25
                    # items[key]['Z'] = items[key]['Z'] + 25
                    logger.debug(f'Adjust: {itemB}')

            logger.debug(f'Output: {key} = {items[key]}')

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
    logger.debug(f'kwargs = {kwargs}')

    global PyVisionCounter
    global RTType
    global itemA
    global itemB
    PyVisionCounter += 1
    logger.debug(f'PyVisionCounter = {PyVisionCounter}')

    logger.debug(f'imageData = {imageData}')
    logger.debug(f'calibData = {calibData}')

    keys = items.keys()
    for key in keys:
        if key == 'Time':
            logger.debug(f'Time = {items[key]}')
        else:
            logger.debug(f'Input: {key} = {items[key]}')

            if items[key]['ModelType'] == 1:
                if items[key]['Id'] == itemA['Id']:
                    items[key]['X'] = items[key]['X'] + 25
                    items[key]['Y'] = items[key]['Y'] + 25
                    # items[key]['Z'] = items[key]['Z'] + 25
                    logger.debug(f'Adjust: {itemA}')
            elif items[key]['ModelType'] == 2:
                if items[key]['Id'] == itemB['Id']:
                    items[key]['X'] = items[key]['X'] + 25
                    items[key]['Y'] = items[key]['Y'] + 25
                    # items[key]['Z'] = items[key]['Z'] + 25
                    logger.debug(f'Adjust: {itemB}')
            else:
                if items[key]['Id'] == itemA['Id']:
                    items[key]['X'] = items[key]['X'] + 25
                    items[key]['Y'] = items[key]['Y'] + 25
                    # items[key]['Z'] = items[key]['Z'] + 25
                    logger.debug(f'Adjust: {itemA}')

            logger.debug(f'Output: {key} = {items[key]}')

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

    global PyDistributionCounter
    global RTType
    global itemA
    global itemB
    PyDistributionCounter += 1
    logger.debug(f'PyDistributionCounter = {PyDistributionCounter}')

    logger.debug(f'WaId = {WaId}')

    keys = items.keys()
    for key in keys:
        if key == 'Time':
            logger.debug(f'Time = {items[key]}')
        else:
            logger.debug(f'Input: {key} = {items[key]}')

            if RTType == 0:
                if items[key]['Id'] == itemA['Id']:
                    items[key]['X'] = items[key]['X'] + 25
                    items[key]['Y'] = items[key]['Y'] + 25
                    # items[key]['Z'] = items[key]['Z'] + 25
                    logger.debug(f'Adjust: {itemA}')
            else:
                if items[key]['Id'] == itemB['Id']:
                    items[key]['X'] = items[key]['X'] + 25
                    items[key]['Y'] = items[key]['Y'] + 25
                    # items[key]['Z'] = items[key]['Z'] + 25
                    logger.debug(f'Adjust: {itemB}')

            logger.debug(f'Output: {key} = {items[key]}')

    return items


def multiply(a,b):
    print("Will compute", a, "times", b)
    c = 0
    for i in range(0, a):
        c = c + b
    return c + 6


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
        pass
    finally:
        pass


if __name__ == "__main__":
    main(sys.argv)
else:
    pass
