import time

class ExternalSensorsUtility:
    def __init__(self):
        """__init__

        """
        super().__init__()
        self.MaxRecipeStatus = 100
    
    def GetRecipeStatus(self):
        if self.MaxRecipeStatus > 0:
            self.MaxRecipeStatus = self.MaxRecipeStatus - 1
        else:
            self.MaxRecipeStatus = 0

    def GetStrobeTime(self):
        return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
        
    def NewPosition(self, objects):
        pass

    def ShowPythonLog(self, log):
        print("ShowPythonLog: {log}")
        