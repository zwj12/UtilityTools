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

    PERS num numHeartBeatInterval:=0.5;
    PERS num numHeartBeatStableTime:=0;
    VAR intnum intHeartBeat;
    VAR intnum intHeartBeatMonitor;
    VAR clock clockHeartBeatMonitor;

    PROC main()
        numHeartBeatStableTime:=0;
        ClkStart clockHeartBeatMonitor;

        IDelete intHeartBeat;
        CONNECT intHeartBeat WITH TRAPHeartBeat;
        ITimer numHeartBeatInterval,intHeartBeat;

        IDelete intHeartBeatMonitor;
        CONNECT intHeartBeatMonitor WITH TRAPHeartBeatMonitor;
        ISignalDI diDNHeartBeat,edge,intHeartBeatMonitor;

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

            IF numGantryCollisionDistance<>-1 THEN
                CollisionAvoidanceGantry;
            ENDIF

            WaitTime numTaskIdleTime;
        ENDWHILE

    ENDPROC

    PROC CollisionAvoidanceGantry()
        !        IF RobOS()=FALSE THEN
        !            RETURN ;
        !        ENDIF
        IF IOUnitState(strDeviceName\Phys)<>IOUNIT_PHYS_STATE_RUNNING OR ValidIO(aoDNGantryX)=FALSE OR ValidIO(aiDNGantryX)=FALSE THEN
            IF sdoGantryCollision<>1 THEN
                Logging "Gantry collision due to the signal is invalid.";
                SetDO sdoGantryCollision,1;
            ENDIF
        ELSEIF Abs(AOutput(aoDNGantryX)-AInput(aiDNGantryX))<numGantryCollisionDistance THEN
            IF sdoGantryCollision<>1 THEN
                Logging "Gantry collision due to the distance is too close.";
                SetDO sdoGantryCollision,1;
            ENDIF
        ELSE
            numHeartBeatStableTime:=ClkRead(clockHeartBeatMonitor);
            IF numHeartBeatStableTime>numHeartBeatInterval*4 THEN
                IF sdoGantryCollision<>1 THEN
                    Logging "Gantry collision due to miss heart beat.";
                    SetDO sdoGantryCollision,1;
                ENDIF
            ELSE
                IF sdoGantryCollision<>0 THEN
                    SetDO sdoGantryCollision,0;
                ENDIF
            ENDIF
        ENDIF

    ENDPROC

    TRAP TRAPHeartBeat
        IF IOUnitState(strDeviceName\Phys)=IOUNIT_PHYS_STATE_RUNNING OR ValidIO(doDNHeartBeat)=TRUE THEN
            InvertDO doDNHeartBeat;
        ENDIF
        !        IF RobOS()=FALSE THEN
        !            ClkReset clockHeartBeatMonitor;
        !        ENDIF
    ENDTRAP

    TRAP TRAPHeartBeatMonitor
        ClkReset clockHeartBeatMonitor;
    ENDTRAP

ENDMODULE