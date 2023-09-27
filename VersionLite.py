import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import contextlib
from PIL import Image

#FRANCHESCO VIRGUNILIIII

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


stopsPos = pd.read_csv('S:\pandas\data\gtfs\stops.csv', usecols=['stop_id','stop_lat','stop_lon'])
stopTime = pd.read_csv('S:\pandas\data\gtfs\stop_times.csv', usecols=['stop_id','arrival_time'])


def getStopInArea(min_lat, min_lon):
    max_lat = min_lat + 0.01
    max_lon = min_lon + 0.01
    filtered_stops = stopsPos[(stopsPos['stop_lat'] >= min_lat) & (stopsPos['stop_lat'] <= max_lat) &
                        (stopsPos['stop_lon'] >= min_lon) & (stopsPos['stop_lon'] <= max_lon)]

    #shows the bus stops near the cegep
    #shape = gpd.GeoDataFrame(stopsPos, geometry=filtered_stops.apply(lambda row: Point(row.stop_lon, row.stop_lat), axis=1))
    #shape.plot()
    return filtered_stops

stopTime['stop_id'] = stopTime['stop_id'].astype(str)
getStopInArea(45.4366, -73.6049)['stop_id'] = getStopInArea(45.4366, -73.6049)['stop_id'].astype(str)
data = pd.merge(stopTime, getStopInArea(45.4366, -73.6049), on='stop_id', how='inner')

# stuck on series object of pandas.core.series modukle
def plotIt():
    for i in range(len(endTimeList)):
            filtered_df = data[(data['arrival_time'] >= startTimeList[i]) & (data['arrival_time'] <= endTimeList[i])]
            nbOfBuses = len(filtered_df)
            shape = gpd.GeoDataFrame(stopsPos, geometry=filtered_df.apply(lambda row: Point(row.stop_lon, row.stop_lat), axis=1))
            fig, ax = plt.subplots(figsize=(5, 5))
            shape.plot(ax=ax)
            ax.set_title(f'{nbOfBuses} bus between {startTimeList[i]} and {endTimeList[i]}')
            plt.show()
                
            
            
def heatItCube():
    for i in range(len(endTimeList)):
        filtered_df = data[(data['arrival_time'] >= startTimeList[i]) & (data['arrival_time'] <= endTimeList[i])]
        nbOfBuses = len(filtered_df)
        plt.figure(figsize=(10, 10))
        sns.histplot(x=filtered_df['stop_lon'], y=filtered_df['stop_lat'], bins=15)
        
        plt.title(f'{nbOfBuses} bus between {startTimeList[i]} and {endTimeList[i]}')

        plt.savefig("imgV3/"+ str(i) + '.png')            
            
            
            
            
def heatIt():
    for i in range(len(endTimeList)):
        filtered_df = data[(data['arrival_time'] >= startTimeList[i]) & (data['arrival_time'] <= endTimeList[i])]
        nbOfBuses = len(filtered_df)
        plt.figure(figsize=(10, 10))
        sns.kdeplot(x=filtered_df['stop_lon'], y=filtered_df['stop_lat'],cmap='coolwarm', fill=True)
        
        plt.title(f'{nbOfBuses} bus between {startTimeList[i]} and {endTimeList[i]}')

        plt.savefig("imgLite/"+ str(i) + '.png')
        fp_in = "imgLite/*.png"
        fp_out = "imageLite.gif"
        
        with contextlib.ExitStack() as stack:
        
            # lazily load images
            imgs = (stack.enter_context(Image.open(f))
                    for f in sorted(glob.glob(fp_in)))
        
            # extract  first image from iterator
            img = next(imgs)
        
            # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
            img.save(fp=fp_out, format='GIF', append_images=imgs,
                     save_all=True, duration=200, loop=0)



heatIt() 