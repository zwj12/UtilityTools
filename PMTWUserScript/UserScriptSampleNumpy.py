"""PickMaster Twin User Script Sample: UserScriptSampleNumpy.py
"""

import os
import sys
import logging
import numpy
import cv2


RTType = 1
itemA = {'Name': 'Item_1', 'Id': '325D3EB5-B563-4F90-B0C5-2F1E770D5C04'}
itemB = {'Name': 'Item_2', 'Id': '9552BEFB-480E-42B3-96D1-9EA297506540'}
logFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWUserScript.log'
PyInitializeCounter = 0
PyAdjusterCounter = 0
PyDistributionCounter = 0


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
    NumPyTest()

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
    NumPyTest()

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
        itemInfo = {
            '0': {'Name': 'Item_1', 'Id': '325D3EB5-B563-4F90-B0C5-2F1E770D5C04'},
            '1': {'Name': 'Item_2', 'Id': '9552BEFB-480E-42B3-96D1-9EA297506540'},
        }
        PyInitialize(type, itemInfo)

        items = {'Time': 1702296806.51,
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
                       'Id': '325D3EB5-B563-4F90-B0C5-2F1E770D5C04'
                       }
                 }
        PyAdjuster(items)

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
                                   'Id': '346563A7-F607-4D65-8DFD-D53AB615EDA8'
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
