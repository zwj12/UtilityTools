MODULE TestModule
    !*****************************************************
    !Module Name: TestModule
    !Version:     1.0
    !Description:
    !Date:        2021-1-6
    !Author:      Michael
    !*****************************************************

    !2021-8-11, Michael, Add GetBaseFramePosZ, DepartGantry, modify MoveGanrtyQuadrantByWobjCur


    TASK PERS jointtarget jointWeldGunPlaneXZ:=[[90,-45,45,0,-68,180],[-875,0,-600,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jointLaserPlaneXZ:=[[66.8628,-41.2321,43.0137,-5.46308E-05,-91.7816,113.137],[578.229,0,-600,9E+09,9E+09,9E+09]];

    PROC MoveWeldGunToGanrtyBaseXZ()
        jointCurrent:=CJointT();
        jointWeldGunPlaneXZ.extax.eax_a:=jointCurrent.extax.eax_a;
        MoveAbsJ jointWeldGunPlaneXZ,speedAir,fine,toolWeldGun\WObj:=wobj0;
        Stop;
    ENDPROC

    PROC RelToolTCP()
        toolWeldGun.tframe.trans:=PoseVect(toolWeldGunLast.tframe,[0,0,0]);
        Logging "tframe1="+ValToStr(toolWeldGun.tframe);
        toolWeldGun.tframe:=PoseMult(toolWeldGunLast.tframe,[[0,0,30],[1,0,0,0]]);
        Logging "tframe2="+ValToStr(toolWeldGun.tframe);
    ENDPROC

ENDMODULE