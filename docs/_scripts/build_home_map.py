import pandas as pd
import json
from os.path import join
import plotly.graph_objects as go 
from plotly.offline import plot
import re

localhost=False

if localhost:
    base_url = 'http://127.0.0.1:4000'
else:
    base_url = 'https://niamaskey.github.io/'

save_dir = r'/Users/nraskey/Documents/Personal/Websites/my-site/niamaskey.github.io/docs/_includes/assets'
token = 'pk.eyJ1IjoibmlhbWFza2V5IiwiYSI6ImNsc2xhZGFucjBienYyanBkbWV2amZsbTQifQ.KBD45j64TKi2gmmTTqS8ag'

data = r'/Users/nraskey/Documents/Personal/Websites/my-site/niamaskey.github.io/docs/_data/map_locations.json'

with open(data) as f:
    location_data = json.load(f)['locations']

df = pd.DataFrame(data=location_data)
data = []

for i in range(len(df)):
    location = df.iloc[i]
    name = location['name']
    page_title = '-'.join(location['page title'].split(' '))
    page_name = location['page name'][11:].rstrip('.md')
    coordinates = location['coordinates']

    page_url = join(base_url, page_name)

    print(page_url)
    lat = float(coordinates.strip('(').strip(')').split(',')[0])
    lon = float(coordinates.strip('(').strip(')').split(',')[1])


    data.append(
        go.Scattermapbox(
            lat = [lat],
            lon = [lon],
            mode = "markers",
            marker=dict(
                size=14
            ),
            text = [name],
            customdata = [page_url],
            hoverinfo='lat+lon+text'
        )
    )

fig = go.Figure(
    data=data
)

fig.update_layout(mapbox_style="outdoors", 
                  mapbox_zoom=5.75, 
                  mapbox_center_lon = 146.5015, 
                  mapbox_center_lat = -41.6001,
                  margin={"r":5,"t":5,"l":5,"b":5},
                  mapbox_accesstoken=token,
                  showlegend=False,
                  width=800,
                  height=600)


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
{plot_div}
{js_callback}
""".format(plot_div=plot_div, js_callback=js_callback)

# Write out HTML file
with open(join(save_dir, 'home_map.html'), 'w') as f:
    f.write(html_str)