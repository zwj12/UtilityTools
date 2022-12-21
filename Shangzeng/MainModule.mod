MODULE MainModule
    PERS wobjdata wobjProcess:=[FALSE,TRUE,"",[[0,0,0],[1,0,0,0]],[[0,0,0],[1,0,0,0]]];
    PERS tooldata toolProcess:=[TRUE,[[0,0,0],[1,0,0,0]],[0.001,[0,0,0.001],[1,0,0,0],0,0,0]];
    PERS speeddata speedProcess:=[200,500,5000,1000];
    PERS robtarget pHome:=[[-1613.47,-251.20,4031.75],[0.0465563,-0.823272,0.56531,-0.0219248],[-1,-1,0,0],[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]];
    PERS robtarget pNext:=[[0.36,-8.81746E-17,-0.82],[-4.32978E-17,0.707107,0.707107,4.32978E-17],[0,-1,-2,0],[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]];

    PERS num numRobotStatus:=1;
    PERS bool boolStart:=FALSE;
    PERS bool boolStop:=FALSE;
    PERS robtarget processTarget{1000};
    PERS num numTargetsCount:=60;

    PERS robtarget p1:=[[-1248.41,-251.20,2085.35],[0.0465545,-0.823272,0.56531,-0.0219229],[-1,-1,0,0],[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]];
    PERS robtarget p2:=[[-1639.45,-121.81,2085.35],[0.046555,-0.823268,0.565316,-0.0219238],[-1,-1,0,0],[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]];
    PERS robtarget p3:=[[-2177.82,-538.51,2085.34],[0.046556,-0.823271,0.565311,-0.0219246],[-1,-1,0,0],[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]];
    PERS robtarget p4:=[[-1761.41,-944.38,2085.34],[0.0465569,-0.823275,0.565305,-0.0219246],[-1,-1,1,0],[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]];
    PERS robtarget p5:=[[-1140.40,-935.74,2085.34],[0.046556,-0.823277,0.565303,-0.0219243],[-1,0,1,0],[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]];

    PROC main()
        SetTPHandlerLogLevel\DEBUG;
        SetFileHandlerLogLevel\DEBUG;

        speedProcess:=v200;
        boolStop:=FALSE;
        boolStart:=FALSE;
        numRobotStatus:=0;

        processTarget{1}:=p1;
        processTarget{2}:=p2;
        processTarget{3}:=p3;
        processTarget{4}:=p4;
        processTarget{5}:=p5;

        WHILE TRUE DO
            IF boolStart THEN
                numRobotStatus:=1;
                boolStop:=FALSE;
                boolStart:=FALSE;

                MoveJ pHome,speedProcess,fine,toolProcess\WObj:=wobjProcess;
                Job1;
                MoveJ pHome,speedProcess,fine,toolProcess\WObj:=wobjProcess;

                numRobotStatus:=0;
            ENDIF

            WaitTime 1;
        ENDWHILE

    ENDPROC

    PROC Job1()
        FOR index FROM 1 TO numTargetsCount DO
            IF boolStop THEN
                boolStop:=FALSE;
                Logging "Stop robot by external command";
                RETURN ;
            ENDIF
            Logging "Moving to target: "+ValToStr(index);
            pNext:=processTarget{index};
            MoveL pNext,speedProcess,z0,toolProcess\WObj:=wobjProcess;
        ENDFOR
    ENDPROC

    PROC TestTargets()
        MoveJ pHome,speedProcess,fine,toolProcess\WObj:=wobjProcess;

        MoveL p1,speedProcess,fine,toolProcess\WObj:=wobjProcess;
        MoveL p2,speedProcess,fine,toolProcess\WObj:=wobjProcess;
        MoveL p3,speedProcess,fine,toolProcess\WObj:=wobjProcess;
        MoveL p4,speedProcess,fine,toolProcess\WObj:=wobjProcess;
        MoveL p5,speedProcess,fine,toolProcess\WObj:=wobjProcess;

        MoveJ pHome,speedProcess,fine,toolProcess\WObj:=wobjProcess;

        processTarget{1}:=p1;
        processTarget{2}:=p2;
        processTarget{3}:=p3;
        processTarget{4}:=p4;
        processTarget{5}:=p5;

    ENDPROC
ENDMODULE