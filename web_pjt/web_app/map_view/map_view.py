import pandas as pd
import folium
#import json

class Map_View:
  
  def __init__(self):
    print('map view initialized\n')
    self.initData()
    #self.boundary_display()
    #self.getMapHtml()

  def initData(self):
    #BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("initdata")
    filePath = "./web_app/map_view/files/vessel_info.csv"
    self.df = pd.read_csv(filePath)

    self.fish2 = self.df.drop_duplicates(subset='기준항', keep='first')
    self.fish2.reset_index()

    #geoPath = './web_app/map_view/maps/seoul_sgg.geojson'
    #self.geo = json.load(open(geoPath, encoding = 'utf-8'))
    self.m = Map_View.getMap(37.778, 130.049)
    self.style = self.style_function()

  def getMap(lat,lng):
    print("getmap")
    return folium.Map([lat, lng],
                      tiles = 'cartodbpositron', 
                      width='100%', height='100%',
                      zoom_start = 6.5)
  
  def style_function(self):
     return { "color": 'yellow', "weight": 3, "opacity": 0.35 }
  
  def boundary_display(self):
    return folium.GeoJson(self.geo, style_function = lambda x : self.style).add_to(self.m)

  def getMapHtml(self):
    # folium.GeoJson(self.geo, style_function = lambda x : self.style).add_to(self.m)
    print("map - getMapHtml")
    for idx, row in self.fish2.iterrows():
      folium.Marker(
          location=[row['위도_기준항'], row['경도_기준항']],
          icon=folium.Icon(color='teal',icon="ship",icon_color="white", prefix="fa"),
          tooltip = f"<h5>{row['기준항']}⚓</h5>",
          popup= folium.Popup(f"<h5>⚓기준항: {row['기준항']}</h5><p>✔️기준지역: {row['기준지역']}</p><p>✔️위치정보: {row['위도_기준항']} / {row['경도_기준항']}</p>",min_width=150, max_width=200)
      ).add_to(self.m)
    ##using legend
    # html_itms = ""
    # for k in legend_dict.keys() :
    #     item_txt = """<br> &nbsp; {item} &nbsp; <i class="fa fa-map-marker fa-2x" style="color:{col}"></i>"""
    #     html_itms += item_txt.format(item= k ,col= legend_dict[k])

    # legend_html = """
    #  <div style="
    #     position: absolute;
    #     bottom: 30px;
    #     right: 30px;
    #     z-index:500;
    #     background-color:white;
    #     border:2px solid grey;
    #     padding: 10px;
    #     font-size:12px;
    #     font-weight: bold;
    #     opacity: 0.8;
    #     box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    #   ">
    #     <div><strong>&lt; Legend &gt;</strong></div>
    #     {itm_txt}
    #     </div>
    # """.format(itm_txt= html_itms)
    # self.m.get_root().html.add_child(folium.Element( legend_html ))
    return self.m.get_root().render( )
