import maya.cmds as mc
import maya.OpenMayaUI as omui # this imports maya's open maya ui module, it can help finding the maya main window
import shiboken2 # this helps with converting the maya main window to the pyside tupe

from PySide2.QtWidgets import (QMainWindow, QWidget) # imports all the widgets needed to build our ui
from PySide2.QtCore import Qt # this has some values we can use to configure out widget, like ther windowType, or oreientation 

def GetMayaMainWindow()->QMainWindow: # getting the maya main window
    mayaMainWindow = omui.MQtUtil.mainWindow() # returns the pointer 
    return shiboken2.wrapInstance(int(mayaMainWindow), QMainWindow) # returning an actual QMainWindow in the Python type

def DeleteWindowWithName(name): # refreshes window
    for window in GetMayaMainWindow().findChildren(QWidget, name): # get the same window we created from GetMayaMainWindow
        window.deleteLater() # deletes the old window whenever we open a new one

class QMayaWindow(QWidget): # creates a window that can be popped up in maya
    def __init__(self): # is a constructor for the super()
        DeleteWindowWithName(self.GetWindowHash()) # deleting anything that has name already
        super().__init__(parent = GetMayaMainWindow()) # the new window we're popping up now is a child of the maya main application so it will behave better
        self.setWindowFlags(Qt.WindowType.Window) # becomes part of maya, in other words when I click out of it the windows doesn't immediatly hide away and it minimizes and appears with maya
        self.setObjectName(self.GetWindowHash()) # creates a new one with the same name while removing the previous one

    def GetWindowHash(self): # the setup for creating a new window with the same name
        return "sggddfhsfhdgfhh" # returns the window to where ever we want it to on maya
    

def IsMesh(obj):
    shapes = mc.listRelatives(obj, s=True)
    if not shapes:
        return False
    
    for s in shapes:
        if mc.objectType(s) == "mesh":
            return True
        
    return False

def IsSkin(obj):
    return mc.objectType(obj) == "skinCluster"

def IsJoint(obj):
    return mc.objectType(obj) == "joint"

def GetUpperStream(obj):
    return mc.listConnections(obj, s=True, d=False, sh=True)

def GetLowerStream(obj):
    return mc.listConnections(obj, s=False, d=True, sh=False)

def GetAllConnectIn(obj, NextFunc, searchDepth = 10, Filter = None):
    AllFound = set()
    nexts = NextFunc(obj)
    while nexts and searchDepth > 0:
        for next in nexts:
            AllFound.add(next)

        nexts = NextFunc(nexts)
        if nexts:
            nexts = [x for x in nexts if x not in AllFound]

            searchDepth = 1

    if not Filter:
        return list(AllFound)
    
    filterd = []
    for found in AllFound:
        if Filter(found):
            filterd.append(found)

    return filterd