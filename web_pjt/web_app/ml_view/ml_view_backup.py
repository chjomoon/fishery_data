import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

plt.rc("font", family="Malgun Gothic")
plt.rcParams["axes.unicode_minus"] = False

import joblib
from geopy.distance import geodesic
from sklearn import set_config
set_config(display="text")

class ML_View:
  def __init__(self,input):
    print('hello machine learning')
    #self.initDataFrame()
    self.input = input
    self.initData()
    

  def initData(self):
    file_name = "./web_app/ml_view/data/buoy_merge.xlsx"
    self.df = pd.read_excel(file_name)
    buoy_name = './web_app/ml_view/data/buoy_df.csv'
    self.df_loc = pd.read_csv(buoy_name)
    self.buoy = self.near_buoy(self.df_loc,self.input['lac'],self.input['long'])
    self.model = self.read_model(self.buoy)

  def read_model(self,buoy):
    loc = str(buoy['지점번호'])
    model_dir = "./web_app/ml_view/best_model/"  # 디렉토리
    file_list = os.listdir(model_dir)
    
    model_file = None
    for f in file_list:
        if loc in f:
            model_file = os.path.join(model_dir, f)
            print(model_file)
            break
    
    if model_file is None:
        raise FileNotFoundError(f"{loc} 관련 모델 파일을 찾을 수 없습니다.")
    
    return joblib.load(model_file)

  def near_buoy(self,df,lat,long):
    # 각 부이와의 거리 계산(km 단위)
    df["거리"] = df.apply(
        lambda x: geodesic([lat,long], (x["위도"], x["경도"])).kilometers,
        axis=1
    )
    # 거리값 중 가장 가까운 부이 Series Return(지점명,지점번호,위도,경도,거리)
    result = df.loc[df["거리"].idxmin()]
    print(result)
    return result
  
  def rolling_avg_columns_safe(df, ym, columns, station_col='지점', station=21229):
    """
    df: 데이터프레임
    ym: 기준 년월 문자열, 'YYYY-MM'
    columns: 반환할 컬럼 리스트
    station_col: 지점 컬럼 이름
    station: 지점 번호
    """
    # 기준 월 datetime 변환
    target_date = pd.to_datetime(ym + '-01')
    
    # ±2년, ±2개월 범위 계산
    start_date = target_date - pd.DateOffset(years=3, months=2)
    end_date   = target_date + pd.DateOffset(years=3, months=2)
    
    # 해당 지점 + 기간 필터링
    mask = (df[station_col] == station) & (df['일자'] >= start_date) & (df['일자'] <= end_date)
    df_filtered = df.loc[mask, columns]
    
    if df_filtered.empty:
        # 데이터가 없으면 NaN 반환
        return pd.Series({col: np.nan for col in columns})
    
    # 수치형 컬럼 평균
    numeric_cols = df_filtered.select_dtypes(include='number').columns
    avg_series = df_filtered[numeric_cols].mean()
    
    # object 컬럼(예: 지점명) 최빈값
    object_cols = df_filtered.select_dtypes(include='object').columns
    mode_series = pd.Series({col: (df_filtered[col].mode().iloc[0] 
                                   if not df_filtered[col].mode().empty else np.nan)
                             for col in object_cols})
    
    # 결과 합치기
    result = pd.concat([avg_series, mode_series])
    
    return result
    
  def get_pred(self):
    ### 예측하기
    avg_reselt = self.rolling_avg_columns_safe(
        df=self.df,
        ym=f"{self.input['YY']}-{self.input['MM']}",
        columns=['평균기압','평균 상대습도','평균 기온','평균 수온',
                '적정수온','최근저수온빈도','최근적정수온빈도',
                '최근고수온빈도'],
        station=self.buoy['지점번호']
    )

    X = np.array([
        int(self.input['YY']),
        int(self.input['MM']),
        int(self.input['DD'])
    ] + avg_reselt.to_list()[:-2])   # 숫자형만 사용

    X = X.reshape(1, -1)   # (1, n_features)
    return self.model.predict(X)