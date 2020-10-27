''' LINKS: 
- GOOGLE API GEOLOCATION DATA 
- DATA ON RELIGIOUS ADHERENCE ACROSS COUNTIES IN MICHIGAN: http://www.thearda.com/Archive/Files/Descriptions/RCMSMGCY.asp
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#import googlemaps
import geopandas as gpd
#from ipywidgets import widgets, interact

#import googlemaps - Used to return lat,lng coordinates for each county
#import geopands - Used to map out geographical data 
#%matplotlib notebook

# Below is the code I used to iteratively retrieve location data from Google's geocoding API.
# The retrieved information was in the JSON format and the lat,long was manually extracted and put into a dataframe 

'''religious_data = pd.read_excel('Religious Data, MI, County level.xlsx', usecols = ([*range(0,11)]))
religious_data.set_index('CNTYNM',inplace = True)
county_names = list(dict.fromkeys(religious_data.index))
geo_data = pd.DataFrame()
geo_data['Addresses'] = county_names
geo_data['lat'] = ""
geo_data['long'] = ""

gmaps = googlemaps.Client(key = 'AIzaSyAKZxTO1uO4rMFFubgpBXn_FxGTvzjX6Zc')

for x in range(len(geo_data)): 
    try:
        print('Receiving data from ' + geo_data['Addresses'][x] )
        result = gmaps.geocode(geo_data['Addresses'][x]+', Michigan')
        geo_data['lat'][x] = result[0]['geometry']['location']['lat']
        geo_data['long'][x] = result[0]['geometry']['location']['lng']
        print('Successful!')
    except IndexError:
        print("Address was wrong...")
    except Exception as e:
        print ("Unexpected error occurred.",e)

geo_data.to_csv('County_geodata.csv')'''

def get_data():
    religious_data = pd.read_excel('Religious Data, MI, County level.xlsx', usecols = ([*range(0,11)]))
    geo_data = pd.read_csv('County_geodata.csv')
    #religious_data=religious_data.where(religious_data['STATEAB'] == 'MI').dropna() -> this step was not required because I manually removed the data of other areas in excel to import in a smaller file to reduce load times 

    geo_data = geo_data[['Addresses','lat','long']]
    geo_data.rename(columns = {'Addresses':'CNTYNM'},inplace = True)
    #geo_data.set_index('Addresses',inplace = True)

    religious_data = religious_data[['CNTYNM','YEAR','TOTPOP','GRPNAME','ADHERENT']]#'CONGREG','RELTRAD','FAMILY'
    religious_data['Religious Density'] = (religious_data['ADHERENT']*100/religious_data['TOTPOP'])
    religious_data.dropna(inplace = True) #remove data with NaN data
    
    #religious_data.set_index('CNTYNM',inplace = True)

    df = pd.merge(geo_data,religious_data, how = 'outer', on = 'CNTYNM')
    df.rename(columns = {'TOTPOP':'Total Population (thousands)','GRPNAME':'Religious group'},inplace = True)
    return df
#Creating a map of michigan counties Using GeoPandas 
df = get_data()
test_df = df[df['Religious group'] == 'Catholic Church']

map_df = gpd.read_file('Counties__v17a_.geojson')
map_df = map_df[['LABEL','geometry']]
map_df.rename(columns={'LABEL':'CNTYNM'},inplace = True)
#map_df.to_excel("map_data.xlsx")
#map_df.to_crs(epsg = 3395)

full = map_df.set_index('CNTYNM').join(test_df.set_index('CNTYNM'))
full = full.reset_index()
full = full[full['YEAR']==1980].dropna()

fig, ax = plt.subplots(1, figsize = (8,8))
ax.axis('off')
ax.set_title('Heat Map of Religious Density /n across Counties in Michigan', fontsize = 15)

color = 'Blues'
vmin, vmax = 0,full['Religious Density'].max()
sm = plt.cm.ScalarMappable(cmap = color, norm = plt.Normalize (vmin = vmin, vmax = vmax))
sm._A = []
cbar = fig.colorbar(sm, s = 10)
cbar.ax.tick_params(labelsize =20)
full.plot(column = 'Religious Density', cmap=color, edgecolor = '0.8' ,linewidth=0.8, ax=ax, figsize=(8,8))

gdf = gpd.GeoDataFrame(
    df, geometry = gpd.points_from_xy(df.long, df.lat)
    )

plt.scatter(df['long'], df['lat'], picker = 5,s = 2)

def onpick(event):
    origin = df.index[event.ind[0]]
    ax.set_subtitle('Selected item came from {}'.format(origin))

# tell mpl_connect we want to pass a 'pick_event' into onpick when the event is detected
plt.gcf().canvas.mpl_connect('pick_event', onpick)
plt.show()
#how do i convert the axes values to accurate lat/long data? 

'''year = widgets.Dropdown(
    options=list(df['YEAR'].unique()),
    value=list(df['YEAR'].unique())[0],
    description='Year:',
)

group = widgets.Dropdown(
    options=list(df['Religious group'].unique()),
    value=list(df['Religious group'].unique())[0],
    description='Religious Group:',
)
def plotit(group):
    test = df[df['Religious group'] == group]
    test = test.head(4)
    plt.bar(list(test['YEAR']),list(test['Religious Density']))

interact(plotit, group = group)'''

