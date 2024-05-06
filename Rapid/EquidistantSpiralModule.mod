MODULE EquidistantSpiralModule

    PERS robtarget pHome:=[[-0.00,0.00,120.00],[2.80501E-9,1.54713E-9,1,6.25082E-10],[0,0,0,0],[0,9E+9,9E+9,9E+9,9E+9,9E+9]];
    PERS robtarget pAproach:=[[5.61002E-7,1.25016E-7,20],[2.80501E-9,1.54713E-9,1,6.25082E-10],[0,0,0,0],[0,9E+9,9E+9,9E+9,9E+9,9E+9]];
    PERS robtarget pFirst:=[[76.2643,76.2643,45],[1,0,0,0],[0,0,0,0],[-45,9E+9,9E+9,9E+9,9E+9,9E+9]];
    PERS robtarget pNext:=[[414.159,0,20],[2.80501E-9,1.54713E-9,1,6.25082E-10],[0,0,0,0],[0,9E+9,9E+9,9E+9,9E+9,9E+9]];

    PERS robtarget pHomeSTN:=[[-0.00,0.00,120.00],[2.80501E-9,1.54713E-9,1,6.25082E-10],[0,0,0,0],[0,9E+9,9E+9,9E+9,9E+9,9E+9]];
    PERS robtarget pAproachSTN:=[[5.61002E-7,1.25016E-7,20],[2.80501E-9,1.54713E-9,1,6.25082E-10],[0,0,0,0],[0,9E+9,9E+9,9E+9,9E+9,9E+9]];
    PERS robtarget pFirstSTN:=[[76.2643,76.2643,20],[2.34326E-17,0.382683,-0.92388,-5.65713E-17],[0,0,0,0],[-45,9E+9,9E+9,9E+9,9E+9,9E+9]];
    PERS robtarget pNextSTN:=[[253.98,253.98,20],[2.34326E-17,0.382683,-0.92388,-5.65713E-17],[0,0,0,0],[-1485,9E+9,9E+9,9E+9,9E+9,9E+9]];

    PERS pos posLayer1{36}:=[[100.2,17.6679,10],[97.2494,35.3959,20],[91.137,52.618,30],[81.9524,68.7663,40],[69.8881,83.2894,50],[55.236,95.6715,60],[38.3806,105.45,70],[19.7894,112.231,80],[0,115.708,90],[-20.3955,115.669,100],[-40.7683,112.01,110],[-60.472,104.741,120],[-78.8632,93.9854,130],[-95.3224,79.985,140],[-109.275,63.09,150],[-120.21,43.753,160],[-127.701,22.5171,170],[-131.416,0,180],[-131.138,-23.1232,190],[-126.771,-46.1408,200],[-118.344,-68.326,210],[-106.018,-88.96,220],[-90.0819,-107.355,230],[-70.9439,-122.879,240],[-49.1255,-134.971,250],[-25.2447,-143.17,260],[0,-147.124,270],[25.8509,-146.608,280],[51.5132,-141.531,290],[76.1799,-131.948,300],[99.0569,-118.051,310],[119.388,-100.179,320],[136.482,-78.7979,330],[149.732,-54.4979,340],[158.639,-27.9724,350],[162.832,0,360]];
    PERS pos posLayer2{36}:=[[162.077,28.5785,370],[156.292,56.8857,380],[145.551,84.0339,390],[130.084,109.154,400],[110.276,131.421,410],[86.6519,150.086,420],[59.8703,164.492,430],[30.7,174.109,440],[0,178.54,450],[-31.3062,177.546,460],[-62.2581,171.053,470],[-91.8879,159.154,480],[-119.251,142.117,490],[-143.454,120.373,500],[-163.689,94.5059,510],[-179.253,65.2428,520],[-189.578,33.4277,530],[-194.248,0,540],[-193.016,-34.0338,550],[-185.813,-67.6305,560],[-172.758,-99.7419,570],[-154.15,-129.348,580],[-130.469,-155.487,590],[-102.36,-177.293,600],[-70.6152,-194.014,610],[-36.1554,-205.047,620],[0,-209.956,630],[36.7615,-208.485,640],[73.003,-200.574,650],[107.596,-186.361,660],[139.444,-166.183,670],[167.52,-140.566,680],[190.896,-110.214,690],[208.774,-75.9877,700],[220.517,-38.883,710],[225.664,0,720]];
    PERS pos posLayer3{36}:=[[223.954,39.4892,730],[215.335,78.3754,740],[199.965,115.45,750],[178.216,149.541,760],[150.663,179.553,770],[118.068,204.499,780],[81.3601,223.535,790],[41.6107,235.986,800],[0,241.372,810],[-42.2168,239.424,820],[-83.7478,230.095,830],[-123.304,213.568,840],[-159.638,190.249,850],[-191.586,160.76,860],[-218.103,125.922,870],[-238.296,86.7325,880],[-251.455,44.3383,890],[-257.08,0,900],[-254.893,-44.9445,910],[-244.856,-89.1203,920],[-227.172,-131.158,930],[-202.282,-169.735,940],[-170.857,-203.619,950],[-133.776,-231.706,960],[-92.105,-253.056,970],[-47.066,-266.924,980],[0,-272.788,990],[47.6721,-270.362,1000],[94.4927,-259.617,1010],[139.012,-240.775,1020],[179.832,-214.315,1030],[215.652,-180.954,1040],[245.31,-141.63,1050],[267.817,-97.4774,1060],[282.394,-49.7937,1070],[288.496,0,1080]];
    PERS pos posLayer4{36}:=[[285.831,50.3998,1090],[274.377,99.8652,1100],[254.379,146.866,1110],[226.348,189.929,1120],[191.051,227.685,1130],[149.484,258.913,1140],[102.85,282.578,1150],[52.5213,297.863,1160],[0,304.203,1170],[-53.1275,301.301,1180],[-105.238,289.138,1190],[-154.72,267.982,1200],[-200.026,238.381,1210],[-239.718,201.148,1220],[-272.517,157.338,1230],[-297.338,108.222,1240],[-313.332,55.249,1250],[-319.911,0,1260],[-316.77,-55.8551,1270],[-303.899,-110.61,1280],[-281.586,-162.574,1290],[-250.414,-210.123,1300],[-211.245,-251.751,1310],[-165.192,-286.12,1320],[-113.595,-312.099,1330],[-57.9766,-328.802,1340],[0,-335.619,1350],[58.5828,-332.239,1360],[115.982,-318.659,1370],[170.428,-295.189,1380],[220.22,-262.447,1390],[263.784,-221.341,1400],[299.724,-173.046,1410],[326.86,-118.967,1420],[344.271,-60.7043,1430],[351.327,0,1440]];
    PERS pos posLayer5{36}:=[[347.709,61.3104,1450],[333.42,121.355,1460],[308.793,178.282,1470],[274.48,230.316,1480],[253.98,253.98,1485],[149.484,258.913,1140],[102.85,282.578,1150],[52.5213,297.863,1160],[0,304.203,1170],[-53.1275,301.301,1180],[-105.238,289.138,1190],[-154.72,267.982,1200],[-200.026,238.381,1210],[-239.718,201.148,1220],[-272.517,157.338,1230],[-297.338,108.222,1240],[-313.332,55.249,1250],[-319.911,0,1260],[-316.77,-55.8551,1270],[-303.899,-110.61,1280],[-281.586,-162.574,1290],[-250.414,-210.123,1300],[-211.245,-251.751,1310],[-165.192,-286.12,1320],[-113.595,-312.099,1330],[-57.9766,-328.802,1340],[0,-335.619,1350],[58.5828,-332.239,1360],[115.982,-318.659,1370],[170.428,-295.189,1380],[220.22,-262.447,1390],[263.784,-221.341,1400],[299.724,-173.046,1410],[326.86,-118.967,1420],[344.271,-60.7043,1430],[351.327,0,1440]];
    PERS pos posLayer6{36}:=[[254.033,44.7929,1810],[243.216,88.5233,1820],[224.905,129.849,1830],[199.608,167.491,1840],[168.052,200.277,1850],[131.158,227.172,1860],[90.0157,247.316,1870],[45.8537,260.049,1880],[0,264.934,1890],[-46.1568,261.768,1900],[-91.2096,250.596,1910],[-133.776,231.706,1920],[-172.54,205.625,1930],[-206.293,173.101,1940],[-233.974,135.085,1950],[-254.696,92.7019,1960],[-267.784,47.2175,1970],[-272.788,0,1980],[-269.503,-47.5206,1990],[-257.977,-93.8958,2000],[-238.508,-137.703,2010],[-211.641,-177.588,2020],[-178.149,-212.31,2030],[-139.012,-240.775,2040],[-95.3881,-262.077,2050],[-48.5814,-275.519,2060],[0,-280.642,2070],[48.8844,-277.237,2080],[96.582,-265.357,2090],[141.63,-245.31,2100],[182.637,-217.658,2110],[218.326,-183.198,2120],[247.577,-142.939,2130],[269.457,-98.0743,2140],[283.253,-49.9452,2150],[288.496,0,2160]];
    PERS pos posLayer7{36}:=[[284.972,50.2483,2170],[272.737,99.2682,2180],[252.112,145.557,2190],[223.674,187.685,2200],[188.246,224.343,2210],[146.866,254.379,2220],[100.761,276.837,2230],[51.309,290.988,2240],[0,296.35,2250],[-51.6121,292.707,2260],[-101.954,280.118,2270],[-149.484,258.913,2280],[-192.734,229.691,2290],[-230.359,193.295,2300],[-261.181,150.793,2310],[-284.218,103.447,2320],[-298.723,52.6728,2330],[-304.203,0,2340],[-300.441,-52.9759,2350],[-287.498,-104.641,2360],[-265.715,-153.411,2370],[-235.707,-197.782,2380],[-198.343,-236.376,2390],[-154.72,-267.982,2400],[-106.133,-291.598,2410],[-54.0367,-306.457,2420],[0,-312.057,2430],[54.3398,-308.176,2440],[107.327,-294.878,2450],[157.338,-272.517,2460],[202.83,-241.724,2470],[242.392,-203.391,2480],[274.784,-158.647,2490],[298.978,-108.819,2500],[314.192,-55.4005,2510],[319.911,0,2520]];
    PERS pos posLayer8{36}:=[[315.911,55.7036,2530],[302.259,110.013,2540],[279.319,161.265,2550],[247.74,207.879,2560],[208.44,248.409,2570],[162.574,281.586,2580],[111.505,306.359,2590],[56.7643,321.927,2600],[0,327.765,2610],[-57.0674,323.645,2620],[-112.699,309.639,2630],[-165.192,286.12,2640],[-212.927,253.757,2650],[-254.425,213.488,2660],[-288.388,166.501,2670],[-313.739,114.192,2680],[-329.661,58.1282,2690],[-335.619,0,2700],[-331.38,-58.4312,2710],[-317.019,-115.386,2720],[-292.922,-169.119,2730],[-259.773,-217.976,2740],[-218.537,-260.442,2750],[-170.428,-295.189,2760],[-116.878,-321.119,2770],[-59.492,-337.396,2780],[0,-343.473,2790],[59.7951,-339.115,2800],[118.072,-324.4,2810],[173.046,-299.724,2820],[223.024,-265.79,2830],[266.458,-223.585,2840],[301.991,-174.355,2850],[328.5,-119.564,2860],[345.131,-60.8558,2870],[351.327,0,2880]];
    PERS pos posLayer9{36}:=[[346.849,61.1589,2890],[331.78,120.758,2900],[306.526,176.973,2910],[271.806,228.073,2920],[228.634,272.475,2930],[178.282,308.793,2940],[122.25,335.88,2950],[62.2197,352.865,2960],[0,359.181,2970],[-62.5227,354.584,2980],[-123.444,339.16,2990],[-180.9,313.327,3000],[-233.121,277.823,3010],[-278.491,233.682,3020],[-315.595,182.209,3030],[-343.26,124.937,3040],[-360.6,63.5835,3050],[-367.035,0,3060],[-362.319,-63.8866,3070],[-346.54,-126.13,3080],[-320.129,-184.827,3090],[-283.839,-238.17,3100],[-238.73,-284.508,3110],[-186.136,-322.396,3120],[-127.623,-350.641,3130],[-64.9473,-368.335,3140],[0,-374.889,3150],[65.2504,-370.053,3160],[128.817,-353.921,3170],[188.754,-326.931,3180],[243.218,-289.856,3190],[290.524,-243.779,3200],[329.198,-190.063,3210],[358.021,-130.309,3220],[376.069,-66.3111,3230],[382.743,0,3240]];
    PERS pos posLayer10{36}:=[[377.788,66.6142,3250],[361.301,131.503,3260],[333.733,192.681,3270],[295.872,248.266,3280],[248.827,296.541,3290],[193.99,336,3300],[132.995,365.401,3310],[67.675,383.804,3320],[0,390.597,3330],[-67.9781,385.523,3340],[-134.189,368.681,3350],[-196.608,340.534,3360],[-253.315,301.889,3370],[-302.557,253.876,3380],[-342.802,197.917,3390],[-372.782,135.681,3400],[-391.538,69.0388,3410],[-398.451,0,3420],[-393.257,-69.3419,3430],[-376.062,-136.875,3440],[-347.336,-200.535,3450],[-307.905,-258.363,3460],[-258.924,-308.574,3470],[-201.844,-349.603,3480],[-138.368,-380.162,3490],[-70.4026,-399.273,3500],[0,-406.305,3510],[70.7057,-400.992,3520],[139.562,-383.442,3530],[204.462,-354.138,3540],[263.412,-313.922,3550],[314.59,-263.973,3560],[356.405,-205.771,3570],[387.542,-141.054,3580],[407.008,-71.7665,3590],[414.159,0,3600]];
    PERS pos posLayerNext{37}:=[[377.788,66.6142,3250],[377.788,66.6142,3250],[361.301,131.503,3260],[333.733,192.681,3270],[295.872,248.266,3280],[248.827,296.541,3290],[193.99,336,3300],[132.995,365.401,3310],[67.675,383.804,3320],[0,390.597,3330],[-67.9781,385.523,3340],[-134.189,368.681,3350],[-196.608,340.534,3360],[-253.315,301.889,3370],[-302.557,253.876,3380],[-342.802,197.917,3390],[-372.782,135.681,3400],[-391.538,69.0388,3410],[-398.451,0,3420],[-393.257,-69.3419,3430],[-376.062,-136.875,3440],[-347.336,-200.535,3450],[-307.905,-258.363,3460],[-258.924,-308.574,3470],[-201.844,-349.603,3480],[-138.368,-380.162,3490],[-70.4026,-399.273,3500],[0,-406.305,3510],[70.7057,-400.992,3520],[139.562,-383.442,3530],[204.462,-354.138,3540],[263.412,-313.922,3550],[314.59,-263.973,3560],[356.405,-205.771,3570],[387.542,-141.054,3580],[407.008,-71.7665,3590],[414.159,0,3600]];

    PERS num numStartRadius:=100;
    PERS num numPitch:=10;
    PERS num numLayerQuantity:=5;
    PERS num numFirstLayerStartIndex:=5;
    PERS num numLastLayerStopIndex:=5;
    PERS num numStartAngle:=45;
    PERS num numStopAngle:=45;

    PERS speeddata speedWeld:=[500,500,5000,1000];
    PERS speeddata speedAir:=[7000,500,5000,1000];
    PERS zonedata zoneWeld:=[FALSE,100,150,150,15,150,15];

    PROC main()
        speedAir:=vmax;
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
        MoveJ pHomeSTN,speedAir,fine,tWeldGun\WObj:=wobjSTN;
        pAproachSTN:=RelTool(pHomeSTN,0,0,100);
        pFirstSTN:=pAproachSTN;
        pNextSTN:=pAproachSTN;
        !        Stop;

        InitEquidistantSpiralCurve numStartRadius,numPitch,numLayerQuantity\StartTheta:=numStartAngle\StopTheta:=numStopAngle;
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

        Stop;
        MoveJ pHomeSTN,speedAir,fine,tWeldGun\WObj:=wobjSTN;

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
        MoveJ pHome,speedAir,fine,tWeldGun\WObj:=WobjPlate;
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
        MoveJ pHome,speedAir,fine,tWeldGun\WObj:=WobjPlate;

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
            trimStartTheta:=StartTheta;
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