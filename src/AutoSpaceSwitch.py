from MayaUtils import *
from PySide2 import QtWidgets
from PySide2.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QVBoxLayout
import maya.cmds as mc

class SpaceSwitchToolWidget(QMayaWindow, QtWidgets.QWidget):
    def GetWindowHash(self):
        return "9a23f7060d61124f1d31ebe505c033ee"
    
    def __init__(self):
        super(SpaceSwitchToolWidget, self).__init__()
        
        self.setWindowTitle("Space Switch Tool")
        self.init_ui()

    def init_ui(self):
        # Layout
        self.masterLayout = QVBoxLayout(self)

        # Object Selection
        self.objectLabel = QLabel("Object to Switch:")
        self.objectField = QLineEdit()
        self.selectObjectBtn = QPushButton("Select")
        self.selectObjectBtn.clicked.connect(self.SelectObject)
        
        objectLayout = QtWidgets.QHBoxLayout()
        objectLayout.addWidget(self.objectLabel)
        objectLayout.addWidget(self.objectField)
        objectLayout.addWidget(self.selectObjectBtn)

        self.masterLayout.addLayout(objectLayout)

        # Parent Options
        self.parentLabel = QLabel("Parent to:")
        self.leftHandRadio = QRadioButton("Left Hand")
        self.rightHandRadio = QRadioButton("Right Hand")
        self.bothHandsRadio = QRadioButton("Both Hands")

        parentLayout = QHBoxLayout()
        parentLayout.addWidget(self.parentLabel)
        parentLayout.addWidget(self.leftHandRadio)
        parentLayout.addWidget(self.rightHandRadio)
        parentLayout.addWidget(self.bothHandsRadio)

        self.masterLayout.addLayout(parentLayout)

        self.selectParentTargetsBtn = QPushButton("Select Switch Targets")
        self.selectParentTargetsBtn.clicked.connect(self.SelectParentTargetsBtnClicked)
        self.masterLayout.addWidget(self.selectParentTargetsBtn)

        # Switch Button
        switchBtn = QtWidgets.QPushButton("Switch Space")
        switchBtn.clicked.connect(self.SwitchSpace)
        self.masterLayout.addWidget(switchBtn)

    def SelectParentTargetsBtnClicked(self):
        selection = mc.ls(sl=True)
        obj = self.objectField.text()
        grpName = f"{obj}_dual_parent_grp"
        mc.group(obj, name=grpName)
        
        parentConstraint = ""
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
            mc.expression(exp)



    def SelectObject(self):
        selectedObjects = mc.ls(selection=True)
        if selectedObjects:
            self.objectField.setText(selectedObjects[0])
        else:
            mc.warning("No object selected.")

    def SwitchSpace(self):
       obj = self.objectField.text()

       if not obj:
           mc.warning("Please select an object.")
           return

       if self.leftHandRadio.isChecked():
           parent = "FKWrist_L" # Replace with actual joint name
       elif self.rightHandRadio.isChecked():
           parent = "FKWrist_R" # Replace with actual joint name
       elif self.bothHandsRadio.isChecked():
            parentLeft = "FKWrist_L" # Replace with actual joint name
            parentRight = "FKWrist_R" # Replace with actual joint name

            # Create a group to parent under both hands
            grpName = mc.group(empty=True, name=f"{obj}_dual_parent_grp")
            
            #Parent constraints with maintain offset
            mc.parentConstraint(parentLeft, grpName, maintainOffset=True)
            mc.parentConstraint(parentRight, grpName, maintainOffset=True)

            mc.parent(obj, grpName)
            return
       else:
           mc.warning("Please select a parent option.")
           return
       
       mc.parent(obj, parent)

spaceSwitchToolWidget = SpaceSwitchToolWidget()
spaceSwitchToolWidget.show()
