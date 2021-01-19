import requests
import json

with open("example_payload.json") as json_file:
    data = json.load(json_file)

#  data = '{ "raster": "s3://copernicus-dem-30m/Copernicus_DSM_COG_10_N55_00_W006_00_DEM/Copernicus_DSM_COG_10_N55_00_W006_00_DEM.tif", "geom": [ { "type": "Polygon", "coordinates": [[[-5.2857375145,55.7018595345],[-5.2792572975,55.7018595345],[-5.2792572975,55.7052207941],[-5.2857375145,55.7052207941],[-5.2857375145,55.7018595345]]] } ] }'

response = requests.post(
    "http://localhost:9000/2015-03-31/functions/function/invocations",
    data=json.dumps(data),
)

print(response.json())
