from django.shortcuts import render
from django.utils import timezone
from .map_view.map_view import Map_View
from .data_view.data_view import Data_View
from .ml_view.ml_view import ML_View
import os 
import unicodedata
import pandas as pd

#plt.rcParams["axes.unicode_minus"] = False

# Create your views here.
def index(request) :
  # function in Django combines a specified HTML template 
  # with a context dictionary (containing data) and 
  # returns an HttpResponse object.
  mv = Map_View()
  dv = Data_View()
  # cards = [
  #       {'title': '데이터 분석 시각화1', 'description': '첫 번째 카드 설명'},
  #       {'title': '데이터 분석 시각화2', 'description': '두 번째 카드 설명'},
  #       {'title': '데이터 분석 시각화3', 'description': '세 번째 카드 설명'},
  #   ]
  print(request)

  return render(
    # request 정의
    request,
    # 응답 html
    "web_app/base.html", 
    # html파일에 넘겨줄 data
    { 
      "data_list":dv.df.iloc[:18,[0,2,5,6,7,8,9,10,11,12,13]].to_html(classes='my-table',index=False,col_space=10),
      "map" : mv.getMapHtml(),
      "data_path" : 'web_app/images/output.png', 
      "htm_path" : 'web_app/images/spearman_heatmap.png', 
      "grp_path" : 'web_app/images/output2.png', 
      "date" : f"{timezone.now()}"
    }    
  )

def show_pairplot(request):
    loc = Data_View().get_pairplot()
    selected_location = request.GET.get('location')  # 콤보박스에서 선택된 값
    selected_location = unicodedata.normalize("NFC", selected_location)
    loc = {unicodedata.normalize("NFC", k): v for k, v in loc.items()}

    #static_dir = '/web_app/images/climate_heatmaps/'
    print(selected_location)
    image_path = loc.get(str(selected_location), None)
    print(image_path)
    print(loc.get(selected_location))
    context = {
        'locations': loc.keys(),
        'selected_location': selected_location,
        'image_path': image_path,
    }
    return render(request, 'web_app/pairplot.html', context)

def show_heatmap(request):
    loc = Data_View().get_heatmap()  # {'가거도': [img1, img2, ...], '거문도': [...]}
    selected_location = request.GET.get('location')  # 콤보박스에서 선택된 지역명
    selected_location = unicodedata.normalize("NFC", selected_location)
    loc = {unicodedata.normalize("NFC", k): v for k, v in loc.items()}
    print(f"선택된 지역: {selected_location}")

    image_paths = loc.get(selected_location, [])  # 리스트로 받음
    print(f"이미지 경로들: {image_paths}")
    print(f"전체 지역 목록: {list(loc.keys())}")

    # 라벨 추출: 파일명에서 항목명만 추출
    labeled_images = []
    for img in image_paths:
        filename = os.path.basename(img)
        parts = filename.split('_')
        if len(parts) >= 3:
            label = parts[2]  # 예: '평균 기온'
        else:
            label = '항목 없음'
        labeled_images.append({'src': img, 'label': label})


    context = {
        'locations': loc.keys(),  # 콤보박스용
        'selected_location': selected_location,
        'image_paths': image_paths,  # 리스트 전달
        'labeled_images': labeled_images,
    }
    return render(request, 'web_app/heatmap.html', context)

def project(request) :
    def get_imgs():
      # 파일경로/URL경로 정의
      dir = "./web_app/static/web_app/images/pjt_intro/"
      static_dir = "/web_app/images/pjt_intro/"

      # 파일 리스트 정렬 (숫자 기준)
      file_list = os.listdir(dir)
      sorted_files = sorted(file_list, key=lambda x: int(os.path.splitext(x)[0]))

      # 정렬된 파일에 경로 붙이기
      f_path = [static_dir + f for f in sorted_files]

      return f_path

    loc = get_imgs()
    print(f"이미지경로 : {loc}")

    context = {
       'image_paths': loc,
    }
    return render(
        # request 정의
        request,
        # 응답 html
        "web_app/pjt_desc.html", 
        # html파일에 넘겨줄 data
        context    
    )

def predict_view(request):
    buoy_name = './web_app/ml_view/data/buoy_df.csv' 
    loc_table = pd.read_csv(buoy_name)
    mv = Map_View()
    if request.method == "POST":
        # 입력값 받기
        date_str = request.POST.get("date")  # 'YYYY-MM-DD'
        lat = float(request.POST.get("lat"))
        lon = float(request.POST.get("lon"))
        
        # input dict 구성
        date_obj = pd.to_datetime(date_str)
        input_dict = {
            "YY": int(date_obj.year),
            "MM": int(date_obj.month),
            "DD": int(date_obj.day),
            "lac": lat,
            "long": lon
        }
        
        # ML_View 실행
        ml = ML_View(input_dict)
        pred = ml.get_pred()   # 예측값
        buoy = ml.buoy            # 가까운 지점 정보
        
        context = {
            "date": date_str,
            "prediction": round(pred[0], 2),
            "lat": lat,
            "lon": lon,
            "station_name": buoy["지점명"],
            "station_id": buoy["지점번호"],
            "distance": round(buoy["거리"], 2)
        }
        return render(request, "web_app/result.html", context)

    return render(request, 
                  "web_app/predict_form.html",
                  {'data_list': loc_table.iloc[:,:-1].to_html(classes='my-table',index=False,col_space=20),
                   'map' : mv.getMapHtml(),
                   })