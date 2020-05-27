#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020-4-15
# @Author  : Michael

import re

strModName = input("Please input mod name (without .mod) :")

#strModName="Ncv3L_OP30R1"
fileOri = open(strModName + '.mod')
strNewModFileName = strModName + "_new.mod"
fileNew = open(strNewModFileName, 'w')
strSeamName = ""
intSeamSubIndex = 0
while True:
    strLine = fileOri.readline()
    if not strLine:
        break
    
    matchComment = re.search( r'^ *!', strLine, re.I)
    if matchComment:
        pass
    else:        
        matchPROC = re.search( r'(?<=PROC ).*(?=\()', strLine.rstrip(), re.I)
        if matchPROC:
            strSeamName = matchPROC.group().strip()
            intSeamSubIndex = 0
        else:   
            matchArcLStart = re.search( r' *Arc[LC]Start.*', strLine.rstrip(), re.I)
            if matchArcLStart:
                matchArcLStartWithoutSeamName = re.search( r'^((?!SeamName:=).)*$', strLine.rstrip(), re.I)
                if matchArcLStartWithoutSeamName:
                    strTemp = matchArcLStartWithoutSeamName.group()
                    if intSeamSubIndex == 0:
                        intSeamSubIndex = intSeamSubIndex + 1
                        strLine = strTemp[0:-1] + '\SeamName:="'+ strSeamName +'";\n'
                        print (strLine)            
                    else:
                        intSeamSubIndex = intSeamSubIndex + 1
                        strLine = strTemp[0:-1] + '\SeamName:="'+ strSeamName + '-' + str(intSeamSubIndex) + '";\n'
                        print (strLine)
    fileNew.write(strLine)

fileOri.close()
fileNew.close()

print ("New module file: " + strNewModFileName + " is created")
input("Press any key to exit")
