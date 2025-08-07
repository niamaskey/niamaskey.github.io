#%%
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go 
from plotly.offline import plot
import re
from geopandas import read_file, GeoDataFrame
import gpxpy

token = 'pk.eyJ1IjoibmlhbWFza2V5IiwiYSI6ImNsc2xhZGFucjBienYyanBkbWV2amZsbTQifQ.KBD45j64TKi2gmmTTqS8ag'
#%%


def get_gpx_data(gpx_file):
    with open(gpx_file, 'r') as f:
        gpx = gpxpy.parse(f)
    
    tracks = []
    waypoints = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                tracks.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation,
                    'time': point.time
                })
    for waypoint in gpx.waypoints:
        waypoints.append({
            'latitude': waypoint.latitude,
            'longitude': waypoint.longitude,
            'elevation': waypoint.elevation,
            'name': waypoint.name
        })
    return pd.DataFrame(tracks), pd.DataFrame(waypoints)


#%%
#geojson file
# geojson = r'/Users/nraskey/Documents/Personal/Hikes/Reynolds_Falls_geojson.js'
# #csv file for main tracks
# csv = r'/Users/nraskey/Documents/Personal/Hikes/Reynolds Falls.csv'
#
gpx_files = ['//Users/nraskey/Documents/Personal/Hikes/Whites-hut.gpx']

central_coords = (-36.31402, 148.3930)     #To center map on
savedir = r'./maps/guthega-whites_river.html'

# track = pd.read_csv(csv)
# gdf = read_file(geojson)
# gdf = GeoDataFrame.from_features(gdf)

# From now on use gpx files not csv and js

# gpx_file = 'your_gpx_file.gpx'
fig = go.Figure() 

for gpx_file in gpx_files:
    dft, dfw = get_gpx_data(gpx_file)

    print(dft, dfw)

    dft.sort_values(by='time', inplace=True)

    #Plot main track
    fig.add_trace(
        go.Scattermap(lat=dft["latitude"], 
                        lon=dft["longitude"],
                        mode='lines')#,height=600, width=600)
    )

    # #Plot waypoints
    # waypoints = gdf.iloc[:-1,0]

    if dfw.empty:
        continue
    waypoint_links = []
    for i, name in enumerate(dfw['name']):

        lat = dfw['latitude'][i]
        lon = dfw['longitude'][i]
        if len(waypoint_links)==0:
            customdata = ''
        else:
            customdata=waypoint_links[i]
        fig.add_trace(
        go.Scattermap(
            lat=[lat],
            lon=[lon],
            # text="""<a href="https://www.google.com/">{}</a>""".format("Text"),
            name=name,
            customdata=[customdata],
            hovertemplate=
            ("%{lat:.2f}, %{lon:.2f}")   
        )
    )

#Update map layout
fig.update_layout(map_style="outdoors", map_zoom=11, map_center_lon = central_coords[1], 
                  map_center_lat = central_coords[0],
                  margin={"r":5,"t":5,"l":5,"b":5},
                #   mapbox_accesstoken=token,
                  showlegend=False, 
                  width=600, 
                  height=600)

####################
### HYPERLINKING ###
####################

# Get HTML representation of plotly.js and this figure
plot_div = plot(fig, output_type='div', include_plotlyjs=True)

# Get id of html div element that looks like
# <div id="301d22ab-bfba-4621-8f5d-dc4fd855bb33" ... >
res = re.search('<div id="([^"]*)"', plot_div)
div_id = res.groups()[0]

# Build JavaScript callback for handling clicks
# and opening the URL in the trace's customdata 
js_callback = """
<script>
var plot_element = document.getElementById("{div_id}");
plot_element.on('plotly_click', function(data){{
    console.log(data);
    var point = data.points[0];
    if (point) {{
        console.log(point.customdata);
        window.open(point.customdata);
    }}
}})
</script>
""".format(div_id=div_id)

# Build HTML string
html_str = """
<html>
<body>
{plot_div}
{js_callback}
</body>
</html>
""".format(plot_div=plot_div, js_callback=js_callback)

# Write out HTML file
with open(savedir, 'w') as f:
    f.write(html_str)