MODULE TestAutoCal
    !!****************************************************************************
    !! Test module for AUTO-CAL Interface  from SERVO-ROBOT 
    !!   
    !! Requirements    Requires the AutoCal2 system module (version ABB200313.001)
    !!                 (Tested with Rel151001.122 on vision system)
    !! Date:           June 16th 2020
    !! Author:         SERVO-ROBOT (Cedric Demers-Roy)
    !! Copyright:      SERVO-ROBOT INC. 2020
    !!
    !!****************************************************************************
    
    !!Tool below is a copy of the tool Ref_Pin defined in MainModule
    PERS tooldata ACAL_My_Tool:=[TRUE,[[-60.4407,4.01094,538.005],[0.981627,0,0.190809,0]],[3,[0,0,1],[1,0,0,0],0,0,0]];
    PERS wobjdata ACAL_My_Cal_Target:=[FALSE,TRUE,"",[[-495.742,-997.479,838.589],[0.713413,-0.00439101,-6.05187E-05,-0.70073]],[[0,0,0],[1,0,0,0]]];
    !!Tool below is used to test calibration result (TCP at OPTICAL origin of laser-camera)
    PERS tooldata ACAL_OpticalTool:=[TRUE,[[22.8319,-5.87382,755.566],[0.0166039,0.0120922,0.999788,-0.0017187]],[2,[50,50,100],[1,0,0,0],0,0,0]];
    
    PERS caldata ACAL_TestCalOut:=[[1.123,0.065,-0.584],39.754,-4.676,850.15,-179.97,-0.00900269,177.77,3];    !Output of the calibration function                            
    !!Next variable stores the WObj used to test the base optimization function
    PERS wobjdata ACAL_OptimizedBase:=[FALSE,TRUE,"",[[968.915,-342.455,475.393],[0.99982,0.00148294,-0.000331306,-0.0188947]],[[0,0,0],[1,0,0,0]]];
    
    PERS num ACAL_LoopCount:=3;
    
    PROC Test_AUTOCAL()
        VAR bool MainClearLog;           !!Variable to control the calibration function
        VAR bool MainCheckOnly;          !!Variable to control the calibration function
        VAR bool MainSkipCheck;          !!Variable to control the calibration function
        VAR num MainNbIter;              !!Variable to control the calibration function
        VAR num StabTime;                !!Variable to control the calibration function
        VAR robtarget CurPos;            !!Temporary position
        VAR string StartTimer;           !!Stores the calibration start time
        VAR bool ACAL_RunLoop;           !!Defines if test program runs in a LOOP or not
        VAR bool ACAL_LogResults;        !!Defines if calibration data is logged on robot controller
        VAR bool ACAL_TestOpticalTool;   !!If TRUE, OpticalTool TCP will be sent to (0,0,0) after calibration
        VAR pose ACAL_OpticalToolOffset; !!Adds an offset to the OpticalTool TCP to test calibration result
        VAR string ACAL_LogFilename;     !!Log file name on robot controller (in HOME folder)
        VAR iodev ACAL_Log;              !!Internal variable for logging the calibration data in this function
        
		ACAL_LogFilename:="ACAL_Test_Data.txt";
        
		ACAL_RunLoop:=FALSE;        !!If TRUE, test routine loops endlessly
        ACAL_TestOpticalTool:=FALSE; !!If TRUE, OpticalTool from calibration will be sent to (0,0,0)
        ACAL_LogResults:=TRUE;      !!If TRUE, calibration data is logged in file indicated below
        MainNbIter:= 3;             !!Number of iteration for calibration (recommended is 3; minimum is 2, maximum is 10)
        MainClearLog:=False;         !!If TRUE, calibration log is cleared at beginning of calibration
        MainCheckOnly:=FALSE;       !!If TRUE, calibration will only perform the check (no new calibration done)
        MainSkipCheck:=FALSE;       !!If TRUE, calibration will be performed but calibration check will be skipped
        StabTime:=1000;             !!Time in milliseconds to wait for stabilization at each point during calibration
        
        !!***IMPORTANT******IMPORTANT********IMPORTANT***********************************************************!
        !!*** Next two lines copy the right TOOL and WOBJ definitions from MAIN program...                      *!
        !!*** (user can define is own directly in this module and DELETE THE NEXT TWO LINES)                    *!
        !!***IMPORTANT******IMPORTANT********IMPORTANT***********************************************************!
        
		ACAL_My_Tool:=toolWeldGun;
        ACAL_My_Cal_Target:=acaltargetV2;
        
		CurPos:=CRobT(\Tool:=ACAL_My_Tool\WObj:=ACAL_My_Cal_Target);
        !!Next instruction simply selects the proper active tool and WObj (stays in current position)
        MoveL CurPos, v100, fine, ACAL_My_Tool\WObj:=ACAL_My_Cal_Target;
        
        !!***IMPORTANT******IMPORTANT********IMPORTANT***********************************************************!
        !!*** Pause at start to allow user to teach correct CLEAR and START positions based on his installation *!
        !!***IMPORTANT******IMPORTANT********IMPORTANT***********************************************************!
        IF NOT ACAL_RunLoop THEN
		    ACALg_SkpStChk:=FALSE;
            TPWrite "Make sure to teach CLEAR and START points before continuing.";
            Stop;
        ELSE
            ACAL_LoopCount:=1;
            ACALg_SkpStChk:=TRUE;
        ENDIF
        
        LoopACALTest:
        
        IF (ACAL_LogResults AND ACAL_RunLoop) THEN
            StartTimer:=CTime();
        ENDIF
        
        Stop;
        !!CLEAR position above calibration target - TEACH TO HAVE PROPER TOOL CLEARANCE TO GO TO THE CALIBRATION START POSITION (Next MoveL below)
        MoveL [[100.34,41.87,26.32],[0.193864,-0.00815517,-0.980983,-0.00473385],[-1,0,-2,1],[-507.555,-599.879,-499.996,9E+09,9E+09,9E+09]], v100, fine, ACAL_My_Tool\WObj:=ACAL_My_Cal_Target;
        
        !!Open communication socket (IMPORTANT: take care to input the proper tool and wObj!)
        IF NOT ACALu_Initialize("192.168.1.3",ACAL_My_Tool,ACAL_My_Cal_Target) THEN
            TPWrite "Can't connect to AUTO-CAL module on vision controller";
            Stop;
        ENDIF
        
        !!Calibration START position - TEACH THIS POINT ACCORDING TO THE AUTO-CAL 2.0 USER MANUAL
        MoveL [[100.34,41.86,26.32],[0.193864,-0.00815676,-0.980983,-0.0047341],[-1,0,-2,1],[-507.555,-599.879,-499.996,9E+09,9E+09,9E+09]], v100, fine, ACAL_My_Tool\WObj:=ACAL_My_Cal_Target;
        
        WaitTime 1;
        
        !!Select STD or HR version depending on laser-camera in use
        ACAL_TestCalOut:=ACALu_Cal_STD(MainNbIter,ACAL_My_Tool,ACAL_My_Cal_Target,MainClearLog,MainCheckOnly,MainSkipCheck,1000,2);
        !ACAL_TestCalOut:=ACALu_Cal_HR(MainNbIter,ACAL_My_Tool,ACAL_My_Cal_Target,MainClearLog,MainCheckOnly,MainSkipCheck,1000,2);
        
        !!Check for error during calibration function
        IF ACAL_TestCalOut.status<0 THEN
            TPWrite "ERROR: Could not complete AUTO-CAL 2.0 calibration!";
            Stop;
        ELSE
            TPWrite "Calibration was successful!";
            TPWrite "Cal check errors: X=" + ValToStr(ACAL_TestCalOut.calerrors.x) + " Y=" + ValToStr(ACAL_TestCalOut.calerrors.y) + " Z=" + ValToStr(ACAL_TestCalOut.calerrors.z);
            TPWrite "Cal data (flange): X=" + ValToStr(ACAL_TestCalOut.tx) + " Y=" + ValToStr(ACAL_TestCalOut.ty) + " Z=" + ValToStr(ACAL_TestCalOut.tz) + " A=" + ValToStr(ACAL_TestCalOut.oa) + " B=" + ValToStr(ACAL_TestCalOut.ob) + " C=" + ValToStr(ACAL_TestCalOut.oc);
            IF (ACAL_LogResults AND ACAL_RunLoop) THEN
                Open "HOME:", \File:=ACAL_LogFilename, ACAL_Log, \Append;
                Write ACAL_Log, CDate() + "; " + StartTimer + "; " + CTime() + "; " + ValToStr(MainNbIter) + "; " \NoNewLine;
                Write ACAL_Log, ValToStr(ACAL_TestCalOut.tx) + ";" + ValToStr(ACAL_TestCalOut.ty) + ";" + ValToStr(ACAL_TestCalOut.tz) + ";" + ValToStr(ACAL_TestCalOut.oa) + ";" + ValToStr(ACAL_TestCalOut.ob) + ";" + ValToStr(ACAL_TestCalOut.oc) + ";" + ValToStr(ACAL_TestCalOut.calerrors.x) + ";" + ValToStr(ACAL_TestCalOut.calerrors.y) + ";" + ValToStr(ACAL_TestCalOut.calerrors.z);
                Close ACAL_Log;
            ENDIF
            
        ENDIF
        
        !!Close communication socket
        IF NOT ACALu_Clear() THEN
            TPWrite "Can't close connection to AUTO-CAL module";
            Stop;
        ENDIF
        
        IF ACAL_TestOpticalTool THEN
            TPWrite "OpticalTool TCP will go to (0,0,0).";
            Stop;
            
            !!Below lines compute the OpticalTool definition based on the calibration data
            ACAL_OpticalTool.tframe.trans.x:=ACAL_TestCalOut.tx;
            ACAL_OpticalTool.tframe.trans.y:=ACAL_TestCalOut.ty;
            ACAL_OpticalTool.tframe.trans.z:=ACAL_TestCalOut.tz;
            ACAL_OpticalTool.tframe.rot:=OrientZYX(ACAL_TestCalOut.oc,ACAL_TestCalOut.ob,ACAL_TestCalOut.oa);
            
            !!OpticalTool will be 112 mm up from the bottom of the field of view of the laser-camera which was calibrated
            !!(offset can be adjusted to bring the profile to a proper position for the current laser-camera)
            ACAL_OpticalToolOffset:=[[0,0,100],[1,0,0,0]];
            
            ACAL_OpticalTool.tframe:=PoseMult(ACAL_OpticalTool.tframe,ACAL_OpticalToolOffset);
            
            !!OpticalTool TCP is sent to the calibration target origin (small 1.2 mm hole)
            Stop;
            MoveL [[0,0,0],[0.999887,-0.00723525,-0.0122464,0.00481853],[-1,-1,1,1],[-465.249,-144.288,-600,9E+09,9E+09,9E+09]], v50, fine, ACAL_OpticalTool\WObj:=ACAL_My_Cal_Target;
            
        ENDIF
        
        IF ACAL_RunLoop THEN
            Incr ACAL_LoopCount;
            GOTO LoopACALTest;
        ENDIF
        
    ENDPROC
    
    PROC TestOptimizeBase()
        VAR robtarget PosA;
        VAR robtarget PosB;
        VAR robtarget PosC;
        
        !Move close to target (initializes tool and WObj)
        MoveL [[-2.09,59.61,41.55],[0.193626,-0.00645953,-0.981034,0.0062766],[-1,-1,2,1],[-465.247,-144.287,-485.852,9E+09,9E+09,9E+09]], v100, z50, ACAL_My_Tool\WObj:=ACAL_My_Cal_Target;
        
        Stop;
        
        !Three approach points taught by operator (in manually defined target user frame)
        !Theoretical values (5 mm above points): A=(0,0,5); B=114,0,5; C=0,108,5)
        PosA:=[[1.27,2.77,3.99],[0.193626,-0.00645967,-0.981034,0.00627775],[0,-1,1,1],[-465.246,-144.287,-485.852,9E+09,9E+09,9E+09]];
        PosB:=[[118.26,3.80,4.70],[0.193624,-0.00645936,-0.981034,0.00627635],[0,-1,1,1],[-465.246,-144.286,-485.852,9E+09,9E+09,9E+09]];
        PosC:=[[0.53,122.05,3.69],[0.193627,-0.00646203,-0.981034,0.0062777],[-1,-1,2,1],[-465.246,-144.287,-485.852,9E+09,9E+09,9E+09]];
        
        IF NOT ACALu_Initialize("192.168.1.3",ACAL_My_Tool,ACAL_My_Cal_Target) THEN
            Stop;
        ENDIF
            
        ACAL_OptimizedBase:=ACALu_Opt_Base(3,ACAL_My_Tool,ACAL_My_Cal_Target,PosA,PosB,PosC);
        !Check for error
        IF NOT ACAL_OptimizedBase.ufprog THEN
            Stop;
        ENDIF
    
        Stop;
        MoveL [[15.05,46.06,112.33],[0.983993,0.00934793,-0.174397,0.0354175],[-1,-2,-1,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]], v100, fine, ACAL_My_Tool\WObj:=ACAL_My_Cal_Target;
    
        IF NOT ACALu_Clear() THEN
            Stop;
        ENDIF
        
    ENDPROC
    
ENDMODULE