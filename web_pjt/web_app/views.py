from django.shortcuts import render
from django.utils import timezone
from .map_view.map_view import Map_View
from .data_view.data_view import Data_View

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
      #"card" : cards,
      "data_list":dv.df.head(10).to_html(classes='my-table', index=False,col_space=10),
      "map" : mv.getMapHtml(),
      "map_list" : mv.df.iloc[:20,[1,6,7,8,9]].sort_values(by='기준지역', ascending=False).to_html(index=False),
      "data_path" : 'web_app/images/fig.png', 
      "date" : f"{timezone.now()}"
    }    
  )
