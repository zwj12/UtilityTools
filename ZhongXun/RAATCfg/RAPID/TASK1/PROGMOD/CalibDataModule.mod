MODULE CalibDataModule
    !*****************************************************
    !Module Name:   CalibDataModule
    !Version:       1.0
    !Description:   
    !Date:          2021-3-25
    !Author:        Michael
    !*****************************************************

    TASK PERS menudata mdDefineWeldGun:=["Define TCP of Weld Gun","","DefTCPofWeldGun",1,"",255,True,1,100,False,201];
    TASK PERS menudata mdDefineLaser:=["Define TCP of Laser","","DefTCPofLaser",1,"",255,True,1,100,False,202];

    TASK PERS bool boolSaveModule:=FALSE;

    TASK PERS tooldata toolWeldGun:=[TRUE,[[-60.4407,4.01094,538.005],[0.981627,0,0.190809,0]],[3,[0,0,1],[1,0,0,0],0,0,0]];
    TASK PERS tooldata toolLaser:=[TRUE,[[40.746,0.415,676.2],[1,0,0,0]],[3,[0,0,1],[1,0,0,0],0,0,0]];
    TASK PERS tooldata toolWeldGunLast:=[TRUE,[[-56.5158,3.15439,544.716],[0.981627,0,0.190809,0]],[3,[0,0,1],[1,0,0,0],0,0,0]];
    TASK PERS tooldata toolLaserLast:=[TRUE,[[40.746,0.415,676.2],[1,0,0,0]],[3,[0,0,1],[1,0,0,0],0,0,0]];

    TASK PERS wobjdata wobjCurrent:=[FALSE,TRUE,"",[[-500,-50,60],[1,0,0,0]],[[0,0,0],[1,0,0,0]]];
    TASK PERS wobjdata wobjTemp:=[FALSE,TRUE,"",[[-513,-36,67],[1,0,0,0]],[[0,0,0],[1,0,0,0]]];

    ! postions for tool definition of weld gun
    TASK PERS jointtarget jtWeldGun1:=[[34.3799,19.4024,-37.6137,40.7878,-76.4594,140.076],[-465.218,39.3053,-432.676,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jtWeldGun2:=[[-32.665,19.2212,-34.5177,-38.3188,-77.555,217.191],[-465.218,39.3047,-432.676,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jtWeldGun3:=[[-5.41069,44.678,-51.6932,-5.8464,-86.4953,186.702],[-465.218,39.3061,-432.676,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jtWeldGun4:=[[0.0637999,-1.25232,0.272104,0.0258803,-67.02,179.931],[-465.218,39.3053,-432.676,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jtWeldGunZ:=[[-23.388,45.5074,-40.1349,34.9712,97.7934,-21.115],[7683.71,268.717,9E+09,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jtWeldGunX:=[[-11.2908,41.3683,-15.0054,38.5769,74.0462,-24.2474],[7683.71,268.717,9E+09,9E+09,9E+09,9E+09]];

    ! postions for tool definition of laser
    TASK PERS jointtarget jtLaser1:=[[1.23463,20.2117,49.1937,-0.0177981,19.9578,1.24529],[2710.99,9E+09,9E+09,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jtLaser2:=[[-4.77355,41.5571,14.5452,9.634,71.2439,-7.0717],[2710.99,9E+09,9E+09,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jtLaser3:=[[16.6953,31.7453,37.9034,-38.2116,46.0125,35.4493],[2710.99,9E+09,9E+09,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jtLaser4:=[[-15.8654,24.7616,60.5945,106.491,27.5027,-123.159],[2710.98,9E+09,9E+09,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jtLaserZ:=[[159.015,8.68591,36.5218,-1.07903,44.8617,-21.0289],[687.115,9E+09,9E+09,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jtLaserX:=[[161.523,27.5424,31.4752,-1.46627,31.0902,-18.0317],[687.112,9E+09,9E+09,9E+09,9E+09,9E+09]];

    TASK PERS jointtarget jointOrigin:=[[0,0,0,0,0,0],[0,0,0,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jointHome:=[[0,-60,40,0,60,0],[-1295.03,-547.513,-500,9E+9,9E+9,9E+9]];
    TASK PERS jointtarget jointTransportation:=[[0,-60,45,0,60,0],[0,500,-500,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jointLoadIdentify:=[[-20,0,0,0,0,0],[0,9E+09,9E+09,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jointCurrent:=[[-120,-75,-15,0,90,-90],[-800,-500,-440,9E+9,9E+9,9E+9]];
    TASK PERS jointtarget jointHomeOld:=[[0,-60,40,0,60,0],[-1295.03,-547.513,-500,9E+9,9E+9,9E+9]];

    TASK PERS robtarget robCurrent:=[[-209.736,482.664,216.543],[0.178965,-0.641361,0.732457,-0.141898],[-2,-1,1,1],[-800,500,0.00276417,9E+09,9E+09,9E+09]];

    PERS speeddata speedAir:=[200,500,5000,1000];
    PERS speeddata speedAproach:=[200,500,5000,1000];
    PERS speeddata speedWeld:=[50,500,5000,1000];
    PERS speeddata speedLaserScan:=[200,500,5000,1000];

    PERS zonedata zoneAir:=[FALSE,200,300,300,30,300,30];
    PERS zonedata zoneAproach:=[FALSE,200,300,300,30,300,30];
    PERS zonedata zoneWeld:=[FALSE,20,30,30,3,30,3];
    PERS zonedata zoneScan:=[FALSE,200,300,300,30,300,30];

    PERS num numAcc:=100;
    PERS num numRamp:=100;

    PROC DefTCPofWeldGun()
        VAR num nMaxErr;
        VAR num nMeanErr;
        VAR num nLastDeviation;
        VAR tooldata toolOld;
        VAR num nUserInputFP:=0;
        VAR string sHeader;
        VAR string sMsg{5};
        VAR btnres nAnswer;
        VAR robtarget pTCP;
        VAR robtarget robtarWeldGun1;
        VAR robtarget robtarWeldGun2;
        VAR robtarget robtarWeldGun3;
        VAR robtarget robtarWeldGun4;

        sHeader:="Robot System"+" ("+GetTaskName()+")";
        sMsg{1}:=" Press Yes to run definition of";
        sMsg{2}:="               tool:  toolWeldGun.";
        sMsg{3}:=" Press No  to cancel.";
        sMsg{4}:="";
        sMsg{5}:="";
        UIMsgBox\Header:=sHeader,sMsg{1}\MsgLine2:=sMsg{2}\MsgLine3:=sMsg{3}\MsgLine4:=sMsg{4}\MsgLine5:=sMsg{5}\Buttons:=btnYesNo\Icon:=iconInfo\Result:=nAnswer;
        IF nAnswer=resNo THEN
            GOTO Calculate;
        ENDIF

        Stop\NoRegain;
        !MoveAbsJ jtWeldGun4,v100,fine,toolWeldGun;
        MoveAbsJ jtWeldGun1,v100,fine,toolWeldGun;
        Stop;
        !MoveAbsJ jtWeldGun4,v100,fine,toolWeldGun;
        MoveAbsJ jtWeldGun2,v100,fine,toolWeldGun;
        Stop;
        !MoveAbsJ jtWeldGun4,v100,fine,toolWeldGun;
        MoveAbsJ jtWeldGun3,v100,fine,toolWeldGun;
        Stop;
        MoveAbsJ jtWeldGun4,v100,fine,toolWeldGun;
        Stop;
        MoveAbsJ jtWeldGunZ,v100,fine,toolWeldGun;
        Stop;
        MoveAbsJ jtWeldGunX,v100,fine,toolWeldGun;
        Stop;

        Calculate:

        toolOld:=toolWeldGun;
        MToolTCPCalib jtWeldGun1,jtWeldGun2,jtWeldGun3,jtWeldGun4,toolWeldGun,nMaxErr,nMeanErr;
        !MToolRotCalib jtWeldGun4,jtWeldGunZ\XPos:=jtWeldGunX,toolWeldGun;
        TPErase;
        TPWrite " nMaxErr  ... "\Num:=nMaxErr;
        TPWrite " nMeanErr ... "\Num:=nMeanErr;
        Logging "toolWeldGun.trans="+ValToStr(toolWeldGun.tframe.trans);
        Logging "toolWeldGun.rot="+ValToStr(toolWeldGun.tframe.rot);
        nLastDeviation:=Distance(toolWeldGun.tframe.trans,toolOld.tframe.trans);
        TPWrite "Deviation="+ValToStr(nLastDeviation);
        robtarWeldGun1:=CalcRobT(jtWeldGun1,toolWeldGun);
        robtarWeldGun2:=CalcRobT(jtWeldGun2,toolWeldGun);
        robtarWeldGun3:=CalcRobT(jtWeldGun3,toolWeldGun);
        robtarWeldGun4:=CalcRobT(jtWeldGun4,toolWeldGun);
        TPWrite " Distance between point1 and point 4 is "\Num:=Distance(robtarWeldGun1.trans,robtarWeldGun4.trans);
        TPWrite " Distance between point2 and point 4 is "\Num:=Distance(robtarWeldGun2.trans,robtarWeldGun4.trans);
        TPWrite " Distance between point3 and point 4 is "\Num:=Distance(robtarWeldGun3.trans,robtarWeldGun4.trans);
        TPReadFK nUserInputFP,"",stEmpty,stEmpty,stEmpty,stEmpty,"OK";
        Stop;

        Calibrate:
        MoveAbsJ jtWeldGun4,v100,fine,toolWeldGun;
        pTCP:=CRobT(\Tool:=toolWeldGun);
        MoveL RelTool(pTCP,0,0,0),v100,fine,toolWeldGun;
        MoveL Reltool(pTCP,0,0,-30),v100,fine,toolWeldGun;
        MoveL Reltool(pTCP,0,0,30),v100,fine,toolWeldGun;
    ENDPROC

    PROC DefTCPofLaser()
        VAR num nMaxErr;
        VAR num nMeanErr;
        VAR num nUserInputFP:=0;
        VAR string sHeader;
        VAR string sMsg{5};
        VAR btnres nAnswer;
        VAR robtarget pTCP;
        VAR robtarget robtarLaser1;
        VAR robtarget robtarLaser2;
        VAR robtarget robtarLaser3;
        VAR robtarget robtarLaser4;

        sHeader:="Robot System"+" ("+GetTaskName()+")";
        sMsg{1}:=" Press Yes to run definition of";
        sMsg{2}:="               tool:  toolLaser.";
        sMsg{3}:=" Press No  to cancel.";
        sMsg{4}:="";
        sMsg{5}:="";
        UIMsgBox\Header:=sHeader,sMsg{1}\MsgLine2:=sMsg{2}\MsgLine3:=sMsg{3}\MsgLine4:=sMsg{4}\MsgLine5:=sMsg{5}\Buttons:=btnYesNo\Icon:=iconInfo\Result:=nAnswer;
        IF nAnswer=resNo THEN
            GOTO Calculate;
        ENDIF

        Stop\NoRegain;
        MoveAbsJ jtLaser1,v100,fine,toolLaser;
        Stop;
        MoveAbsJ jtLaser2,v100,fine,toolLaser;
        Stop;
        MoveAbsJ jtLaser3,v100,fine,toolLaser;
        Stop;
        MoveAbsJ jtLaser4,v100,fine,toolLaser;
        Stop;
        MoveAbsJ jtLaserZ,v100,fine,toolLaser;
        Stop;
        MoveAbsJ jtLaserX,v100,fine,toolLaser;
        Stop;

        Calculate:

        MToolTCPCalib jtLaser1,jtLaser2,jtLaser3,jtLaser4,toolLaser,nMaxErr,nMeanErr;
        !MToolRotCalib jtLaser4,jtLaserZ\XPos:=jtLaserX,toolLaser;
        TPErase;
        TPWrite " nMaxErr  ... "\Num:=nMaxErr;
        TPWrite " nMeanErr ... "\Num:=nMeanErr;
        robtarLaser1:=CalcRobT(jtLaser1,toolLaser);
        robtarLaser2:=CalcRobT(jtLaser2,toolLaser);
        robtarLaser3:=CalcRobT(jtLaser3,toolLaser);
        robtarLaser4:=CalcRobT(jtLaser4,toolLaser);
        TPWrite " Distance between point1 and point 4 is "\Num:=Distance(robtarLaser1.trans,robtarLaser4.trans);
        TPWrite " Distance between point2 and point 4 is "\Num:=Distance(robtarLaser2.trans,robtarLaser4.trans);
        TPWrite " Distance between point3 and point 4 is "\Num:=Distance(robtarLaser3.trans,robtarLaser4.trans);
        TPReadFK nUserInputFP,"",stEmpty,stEmpty,stEmpty,stEmpty,"OK";
        Stop;

        Calibrate:
        MoveAbsJ jtLaser4,v100,fine,toolLaser;
        pTCP:=CRobT(\Tool:=toolLaser);
        MoveL RelTool(pTCP,0,0,0),v100,fine,toolLaser;
        MoveL Reltool(pTCP,0,0,-70),v100,fine,toolLaser;
        MoveL Reltool(pTCP,0,0,5),v100,fine,toolLaser;

    ENDPROC

    PROC MoveSpecialPoint()
        MoveAbsJ jointHome,v1000,fine,toolWeldGun\WObj:=wobj0;
        Stop;
        MoveAbsJ jointOrigin,v1000,fine,toolWeldGun\WObj:=wobj0;
        Stop;
        MoveAbsJ jointTransportation,v1000,fine,toolWeldGun\WObj:=wobj0;
        Stop;
        MoveAbsJ jointLoadIdentify,speedAir,fine,toolWeldGun\WObj:=wobj0;
        Stop;
        MoveAbsJ jointCurrent,speedAir,fine,toolWeldGun\WObj:=wobj0;
        Stop;
        MoveJ robCurrent,speedAir,fine,toolWeldGun\WObj:=wobj0;
        Stop;
    ENDPROC

ENDMODULE