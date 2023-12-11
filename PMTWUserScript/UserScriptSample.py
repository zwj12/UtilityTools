"""PickMaster Twin User Script Sample: UserScriptSample.py
"""

import os
import sys 
import logging

RTType = 1
itemA = {'Name': 'Item_1', 'Id': '325D3EB5-B563-4F90-B0C5-2F1E770D5C04'}
itemB = {'Name': 'Item_2', 'Id': '9552BEFB-480E-42B3-96D1-9EA297506540'}
logFilePath = r'C:\ProgramData\ABB\PickMaster Twin 2\PickMaster Twin Host 2\PickMaster Runtime\Log\PMTWUserScript.log'
PyInitializeCounter = 0


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
        formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
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
    global item_1
    global item_2
    PyInitializeCounter += 1
    logger.debug(f'PyInitializeCounter = {PyInitializeCounter}')
    RTType = type
    logger.debug(f'RTType = {RTType}')
    items_list = list(itemInfo.items())
    if len(items_list)>0:
        itemA = items_list[0][1]
        logger.debug(f'itemA = {itemA}')
    if len(items_list)>1:
        itemB = items_list[1][1]
        logger.debug(f'itemB = {itemB}')      


def main(argv):
    """main

    """
    print(argv)
    try:
        logger = get_logging()
        logger.debug(argv)
        type = 0
        itemInfo = {
            '0': {'Name': 'Item_1', 'Id': '325D3EB5-B563-4F90-B0C5-2F1E770D5C04'},
            '1': {'Name': 'Item_2', 'Id': '9552BEFB-480E-42B3-96D1-9EA297506540'},
        }
        PyInitialize(type, itemInfo)

    except Exception:
        pass
    finally:
        pass


if __name__ == "__main__":
    main(sys.argv)
else:
    pass
