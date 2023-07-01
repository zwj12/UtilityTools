MODULE ServiceModule
    !*****************************************************
    !Module Name: ServiceModule
    !Version:     1.0
    !Description: -
    !Date:        2021-10-5
    !Author:      Michael
    !*****************************************************

    !2021-12-19, Michael, Add numWireFeedFwd

    TASK PERS menudata mdTorchClean:=["Clean Weld Gun","","TorchServicesByMoveL",1,"",255,True,2,0,False,123];

    TASK PERS robtarget rtMechCleanApproach:=[[-2546.69,-135.51,1697.11],[0.654664,-0.660964,0.25421,0.264421],[0,0,-1,0],[-2154.78,-90.7705,303.354,9E+09,9E+09,9E+09]];
    TASK PERS robtarget rtMechClean:=[[-2543.12,-106.77,1697.11],[0.654666,-0.660962,0.254219,0.264413],[0,0,-1,0],[-2154.78,-90.7705,303.354,9E+09,9E+09,9E+09]];
    TASK PERS robtarget rtSprayApproach:=[[-2464.37,-188.44,1698.89],[0.654774,-0.660996,0.25407,0.264204],[0,0,-1,0],[-2154.78,-90.7713,303.354,9E+09,9E+09,9E+09]];
    TASK PERS robtarget rtSpray:=[[-2464.36,-120.17,1698.89],[0.654774,-0.660995,0.25407,0.264205],[0,0,-1,0],[-2154.78,-90.7713,303.354,9E+09,9E+09,9E+09]];
    TASK PERS robtarget rtCutApproach:=[[-2546.69,-176.52,1772.18],[0.653825,-0.661992,0.249485,0.268397],[0,0,-1,0],[-2154.78,-90.7705,303.354,9E+09,9E+09,9E+09]];
    TASK PERS robtarget rtCut:=[[-2546.69,-45.88,1772.19],[0.653828,-0.661986,0.249488,0.2684],[0,0,-1,0],[-2154.78,-90.7713,303.354,9E+09,9E+09,9E+09]];

    TASK PERS jointtarget jointMechCleanApproach:=[[0,0,0,0,0,0],[0,0,0,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jointMechClean:=[[0,0,0,0,0,0],[0,0,0,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jointSprayApproach:=[[0,0,0,0,0,0],[0,0,0,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jointSpray:=[[0,0,0,0,0,0],[0,0,0,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jointCutApproach:=[[0,0,0,0,0,0],[0,0,0,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jointCut:=[[0,0,0,0,0,0],[0,0,0,9E+09,9E+09,9E+09]];

    TASK PERS num numTorchCleanOffsetZ:=-50;
    TASK PERS num numTorchCleanTime:=3;
    TASK PERS num numTorchSprayTime:=2;
    TASK PERS num numTorchCutTime:=1;
    TASK PERS num numStopPointTime:=1;
    TASK PERS num numWireFeedFwd:=1;

    PROC MovetoHome()
        VAR jointtarget jointCur;
        EOffsOff;
        WHILE jointHome.robax<>jointHomeOld.robax DO
            UIMsgBox\Header:="Home Position Changed",""\MsgLine2:="Robot Home Position has been changed."\MsgLine3:="Please check it."\MsgLine4:="Restart the robot controller to update it."\Buttons:=btnOK\Icon:=iconWarning;
        ENDWHILE
        jointCur:=CJointT();
        jointHome.extax.eax_a:=jointCur.extax.eax_a;
        jointHome.extax.eax_b:=jointCur.extax.eax_b;
        !jointHome.extax.eax_c:=extGantryHome.eax_c;
        MoveAbsJ jointHome,speedAir,fine,toolWeldGun\WObj:=wobj0;
    ENDPROC

    PROC TorchServicesByMoveAbsJ()
        jointCurrent:=CJointT();

        !jointMechCleanApproach.extax:=jointCurrent.extax;
        !jointMechClean.extax:=jointCurrent.extax;
        !jointSprayApproach.extax:=jointCurrent.extax;
        !jointSpray.extax:=jointCurrent.extax;
        !jointCutApproach.extax:=jointCurrent.extax;
        !jointCut.extax:=jointCurrent.extax;

        jointMechCleanApproach.extax.eax_a:=jointCurrent.extax.eax_a;
        jointMechClean.extax.eax_a:=jointCurrent.extax.eax_a;
        jointSprayApproach.extax.eax_a:=jointCurrent.extax.eax_a;
        jointSpray.extax.eax_a:=jointCurrent.extax.eax_a;
        jointCutApproach.extax.eax_a:=jointCurrent.extax.eax_a;
        jointCut.extax.eax_a:=jointCurrent.extax.eax_a;


        MoveAbsJ jointCutApproach,speedAir,zoneAir,toolWeldGun\WObj:=wobj0;
        MoveAbsJ jointCut,speedAir,fine,toolWeldGun\WObj:=wobj0;
        SetDO doTS1_CutterSt,1;
        WaitTime numTorchCutTime;
        SetDO doTS1_CutterSt,0;

        MoveAbsJ jointMechCleanApproach,speedAir,zoneAir,toolWeldGun\WObj:=wobj0;
        MoveAbsJ jointMechClean,speedAir,fine,toolWeldGun\WObj:=wobj0;
        SetDO doTS1_St,1;
        WaitTime numTorchCleanTime;
        SetDO doTS1_St,0;
        WaitTime numTorchCleanTime;
        MoveAbsJ jointMechCleanApproach,speedAir,zoneAir,toolWeldGun\WObj:=wobj0;

        MoveAbsJ jointSprayApproach,speedAir,zoneAir,toolWeldGun\WObj:=wobj0;
        MoveAbsJ jointSpray,speedAir,fine,toolWeldGun\WObj:=wobj0;
        SetDO doTS1_SpOn,1;
        WaitTime numTorchSprayTime;
        SetDO doTS1_SpOn,0;
        MoveAbsJ jointSprayApproach,speedAir,zoneAir,toolWeldGun\WObj:=wobj0;
        MoveAbsJ jointCutApproach,speedAir,zoneAir,toolWeldGun\WObj:=wobj0;

        Logging\INFO,"TorchServicesByMoveAbsJ has been done!";

    UNDO
        SetDO doTS1_St,0;
        SetDO doTS1_SpOn,0;
        SetDO doTS1_CutterSt,0;
    ENDPROC

    PROC TorchServicesByMoveL()
        MovetoHome;

        jointCurrent:=CJointT();

        rtMechCleanApproach.trans.x:=rtMechCleanApproach.trans.x+jointCurrent.extax.eax_a-rtMechCleanApproach.extax.eax_a;
        rtMechClean.trans.x:=rtMechClean.trans.x+jointCurrent.extax.eax_a-rtMechClean.extax.eax_a;

        rtSprayApproach.trans.x:=rtSprayApproach.trans.x+jointCurrent.extax.eax_a-rtSprayApproach.extax.eax_a;
        rtSpray.trans.x:=rtSpray.trans.x+jointCurrent.extax.eax_a-rtSpray.extax.eax_a;

        rtCutApproach.trans.x:=rtCutApproach.trans.x+jointCurrent.extax.eax_a-rtCutApproach.extax.eax_a;
        rtCut.trans.x:=rtCut.trans.x+jointCurrent.extax.eax_a-rtCut.extax.eax_a;

        rtMechCleanApproach.extax.eax_a:=jointCurrent.extax.eax_a;
        rtMechClean.extax.eax_a:=jointCurrent.extax.eax_a;
        rtSprayApproach.extax.eax_a:=jointCurrent.extax.eax_a;
        rtSpray.extax.eax_a:=jointCurrent.extax.eax_a;
        rtCutApproach.extax.eax_a:=jointCurrent.extax.eax_a;
        rtCut.extax.eax_a:=jointCurrent.extax.eax_a;


        MoveJ rtCutApproach,speedAir,zoneAir,toolWeldGun\WObj:=wobj0;
        MoveL RelTool(rtCut,0,0,numTorchCleanOffsetZ),speedAproach,zoneAproach,toolWeldGun\WObj:=wobj0;
        MoveL rtCut,speedAproach,fine,toolWeldGun\WObj:=wobj0;
        WaitTime numStopPointTime;
        PulseDO\High\PLength:=numWireFeedFwd,soAwManFeedFwd;
        WaitTime numWireFeedFwd+numTorchCutTime;
        SetDO doTS1_CutterSt,1;
        WaitTime numTorchCutTime;
        SetDO doTS1_CutterSt,0;
        MoveL RelTool(rtCut,0,0,numTorchCleanOffsetZ),speedAproach,zoneAproach,toolWeldGun\WObj:=wobj0;
        MoveJ rtCutApproach,speedAir,zoneAir,toolWeldGun\WObj:=wobj0;

        WaitDI diTS1_ClClo,0;
        MoveJ rtMechCleanApproach,speedAir,zoneAir,toolWeldGun\WObj:=wobj0;
        MoveL RelTool(rtMechClean,0,0,numTorchCleanOffsetZ),speedAproach,zoneAproach,toolWeldGun\WObj:=wobj0;
        MoveL rtMechClean,speedAproach,fine,toolWeldGun\WObj:=wobj0;
        WaitTime numStopPointTime;
        SetDO doTS1_St,1;
        WaitDI diTS1_ClClo,1;
        SetDO doTS1_ReaUp,1;
        WaitTime numTorchCleanTime;
        SetDO doTS1_ReaUp,0;
        SetDO doTS1_St,0;
        WaitTime numTorchCleanTime;
        WaitDI diTS1_ClClo,0;
        MoveL RelTool(rtMechClean,0,0,numTorchCleanOffsetZ),speedAproach,zoneAproach,toolWeldGun\WObj:=wobj0;
        MoveJ rtMechCleanApproach,speedAir,zoneAir,toolWeldGun\WObj:=wobj0;

        MoveJ rtSprayApproach,speedAir,zoneAir,toolWeldGun\WObj:=wobj0;
        MoveL RelTool(rtSpray,0,0,numTorchCleanOffsetZ),speedAproach,zoneAproach,toolWeldGun\WObj:=wobj0;
        MoveL rtSpray,speedAproach,fine,toolWeldGun\WObj:=wobj0;
        WaitTime numStopPointTime;
        SetDO doTS1_SpOn,1;
        WaitTime numTorchSprayTime;
        SetDO doTS1_SpOn,0;
        MoveL RelTool(rtSpray,0,0,numTorchCleanOffsetZ),speedAproach,zoneAproach,toolWeldGun\WObj:=wobj0;
        MoveJ rtSprayApproach,speedAir,zoneAir,toolWeldGun\WObj:=wobj0;

        MovetoHome;
        Logging\INFO,"TorchServices has been done!";

    UNDO
        SetDO doTS1_St,0;
        SetDO doTS1_SpOn,0;
        SetDO doTS1_CutterSt,0;
        SetDO doTS1_ReaUp,0;
        SetDO soAwManFeedFwd,0;
    ENDPROC

    PROC TorchServices()
        jointCurrent:=CJointT();

        rtMechCleanApproach.trans.x:=rtMechCleanApproach.trans.x+jointCurrent.extax.eax_a-rtMechCleanApproach.extax.eax_a;
        rtMechClean.trans.x:=rtMechClean.trans.x+jointCurrent.extax.eax_a-rtMechClean.extax.eax_a;

        rtSprayApproach.trans.x:=rtSprayApproach.trans.x+jointCurrent.extax.eax_a-rtSprayApproach.extax.eax_a;
        rtSpray.trans.x:=rtSpray.trans.x+jointCurrent.extax.eax_a-rtSpray.extax.eax_a;

        rtCutApproach.trans.x:=rtCutApproach.trans.x+jointCurrent.extax.eax_a-rtCutApproach.extax.eax_a;
        rtCut.trans.x:=rtCut.trans.x+jointCurrent.extax.eax_a-rtCut.extax.eax_a;

        rtMechCleanApproach.extax.eax_a:=jointCurrent.extax.eax_a;
        rtMechClean.extax.eax_a:=jointCurrent.extax.eax_a;
        rtSprayApproach.extax.eax_a:=jointCurrent.extax.eax_a;
        rtSpray.extax.eax_a:=jointCurrent.extax.eax_a;
        rtCutApproach.extax.eax_a:=jointCurrent.extax.eax_a;
        rtCut.extax.eax_a:=jointCurrent.extax.eax_a;


        MoveJ rtCutApproach,speedAir,zoneAir,toolWeldGun\WObj:=wobj0;
        MoveWireCutJ rtCutApproach,rtCut,speedAproach,fine,toolWeldGun\WObj:=wobj0;
        MoveJ rtCutApproach,speedAir,zoneAir,toolWeldGun\WObj:=wobj0;

        MoveJ rtMechCleanApproach,speedAir,zoneAir,toolWeldGun\WObj:=wobj0;
        MoveMechCleanJ rtMechCleanApproach,rtMechClean,speedAproach,fine,toolWeldGun\WObj:=wobj0;
        MoveJ rtMechCleanApproach,speedAir,zoneAir,toolWeldGun\WObj:=wobj0;

        MoveJ rtSprayApproach,speedAir,zoneAir,toolWeldGun\WObj:=wobj0;
        MoveSprayJ rtSprayApproach,rtSpray,speedAproach,fine,toolWeldGun\WObj:=wobj0;
        MoveJ rtSprayApproach,speedAir,zoneAir,toolWeldGun\WObj:=wobj0;

        Logging\INFO,"TorchServices has been done!";
    ENDPROC

ENDMODULE