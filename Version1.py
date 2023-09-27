import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import csv
import glob
import contextlib
from PIL import Image

#very slow

mtlStops = pd.read_csv('S:\pandas\data\gtfs\stops.csv')
mtlShapes = pd.read_csv('S:\pandas\data\gtfs\Shapes.csv')
ile = gpd.read_file(r'S:\pandas\data\mtl\limites-terrestres.shp')
stopTime ='S:\pandas\data\gtfs\stop_times.csv'


#i got lazy
startTimeList = [
    '4:15:00', '4:30:00', '4:45:00',
    '5:00:00', '5:15:00', '5:30:00', '5:45:00',
    '6:00:00', '6:15:00', '6:30:00', '6:45:00',
    '7:00:00', '7:15:00', '7:30:00', '7:45:00',
    '8:00:00', '8:15:00', '8:30:00', '8:45:00',
    '9:00:00', '9:15:00', '9:30:00', '9:45:00',
    '10:00:00', '10:15:00', '10:30:00', '10:45:00',
    '11:00:00', '11:15:00', '11:30:00', '11:45:00',
    '12:00:00', '12:15:00', '12:30:00', '12:45:00',
    '13:00:00', '13:15:00', '13:30:00', '13:45:00',
    '14:00:00', '14:15:00', '14:30:00', '14:45:00',
    '15:00:00', '15:15:00', '15:30:00', '15:45:00',
    '16:00:00', '16:15:00', '16:30:00', '16:45:00',
    '17:00:00', '17:15:00', '17:30:00', '17:45:00',
    '18:00:00', '18:15:00', '18:30:00', '18:45:00',
    '19:00:00', '19:15:00', '19:30:00', '19:45:00',
    '20:00:00', '20:15:00', '20:30:00', '20:45:00',
    '21:00:00', '21:15:00', '21:30:00', '21:45:00',
    '22:00:00', '22:15:00', '22:30:00', '22:45:00',
    '23:00:00', '23:15:00', '23:30:00', '23:45:00',
    '24:00:00', '24:15:00', '24:30:00', '24:45:00',
    '25:00:00', '25:15:00', '25:30:00', '25:45:00'
]


endTimeList = [
    '4:30:00', '4:45:00',
    '5:00:00', '5:15:00', '5:30:00', '5:45:00',
    '6:00:00', '6:15:00', '6:30:00', '6:45:00',
    '7:00:00', '7:15:00', '7:30:00', '7:45:00',
    '8:00:00', '8:15:00', '8:30:00', '8:45:00',
    '9:00:00', '9:15:00', '9:30:00', '9:45:00',
    '10:00:00', '10:15:00', '10:30:00', '10:45:00',
    '11:00:00', '11:15:00', '11:30:00', '11:45:00',
    '12:00:00', '12:15:00', '12:30:00', '12:45:00',
    '13:00:00', '13:15:00', '13:30:00', '13:45:00',
    '14:00:00', '14:15:00', '14:30:00', '14:45:00',
    '15:00:00', '15:15:00', '15:30:00', '15:45:00',
    '16:00:00', '16:15:00', '16:30:00', '16:45:00',
    '17:00:00', '17:15:00', '17:30:00', '17:45:00',
    '18:00:00', '18:15:00', '18:30:00', '18:45:00',
    '19:00:00', '19:15:00', '19:30:00', '19:45:00',
    '20:00:00', '20:15:00', '20:30:00', '20:45:00',
    '21:00:00', '21:15:00', '21:30:00', '21:45:00',
    '22:00:00', '22:15:00', '22:30:00', '22:45:00',
    '23:00:00', '23:15:00', '23:30:00', '23:45:00',
    '24:00:00', '24:15:00', '24:30:00', '24:45:00',
    '25:00:00', '25:15:00', '25:30:00', '25:45:00',
    '26:00:00'
]


#Created the points
pointsStops = mtlStops.apply(lambda row: Point(row.stop_lon, row.stop_lat), axis=1)
pointsShapes = mtlShapes.apply(lambda row: Point(row.shape_pt_lon, row.shape_pt_lat), axis=1)




#Geodata Frame
stops = gpd.GeoDataFrame(mtlStops, geometry=pointsStops)
shapes = gpd.GeoDataFrame(mtlShapes, geometry=pointsShapes)

stops.crs = {'init' : 'epsg:32188'}#4326
shapes.crs = {'init' : 'epsg:32188'}
ile.crs = {'init' : 'epsg:32188'}

# Create a set to store distinct "stop_id" values
distinctStopIds = set()
for i in range(len(endTimeList)):
    distinctStopIds.clear()
    with open(stopTime, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            arrivalTime = row['arrival_time']
            if startTimeList[i] <= arrivalTime <= endTimeList[i]:
                distinctStopIds.add(row['stop_id'])
    
    selectedRowsStopID = stops[stops['stop_id'].isin(distinctStopIds)]

    if not selectedRowsStopID.empty:
        fig, ax1 = plt.subplots(figsize=(10, 8))
        ile.plot(ax = ax1, figsize = (10,8))
        selectedRowsStopID.plot(ax=ax1, cmap='hsv', markersize=2.5)
        plt.savefig("imgV1/"+ str(i) + '.png')
    else:
         print("Stop IDs not found.")
    
    
#https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
fp_in = "imgV1/*.png"
fp_out = "imageV1.gif"

with contextlib.ExitStack() as stack:

        # lazily load images
    imgs = (stack.enter_context(Image.open(f))
                for f in sorted(glob.glob(fp_in)))

        # extract  first image from iterator
    img = next(imgs)

        # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
    img.save(fp=fp_out, format='GIF', append_images=imgs,save_all=True, duration=200, loop=0)




#to read csv files instead of shapefiles : https://www.youtube.com/watch?v=EsSU0SSBPw8&ab_channel=JonathanSoma