MODULE LubricationModule
    !*****************************************************
    !Module Name: LubricationModule
    !Version:     1.0
    !Description: This module is used for track lubrication
    !Date:        2025-12-09
    !Author:      ABB
    !*****************************************************

    !Unit: second
    PERS dnum numLubOnCounter:=0;
    PERS dnum numLubOnCounterInterval:=518400;
    PERS dnum numLubOnCounterIntervalMin:=450;

    PERS num numLubValueOnLength:=60;
    PERS num numLubValueOnCycle:=75;
    PERS num numLubValueOnQuantity:=6;

    VAR intnum intCheckLubState1;
    VAR intnum intCheckLubState2;
    VAR intnum intCheckLubState3;
    VAR intnum intCheckLubState4;
    VAR bool boolLubSucceed1:=FALSE;
    VAR bool boolLubSucceed2:=FALSE;
    VAR bool boolLubSucceed3:=FALSE;
    VAR bool boolLubSucceed4:=FALSE;

    CONST string strLubHeader:="Lubrication On";
    CONST string strLubDetectedHeader:="Lubrication Detected";
    CONST string strLubDetectedReason:="Lubrication sensor detected";
    CONST string strLubFailedHeader:="Lubrication Failed";
    CONST string strLubFailedReason:="Lubrication sensor detection failed";
    CONST string strErrorLubHeader:="Lubrication Error";
    CONST string strErrorLubReason:="Lubrication Internal Error";

    PROC main()
        Lubrication;
        WaitTime 60;
    ENDPROC

    PROC Lubrication()
        WHILE TRUE DO
            Incr numLubOnCounter;
            numLubOnCounterInterval:=GOutputDnum(sgoLubOnCounterInterval);
            IF numLubOnCounterInterval<numLubOnCounterIntervalMin THEN
                numLubOnCounterInterval:=numLubOnCounterIntervalMin;
            ENDIF
            IF numLubOnCounter>=numLubOnCounterInterval THEN
                IF sgoLubQuantity>=1 THEN
                    AutoLubrication 1;
                ENDIF
                IF sgoLubQuantity>=2 THEN
                    AutoLubrication 2;
                ENDIF
                IF sgoLubQuantity>=3 THEN
                    AutoLubrication 3;
                ENDIF
                IF sgoLubQuantity>=4 THEN
                    AutoLubrication 4;
                ENDIF
                numLubOnCounter:=0;
            ENDIF
            SetGO sgoLubOnCounter,numLubOnCounter;
            WaitTime 1;
        ENDWHILE

    ERROR
        ErrWrite\W,strErrorLubHeader,strErrorLubReason;
        RETURN ;
    ENDPROC

    PROC AutoLubrication(num Index)
        TEST Index
        CASE 1:
            boolLubSucceed1:=FALSE;
            IDelete intCheckLubState1;
            CONNECT intCheckLubState1 WITH TRAPCheckLubState1;
            ISignalDI\Single,diTrackLubState1,edge,intCheckLubState1;
            FOR i FROM 1 TO numLubValueOnQuantity DO
                ErrWrite\I,strLubHeader,"Lubrication: "+ValToStr(Index)\RL2:="Lubrication Count: "+ValToStr(i);
                PulseDO\High\PLength:=numLubValueOnLength,doTrackLubOn1;
                WaitTime numLubValueOnCycle;
            ENDFOR
            IF boolLubSucceed1=FALSE THEN
                ErrWrite\W,strLubFailedHeader,strLubFailedReason\RL2:="Lubrication: "+ValToStr(Index);
            ENDIF
        CASE 2:
            boolLubSucceed2:=FALSE;
            IDelete intCheckLubState2;
            CONNECT intCheckLubState2 WITH TRAPCheckLubState2;
            ISignalDI\Single,diTrackLubState2,edge,intCheckLubState2;
            FOR i FROM 1 TO numLubValueOnQuantity DO
                ErrWrite\I,strLubHeader,"Lubrication: "+ValToStr(Index)\RL2:="Lubrication Count: "+ValToStr(i);
                PulseDO\High\PLength:=numLubValueOnLength,doTrackLubOn2;
                WaitTime numLubValueOnCycle;
            ENDFOR
            IF boolLubSucceed2=FALSE THEN
                ErrWrite\W,strLubFailedHeader,strLubFailedReason\RL2:="Lubrication: "+ValToStr(Index);
            ENDIF
        CASE 3:
            boolLubSucceed3:=FALSE;
            IDelete intCheckLubState3;
            CONNECT intCheckLubState3 WITH TRAPCheckLubState3;
            ISignalDI\Single,diTrackLubState3,edge,intCheckLubState3;
            FOR i FROM 1 TO numLubValueOnQuantity DO
                ErrWrite\I,strLubHeader,"Lubrication: "+ValToStr(Index)\RL2:="Lubrication Count: "+ValToStr(i);
                PulseDO\High\PLength:=numLubValueOnLength,doTrackLubOn3;
                WaitTime numLubValueOnCycle;
            ENDFOR
            IF boolLubSucceed3=FALSE THEN
                ErrWrite\W,strLubFailedHeader,strLubFailedReason\RL2:="Lubrication: "+ValToStr(Index);
            ENDIF
        CASE 4:
            boolLubSucceed4:=FALSE;
            IDelete intCheckLubState4;
            CONNECT intCheckLubState4 WITH TRAPCheckLubState4;
            ISignalDI\Single,diTrackLubState4,edge,intCheckLubState4;
            FOR i FROM 1 TO numLubValueOnQuantity DO
                ErrWrite\I,strLubHeader,"Lubrication: "+ValToStr(Index)\RL2:="Lubrication Count: "+ValToStr(i);
                PulseDO\High\PLength:=numLubValueOnLength,doTrackLubOn4;
                WaitTime numLubValueOnCycle;
            ENDFOR
            IF boolLubSucceed4=FALSE THEN
                ErrWrite\W,strLubFailedHeader,strLubFailedReason\RL2:="Lubrication: "+ValToStr(Index);
            ENDIF
        ENDTEST
    ENDPROC

    TRAP TRAPCheckLubState1
        boolLubSucceed1:=TRUE;
        SetDO sdoLubSucceed1,1;
        ErrWrite\I,strLubDetectedHeader,strLubDetectedReason\RL2:="Lubrication: 1";
    ENDTRAP

    TRAP TRAPCheckLubState2
        boolLubSucceed2:=TRUE;
        SetDO sdoLubSucceed2,1;
        ErrWrite\I,strLubDetectedHeader,strLubDetectedReason\RL2:="Lubrication: 2";
    ENDTRAP

    TRAP TRAPCheckLubState3
        boolLubSucceed3:=TRUE;
        SetDO sdoLubSucceed3,1;
        ErrWrite\I,strLubDetectedHeader,strLubDetectedReason\RL2:="Lubrication: 3";
    ENDTRAP

    TRAP TRAPCheckLubState4
        boolLubSucceed4:=TRUE;
        SetDO sdoLubSucceed4,1;
        ErrWrite\I,strLubDetectedHeader,strLubDetectedReason\RL2:="Lubrication: 4";
    ENDTRAP
ENDMODULE