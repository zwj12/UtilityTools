MODULE WorldZoneModule
    !*****************************************************
    !Module Name:   WorldZoneModule
    !Version:       1.0
    !Description:   -
    !Date:          2018-4-20
    !Author:        Michael
    !*****************************************************

    VAR wztemporary wztemporaryHome;
    VAR wzstationary wzstationaryHome;
    VAR wzstationary wzstationaryService;

    TASK PERS jointtarget jointHomeDelta:=[[10,10,10,10,10,10],[9E+09,9E+09,10,9E+09,9E+09,9E+09]];
    TASK PERS pos posServiceDelta:=[10,10,10];

    PROC WorldZoneTemporary()
        VAR shapedata shapeJoint;
        VAR jointtarget jointHomeTemp;
        jointHome:=jointHome;
        jointHomeTemp.extax.eax_a:=9E+09;
        WZFree wztemporaryHome;
        WZHomeJointDef\Inside,shapeJoint,jointHomeTemp,jointHomeDelta;
        WZDOSet\Temp,wztemporaryHome\Inside,shapeJoint,doSysOutAtHome_1,1;
        TPWrite "WorldZone is set";
    ENDPROC

    PROC WorldZonePowerOn()
        WorldZoneHome;
    ENDPROC

    PROC WorldZoneHome()
        VAR shapedata shapeJointHome;
        VAR jointtarget jointHomeTemp;

        !Set WorldZone of home position
        jointHomeTemp:=jointHome;
        jointHomeTemp.extax.eax_a:=9E+09;
        jointHomeTemp.extax.eax_b:=9E+09;
        !jointHomeTemp.extax.eax_c:=9E+09;
        jointHomeTemp.extax.eax_d:=9E+09;
        jointHomeTemp.extax.eax_e:=9E+09;
        jointHomeTemp.extax.eax_f:=9E+09;
        WZHomeJointDef\Inside,shapeJointHome,jointHomeTemp,jointHomeDelta;
        WZDOSet\Stat,wzstationaryHome\Inside,shapeJointHome,doSysOutAtHome_1,1;

        jointHomeOld:=jointHome;

        !bSafeMutex:=FALSE;
        IF RobOS() THEN
            SetDO sdoVirtualController,0;
        ELSE
            SetDO sdoVirtualController,1;
        ENDIF
    ENDPROC

ENDMODULE