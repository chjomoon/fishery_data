import pandas as pd
import folium
from folium import IFrame
import matplotlib.pyplot as plt

plt.rc('font', family='AppleGothic')   # macOS
plt.rcParams["axes.unicode_minus"] = False


#import json

class Map_View:
  
  def __init__(self):
    print('map view initialized\n')
    self.initData()
    #self.boundary_display()
    #self.getMapHtml()

  def initData(self):

    print("initdata")

    filePath = "./web_app/map_view/files/result.csv"
    filePath2 = './web_app/map_view/files/buoy_df.xlsx'
    self.df = pd.read_csv(filePath)
    self.buoy_df = pd.read_excel(filePath2)
    self.m = Map_View.getMap(36.15, 129.35)

    # self.fish2 = self.df.drop_duplicates(subset='기준항', keep='first')
    # self.fish2.reset_index()
    #geoPath = './web_app/map_view/maps/seoul_sgg.geojson'
    #self.geo = json.load(open(geoPath, encoding = 'utf-8'))
    
    #self.style = self.style_function()

  def getMap(lat,lng):
    print("getmap")
    return folium.Map([lat, lng],
                      tiles = 'cartodbpositron', #cartodbpositron, OpenStreetMap
                      width='100%', height='100%',
                      zoom_start = 6.5)
  
  def style_function(self):
     return { "color": 'yellow', "weight": 3, "opacity": 0.35 }
  
  # def boundary_display(self):
  #   return folium.GeoJson(self.geo, style_function = lambda x : self.style).add_to(self.m)

  def getMapHtml(self):
    # folium.GeoJson(self.geo, style_function = lambda x : self.style).add_to(self.m)
    print("map - getMapHtml")
    base_ids = set(self.df['지점번호'].dropna().astype(int))

    # 관측소 지점번호 목록
    unique_ids = self.buoy_df['지점번호'].dropna().astype(int).unique()

    # berlin colormap으로 색상 매핑
    cmap = plt.get_cmap('ocean')
    color_dict = {id_: cmap(i / len(unique_ids)) for i, id_ in enumerate(unique_ids)}

    # RGB → HEX 변환 함수
    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % tuple(int(c * 255) for c in rgb[:3])

    # 기준항 마커 추가
    for _, row in self.df.iterrows():
        id_ = int(row['지점번호'])
        color = rgb_to_hex(color_dict.get(id_, (0.5, 0.5, 0.5)))  # 기본 회색
        folium.Marker(
            location=[row['위도'], row['경도']],
            icon=folium.Icon(color='white', icon="fish", icon_color=color, prefix="fa"),
            tooltip=f"<h5>{row['기준항']}⚓</h5>",
            popup=folium.Popup(
                f"<h5>⚓기준항: {row['기준항']}</h5><p>✔️기준지역: {row['지점명']}</p><p>✔️위치정보: {row['위도']:.3f} / {row['경도']:.3f}</p>",
                min_width=150, max_width=200
            )
        ).add_to(self.m)

    # 관측소 마커 추가
    for _, row in self.buoy_df.iterrows():
        id_ = int(row['지점번호'])
        if id_ in base_ids:
            color = rgb_to_hex(color_dict[id_])
        else:
            color = 'white'  # 기준항에 없는 경우 회색
        
        # html = f"""
        #     <div style="width: 200px;">
        #         <p><strong>✔️관측소:</strong> {row['지점명']} ({row['지점번호']})</p>
        #         <p><strong>✔️위치정보:</strong> {float(row['위도']):.3f} / {float(row['경도']):.3f}</p>
        #         <p><a href="/heatmap/?location={row['지점명']}">📊 히트맵 보기</a></p>
        #         <p><a href="/pairplot/?location={row['지점명']}">📈 페어플롯 보기</a></p>
        #     </div>
        # """

        # iframe = IFrame(html=html, width=250, height=150)
        # popup = folium.Popup(iframe, max_width=250)

        # folium.CircleMarker(
        #     location=[float(row['위도']), float(row['경도'])],
        #     radius=20,
        #     color=color,
        #     fill=True,
        #     fill_color=color,
        #     fill_opacity=1,
        #     tooltip=f"<h5>{row['지점명']}📍</h5>",
        #     popup=popup
        # ).add_to(self.m)
        folium.CircleMarker(
            location=[float(row['위도']), float(row['경도'])],
            radius=20,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=1,
            tooltip=f"<h5>{row['지점명']}📍</h5>",
            popup=f"""
                <div style="width: 200px;">
                    <p><strong>✔️관측소:</strong> {row['지점명']} ({row['지점번호']})</p>
                    <p><strong>✔️위치정보:</strong> {float(row['위도']):.3f} / {float(row['경도']):.3f}</p>
                    <p><a href="/heatmap/?location={row['지점명']}" >📊 히트맵 보기</a></p>
                    <p><a href="/pairplot/?location={row['지점명']}">📈 페어플롯 보기</a></p>
                </div>
            """
        ).add_to(self.m)
    #self.m.save('./map.html')
    return self.m.get_root().render()
