setstr -strvar $TMP_ARC -value $BOOTPATH
setstr -strvar $BOOTPATH -value "$HOME/RAATCfg"

config -filename $BOOTPATH/config/EIO_521701.cfg -domain EIO -replace
config -filename $BOOTPATH/config/SIO_521701.cfg -domain SIO -replace

config -filename $BOOTPATH/config/EIO_Virtual_ProductionManager.cfg -domain EIO -replace
config -filename $BOOTPATH/config/PROC_Virtual_ProductionManager.cfg -domain PROC -replace
config -filename $BOOTPATH/config/MMC_Virtual_ProductionManager.cfg -domain MMC -replace

config -filename $BOOTPATH/config/EIO_Virtual_SystemInOut.cfg -domain EIO -replace

config -filename $BOOTPATH/config/EIO_LocalIO.cfg -domain EIO -replace

config -filename $BOOTPATH/config/EIO_Virtual.cfg -domain EIO -replace
config -filename $BOOTPATH/config/PROC_Virtual.cfg -domain PROC -replace

config -filename $BOOTPATH/config/EIO_PN_Internal_Device.cfg -domain EIO -replace
config -filename $BOOTPATH/config/SIO_PN_Internal_Device.cfg -domain SIO -replace

config -filename $BOOTPATH/config/EIO_FroniusSmarTac.cfg -domain EIO -replace
config -filename $BOOTPATH/config/PROC_FroniusSmarTac.cfg -domain PROC -replace

config -filename $BOOTPATH/config/EIO_DN_521702.cfg -domain EIO -replace
#config -filename $BOOTPATH/config/EIO_DN_Internal_Device.cfg -domain EIO -replace

config -filename $BOOTPATH/config/PROC_TorchServices.cfg -domain PROC -replace

config -filename $BOOTPATH/config/SYS.cfg -domain SYS -replace

setstr -strvar $BOOTPATH -value "$TMP_ARC"