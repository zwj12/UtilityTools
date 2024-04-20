MODULE EquidistantSpiralModule

    PERS robtarget pHome:=[[-0.00,0.00,120.00],[2.80501E-9,1.54713E-9,1,6.25082E-10],[0,0,0,0],[0,9E+9,9E+9,9E+9,9E+9,9E+9]];
    PERS robtarget pAproach:=[[5.61002E-7,1.25016E-7,20],[2.80501E-9,1.54713E-9,1,6.25082E-10],[0,0,0,0],[0,9E+9,9E+9,9E+9,9E+9,9E+9]];
    PERS robtarget pFirst:=[[100,0,0],[1,0,0,0],[0,0,0,0],[0,9E+9,9E+9,9E+9,9E+9,9E+9]];
    PERS robtarget pNext:=[[414.159,0,20],[2.80501E-9,1.54713E-9,1,6.25082E-10],[0,0,0,0],[0,9E+9,9E+9,9E+9,9E+9,9E+9]];

    PERS robtarget pHomeSTN:=[[-0.00,0.00,120.00],[2.80501E-9,1.54713E-9,1,6.25082E-10],[0,0,0,0],[0,9E+9,9E+9,9E+9,9E+9,9E+9]];
    PERS robtarget pAproachSTN:=[[5.61002E-7,1.25016E-7,20],[2.80501E-9,1.54713E-9,1,6.25082E-10],[0,0,0,0],[0,9E+9,9E+9,9E+9,9E+9,9E+9]];
    PERS robtarget pFirstSTN:=[[100,0,20],[3.7494E-33,6.12323E-17,1,6.12323E-17],[0,0,0,0],[0,9E+9,9E+9,9E+9,9E+9,9E+9]];
    PERS robtarget pNextSTN:=[[414.159,0,20],[6.75271E-32,1.1028E-15,-1,-6.12323E-17],[0,0,0,0],[-1800,9E+9,9E+9,9E+9,9E+9,9E+9]];

    PERS pos posLayer1{36}:=[[100.2,17.6679,10],[97.2494,35.3959,20],[91.137,52.618,30],[81.9524,68.7663,40],[69.8881,83.2894,50],[55.236,95.6715,60],[38.3806,105.45,70],[19.7894,112.231,80],[0,115.708,90],[-20.3955,115.669,100],[-40.7683,112.01,110],[-60.472,104.741,120],[-78.8632,93.9854,130],[-95.3224,79.985,140],[-109.275,63.09,150],[-120.21,43.753,160],[-127.701,22.5171,170],[-131.416,0,180],[-131.138,-23.1232,190],[-126.771,-46.1408,200],[-118.344,-68.326,210],[-106.018,-88.96,220],[-90.0819,-107.355,230],[-70.9439,-122.879,240],[-49.1255,-134.971,250],[-25.2447,-143.17,260],[0,-147.124,270],[25.8509,-146.608,280],[51.5132,-141.531,290],[76.1799,-131.948,300],[99.0569,-118.051,310],[119.388,-100.179,320],[136.482,-78.7979,330],[149.732,-54.4979,340],[158.639,-27.9724,350],[162.832,0,360]];
    PERS pos posLayer2{36}:=[[162.077,28.5785,370],[156.292,56.8857,380],[145.551,84.0339,390],[130.084,109.154,400],[110.276,131.421,410],[86.6519,150.086,420],[59.8703,164.492,430],[30.7,174.109,440],[0,178.54,450],[-31.3062,177.546,460],[-62.2581,171.053,470],[-91.8879,159.154,480],[-119.251,142.117,490],[-143.454,120.373,500],[-163.689,94.5059,510],[-179.253,65.2428,520],[-189.578,33.4277,530],[-194.248,0,540],[-193.016,-34.0338,550],[-185.813,-67.6305,560],[-172.758,-99.7419,570],[-154.15,-129.348,580],[-130.469,-155.487,590],[-102.36,-177.293,600],[-70.6152,-194.014,610],[-36.1554,-205.047,620],[0,-209.956,630],[36.7615,-208.485,640],[73.003,-200.574,650],[107.596,-186.361,660],[139.444,-166.183,670],[167.52,-140.566,680],[190.896,-110.214,690],[208.774,-75.9877,700],[220.517,-38.883,710],[225.664,0,720]];
    PERS pos posLayer3{36}:=[[223.954,39.4892,730],[215.335,78.3754,740],[199.965,115.45,750],[178.216,149.541,760],[150.663,179.553,770],[118.068,204.499,780],[81.3601,223.535,790],[41.6107,235.986,800],[0,241.372,810],[-42.2168,239.424,820],[-83.7478,230.095,830],[-123.304,213.568,840],[-159.638,190.249,850],[-191.586,160.76,860],[-218.103,125.922,870],[-238.296,86.7325,880],[-251.455,44.3383,890],[-257.08,0,900],[-254.893,-44.9445,910],[-244.856,-89.1203,920],[-227.172,-131.158,930],[-202.282,-169.735,940],[-170.857,-203.619,950],[-133.776,-231.706,960],[-92.105,-253.056,970],[-47.066,-266.924,980],[0,-272.788,990],[47.6721,-270.362,1000],[94.4927,-259.617,1010],[139.012,-240.775,1020],[179.832,-214.315,1030],[215.652,-180.954,1040],[245.31,-141.63,1050],[267.817,-97.4774,1060],[282.394,-49.7937,1070],[288.496,0,1080]];
    PERS pos posLayer4{36}:=[[285.831,50.3998,1090],[274.377,99.8652,1100],[254.379,146.866,1110],[226.348,189.929,1120],[191.051,227.685,1130],[149.484,258.913,1140],[102.85,282.578,1150],[52.5213,297.863,1160],[0,304.203,1170],[-53.1275,301.301,1180],[-105.238,289.138,1190],[-154.72,267.982,1200],[-200.026,238.381,1210],[-239.718,201.148,1220],[-272.517,157.338,1230],[-297.338,108.222,1240],[-313.332,55.249,1250],[-319.911,0,1260],[-316.77,-55.8551,1270],[-303.899,-110.61,1280],[-281.586,-162.574,1290],[-250.414,-210.123,1300],[-211.245,-251.751,1310],[-165.192,-286.12,1320],[-113.595,-312.099,1330],[-57.9766,-328.802,1340],[0,-335.619,1350],[58.5828,-332.239,1360],[115.982,-318.659,1370],[170.428,-295.189,1380],[220.22,-262.447,1390],[263.784,-221.341,1400],[299.724,-173.046,1410],[326.86,-118.967,1420],[344.271,-60.7043,1430],[351.327,0,1440]];
    PERS pos posLayer5{36}:=[[347.709,61.3104,1450],[333.42,121.355,1460],[308.793,178.282,1470],[274.48,230.316,1480],[231.438,275.817,1490],[180.9,313.327,1500],[124.34,341.62,1510],[63.4319,359.74,1520],[0,367.035,1530],[-64.0381,363.178,1540],[-126.727,348.181,1550],[-186.136,322.396,1560],[-240.413,286.513,1570],[-287.85,241.535,1580],[-326.931,188.754,1590],[-356.381,129.712,1600],[-375.21,66.1596,1610],[-382.743,0,1620],[-378.647,-66.7658,1630],[-362.941,-132.1,1640],[-336,-193.99,1650],[-298.546,-250.51,1660],[-251.632,-299.883,1670],[-196.608,-340.534,1680],[-135.085,-371.142,1690],[-68.8873,-390.679,1700],[0,-398.451,1710],[69.4934,-394.117,1720],[137.472,-377.702,1730],[201.844,-349.603,1740],[260.607,-310.579,1750],[311.916,-261.729,1760],[354.138,-204.462,1770],[385.902,-140.457,1780],[406.148,-71.6149,1790],[414.159,0,1800]];
    PERS pos posLayer6{36}:=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]];
    PERS pos posLayer7{36}:=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]];
    PERS pos posLayer8{36}:=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]];
    PERS pos posLayer9{36}:=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]];
    PERS pos posLayer10{36}:=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]];

    PERS num numStartRadius:=100;
    PERS num numPitch:=10;
    PERS num numLayerQuantity:=5;
    PERS num numFirstLayerStartIndex:=1;
    PERS num numLastLayerStopIndex:=36;
    PERS speeddata speedWeld:=[500,500,5000,1000];
    PERS zonedata zoneWeld:=[FALSE,100,150,150,15,150,15];

    PROC main()
        speedWeld:=v500;
        zoneWeld:=z100;
        ActUnit M7DM1;
        !        SpiralStationary;
        SpiralCoordinated;
    ENDPROC

    PROC SpiralCoordinated()
        VAR pos posLayerCur{36};        

        !        TPReadNum numStartRadius,"Please input the inner radius:";
        !        TPReadNum numPitch,"Please input the layer interval distance:";
        !        TPReadNum numLayerQuantity,"Please input the layer count:";
        !        numStartRadius:=UINumEntry(\Header:="Inner Radius"\Message:="Please input the inner radius:"\Icon:=iconQuestion\InitValue:=numStartRadius\MinValue:=0);
        !        numPitch:=UINumEntry(\Header:="Interval Distances"\Message:="Please input the layer interval distance:"\Icon:=iconQuestion\InitValue:=numPitch\MinValue:=1);
        !        numLayerQuantity:=UINumEntry(\Header:="Layer Count"\Message:="Please input the layer count:"\Icon:=iconQuestion\InitValue:=numLayerQuantity\MinValue:=2\AsInteger);

        SetDO sdoTCPTrace,0;
        MoveJ pHomeSTN,v1000,fine,tWeldGun\WObj:=wobjSTN;
        pAproachSTN:=RelTool(pHomeSTN,0,0,100);
        pFirstSTN:=pAproachSTN;
        pNextSTN:=pAproachSTN;
        !        Stop;

        InitEquidistantSpiralCurve numStartRadius,numPitch,numLayerQuantity;
        pFirstSTN.trans.z:=pAproachSTN.trans.z;
        pFirstSTN.rot:=OrientZYX(180-pFirstSTN.extax.eax_a,0,180);

        MoveL pFirstSTN,speedWeld,fine,tWeldGun\WObj:=wobjSTN;
        SetDO sdoTCPTrace,1;
        FOR i FROM numFirstLayerStartIndex TO 36 DO
            pNextSTN.trans.x:=posLayer1{i}.x;
            pNextSTN.trans.y:=posLayer1{i}.y;
            pNextSTN.extax.eax_a:=0-posLayer1{i}.z;
            pNextSTN.rot:=OrientZYX(180-pNextSTN.extax.eax_a,0,180);
            MoveL pNextSTN,speedWeld,zoneWeld,tWeldGun\WObj:=wobjSTN;
        ENDFOR

        IF numLayerQuantity>2 THEN
            FOR LayerIndex FROM 2 TO numLayerQuantity-1 DO
                GetDataVal "posLayer"+ValToStr(LayerIndex),posLayerCur;
                FOR i FROM 1 TO 36 DO
                    pNextSTN.trans.x:=posLayerCur{i}.x;
                    pNextSTN.trans.y:=posLayerCur{i}.y;
                    pNextSTN.extax.eax_a:=0-posLayerCur{i}.z;
                    pNextSTN.rot:=OrientZYX(180-pNextSTN.extax.eax_a,0,180);
                    MoveL pNextSTN,speedWeld,zoneWeld,tWeldGun\WObj:=wobjSTN;
                ENDFOR
                GetDataVal "posLayer"+ValToStr(LayerIndex),posLayerCur;
            ENDFOR
        ENDIF

        GetDataVal "posLayer"+ValToStr(numLayerQuantity),posLayerCur;
        FOR i FROM 1 TO numLastLayerStopIndex DO
            pNextSTN.trans.x:=posLayerCur{i}.x;
            pNextSTN.trans.y:=posLayerCur{i}.y;
            pNextSTN.extax.eax_a:=0-posLayerCur{i}.z;
            pNextSTN.rot:=OrientZYX(180-pNextSTN.extax.eax_a,0,180);
            IF i=numLastLayerStopIndex THEN
                MoveL pNextSTN,speedWeld,fine,tWeldGun\WObj:=wobjSTN;
                SetDO sdoTCPTrace,0;
            ELSE
                MoveL pNextSTN,speedWeld,zoneWeld,tWeldGun\WObj:=wobjSTN;
            ENDIF

        ENDFOR

        !        Stop;
        MoveJ pHomeSTN,v1000,fine,tWeldGun\WObj:=wobjSTN;

    UNDO
        SetDO sdoTCPTrace,0;
    ENDPROC

    PROC SpiralStationary()
        VAR pos posLayerCur{36};

        !        TPReadNum numStartRadius,"Please input the inner radius:";
        !        TPReadNum numPitch,"Please input the layer interval distance:";
        !        TPReadNum numLayerQuantity,"Please input the layer count:";
        !        numStartRadius:=UINumEntry(\Header:="Inner Radius"\Message:="Please input the inner radius:"\Icon:=iconQuestion\InitValue:=numStartRadius\MinValue:=0);
        !        numPitch:=UINumEntry(\Header:="Interval Distances"\Message:="Please input the layer interval distance:"\Icon:=iconQuestion\InitValue:=numPitch\MinValue:=1);
        !        numLayerQuantity:=UINumEntry(\Header:="Layer Count"\Message:="Please input the layer count:"\Icon:=iconQuestion\InitValue:=numLayerQuantity\MinValue:=2\AsInteger);

        SetDO sdoTCPTrace,0;
        MoveJ pHome,v1000,fine,tWeldGun\WObj:=WobjPlate;
        pAproach:=RelTool(pHome,0,0,100);
        pFirst:=pAproach;
        pNext:=pAproach;
        !        Stop;

        InitEquidistantSpiralCurve numStartRadius,numPitch,numLayerQuantity;
        pFirst.trans.z:=pAproach.trans.z;

        MoveL pFirst,speedWeld,fine,tWeldGun\WObj:=WobjPlate;
        SetDO sdoTCPTrace,1;
        FOR i FROM numFirstLayerStartIndex TO 36 DO
            pNext.trans.x:=posLayer1{i}.x;
            pNext.trans.y:=posLayer1{i}.y;
            MoveL pNext,speedWeld,zoneWeld,tWeldGun\WObj:=WobjPlate;
        ENDFOR

        IF numLayerQuantity>2 THEN
            FOR LayerIndex FROM 2 TO numLayerQuantity-1 DO
                GetDataVal "posLayer"+ValToStr(LayerIndex),posLayerCur;
                FOR i FROM 1 TO 36 DO
                    pNext.trans.x:=posLayerCur{i}.x;
                    pNext.trans.y:=posLayerCur{i}.y;
                    MoveL pNext,speedWeld,zoneWeld,tWeldGun\WObj:=WobjPlate;
                ENDFOR
                GetDataVal "posLayer"+ValToStr(LayerIndex),posLayerCur;
            ENDFOR
        ENDIF

        GetDataVal "posLayer"+ValToStr(numLayerQuantity),posLayerCur;
        FOR i FROM 1 TO numLastLayerStopIndex DO
            pNext.trans.x:=posLayerCur{i}.x;
            pNext.trans.y:=posLayerCur{i}.y;
            IF i=numLastLayerStopIndex THEN
                MoveL pNext,speedWeld,fine,tWeldGun\WObj:=WobjPlate;
                SetDO sdoTCPTrace,0;
            ELSE
                MoveL pNext,speedWeld,zoneWeld,tWeldGun\WObj:=WobjPlate;
            ENDIF

        ENDFOR

        !        Stop;
        MoveJ pHome,v1000,fine,tWeldGun\WObj:=WobjPlate;

    UNDO
        SetDO sdoTCPTrace,0;
    ENDPROC

    PROC InitEquidistantSpiralCurve(num StartRadius,num Pitch,num LayerCount\num StartTheta\num StopTheta)
        VAR num trimStartTheta:=0;
        VAR num addStopTheta:=360;
        VAR num theta;
        VAR num pointQuantity;
        VAR pos posLayerCur{36};
        LayerCount:=Round(LayerCount);
        IF StartRadius<0 THEN
            TPWrite "Start radius can't be lower than 0";
            RETURN ;
        ELSEIF Pitch<=0 THEN
            TPWrite "Pitch must be greater than 0";
            RETURN ;
        ELSEIF LayerCount<=1 THEN
            TPWrite "Layer Count must be greater than 1";
            RETURN ;
        ENDIF
        IF Present(StartTheta) THEN
            IF StartTheta<0 OR StartTheta>=360 THEN
                TPWrite "Start angle must be between 0 and 360(exclude 360)";
                RETURN ;
            ENDIF
            trimStartTheta:=trimStartTheta;
        ENDIF
        IF Present(StopTheta) THEN
            IF StopTheta<=0 OR StopTheta>360 THEN
                TPWrite "Start angle must be between 0 and 360(exclude 0)";
                RETURN ;
            ENDIF
            addStopTheta:=StopTheta;
        ENDIF

        pFirst.trans:=GetEquidistantSpiralPos(StartRadius,Pitch,trimStartTheta);
        pFirst.extax.eax_a:=0-trimStartTheta;
        pFirstSTN.trans:=GetEquidistantSpiralPos(StartRadius,Pitch,trimStartTheta);
        pFirstSTN.extax.eax_a:=0-trimStartTheta;
        numFirstLayerStartIndex:=Trunc(trimStartTheta/10)+1;
        FOR i FROM numFirstLayerStartIndex TO 36 DO
            posLayer1{i}:=GetEquidistantSpiralPos(StartRadius,Pitch,i*10);
        ENDFOR

        IF LayerCount>2 THEN
            FOR LayerIndex FROM 2 TO LayerCount-1 DO
                FOR i FROM 1 TO 36 DO
                    posLayerCur{i}:=GetEquidistantSpiralPos(StartRadius,Pitch,i*10+(LayerIndex-1)*360);
                ENDFOR
                SetDataVal "posLayer"+ValToStr(LayerIndex),posLayerCur;
            ENDFOR
        ENDIF

        numLastLayerStopIndex:=36-Trunc((360-addStopTheta)/10);
        FOR i FROM 1 TO numLastLayerStopIndex DO
            IF i=numLastLayerStopIndex THEN
                posLayerCur{i}:=GetEquidistantSpiralPos(StartRadius,Pitch,addStopTheta+(LayerCount-1)*360);
            ELSE
                posLayerCur{i}:=GetEquidistantSpiralPos(StartRadius,Pitch,i*10+(LayerCount-1)*360);
            ENDIF
        ENDFOR
        SetDataVal "posLayer"+ValToStr(LayerCount),posLayerCur;

    ENDPROC

    FUNC pos GetEquidistantSpiralPos(num StartRadius,num Pitch,num Theta)
        VAR num radius;
        VAR pos spiralPos;
        radius:=StartRadius+Pitch*Theta/180*pi;
        spiralPos.x:=radius*cos(Theta);
        spiralPos.y:=radius*sin(Theta);
        spiralPos.z:=Theta;
        RETURN spiralPos;
    ENDFUNC

ENDMODULE