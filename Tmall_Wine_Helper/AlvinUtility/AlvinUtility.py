from datetime import *
import time

class AlvinUtility():
    @staticmethod
    def GetFileNameFromDate():
        return date.today()

    def Run(self,txt='hello'):
        return txt

#print(AlvinUtility.GetFileNameFromDate())