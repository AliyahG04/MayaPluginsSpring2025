import maya.cmds as mc

root = mc.ls(sl=True)[0]

def CreateFollowingCpy(original):
    children = mc.listRelatives(original, c=True, type="joint")
    copiedChildren = [] 
    if children:
        for child in children:
            copiedChildren.append(CreateFollowingCpy(child))

    mc.select(cl=True)
    cpyName = original + "_export"
    mc.joint(n=cpyName)
    mc.matchTransform(cpyName, original)
    mc.parentConstraint(original, cpyName)
    mc.scaleConstraint(original, cpyName)
    if copiedChildren:
        mc.parent(copiedChildren, cpyName)
    
    return cpyName
    
CreateFollowingCpy(root)