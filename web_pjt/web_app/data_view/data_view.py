
import pandas as pd
### 숫자 데이터 처리 
import numpy as np

### 파이썬에서 가장 기본적으로 사용하는 시각화 라이브러리
import matplotlib.pyplot as plt

### 히트맵 라이브러리
import seaborn as sns

### 한글처리(시각화 시 그래프 내에 한글이 포함되는 경우 한글 깨짐 현상 방지)
plt.rc("font", family="Malgun Gothic")

### 특수기호(마이너스 기호) 처리
plt.rcParams["axes.unicode_minus"] = False

#from sklearn.model_selection import train_test_split


# from sklearn.linear_model import LinearRegression
# from sklearn.preprocessing import PolynomialFeatures # 다항회귀 모델
# from sklearn.ensemble import RandomForestClassifier # 랜덤 포레스트 분류 모델

# ### 앙상블 모델들....
# # - 랜덤포레스트(회귀/분류 모두 가능한 모델)
# from sklearn.ensemble import RandomForestClassifier
# # - 엑스트라트리(회귀/분류 모두 가능한 모델)
# from sklearn.ensemble import ExtraTreesClassifier
# # - 그레디언트부스팅(회귀/분류 모두 가능한 모델)
# from sklearn.ensemble import GradientBoostingClassifier
# # - 히스트그레디언트부스팅(회귀/분류 모두 가능한 모델)
# from sklearn.ensemble import HistGradientBoostingClassifier
# # - 엑스지부스트(회귀/분류 모두 가능한 모델) = 히스트그레디언트부스팅과 동급(성능이 비슷함)
# #from xgboost import XGBClassifier


# from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# # confusion matrix 시각화 및 보고서 생성을 위한 라이브러리
# from sklearn.metrics import ConfusionMatrixDisplay,classification_report, confusion_matrix 
# # Cloassifier 평가 지표
# from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


class Data_View:
    def __init__(self):
      print('data view initialized\n')
      self.initDataFrame()
      self.data_preprocess()
      self.initVisualization()
      self.saveFig()

    def initDataFrame(self):
      self.file_name = "./web_app/data_view/data/01_Real_Estate_List.csv"
      self.df = pd.read_csv(self.file_name, encoding='utf-8')
      print(self.df.head())

    def data_preprocess(self):
       self.correlation_matrix = self.df.corr()
       print(self.correlation_matrix)

    def scaler_process(scaler, train_input):
      scaler.fit(train_input)
      return scaler.transform(train_input)

    def initVisualization(self):
      print("get map") 
      self.fig = plt.figure(figsize=(10, 8))

      sns.heatmap(self.correlation_matrix, annot=True, fmt=".3f", linewidths=0.5, cmap="berlin")
      plt.yticks(rotation=0,color='teal')
      plt.xticks(rotation=45,color='teal')
      ### 그래프 전체 제목 넣기
      self.fig.suptitle("Real Estate Index Correlation Data",size=20,color='teal',weight='bold')
      
      ### 그래프 겹치지 않게 정렬하기
      self.fig.tight_layout()
      
    def saveFig(self):
      self.fig.savefig("./web_app/static/web_app/images/fig.png")
      print(self.fig)