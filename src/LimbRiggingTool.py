from PySide2.QtGui import QColor
import maya.cmds as mc # imports maya's cmd module so we can use it to do stuff in maya
import maya.mel as mel
from maya.OpenMaya import MVector

from PySide2.QtWidgets import (QColorDialog, QLineEdit, QMainWindow, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton) # imports all the widgets needed to build our ui
from PySide2.QtCore import Qt # this has some values we can use to configure out widget, like ther windowType, or oreientation 
from MayaUtils import QMayaWindow
    
class LimbRigger: # represents the actual functionality of the limric tool
    def __init__(self): # constructor for the self.root, self.mid, self. end, and self.controllerSize
        self.root = "" # the default setting for the joint
        self.mid = "" # the default setting for the joint
        self.end = "" # the default setting for the joing
        self.controllerSize = 5 # the default size for the controller 

    def AutoFindJnts(self): # will be called when we click on the "Auto Find" button and when its called its basically only finding the three joints basis
        self.root = mc.ls(sl=True, type="joint")[0] # the root joint is the one we select, that way we're populating this array
        self.mid = mc.listRelatives(self.root, c=True, type="joint")[0] # we're getting the mid joint from finding the children of the new joint 
        self.end = mc.listRelatives(self.mid, c=True, type="joint")[0] # we're getting the end joint from finding the middle joint 
        
    def CreateFKControlForJnt(self, jntName): # this is where we create controllers
        ctrlName = "ac_fk_" + jntName # creates controller for the "ac_fk"
        ctrlGrpName = ctrlName + "_grp" # creates controller for the "_grp"
        mc.circle(n=ctrlName, r=self.controllerSize, nr = (1,0,0)) # creates a circl controller while properly aligning

        mc.group(ctrlName, n=ctrlGrpName) # we group out ctrlName with the n=ctrlGrpName
        mc.matchTransform(ctrlGrpName, jntName) # we're matching the ctrlGrpName to the joints
        mc.orientConstraint(ctrlName, jntName) # this is an orient to circle contraint the joint
        return ctrlName, ctrlGrpName # repeats the process of repeating it manually

    def CreateBoxController(self, name):
        mel.eval(f"curve -n {name} -d 1 -p -0.5 0.5 0.5 -p 0.5 0.5 0.5 -p 0.5 -0.5 0.5 -p -0.5 -0.5 0.5 -p -0.5 0.5 0.5 -p -0.5 0.5 -0.5 -p 0.5 0.5 -0.5 -p 0.5 0.5 0.5 -p 0.5 -0.5 0.5 -p 0.5 -0.5 -0.5 -p 0.5 0.5 -0.5 -p -0.5 0.5 -0.5 -p -0.5 -0.5 -0.5 -p 0.5 -0.5 -0.5 -p 0.5 0.5 -0.5 -p -0.5 0.5 -0.5 -p -0.5 0.5 0.5 -p -0.5 -0.5 0.5 -p -0.5 -0.5 -0.5 -p -0.5 0.5 -0.5 -p -0.5 0.5 0.5 -p -0.5 -0.5 0.5 -p -0.5 -0.5 -0.5 -p 0.5 -0.5 -0.5 -p 0.5 -0.5 0.5 -p -0.5 -0.5 0.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 ;")
        mc.scale(self.controllerSize, self.controllerSize, self.controllerSize, name)
        mc.makeIdentity(name, apply = True) # this is freeze transformation

        grpName = name + "_grp"
        mc.group(name, n=grpName)
        return name, grpName
    
    def CreatePlusController(self, name):
        mel.eval(f"curve -n {name} -d 1 -p 1.024225 0.969909 0 -p 1.011059 2.997485 0 -p -0.97702 2.997485 0 -p -0.990186 0.996241 0 -p -3.017763 1.009407 0 -p -3.004597 -1.044502 0 -p -0.963854 -1.044502 0 -p -0.97702 -3.045747 0 -p 1.011059 -2.993083 0 -p 1.037391 -1.01817 0 -p 3.02547 -1.044502 0 -p 3.02547 0.996241 0 -p 1.024225 0.956742 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 ;")
        # mc.scale(self.controllerSize/3, self.controllerSize/3, self.controllerSize/3)
        # mc.makeIdentity(name, apply = True)

        grpName = name + "_grp"
        mc.group(name, n=grpName)
        return name, grpName
    
    def GetObjectLoc(self, objectName)->MVector:
        x, y, z = mc.xform(objectName, q=True, t=True, ws=True) # get the world space translation of the objectName
        return MVector(x, y, z)
    
    def PrintMVector(self, vectorToPrint):
        print(f"<{vectorToPrint.x}, {vectorToPrint.y}, {vectorToPrint.z}>")

    def RigLimb(self, r, g, b): # the is where we acutally start rigging the limb with the three joints we collected already
        rootFKCtrl, rootFKCtrlGrp = self.CreateFKControlForJnt(self.root) # this calls from the CreateFKControlForJnt to manually contraint the root
        midFKCtrl, midFKCtrlGrp = self.CreateFKControlForJnt(self.mid) # this calls form the CreateFKControlForJnt to manually contraint the mid
        endFKCtrl, endFKCtrlGrp = self.CreateFKControlForJnt(self.end) # this calls from the CreateFKControlForJnt to manually contraint the end

        mc.parent(midFKCtrlGrp, rootFKCtrl) # this puts this parent function into the hierarchy that we want to have
        mc.parent(endFKCtrlGrp, midFKCtrl) # this puts this parent function into the hierarchy that we want to have

        ikEndCtrl = "ac_ik_" + self.end
        ikEndCtrl, ikEndCtrlGrp = self.CreateBoxController(ikEndCtrl)
        mc.matchTransform(ikEndCtrlGrp, self.end)
        endOrientConstraint = mc.orientConstraint(ikEndCtrl, self.end)[0]

        rootJntLoc = self.GetObjectLoc(self.root)
        endJntLoc = self.GetObjectLoc(self.end)

        rootToEndVec = endJntLoc - rootJntLoc

        ikHandleName = "ikHandle_" + self.end
        mc.ikHandle(n=ikHandleName, sj=self.root, ee = self.end, sol="ikRPsolver")
        ikPoleVectorVals = mc.getAttr(ikHandleName + ".poleVector")[0]
        ikPoleVector = MVector(ikPoleVectorVals[0], ikPoleVectorVals[1], ikPoleVectorVals[2])

        ikPoleVector.normalize()
        ikPoleVectorCtrlLoc = rootJntLoc + rootToEndVec / 2 + ikPoleVector * rootToEndVec.length()

        ikPoleVectorCtrlName = "ac_ik_" + self.mid
        mc.spaceLocator(n=ikPoleVectorCtrlName)
        ikPoleVectorCtrlGrp = ikPoleVectorCtrlName + "_grp"
        mc.group(ikPoleVectorCtrlName, n=ikPoleVectorCtrlGrp)
        mc.setAttr(ikPoleVectorCtrlGrp+".t", ikPoleVectorCtrlLoc.x, ikPoleVectorCtrlLoc.y, ikPoleVectorCtrlLoc.z, typ = "double3")
        mc.poleVectorConstraint(ikPoleVectorCtrlName, ikHandleName)

        ikfkBlendCtrlName = "ac_ikfk_blend_" + self.root
        ikfkBlendCtrlName, ikfkBlendCtrlGrp = self.CreatePlusController(ikfkBlendCtrlName)
        ikfkBlendCtrlLoc = rootJntLoc + MVector(rootJntLoc.x, 0, rootJntLoc.z)
        mc.setAttr(ikfkBlendCtrlGrp+".t", ikfkBlendCtrlLoc.x, ikfkBlendCtrlLoc.y, ikfkBlendCtrlLoc.z, typ="double3")

        ikfkBlendAttrName = "ikfkBlend"
        mc.addAttr(ikfkBlendCtrlName, ln=ikfkBlendAttrName, min=0, max=1, k=True)
        ikfkBlendAttr = ikfkBlendCtrlName + "." + ikfkBlendAttrName

        mc.expression(s=f"{ikHandleName}.ikBlend = {ikfkBlendAttr}")
        mc.expression(s=f"{ikEndCtrlGrp}.v = {ikPoleVectorCtrlGrp}.v = {ikfkBlendAttr}")
        mc.expression(s=f"{rootFKCtrlGrp}.v = 1 - {ikfkBlendAttr}")
        mc.expression(s=f"{endOrientConstraint}.{endFKCtrl}W0 = 1-{ikfkBlendAttr}")
        mc.expression(s=f"{endOrientConstraint}.{ikEndCtrl}W1 = {ikfkBlendAttr}")

        mc.parent(ikHandleName, ikEndCtrl)
        mc.setAttr(ikHandleName+".v", 0)

        topGrpName = self.root + "_rig_grp"
        mc.group({rootFKCtrlGrp,ikEndCtrlGrp, ikPoleVectorCtrlGrp, ikfkBlendCtrlGrp}, n= topGrpName)
        mc.setAttr(topGrpName+".overrideEnabled", 1)
        mc.setAttr(topGrpName+".overrideRGBColors", 1)
        mc.setAttr(topGrpName+".overrideColorRGB", r, g, b, type="double3")

