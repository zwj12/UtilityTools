MODULE SocketModuleShangZeng
    !*****************************************************
    !Module Name: SocketModuleShangZeng
    !Version:     1.0
    !Description:
    !Date:        2022-12-13
    !Author:      Michael
    !*****************************************************

    VAR socketdev socketServer;
    VAR socketdev socketClient;
    VAR string strIPAddressServer:="127.0.0.1";
    VAR num numPort:=3008;
    VAR string strIPAddressClient:="";
    VAR rawbytes raw_data_out;
    VAR rawbytes raw_data_in;

    !stringHeader: Only indexs from 1 to 128 can be set, the indexs from 129 to 256 are for response command
    CONST string stringHeader{256}:=["CloseConnection","SendData","Start","Stop","GetRobotStatus","ClearData","","",
        "","","","","","","","",
        "","","","","","","","",
        "","","","","","","","",
        "","","","","","","","",
        "","","","","","","","",
        "","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""];

    VAR num numDataInLength:=0;
    VAR num numMessageFormatError:=0;

    PERS string strDataTaskName:="T_ROB1";
    PERS num numRobotStatus:=1;
    PERS bool boolStart:=FALSE;
    PERS bool boolStop:=FALSE;
    PERS robtarget processTarget{1000};
    PERS num numTargetsCount:=60;

    VAR string strDataFileName:="shangzeng.txt";
    VAR iodev iodevDataFile;

    PROC main()
        SetTPHandlerLogLevel\DEBUG;
        SetFileHandlerLogLevel\DEBUG;
        IF RobOS()=TRUE THEN
            strIPAddressServer:="192.168.0.62";
            !strIPAddressServer:="127.0.0.1";
        ELSE
            strIPAddressServer:="10.137.68.253";
        ENDIF
        WHILE TRUE DO
            SocketCreate socketServer;
            SocketBind socketServer,strIPAddressServer,numPort;
            SocketListen socketServer;
            commandReceive;
            SocketClose socketServer;
            WaitTime 2;
        ENDWHILE
    ENDPROC

    PROC CommandReceive(\switch Network)
        VAR num commandIn;
        SocketAccept socketServer,socketClient\ClientAddress:=strIPAddressClient\Time:=WAIT_MAX;
        Logging\WARNING,\LoggerName:="SocketModule","Client "+strIPAddressClient+" is connected.";
        WHILE true DO
            numMessageFormatError:=0;
            ClearRawBytes raw_data_in;
            SocketReceive socketClient\RawData:=raw_data_in\Time:=WAIT_MAX;
            IF RawBytesLen(raw_data_in)>=8 THEN
                UnpackRawBytes raw_data_in\Network?Network,1,commandIn\IntX:=UDINT;
                UnpackRawBytes raw_data_in\Network?Network,5,numDataInLength\IntX:=UDINT;
                Logging\INFO,\LoggerName:="SocketModule","Command="+ValToStr(commandIn)+", RawBytesLen="+ValToStr(RawBytesLen(raw_data_in));
                IF RawBytesLen(raw_data_in)=numDataInLength+8 THEN
                    IF commandIn=0 THEN
                        ResponseSocketCommand 128;
                        SocketClose socketClient;
                        Logging\WARNING,\LoggerName:="SocketModule","The connection "+strIPAddressClient+" is closed!";
                        RETURN ;
                    ELSE
                        IF StrLen(stringHeader{commandIn+1})>0 THEN
                            Logging\DEBUG,\LoggerName:="SocketModule","Execute command "+ValToStr(commandIn+1)+" of "+stringHeader{commandIn+1};
                            %stringHeader{commandIn+1}%commandIn\Network?Network;
                        ELSE
                            numMessageFormatError:=3;
                        ENDIF
                    ENDIF
                ELSE
                    numMessageFormatError:=2;
                ENDIF
            ELSE
                numMessageFormatError:=1;
            ENDIF

            TEST numMessageFormatError
            CASE 1:
                Logging\ERRORING,\LoggerName:="SocketModule","The command ("+ValToStr(commandIn)+") message should be sent from client as a whole!";
                ResponseError commandIn;
            CASE 2:
                Logging\ERRORING,\LoggerName:="SocketModule","The command's ("+ValToStr(commandIn)+") data length ("+ValToStr(numDataInLength)+") is not right!";
                ResponseError commandIn;
            CASE 3:
                Logging\ERRORING,\LoggerName:="SocketModule","Command ("+ValToStr(commandIn)+") is not set in stringHeader!";
                ResponseError commandIn;
            DEFAULT:
            ENDTEST

        ENDWHILE

    ERROR
        IF ERRNO=ERR_SOCK_TIMEOUT OR ERRNO=ERR_SOCK_CLOSED THEN
            SocketClose socketClient;
            Logging\ERRORING,\LoggerName:="SocketModule","The connection "+strIPAddressClient+" is closed abnormally!";
            RETURN ;
        ELSEIF ERRNO=ERR_REFUNKPRC THEN
            Logging\ERRORING,\LoggerName:="SocketModule","ERR_REFUNKPRC!";
            TRYNEXT;
        ELSEIF ERRNO=ERR_CALLPROC THEN
            Logging\ERRORING,\LoggerName:="SocketModule","ERR_CALLPROC!";
            TRYNEXT;
        ENDIF
    ENDPROC

    PROC PackSocketHeader(num commandOut\switch Network)
        VAR rawbytes raw_data_temp;
        CopyRawBytes raw_data_out,1,raw_data_temp,1;
        ClearRawBytes raw_data_out;
        PackRawBytes commandOut,raw_data_out\Network?Network,1\IntX:=UDINT;
        PackRawBytes RawBytesLen(raw_data_temp),raw_data_out\Network?Network,5\IntX:=UDINT;
        CopyRawBytes raw_data_temp,1,raw_data_out,9;
    ENDPROC

    PROC ResponseSocketCommand(num commandOut\switch Network)
        ClearRawBytes raw_data_out;
        PackSocketHeader commandOut\Network?Network;
        SocketSend socketClient\RawData:=raw_data_out;
    ENDPROC

    PROC ResponseError(byte commandIn\switch Network)
        VAR byte commandOut;
        commandOut:=255;
        ClearRawBytes raw_data_out;
        PackSocketHeader commandOut\Network?Network;
        SocketSend socketClient\RawData:=raw_data_out;
    ENDPROC

    PROC Start(byte commandIn\switch Network)
        VAR byte commandOut;
        ClearRawBytes raw_data_out;
        commandOut:=commandIn+100;
        PackRawBytes 0,raw_data_out\Network?Network,1\IntX:=DINT;
        PackSocketHeader commandOut\Network?Network;
        SocketSend socketClient\RawData:=raw_data_out;
        boolStart:=TRUE;
        Logging\DEBUG,\LoggerName:="SocketModule",stringHeader{commandIn+1}+" : "+ValToStr(numRobotStatus);
    ENDPROC

    PROC SendData(byte commandIn\switch Network)
        VAR byte commandOut;
        VAR num numCount;
        VAR num numTemp;
        Close iodevDataFile;
        Open "HOME:"\File:=strDataFileName,iodevDataFile\Append;

        numCount:=numDataInLength/44;
        numTemp:=RawBytesLen(raw_data_in);
        Logging\DEBUG,\LoggerName:="SocketModule","numCount="+ValToStr(numCount)+", numDataInLength="+ValToStr(numDataInLength)+", numTemp="+ValToStr(numTemp);

        FOR i FROM 1 TO numCount DO
            UnpackRawBytes raw_data_in\Network?Network,(i-1)*44+9,numTemp\Float4;
            processTarget{numTargetsCount+i}.trans.x:=numTemp;
            UnpackRawBytes raw_data_in\Network?Network,(i-1)*44+4+9,numTemp\Float4;
            processTarget{numTargetsCount+i}.trans.y:=numTemp;
            UnpackRawBytes raw_data_in\Network?Network,(i-1)*44+8+9,numTemp\Float4;
            processTarget{numTargetsCount+i}.trans.z:=numTemp;
            UnpackRawBytes raw_data_in\Network?Network,(i-1)*44+12+9,numTemp\Float4;
            processTarget{numTargetsCount+i}.rot.q1:=numTemp;
            UnpackRawBytes raw_data_in\Network?Network,(i-1)*44+16+9,numTemp\Float4;
            processTarget{numTargetsCount+i}.rot.q2:=numTemp;
            UnpackRawBytes raw_data_in\Network?Network,(i-1)*44+20+9,numTemp\Float4;
            processTarget{numTargetsCount+i}.rot.q3:=numTemp;
            UnpackRawBytes raw_data_in\Network?Network,(i-1)*44+24+9,numTemp\Float4;
            processTarget{numTargetsCount+i}.rot.q4:=numTemp;
            UnpackRawBytes raw_data_in\Network?Network,(i-1)*44+28+9,numTemp\IntX:=DINT;
            processTarget{numTargetsCount+i}.robconf.cf1:=numTemp;
            UnpackRawBytes raw_data_in\Network?Network,(i-1)*44+32+9,numTemp\IntX:=DINT;
            processTarget{numTargetsCount+i}.robconf.cf4:=numTemp;
            UnpackRawBytes raw_data_in\Network?Network,(i-1)*44+36+9,numTemp\IntX:=DINT;
            processTarget{numTargetsCount+i}.robconf.cf6:=numTemp;
            UnpackRawBytes raw_data_in\Network?Network,(i-1)*44+40+9,numTemp\IntX:=DINT;
            processTarget{numTargetsCount+i}.robconf.cfx:=numTemp;

            Write iodevDataFile,CDate()+" "+CTime()+":"+"Target "+ValToStr(+numTargetsCount+i)+"=["\NoNewLine;
            Write iodevDataFile,ValToStr(processTarget{numTargetsCount+i}.trans)\NoNewLine;
            Write iodevDataFile,","+ValToStr(processTarget{numTargetsCount+i}.rot)\NoNewLine;
            Write iodevDataFile,","+ValToStr(processTarget{numTargetsCount+i}.robconf)\NoNewLine;
            Write iodevDataFile,",[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]]";
        ENDFOR
        numTargetsCount:=numTargetsCount+numCount;

        Close iodevDataFile;

        ClearRawBytes raw_data_out;
        commandOut:=commandIn+100;
        PackRawBytes 0,raw_data_out\Network?Network,1\IntX:=DINT;
        PackSocketHeader commandOut\Network?Network;
        SocketSend socketClient\RawData:=raw_data_out;
        Logging\DEBUG,\LoggerName:="SocketModule",stringHeader{commandIn+1}+" : numCount="+ValToStr(numCount);
    ENDPROC

    PROC Stop(byte commandIn\switch Network)
        VAR byte commandOut;
        ClearRawBytes raw_data_out;
        commandOut:=commandIn+100;
        PackRawBytes 0,raw_data_out\Network?Network,1\IntX:=DINT;
        PackSocketHeader commandOut\Network?Network;
        SocketSend socketClient\RawData:=raw_data_out;
        boolStop:=TRUE;
        Logging\DEBUG,\LoggerName:="SocketModule",stringHeader{commandIn+1}+" : numRobotStatus="+ValToStr(numRobotStatus);
    ENDPROC

    PROC GetRobotStatus(byte commandIn\switch Network)
        VAR byte commandOut;
        ClearRawBytes raw_data_out;
        commandOut:=commandIn+100;
        PackRawBytes 0,raw_data_out\Network?Network,1\IntX:=DINT;
        PackRawBytes numRobotStatus,raw_data_out\Network?Network,5\IntX:=DINT;
        PackSocketHeader commandOut\Network?Network;
        SocketSend socketClient\RawData:=raw_data_out;
        Logging\DEBUG,\LoggerName:="SocketModule",stringHeader{commandIn+1}+" : numRobotStatus="+ValToStr(numRobotStatus);
    ENDPROC

    PROC ClearData(byte commandIn\switch Network)
        VAR byte commandOut;
        ClearRawBytes raw_data_out;
        commandOut:=commandIn+100;
        PackRawBytes 0,raw_data_out\Network?Network,1\IntX:=DINT;
        PackSocketHeader commandOut\Network?Network;
        SocketSend socketClient\RawData:=raw_data_out;
        numTargetsCount:=0;
        Logging\DEBUG,\LoggerName:="SocketModule",stringHeader{commandIn+1}+" : numRobotStatus="+ValToStr(numRobotStatus);
    ENDPROC

ENDMODULE