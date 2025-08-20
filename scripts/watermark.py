#%%
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go 
from plotly.offline import plot
import re
from geopandas import read_file, GeoDataFrame
import gpxpy

from PIL import Image, ImageDraw, ImageFont

image_assets
original_image = Image.open("Images/butterfly.jpg")
draw = ImageDraw.Draw(original_image)
watermark_text = "Tutorialspoint"
font_size = 20
font = ImageFont.truetype("arial.ttf", font_size)  
text_color = (255, 255, 255)  

#White color (RGB)
text_width, text_height = draw.textsize(watermark_text, font)
image_width, image_height = original_image.size
margin = 10  

#Margin from the right and bottom edges
position = (image_width - text_width - margin, image_height - text_height - margin)
draw.text(position, watermark_text, font=font, fill=text_color)
original_image.save("output Image/watermarked_image.png")
original_image.show() 