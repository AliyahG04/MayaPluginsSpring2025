from MayaUtils import *
from PySide2 import QtWidgets
from PySide2.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QRadioButton, QVBoxLayout
import maya.cmds as mc

def TryAction(action): #This will show the error window
    def wrapper(*args, **kwargs):
        try:
            action(*args, **kwargs)
        except Exception as e:
            QMessageBox().critical(None, "Error", f"{e}")

    return wrapper


class SpaceSwitchToolWidget(QMayaWindow, QtWidgets.QWidget):
    def GetWindowHash(self):
        return "9a23f7060d61124f1d31ebe505c033ee"
    
    def __init__(self):
        super(SpaceSwitchToolWidget, self).__init__()
        
        self.setWindowTitle("Space Switch Tool")
        self.init_ui()

    def init_ui(self):
        self.masterLayout = QVBoxLayout(self)
        self.setLayout(self.masterLayout)

        # Object Selection
        self.masterLayout.addWidget(QLabel("Object to Switch:"))
        self.objectField = QLineEdit()
        
        self.selectObjectBtn = QPushButton("Select")
        self.selectObjectBtn.clicked.connect(self.SelectObject)
        self.masterLayout.addWidget(self.selectObjectBtn)
        
        objectLayout = QtWidgets.QHBoxLayout()
        
        objectLayout.addWidget(self.objectField)
        objectLayout.addWidget(self.selectObjectBtn)

        self.masterLayout.addLayout(objectLayout)

        self.selectParentTargetsBtn = QPushButton("Select Switch Targets") # select the hand joints and any third joint on the rig and it will parent the object to the joints.
        self.selectParentTargetsBtn.clicked.connect(self.SelectParentTargetsBtnClicked)
        self.masterLayout.addWidget(self.selectParentTargetsBtn)

    @TryAction
    def SelectParentTargetsBtnClicked(self):
        selection = mc.ls(sl=True)
        if not selection:
            raise Exception("Nothing Selected, Please Select a joint")
        
        selectedJnt = selection[0]
        if not IsJoint(selectedJnt):
            raise Exception(f"{selectedJnt} is not a joint, Please select any joint of the Rig!")
        
        parentConstraint = ""
        obj = self.objectField.text()
        grpName = f"{obj}_dual_parent_grp"
        mc.group(obj, name=grpName)
        # print(selection)
        for sel in selection:
            print(sel)
            parentConstraint = mc.parentConstraint(sel, grpName)[0]

        ctrlAttrName = "space"
        enums = ":".join(selection) + ":"
        mc.addAttr(grpName, ln=ctrlAttrName, at="enum", en=enums, k=True)

        for i, sel in enumerate(selection):
            attrName = sel + f"W{i}"
            fullAttrName = parentConstraint + "." + attrName
            exp = f"{fullAttrName} = {grpName}.{ctrlAttrName} == {i} ? 1:0;"
            print(exp)
            mc.expression(s=exp)

    @TryAction
    def SelectObject(self):
        selectedObjs = mc.ls(sl=True)
        if not selectedObjs:
            raise Exception("Nothing Selected, Please Select any object you like to parent!")
        
        selectedMesh = selectedObjs[0]
        if not IsMesh(selectedMesh):
            raise Exception(f"{selectedMesh} is not a mesh, Please select any object you like to parent!")
        
        self.objectField.setText(selectedObjs[0])

def Run():
    spaceSwitchToolWidget = SpaceSwitchToolWidget()
    spaceSwitchToolWidget.show()
