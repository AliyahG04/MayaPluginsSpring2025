from MayaUtils import *
from PySide2.QtWidgets import QLabel, QPushButton, QVBoxLayout
import maya.cmds as mc

class AutoSpaceSwitch:
    def __init__(self):
        self.Obj = ""
        self.leftHand = []
        self.rightHand = []

class SpaceSwitchWidget(QMayaWindow):
    def GetWindowHash(self):
        return "655a767a6055d54b57684cca7fcc06aa"
    
    def __init__(self):
        super().__init__()
        self.autoSpaceSwitch = AutoSpaceSwitch()
        self.setWindowTitle("Object Space Switch")

        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

        self.tipLabel = QLabel("Select Object to Switch and then select the desired parent(s)")
        self.masterLayout.addWidget(self.tipLabel)

        populateObjFieldBtn = QPushButton("Get Left Hand")
        populateObjFieldBtn.clicked.connect(self.PopulateObjField)
        self.masterLayout.addWidget(populateObjFieldBtn)

    def PopulateObjField(self, field):
        # sel = mc.ls(selection=True)
        # if sel:
        #     mc.textField(field, edit=True, text=sel[0])
        # else:
        #     mc.warning("Nothing selected.")

        selection = mc.ls(sl=True)
        if not selection:
            raise Exception("Nothing Selected")

    def PopulateField(self, field):
        # sel = mc.ls(selection=True)
        # if sel:
        #     mc.textField(field, edit=True, text=sel[0])
        # else:
        #     mc.warning("Nothing selected.")

        selection = mc.ls(sl=True)
        if not selection:
            raise Exception("Nothing Selected")

spaceSwitchWidget = SpaceSwitchWidget()
spaceSwitchWidget.show()
