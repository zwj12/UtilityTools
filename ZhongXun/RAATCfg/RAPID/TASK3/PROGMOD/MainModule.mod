MODULE MainModule
    !*****************************************************
    !Module Name:   MainModule
    !Version:       1.0
    !Description:
    !Date:          2023-7-1
    !Author:        Michael
    !*****************************************************

    PERS num numGantryCollisionDistance:=-1;
    !strDeviceName: DN_Internal_Device or DN521702
    PERS string strDeviceName:="DN521702";

    TASK PERS jointtarget jointCurrent:=[[0,-60,40,0,60,0],[0,0,-500,9E+9,9E+9,9E+9]];
    TASK PERS num numTaskIdleTime:=0.05;

    PROC main()
        WHILE TRUE DO
            jointCurrent:=CJointT(\TaskName:="T_ROB1");

            IF Abs(jointCurrent.extax.eax_a)>=-32767 AND Abs(jointCurrent.extax.eax_a)<=32767 THEN
                SetAO Ao144_GantryX,Round(jointCurrent.extax.eax_a);
            ELSE
                SetAO Ao144_GantryX,-32768;
            ENDIF
            IF Abs(jointCurrent.extax.eax_b)>=-32767 AND Abs(jointCurrent.extax.eax_b)<=32767 THEN
                SetAO Ao160_GantryY,Round(jointCurrent.extax.eax_b);
            ELSE
                SetAO Ao160_GantryY,-32768;
            ENDIF
            IF Abs(jointCurrent.extax.eax_c)>=-32767 AND Abs(jointCurrent.extax.eax_c)<=32767 THEN
                SetAO Ao176_GantryZ,Round(jointCurrent.extax.eax_c);
            ELSE
                SetAO Ao176_GantryZ,-32768;
            ENDIF

            IF IOUnitState(strDeviceName\Phys)=IOUNIT_PHYS_STATE_RUNNING AND ValidIO(aoDNGantryX)=TRUE THEN
                IF Abs(jointCurrent.extax.eax_a)>=-32767 AND Abs(jointCurrent.extax.eax_a)<=32767 THEN
                    SetAO aoDNGantryX,Round(jointCurrent.extax.eax_a);
                ELSE
                    SetAO aoDNGantryX,-32768;
                ENDIF
                IF Abs(jointCurrent.extax.eax_b)>=-32767 AND Abs(jointCurrent.extax.eax_b)<=32767 THEN
                    SetAO aoDNGantryY,Round(jointCurrent.extax.eax_b);
                ELSE
                    SetAO aoDNGantryY,-32768;
                ENDIF
                IF Abs(jointCurrent.extax.eax_c)>=-32767 AND Abs(jointCurrent.extax.eax_c)<=32767 THEN
                    SetAO aoDNGantryZ,Round(jointCurrent.extax.eax_c);
                ELSE
                    SetAO aoDNGantryZ,-32768;
                ENDIF
            ENDIF

            CollisionAvoidanceGantry;

            WaitTime numTaskIdleTime;
        ENDWHILE

    ENDPROC

    PROC CollisionAvoidanceGantry()
        IF RobOS()=FALSE THEN
            RETURN ;
        ENDIF
        IF IOUnitState(strDeviceName\Phys)<>IOUNIT_PHYS_STATE_RUNNING OR ValidIO(aoDNGantryX)=FALSE OR ValidIO(aiDNGantryX)=FALSE THEN
            SetDO sdoGantryCollision,1;
        ELSEIF Abs(AOutput(aoDNGantryX)-AInput(aiDNGantryX))<numGantryCollisionDistance THEN
            SetDO sdoGantryCollision,1;
        ELSE
            SetDO sdoGantryCollision,0;
        ENDIF

    ENDPROC
ENDMODULE