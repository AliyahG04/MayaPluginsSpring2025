from MayaUtils import *
from PySide2 import QtWidgets
from PySide2.QtWidgets import QLabel, QPushButton, QVBoxLayout
import maya.cmds as mc

class SpaceSwitchTool(QtWidgets.Qwidget):
    def __init__(self, parent=None):
        super(SpaceSwitchTool, self).__init__(parent)
        
        self.setWindowTitle("Space Switch Tool")
        self.InitUi()

        def InitUi(self):
            masterLayout = QtWidgets.QVBoxLayout()

            self.objectLabel = QtWidgets.QLabel("Object:")
            self.objectField = QtWidgets.QLineEdit()
            self.selectObjBtn = QtWidgets.QPushButton("select")
    

spaceSwitchTool = SpaceSwitchTool()
spaceSwitchTool.show()
