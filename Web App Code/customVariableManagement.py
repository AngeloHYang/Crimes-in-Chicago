'''
    Custom Variable Management, to store commonly used data in this Web App across the project
'''

def init_cvm():
    global cvm_dict
    cvm_dict = dict()

def setValue_cvm(key, value):
    cvm_dict[key] = value

def getValue_cvm(key, ErrorReturn = None):
    try:
        return cvm_dict[key]
    except KeyError:
        return ErrorReturn
    
def delValue_cvm(key, KeyError=None):
    return cvm_dict.pop(key, KeyError)