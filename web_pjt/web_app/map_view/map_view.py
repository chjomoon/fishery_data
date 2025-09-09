import pandas as pd
import folium
import matplotlib.pyplot as plt

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
    filePath = "./web_app/map_view/files/result.csv"
    filePath2 = './web_app/map_view/files/buoy_df.xlsx'
    self.df = pd.read_csv(filePath)
    self.buoy_df = pd.read_excel(filePath2)

    # self.fish2 = self.df.drop_duplicates(subset='기준항', keep='first')
    # self.fish2.reset_index()
    #geoPath = './web_app/map_view/maps/seoul_sgg.geojson'
    #self.geo = json.load(open(geoPath, encoding = 'utf-8'))
    self.m = Map_View.getMap(37.778, 130.049)
    self.style = self.style_function()

  def getMap(lat,lng):
    print("getmap")
    return folium.Map([lat, lng],
                      tiles = 'cartodbpositron', #cartodbpositron, OpenStreetMap
                      width='100%', height='100%',
                      zoom_start = 6.5)
  
  def style_function(self):
     return { "color": 'yellow', "weight": 3, "opacity": 0.35 }
  
  def boundary_display(self):
    return folium.GeoJson(self.geo, style_function = lambda x : self.style).add_to(self.m)

  def getMapHtml(self):
    # folium.GeoJson(self.geo, style_function = lambda x : self.style).add_to(self.m)
    print("map - getMapHtml")
    base_ids = set(self.df['지점번호'].dropna().astype(int))

    # 관측소 지점번호 목록
    unique_ids = self.buoy_df['지점번호'].dropna().astype(int).unique()

    # berlin colormap으로 색상 매핑
    cmap = plt.get_cmap('Oranges')
    color_dict = {id_: cmap(i / len(unique_ids)) for i, id_ in enumerate(unique_ids)}

    #all_coords = []

    # RGB → HEX 변환 함수
    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % tuple(int(c * 255) for c in rgb[:3])

    # 기준항 마커 추가
    for idx, row in self.df.iterrows():
        id_ = int(row['지점번호'])
        #all_coords.append([row['위도'], row['경도']])
        color = rgb_to_hex(color_dict.get(id_, (0.5, 0.5, 0.5)))  # 기본 회색
        folium.Marker(
            location=[row['위도'], row['경도']],
            icon=folium.Icon(color='white', icon="ship", icon_color=color, prefix="fa"),
            tooltip=f"<h5>{row['기준항']}⚓</h5>",
            popup=folium.Popup(
                f"<h5>⚓기준항: {row['기준항']}</h5><p>✔️기준지역: {row['지점명']}</p><p>✔️위치정보: {row['위도']} / {row['경도']}</p>",
                min_width=150, max_width=200
            )
        ).add_to(self.m)

    # 관측소 마커 추가
    for idx, row in self.buoy_df.iterrows():
        id_ = int(row['지점번호'])
        #all_coords.append([float(row['위도']), float(row['경도'])])
        if id_ in base_ids:
            color = rgb_to_hex(color_dict[id_])
        else:
            color = '#999999'  # 기준항에 없는 경우 회색

        folium.CircleMarker(
            location=[float(row['위도']), float(row['경도'])],
            radius=80,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.3,
            popup=f"<p>관측소: {row['지점명']}({row['지점번호']})</p><p>위치정보: {row['위도']}/{row['경도']}</p>"
        ).add_to(self.m)

    # 지도 범위 자동 조정
    #self.m.fit_bounds(all_coords)

    return self.m.get_root().render( )