class ColorPicker(QWidget):
    def __init__(self):
        super().__init__()
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)
        self.colorPickerBtn = QPushButton()
        self.colorPickerBtn.setStyleSheet(f"background-color:black")
        self.masterLayout.addWidget(self.colorPickerBtn)
        self.colorPickerBtn.clicked.connect(self.ColorPickerBtnClicked)
        self.color = QColor(0,0,0)

    def ColorPickerBtnClicked(self):
        self.color = QColorDialog.getColor()
        self.colorPickerBtn.setStyleSheet(f"background-color:{self.color.name()}")

class LimbRigToolWidget(QMayaWindow): # contains all the functioning data for the window and display the widget
    def __init__(self): # constructor for the super()
        super().__init__() # executing the parents intiallization logic 
        self.setWindowTitle("Limb Rigging Tool") # names the new tool window on maya(proving thats our window)
        self.rigger = LimbRigger() # this is our own copy of the rigger

        self.masterLayout = QVBoxLayout() # sets up the box layout in a verticl e postion
        self.setLayout(self.masterLayout) # sets up the master layout

        self.tipLabel = QLabel("Select the First Joint of the Limb, and click on the Auto Find Button") # the set up for the label instructing us on how to use the new tool
        self.masterLayout.addWidget(self.tipLabel) # adds the tipLabel to the masterLayout in order to show the text

        self.jointSelectionText = QLineEdit() # adds in a text box to display 
        self.masterLayout.addWidget(self.jointSelectionText) # creates an empty text box to display in the window
        self.jointSelectionText.setEnabled(False) # this text box in non-editable, it is only there to display the text when we click the joints and Auto Find button

        self.autoFindBtn = QPushButton("Auto Find") # this is the label for the button
        self.masterLayout.addWidget(self.autoFindBtn) # creates the widget as the "Auto Find" button in the window
        self.autoFindBtn.clicked.connect(self.AutoFindBtnClicked) # it immedialty shows the text from AutoFindBtnClicked when we click the "Auto Find" button clicled 

        ctrlSliderLayout = QHBoxLayout() # this creates the box layout, showing the any number from 1-30 whenever we move the slider up or down
        
        self.ctrlSizeSlider = QSlider() # this creates a slider so we can set the size of our circle control for our joints
        self.ctrlSizeSlider.setValue(self.rigger.controllerSize) # this sets the defualt size value of our controller which is taken from LimbRigger class
        self.ctrlSizeSlider.valueChanged.connect(self.CtrlSizeValueChanged) # we can change the value size on the slider for the controller
        self.ctrlSizeSlider.setRange(1, 30) # this is created so the controller/slider can be render from 1-30
        self.ctrlSizeSlider.setOrientation(Qt.Horizontal) # this is making the slider a horizontal orientation
        ctrlSliderLayout.addWidget(self.ctrlSizeSlider) # after we create the slider we add it to the layout
        self.ctrlSizeLabel = QLabel(f"{self.rigger.controllerSize}") # this shows the text number of the slider so we can see what number it changes to when we move the slider
        ctrlSliderLayout.addWidget(self.ctrlSizeLabel) # after we create the slider we add it to the layout
       
        self.masterLayout.addLayout(ctrlSliderLayout) # this is nesting the layout instead of the masterLayout

        self.colorPicker = ColorPicker()
        self.masterLayout.addWidget(self.colorPicker)

        self.setColorBtn = QPushButton("Set Color")
        self.masterLayout.addWidget(self.setColorBtn)
        self.setColorBtn.clicked.connect(self.SetColorBtnClicked)

        self.rigLimbBtn = QPushButton("Rig Limb") # this is the label for the button
        self.masterLayout.addWidget(self.rigLimbBtn) # creates the widget as the "Rig Limb" button in the window
        self.rigLimbBtn.clicked.connect(self.RigLimbBtnClicked) # it immedialty shows the text from RigLimbBtnClicked when we click the "Rig Limb" button clicled
        
    def SetColorBtnClicked(self):
        selection = mc.ls(sl=True)[0]
        mc.setAttr(selection+".overrideEnabled", 1)
        mc.setAttr(selection+".overrideRGBColors", 1)
        mc.setAttr(selection+".overrideColorRGB", self.colorPicker.color.redF(), self.colorPicker.color.greenF(),self.colorPicker.color.blueF(), type="double3")

    def CtrlSizeValueChanged(self, newValue): # contains the function to help change the value of the controller and tell the size the user wants
        self.rigger.controllerSize = newValue # this function is created so we can actually change the value of the slider
        self.ctrlSizeLabel.setText(f"{self.rigger.controllerSize}") # this is updating the ctrlSizeLabel, that way so we can see the number actaully change when we move the slider
    
    def RigLimbBtnClicked(self): # contains the function to activate the rig limb button
        self.rigger.RigLimb(self.colorPicker.color.redF(), self.colorPicker.color.greenF(), self.colorPicker.color.blueF()) # telling the button to rig the limb
        
    def AutoFindBtnClicked(self): # contains the function to activate the auto find botton
        try: # contains the function that displays the results in our edit line
            self.rigger.AutoFindJnts() # telling the rigger to do the real job
            self.jointSelectionText.setText(f"{self.rigger.root},{self.rigger.mid},{self.rigger.end}") # displays the results in our text in our line edit 
        except Exception as e: # contains the error function
            QMessageBox.critical(self, "Error", "Wrong Selection, please select the first joint of a limb!") # this text will display whenever we click a joint (or nothing at all) that isn't the first one of the limb
def Run():
    limbRigToolWidget = LimbRigToolWidget() # connects to the LimbRigToolWidget to better dispay its functions
    limbRigToolWidget.show() # shows the the limb rig tool window on maya 


