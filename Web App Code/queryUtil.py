'''
    Utilities related to dataframe queries
'''

def createSingleSelection(columnName, toWhat, how="==", toWhatIsStr=True):
    # How can be ==, <=, >=
    #dataframe[columnName] == euqalTo
    string = ""
    
    columnNameSelection = "`" + columnName + "`"
    
    if toWhatIsStr:
        toWhatSelection = "'" + toWhat + "'"
    else:
        toWhatSelection = toWhat
        
    string = "(" + columnNameSelection + " " + how + " " + str(toWhatSelection) + ")"
    return string

def addAnd(string1, string2):
    if string1 == "" or string1 == False or string1 == None:
        return string2
    if string2 == "" or string2 == False or string2 == None:
        return string1
    string = string1 + " & " + string2
    return string

def addOr(string1, string2):
    if string1 == "" or string1 == False or string1 == None:
        return string2
    if string2 == "" or string2 == False or string2 == None:
        return string1
    string = string1 + " or " + string2
    return string

def addNot(string):
    string = "not" + string
    return string

def addParentheses(string):
    string = "(" + string + ")"
    return string