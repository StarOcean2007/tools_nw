# import system modules
# coding=utf-8
import os
import json
import arcpy
def testShpfile():
    arcpy.env.workspace = "C:/Users/Administrator/Documents/ArcGIS/Default.gdb"
    #geojson_point = {"points": [[114.00509,32.135089],[114.070777,32.110691],[114.109788,32.083592]],"spatialReference":{"wkid":4326}}
    geojson_point = {"x": 114.00509,  "y": 32.135089,   "spatialReference": { "wkid": 4326}}

    points = arcpy.AsShape(geojson_point,True)
    arcpy.CopyFeatures_management(points, "points")
    arcpy.SelectLayerByLocation_management("c140_P", "INTERSECT", "points", "", "NEW_SELECTION")

    # Within the selection (done above) further select only those cities that have a population >10,000
    arcpy.SelectLayerByAttribute_management("c140_P", "SUBSET_SELECTION", "DEPTH2D > 0")
    #Write the selected features to a new featureclass
    arcpy.CopyFeatures_management("c140_P", "c140_P_p1")
def testContans():
    #feature=[[]]
    #P= arcpy.Polygon( arcpy.Array([arcpy.Point(*coords) for coords in feature]))
    #geojson_point = {"type": "Point", "coordinates": [114.00509,32.135089],"spatialReference":{"wkid":4326}}
    #point = arcpy.AsShape(geojson_point)
    point = arcpy.PointGeometry(arcpy.Point(114.00509,32.135089))

    polygon = arcpy.AsShape(geojson_polygon)
    if(polygon.contains(point)):
        print("contains")
    else:
        print("not contains")



def testShp():
    feature_class = "C:/Users/Administrator/Documents/ArcGIS/Default.gdb/c6_Project2d"
    cursor = arcpy.da.SearchCursor(feature_class, ["SHAPE@","OBJECTID","SHAPE@WKT", "SHAPE@JSON"])#,"tri_no"
    tagInfo=[[1,"铁路桥",114.109788,32.083592],[2,"安桥",114.121957,32.083947],[3,"福桥",114.134917,32.09054],[4,"G4京港澳高速",114.211029,32.107146],
             [5,"民桥",114.070777,32.110691],[6,"申桥",114.06136,32.117672],[7,"关桥",114.055833,32.125278],[8,"琴桥",114.099083,32.090762],
             [9,"虹桥",114.047333,32.126389],[10,"贤桥",114.00509,32.135089]]
    for tag in tagInfo:
        #point = arcpy.Point(tag[2],tag[3])
        #ptGeometry = arcpy.PointGeometry(point)
        geojson_point = {"type": "Point", "coordinates": [tag[2],tag[3]],"spatialReference":{"wkid":4326}}
        ptGeometry = arcpy.AsShape(geojson_point)
        tag.append(ptGeometry)
        #print("XY:{0}".format(ptGeometry.WKT))

    for row in cursor:
        # Get the geometry object from the shape field
        #print("Number of Hawaiian islands: {0}".format(row[0].partCount))
        for tag in tagInfo:
            if(row[0].overlaps(tag[4])):
                print("overlaps  {0}: extent=({1}) area={2},length={3}".format(row[1],row[0].extent,row[0].getArea(),row[0].getLength()))
            #else:
                #print("distanceTo={0}  tag={1}".format(row[0].distanceTo(tag[4]), tag))
            if(row[0].crosses(tag[4])):
                print("crosses  {0}: extent=({1}) area={2},length={3}".format(row[1],row[0].extent,row[0].getArea(),row[0].getLength()))
            if(row[0].contains(tag[4])):
                tag.append(row[1])
                print("contains {0}: extent=({1}) area={2},length={3}".format(row[1],row[0].extent,row[0].getArea(),row[0].getLength()))

    print(tagInfo)
# set workspace environment
#arcpy.env.workspace = "D:/workspace/arcGis/nwgk/1000"
try:
        #testShp()
        #testContans()
        #testShpfile()
        data = [ { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5 } ]

        json = json.dumps(data)
        print json
        #dsc = arcpy.Describe(fc)
        #sr =dsc.spatialReference
        #if(fc.name=="Unknown"):
            #print( fc + " 未定义投影坐标/n")
        #else:
            #print(fc+":"+sr.name)
except arcpy.ExecuteError:
    print(arcpy.GetMessages())
    
except Exception as ex:
    print(ex.args[0])