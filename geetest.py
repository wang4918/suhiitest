import ee
ee.Initialize()
import folium
from IPython.display import display

def add_ee_layer(self, eeImageObject, visParams, name):
  mapID = ee.Image(eeImageObject).getMapId(visParams)
  folium.raster_layers.TileLayer(
    tiles = "https://earthengine.googleapis.com/map/"+mapID['mapid']+
      "/{z}/{x}/{y}?token="+mapID['token'],
    attr = "Map Data © Google Earth Engine",
    name = name,
    overlay = True,
    control = True
  ).add_to(self)
  
folium.Map.add_ee_layer = add_ee_layer

roi = ee.FeatureCollection('users/michaelwangye/Santiago_di_Chile/Santiago_di_Chile_DIS_Indizes')
isa = ee.ImageCollection('users/michaelwangye/WSFBinary').filterBounds(roi).reduce(reducer = ee.Reducer.max()).select(["b1_max"],["b1"]).clip(roi)

myMap = folium.Map(location=[20, 0], zoom_start=3, height=500)
myMap.add_ee_layer(isa, {}, 'New')
myMap.add_child(folium.LayerControl())

display(myMap)

#Testing a thing, just to see if it works
#Learning is #fun