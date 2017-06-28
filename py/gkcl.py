# import system modules
# coding=gbk
import os
import arcpy

def copyFiles(sourceDir, targetDir,changeSize=False):
    #for (path,dirs,files) in os.walk(path):
    for file in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir,  file)
            if not os.path.exists(targetDir):
                print(targetDir)
                os.makedirs(targetDir)
            targetFile = os.path.join(targetDir,  file)
            if os.path.isfile(sourceFile):
                targetFile = getNewGKFileName(targetFile)
                if not os.path.exists(targetFile) or(changeSize and os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                    open(targetFile, "wb").write(open(sourceFile, "rb").read())
            if os.path.isdir(sourceFile):
                print(targetFile)
                copyFiles(sourceFile, targetFile)
def copyGkFiles(sourceDir, targetDir,prefix ,changeSize=False):
    #for (path,dirs,files) in os.walk(path):
    for file in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir,  file)
            #if not os.path.exists(targetDir):
            #    print(targetDir)
            #    os.makedirs(targetDir)
            #targetFile = os.path.join(targetDir,  file)
            if os.path.isfile(sourceFile):
                targetFile =prefix+ getNewGKFileName(file)
                targetFile = os.path.join(targetDir,  targetFile)
                print(prefix+"=>"+targetFile)
                if not os.path.exists(targetFile) or(changeSize and os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                    open(targetFile, "wb").write(open(sourceFile, "rb").read())
            if os.path.isdir(sourceFile):
                nextPrefix=prefix+ file+"_"
                print(targetDir+"=>"+nextPrefix)
                copyGkFiles(sourceFile, targetDir,nextPrefix )
def getNewGKFileName(fileName):
    #path = os.path.normcase(fileName)
    p,f = os.path.split(fileName)
    oldf,ext = os.path.splitext(f)
    if(f.endswith(".shp.xml")):
        ext = ".shp.xml"
        oldf=f[:-len(ext)]
    newFileName=oldf
    if(oldf.find(".")<0):
         newFileName += "0"
    else:
        newFileName=newFileName.replace(".", "")
    if (len(newFileName)<3):
        newFileName = "0"+newFileName
    newFileName+= ext
    newFileName= os.path.join(p,newFileName)
    return newFileName

def defineProjection_BJ(path):
    for file in os.listdir(path):
         sourceFile = os.path.join(path,  file)
         if os.path.isdir(sourceFile):
            defineProjection_BJ(sourceFile)
    arcpy.env.workspace = path
    fcs = arcpy.ListFeatureClasses()
    coord_sys = getBeijing_1954_SpatialReference()
    for fc in fcs:
        #定义投影 (Data Management)  投影和变换工具集
        arcpy.DefineProjection_management(fc, coord_sys)
        print(arcpy.GetMessages())

def repairGeometry(path):
    for file in os.listdir(path):
         sourceFile = os.path.join(path,  file)
         if os.path.isdir(sourceFile):
            repairGeometry(sourceFile)
    arcpy.env.workspace = path
    fcs = arcpy.ListFeatureClasses()
    for fc in fcs:
         #修复几何 要素工具集
        arcpy.RepairGeometry_management(fc)
        print(arcpy.GetMessages())

def getBeijing_1954_SpatialReference():
     #Beijing_1954_3_Degree_GK_CM_114E 中"_"必须用空格代替
    return arcpy.SpatialReference("Beijing_1954_3_Degree_GK_CM_114E".replace("_", " "))
def setProject_WGS84(inPath, outPath):
    for file in os.listdir(inPath):
         sourceFile = os.path.join(inPath,  file)
         targetFile= os.path.join(outPath,  file)
         if os.path.isdir(sourceFile):
            setProject_WGS84(sourceFile,targetFile)
    arcpy.env.workspace = inPath
    # Set output coordinate system
    outCS = arcpy.SpatialReference("WGS 1984")
    fcs = arcpy.ListFeatureClasses()
    for fc in fcs:
        # Determine if the input has a defined coordinate system, can't project it if it does not
        dsc = arcpy.Describe(fc)

        if dsc.spatialReference.Name == "Unknown":
            print ('skipped this fc due to undefined coordinate system: ' + infc)
        else:
            # Determine the new output feature class path and name
            outfc = os.path.join(outPath, fc)
            # run project tool
            arcpy.Project_management(fc, outfc, outCS,"Beijing_1954_To_WGS_1984_2")
        print(arcpy.GetMessages())


sourceDir = "D:/workspace/arcGis/nwgk"

try:

    #print(os.path.split("D:/workspace/arcGis/nwgk/1000/7.shp.xml"))
    #getNewGKFileName("7.shp.xml")
    #targetDir= "D:/workspace/arcGis/newnwgk84/400" #os.path.join(sourceDir,"../newnwgk/600")
    targetDir="D:/workspace/arcGis/nwgk_d"
    copyGkFiles(sourceDir, targetDir, "ST_")
    #定义Beijing_1954_3_Degree_GK_CM_114E
    defineProjection_BJ(targetDir)
    #修复几何
    repairGeometry(targetDir)
    #转换成wgs84
    sourceDir = "D:/workspace/arcGis/nwgk_d"
    targetDir="D:/workspace/arcGis/nwgk_WGS84"
    setProject_WGS84(sourceDir,targetDir)
    #print(arcpy.GetMessages())
except arcpy.ExecuteError:
    print(arcpy.GetMessages())
except Exception as ex:
    print(ex.args)