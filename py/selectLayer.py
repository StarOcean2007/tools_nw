# import system modules
# coding=utf-8
import os
import arcpy
import uuid
import json
import time

def selectOneLayer(p,path,layer):
    arcpy.env.workspace =path
    curLayer="selectLayer_{0}".format(uuid.uuid1())
    #print(curLayer)
    arcpy.MakeFeatureLayer_management(layer, curLayer) #必须先获得图层，否则SelectLayerByLocation_management操作会报无效参数
    arcpy.SelectLayerByLocation_management(curLayer, "INTERSECT", p, "", "NEW_SELECTION")
    arcpy.SelectLayerByAttribute_management(curLayer, "SUBSET_SELECTION", "DEPTH2D > 0")
    cursor = arcpy.da.SearchCursor(curLayer, ["SHAPE@","tri_no", "ANGLE2D", "DEPTH2D", "elevation2", "froude2d", "SPEED2D", "unitflow2d"])#,"tri_no"
    result={}
    for row in cursor:
        result={"tri_no": row[1], "ANGLE2D":row[2], "DEPTH2D":row[3], "elevation2":row[4], "froude2d":row[5], "SPEED2D":row[6], "unitflow2d":row[7]}
        #row[0].getArea(), row[0].getLength()
       # print(result)
    return result
def getPointLayer(x , y):
    #geojson_point = {"points": [[tag[2],tag[3]]],"spatialReference":{"wkid":4326}}
    geojson_point = {"x":x,  "y": y,   "spatialReference": {"wkid": 4326}}
    return arcpy.AsShape(geojson_point, True)
def selectAllData(path):
    result=[]
    for file in os.listdir(path):
         sourceFile = os.path.join(path,  file)
         if os.path.isdir(sourceFile):
            result.append(selectAllData(sourceFile))
    result.extend(selectData(path))
    return result

def selectData(path):


    tagInfo=[[1,u"铁路桥",114.109964,32.084843],[2,u"安桥",114.121569,32.083887],[3,u"福桥",114.134936,32.089657],[4,u"G4京港澳高速",114.210582,32.107004],
             [5,u"民桥",114.070678,32.111191],[6,u"申桥",114.060919,32.118463],[7,u"关桥",114.055151,32.125189],[8,u"琴桥",114.098704,32.090966],
             [9,u"虹桥",114.047055,32.126446],[10,u"贤桥",114.004884,32.134618]]
    result=[]
    for tag in tagInfo:
        row = {"id": tag[0], "mc": tag[1], "x": tag[2], "y": tag[3], "data": []}
        result.append(row)
    arcpy.env.workspace = path
    fcs = arcpy.ListFeatureClasses()
    i = 0
    icount = len(fcs)
    for fc in fcs:
        for row in result:
            info =u"{0}、{1} {2}".format( row["id"], row["mc"], fc)

            item=selectOneLayer(getPointLayer(row["x"],row["y"]),path,fc)
            if(len(item)>0):
                item["shp"] = fc
                row["data"].append(item)
                info += u"(淹没)"
            else:
                info += u"(未淹没)"
            print(u"{0}:{1}".format(info, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) )
        i+= 1
        print(u"已完成({0}/{1})".format(i, icount) )
    return result
try:
    #path = "C:/Users/Administrator/Documents/ArcGIS/Default.gdb"
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print u"开始时间为 :", localtime


    targetFile="D:/workspace/arcGis/nwgk.txt"
    targetDir= "D:/workspace/arcGis/nwgk_WGS84" #os.path.join(sourceDir,"../newnwgk/600")
    data=selectData(targetDir)
    json = json.dumps(data)
    open(targetFile, "wb").write(json)

    # Within the selection (done above) further select only those cities that have a population >10,000
    #arcpy.SelectLayerByAttribute_management("c140_P", "SUBSET_SELECTION", "DEPTH2D > 0")
    #Write the selected features to a new featureclass
    #arcpy.CopyFeatures_management("c140_P", "c140_P_p")
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print u"结束时间为 :", localtime
except arcpy.ExecuteError:
    print(arcpy.GetMessages())
    
except Exception as ex:
    print(ex.args[0])