'''
    Utilities that are related to readme file creation about noting time
    You may only create the object, write times, and then delete it. No need to worry about others.
'''

from collections import OrderedDict
import time

# This Readme Util only helps with total and individual time
class ReadmeUtil:
    
    filestream = None
    timeTable = OrderedDict()
    ERROR = False
    TotalStartTime = None
    TotalEndTime = None
    
    def __init__(self):
        self.ERROR = True
    
    def __init__(self, filepath):
        # Create the file
        if filepath[-1] != '/':
            filepath += '/'
        filename = filepath + 'README.txt'
        self.filestream = open(filename, 'w')
        self.ERROR = False
        if not self.filestream:
            self.ERROR = True
            return
        # Nothing wrong, so keep up with the initialization
        self.timeTable = OrderedDict()
        self.TotalStartTime = time.time()
        
    # For each task, you should add both a start time and an end time
    ## Just treat this as add to time table
    def write(self, objectName, isStartTime=True):
        if self.ERROR: return False
        
        if objectName not in self.timeTable:
            self.timeTable[objectName] = dict()
        
        theTime = time.time()
        if isStartTime:
            self.timeTable[objectName]['startTime'] = theTime
        else:
            self.timeTable[objectName]['endTime'] = theTime
        #print(self.timeTable)
        self.saveFile()
        
        
    def saveFile(self):
        self.filestream.fseek(0, 0)
        self.TotalEndTime = time.time()
        # Total Start Time
        self.filestream.write("Total Start Time: " + time.strftime('%Y-%m-%d %H:%M:%S %z' , time.localtime(self.TotalStartTime)) + "\n\n")
        # Individual tasks' time
        for i in self.timeTable:
            timeError = False
            # Check if the time is alright
            if not ('startTime' in self.timeTable[i] and 'endTime' in self.timeTable[i]):
                timeError = True
            elif self.timeTable[i]['endTime'] < self.timeTable[i]['startTime']:
                timeError = True
            # Write the object to readme file
            if timeError:
                self.filestream.write("*")
            self.filestream.write(i + ":\n")
            if 'startTime' in self.timeTable[i]:
                self.filestream.write("Start Time: " + time.strftime('%Y-%m-%d %H:%M:%S %z' , time.localtime(self.timeTable[i]['startTime'])) + "\n")
            if 'endTime' in self.timeTable[i]:
                self.filestream.write("End Time: " + time.strftime('%Y-%m-%d %H:%M:%S %z' , time.localtime(self.timeTable[i]['endTime'])) + "\n")
            if not timeError:
                self.filestream.write("Took: " + time.strftime("%H:%M:%S", time.gmtime(self.timeTable[i]['endTime'] - self.timeTable[i]['startTime'])) + "\n")
            # New line
            self.filestream.write("\n")            
        # Total End Time and duration
        self.filestream.write("\nTotal End Time: " + time.strftime('%Y-%m-%d %H:%M:%S %z' , time.localtime(self.TotalEndTime)) + "\n")
        self.filestream.write("Took: " + time.strftime("%H:%M:%S", time.gmtime(self.TotalEndTime - self.TotalStartTime)) + "\n")
    
    def __del__(self):
        if self.ERROR: return
        if self.filestream:
            self.saveFile()
            self.filestream.close()
            self.filestream = None
        

# This could also help to calculate model evaluation result
class ReadmeModelUill(ReadmeUtil):
    def writeEvaluation(self, objectName, evaluationType, evaluationValue):
        if self.ERROR: return False
        if objectName not in self.timeTable:
            self.ERROR = False
            return False
        self.timeTable[objectName][evaluationType] = evaluationValue
        self.saveFile()
        
    def saveFile(self):
        self.filestream.fseek(0, 0)
        self.TotalEndTime = time.time()
        # Total Start Time
        self.filestream.write("Total Start Time: " + time.strftime('%Y-%m-%d %H:%M:%S %z' , time.localtime(self.TotalStartTime)) + "\n\n")
        # Individual tasks' time
        for i in self.timeTable:
            timeError = False
            # Check if the time is alright
            if not ('startTime' in self.timeTable[i] and 'endTime' in self.timeTable[i]):
                timeError = True
            elif self.timeTable[i]['endTime'] < self.timeTable[i]['startTime']:
                timeError = True
            # Write the object to readme file
            if timeError:
                self.filestream.write("*")
            self.filestream.write(i + ":\n")
            if 'startTime' in self.timeTable[i]:
                self.filestream.write("Start Time: " + time.strftime('%Y-%m-%d %H:%M:%S %z' , time.localtime(self.timeTable[i]['startTime'])) + "\n")
            if 'endTime' in self.timeTable[i]:
                self.filestream.write("End Time: " + time.strftime('%Y-%m-%d %H:%M:%S %z' , time.localtime(self.timeTable[i]['endTime'])) + "\n")
            if not timeError:
                self.filestream.write("Took: " + time.strftime("%H:%M:%S", time.gmtime(self.timeTable[i]['endTime'] - self.timeTable[i]['startTime'])) + "\n")
            # Write evaluation results:
            if ('MAE' in self.timeTable[i] 
                and 'MSE' in self.timeTable[i]
                and 'RMSE' in self.timeTable[i]
                and 'Explained variance' in self.timeTable[i]
                and 'Coefficient of determination' in self.timeTable[i]
            ):
                self.filestream.write("MAE: " + str(self.timeTable[i]['MAE']) + '\n')
                self.filestream.write("MSE: " + str(self.timeTable[i]['MSE']) + '\n')
                self.filestream.write("RMSE: " + str(self.timeTable[i]['RMSE']) + '\n')
                self.filestream.write("Explained variance: " + str(self.timeTable[i]['Explained variance']) + '\n')
                self.filestream.write("Coefficient of determination: " + str(self.timeTable[i]['Coefficient of determination']) + '\n')
            # Write Model or Evaluation not exist:
                if 'Existance' in self.timeTable[i]:
                    self.filestream.write("Existance: " + str(self.timeTable[i]['Existance']) + '\n')
                if 'Evaluation' in self.timeTable[i]:
                    self.filestream.write("Evaluation: " + str(self.timeTable[i]['Evaluation']) + '\n')
                
            # New line
            self.filestream.write("\n")            
        # Total End Time and duration
        self.filestream.write("\nTotal End Time: " + time.strftime('%Y-%m-%d %H:%M:%S %z' , time.localtime(self.TotalEndTime)) + "\n")
        self.filestream.write("Took: " + time.strftime("%H:%M:%S", time.gmtime(self.TotalEndTime - self.TotalStartTime)) + "\n")
    