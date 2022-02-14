<< BigQuery Machine Learning >>
===

# 1. Recommendation System 개요
> - 정보 필터링 기술의 일종으로, 특정 사용자가 관심을 가질만한 정보(영화, 음악, 책, 뉴스, 이미지, 웹페이지 등)을 추천
> - 등급 또는 과거 구매를 기반으로 다음 제품을 권장
> - ***Collaborative Filtering(협업 필터링)*** 방식과 ***Content-based Filtering(컨텐츠 기반 필터링)*** 방식을 통해 추천 목록을 구성

## 1.1. Collaborative filtering
> _콘텐츠 기반 필터링의 일부 제한 사항을 해결하기 위해 협업 필터링은 사용자와 항목 간의 유사성을 동시에 사용 하여 권장 사항을 제공합니다. 즉, 협업 필터링 모델은 유사한 사용자 B의 관심사를 기반으로 사용자 A에게 항목을 추천할 수 있습니다._

> 예시 : 영화 추천 시스템
>> 다음 항목을 이용하여 영화를 추천
>>  - 각 행은 사용자
>>  - 각 열은 항목(영화)
>>  - 사용자가 과거에 좋아했던 영화와의 유사성    
>>  - 유사한 사용자가 좋아한 영화

### 1.1.1. 1D Embedding
- 영화에 스칼라값 할당
  - 영화가 어린이용인지(-1, 부정적 가치) 성인용인지(1, 긍정적 가치)로 [-1, 1] 범위
  - 사용자가 어린이영화에 관심(-1, 부정적 가치) 성인용영화 관심(1, 긍정적 가치)로 [-1, 1] 범위
  ![image](https://user-images.githubusercontent.com/77611557/150443399-549f4087-2cd3-4639-bc54-1cf91a9a10da.png)
  
- 아래 다이어그램으로 특정 사용자가 시청한 영화를 식별
![image](https://user-images.githubusercontent.com/77611557/150443461-476d3fd4-13cf-4883-bbfd-4924d66de704.png)
```
단일 feature로 설명되지 않는 값 존재
```

### 1.1.2. 2D Embedding

- 영화가 블록버스터인지 아트하우스(예술영화) 인지 feature 추가
![image](https://user-images.githubusercontent.com/77611557/150443499-f708dbb6-47cf-4125-89c4-0d7e035220b3.png)
```
동일한 embedding 공간에 배치
시청한 영화에 대하여 1에 가깝고, 그렇지 않으면 0
```

- 사용자를 동일한 임베딩 공간에 재배치
![image](https://user-images.githubusercontent.com/77611557/150443518-ac335d94-d2de-40ef-af63-8cf967780385.png)

### 1.1.3. Matrix Factorization

- 행렬 인수분해 및 임베딩 학습
  - Rating Matrix를 User Latent Matrix와 Item Latent Matrix로 분해
  ![image](https://user-images.githubusercontent.com/77611557/150443563-4c52517f-4d68-4a41-b9c4-16f2c6bd3825.png)
  - Objective Function(목적 함수) 선택
  ![image](https://user-images.githubusercontent.com/77611557/150443621-e80e1b0d-c629-4640-aef1-1faa0c4bb905.png)   

    - Observed Only MF
      - 제곱 오차 합계를 최소화 하기 위한 Squared distance
      - 관찰되지 않은 값을 0으로 처리하고, 행렬의 모든 항목에 대한 합계 계산
      - not good idea : 효과적인 추천을 할 수 없고 일반화되지 않음   
    
    - SVD(Single Value Decomposition, 특이값 분해) 계산
      - https://m.blog.naver.com/car9380/221175862829   
      - Single Value Decomposition => sparse matrix ~ approximation = User factor * Item factor
      - 3개 행렬로 나누고(User, 속성들의 가중치, Item)

    - Weighted Matrix Factorization
      - 관찰된 항목에 대한 합계와 관찰되지 않은 항목에 대한 합계(0으로 처리)로 두가지로 분해
      - 두 항에 하이퍼파라미터로 가중치 부여하여   

  - 학습속도 향상을 위한 목적 함수의 최소화 알고리즘 적용
    - https://m.blog.naver.com/car9380/221182254937
    - Stochastic Gradient Descent(확률적 경사 하강법)
      - 행렬의 일부 값을 랜덤으로 추출하여 U,V 행렬의 성분을 조정 반복
    - Weighted Alternating Least Squares(W-ALS)
      - V매트릭스에만 값을 채우고 U매트릭스 최적화, 반대로 수행하면서 반복

  - SGD / WALS 장단점
    - SGD의 장단점
      - 장점 
        - 매우 유연하여 다른 Loss function을 사용할 수 있다.
        - 병렬화 할 수 있다.
      - 단점
        - 느림 - 빠르게 수렴하지 않는다.
        - 관찰되지 않은 항목을 다루기가 더 어렵다(Negative Sampling 또는 Gravity를 사용해야 함).
    - WALS의 장단점
      - 장점
        - 병렬화 할 수 있다.
        - SGD보다 빠르게 수렴한다.
        - 관찰되지 않은 항목을 더 쉽게 처리할 수 있다.
      - 단점
        - Loss Squares에만 의존한다.

## 1.2. 콘텐츠 기반 필터링
> _사용자의 과거 행동, 좋아하는 것, 피드백을 통하여 유사한 다른 것을 추천하는 것_

> 예시 : 어플리케이션 추천 시스템 

![image](https://user-images.githubusercontent.com/77611557/150443707-1375cc50-ba47-4231-9c63-063eddb7c910.png)
- 좌측 : 카테고리와 앱으로 이루어진 사용자가 설치한 앱 및 각 앱의 기능 표현
- 우측 : 각 개발사의 개인 사용자에 대한 유사성 메트릭에 따른 점수 할당
- 장단점
  - 장점
    - 권장 사항은 이 사용자에게만 적용되므로 다른 사용자의 데이터가 필요하지 않음, 많은 수의 사용자로 쉽게 확장됨
    - 사용자의 특정 관심사를 포착할 수 있으며 다른 사용자가 관심을 갖지 않는 틈새 항목 추천 가능
  - 단점
    - 항목별 기능 표현은 직접 관리되므로, 많은 도메인 지식 필요
    - 사용자의 기존 관심사를 기반으로만 추천 가능, 제한적

# 2. 추천 시스템 모델링
>무비렌즈 데이터셋을 활용하여 협업 필터링 행렬분해 사용
## 2.1. 행렬분해 모델 생성

***[model_type='matrix_factorization']*** : 사용자 팩터와 아이템 팩터의 2개의 벡터로 분해하는 협업 필터링 기술이며, 기본 설정으로는 학습 시간 오래걸림

```sql
CREATE OR REPLACE MODEL ch09eu.movie_recommender
options(model_type='matrix_factorization',
        user_col='userId', item_col='movieId', rating_col='rating')
AS
SELECT 
userId, movieId, rating
FROM ch09eu.movielens_ratings
```
결과
- 반복 : 5회
- 최종 학습손실 : 0.5734
- 최종 평가손실 : ```174.4057```
- 총 시간 : 1시간


***[l2_reg=0.2]*** : 적용된 L2 정규화의 양
> ***L2 regularization*** : 가중치의 제곱합에 비례하여 가중치에 페널티를 주는 정규화 유형. L2 정규화는 이상치 가중치(양수 값이 높거나 음수 값이 낮은 값)를 0에 가깝게 만드는 데 도움이 되지만 0에 가깝지는 않다. (L1 정규화와 대조) L2 정규화는 항상 선형 모델의 일반화를 향상시킨다.<br>
(https://developers.google.com/machine-learning/glossary?hl=en#l2-regularization)

```sql
CREATE OR REPLACE MODEL ch09eu.movie_recommender_l2
options(model_type='matrix_factorization',
        user_col='userId', item_col='movieId', rating_col='rating', l2_reg=0.2)
AS
SELECT 
userId, movieId, rating
FROM ch09eu.movielens_ratings
```
결과
- 반복 : 3회
- 최종 학습손실 : 0.6509
- 최종 평가손실 : ```1.4596```
- 총 시간 : 35분

***[num_factors=16]*** : 행렬 분해 모델에 사용할 잠재요인의 수를 지정
```sql
CREATE OR REPLACE MODEL ch09eu.movie_recommender_16
options(model_type='matrix_factorization',
        user_col='userId', item_col='movieId', rating_col='rating', l2_reg=0.2, num_factors=16)
AS
SELECT 
userId, movieId, rating
FROM ch09eu.movielens_ratings
```
결과
- 최종 평가손실 : ```0.97```

## 2.2. 행렬분해 모델 활용
```sql 
SELECT * FROM
ML.PREDICT(MODEL ch09eu.movie_recommender_16, (
  SELECT 
    movieId, title, 903 AS userId
  FROM ch09eu.movielens_movies, UNNEST(genres) g
  WHERE g = 'Comedy'
))
ORDER BY predicted_rating DESC
LIMIT 5
```
- 학습된 모델을 사용해 추천 목록 제공
- ML.PREDICT 함수를 호출할 때 학습된 추천 모델을 전달하고 예측 수행에 필요한 일련의 movieId 및 userId를 제공

## 2.3. BigQuery ML 요금제
> 행렬분해는 ***정액제나 예약 고객만 사용 가능***하며, ***주문형 고객은 가변슬롯***을 통해 행렬분해를 사용해야 함
### 2.3.1. On-Demand 요금제
![image](https://user-images.githubusercontent.com/77611557/150450797-4d83938c-e08b-4ade-98b0-411955de60ab.png)

### 2.3.2. Capacity Commitment and Reservation 요금제(slot 요금제)
![image](https://user-images.githubusercontent.com/77611557/150450702-0d296505-e31d-43ef-862c-98b04dede333.png)


# 3. GCP의 커스텀 머신러닝 모델
## 3.1. Hyperparameter Tuning

- 머신러닝 수행 시 많은 파라미터들을 임의로 선택함. 
  - 학습률 : LEARN_RATE
  - L2 정규화 수준 : L2_REG
  - 신경망의 계층 및 노드 수 : BATCH_SIZE 
  - 부스팅 트리의 최대 심도 : AUTO_CLASS_WEIGHTS 
  - 행렬분해 모델의 feature 수 : NUM_FACTORS
> 각 파라미터에 대하여 어떤 값을 선택하는지에 따라 더 나은 모델을 만들 수 있는데, 이렇게 적절한 값을 선택하는것을 하이퍼파라미터 튜닝이라고 함   

### 3.1.1. 파이썬에서 하이퍼 파라미터 튜닝하기
```python
# On Notebook instances in Google Cloud, these are already installed
#!python -m pip install google-cloud-bigquery
#%load_ext google.cloud.bigquery

from multiprocessing.dummy import Pool as ThreadPool
from google.cloud import bigquery
import numpy as np
PROJECT='cloud-training-demos'  # CHANGE THIS

class Range:
    def __init__(self, minvalue, maxvalue, incr=1):
        self._minvalue = minvalue
        self._maxvalue = maxvalue
        self._incr = incr
    def values(self):
        return range(self._minvalue, self._maxvalue, self._incr) 

class Params:
    def __init__(self, num_clusters):
        self._num_clusters = num_clusters
        self._model_name = 'ch09eu.london_station_clusters_{}'.format(num_clusters)
        self._train_query = """
          CREATE OR REPLACE MODEL {}
          OPTIONS(model_type='kmeans', 
                  num_clusters={}, 
                  standardize_features = true) AS
          SELECT * except(station_name)
          from ch09eu.stationstats
        """.format(self._model_name, self._num_clusters)
        self._eval_query = """
          SELECT davies_bouldin_index AS error
          FROM ML.EVALUATE(MODEL {});
        """.format(self._model_name)
        self._error = None
        
    def run(self):
        bq = bigquery.Client(project=PROJECT)
        job = bq.query(self._train_query, location='EU')
        job.result() # wait for job to finish
        evaldf = bq.query(self._eval_query, location='EU').to_dataframe()
        self._error = evaldf['error'][0]
        return self
    
    def __str__(self):
        fmt = '{!s:<40} {:>10f} {:>5d}'
        return fmt.format(self._model_name, self._error, self._num_clusters)
    
def train_and_evaluate(num_clusters: Range, max_concurrent=3):
    # grid search means to try all possible values in range
    params = []
    for k in num_clusters.values():
        params.append(Params(k))
    
    # 멀티쓰레드를 사용하여 전체작업 수행
    print('Grid search of {} possible parameters'.format(len(params)))
    pool = ThreadPool(max_concurrent)
    # Parms 클래스의 run 메서드를 이용하여 학습 및 평가쿼리 호출
    results = pool.map(lambda p: p.run(), params)
    
    # 오름차순 정렬
    return sorted(results, key=lambda p: p._error)
    
params = train_and_evaluate(Range(3, 20))
print(*params, sep='\n')
```
***결과***
```cmd
ch09eu.london_station_clusters_19          1.400756    19
ch09eu.london_station_clusters_15          1.415517    15
ch09eu.london_station_clusters_18          1.429912    18
ch09eu.london_station_clusters_14          1.438088    14
ch09eu.london_station_clusters_13          1.438440    13
ch09eu.london_station_clusters_17          1.454715    17
ch09eu.london_station_clusters_16          1.456185    16
ch09eu.london_station_clusters_11          1.502263    11
ch09eu.london_station_clusters_12          1.511940    12
ch09eu.london_station_clusters_10          1.529150    10
ch09eu.london_station_clusters_7           1.551265     7
ch09eu.london_station_clusters_9           1.571020     9
ch09eu.london_station_clusters_6           1.571398     6
ch09eu.london_station_clusters_4           1.596398     4
ch09eu.london_station_clusters_8           1.621974     8
ch09eu.london_station_clusters_5           1.660766     5
ch09eu.london_station_clusters_3           1.681441     3
```

## 3.2. AutoML
> - AutoML은 코드를 작성하지 않고도 자동으로 최첨단의 머신러닝 모델을 생성하고 배포하는 제품
> - 최고의 머신러닝 전문가가 수동으로 제작한 모델과 비슷한 품질의 모델을 빌드하기 위해 다양한 피처 엔지니어링, 하이퍼파라미터 튜닝, 신경 구조 검색, 전송 학습 방법을 혼합해 적용한다.   
> - AutoML 비전은 이미지를 업로드하고 이미지의 레이블을 식별해서 이미지 분류나 객체 감지 모델 학습을 시작하기 위한 웹 기반 인터페이스를 제공한다.   
> - 빅쿼리는 주로 구조화된 데이터나 준구조화된 데이터를 다루고, 관련 AutoML 모델은 AutoML 자연어, AutoML 테이블, AutoML 추천 등에 주로 사용한다.
>> [Vertex AI Create Dataset](https://console.cloud.google.com/vertex-ai/datasets/create?project=looker-data-grfit)
## 3.3. TensorFlow
> - Deep Learning Framework : <a href="https://www.tensorflow.org/?hl=ko" target="_blank">TensorFlow</a>
> - 빅쿼리 ML은 확장 가능하고 편리, AutoML은 강력하고 정확   
> - 케라스 또는 텐서플로 ML 라이브러리를 이용하여 고유한 사용자 지정 모델을 구축해야 하는 경우 존재   
> - 빅쿼리와 텐서플로 모델 간에는 상호운용성이 있음
>> - 텐서플로 모델을 빅쿼리에 로드하고 빅쿼리 모델을 텐서플로의 SavedModel 형식으로 내보낼 수 있음
>> - 텐서플로로 모델을 학습시키고 빅쿼리로 예측하거나
>> - 빅쿼리에서 모델을 학습시킨 후 텐서플로 서빙에 배포하는것이 유리할 수 있음
>> - 텐서플로 코드에서 빅쿼리에 직접 접근하고 빅쿼리 테이블을 텐서플로 레코드로 내보내 데이터를 변환하는 것도 가능

### 3.3.1. 텐서플로 빅쿼리 클라이언트
- https://github.com/tensorflow/io/blob/master/tensorflow_io/bigquery.md
- 빅쿼리 스토리지에서 효율적으로 쿼리 실행하지 않고 직접 데이터를 읽기 위해 스토리지 API를 사용

### 3.3.2. 텐서플로로 내보내기
- 자바스크립트와 tensorflow.js를 사용하는 웹 브라우저, 텐서플로 라이트를 사용하는 임베디드 장치나 모바일 애플리케이션, kubeflow를 사용하는 쿠버네티스 클러스터, API 플랫폼 예측을 사용하는 REST API 등 다양한 방법으로 텐서플로 모델에 대한 예측을 실행할 수 있음
- 빅쿼리 ML 모델을 텐서플로의 SavedModel로 내보내는 것이 유리할 때가 있음

### 3.3.3. 텐서플로 모델로 예측하기
- 텐서플로에서 모델을 학습하고 SavedModel로 내보냈다면, 텐서플로 모델을 빅쿼리로 가져와 ML.PREDICT SQL 함수로 예측할 수 있음
빅쿼리는 어떤 쿼리도 예약이 가능하므로 이 방법은 배치예측을 실행하는 경우에 매우 유용함
- 모델을 빅쿼리로 가져오려면 그저 다른 MODEL_TYPE을 지정하고 SavedModel을 내보낸 모델 경로를 지정하기만 하면 됨
```sql
-- 텐서플로 모델을 생성하는 쿼리
CREATE OR REPLACE MODEL ch09eu.txtclass_tf
OPTIONS (model_type='tensorflow',
         model_path='gs://bucket/some/dir/1549825580/*')
```

# Reference
- [ 구글 빅쿼리 완벽 가이드: 발리아파 락쉬마난, 조던 티가니 저/변성윤, 장현희 역, 책만, 2020 ]
- [Introduction | Recommendation Systems | Google Developers](https://developers.google.com/machine-learning/recommendation?hl=en)   
- [Hyperparameter tuning in Cloud Machine Learning Engine using Bayesian Optimization | Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/hyperparameter-tuning-cloud-machine-learning-engine-using-bayesian-optimization)   
- [Next Steps | Machine Learning Crash Course | Google Developers](https://developers.google.com/machine-learning/crash-course/next-steps)   
- [BigQuery ML documentation | Google Cloud](https://cloud.google.com/bigquery-ml/docs#docs)   
- [The CREATE MODEL statement | BigQuery ML | Google Cloud](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-create)   
- [AutoML Tables documentation | Google Cloud](https://cloud.google.com/automl-tables/docs)   
- [BigQuery ML pricing | BigQuery: Cloud Data Warehouse | Google Cloud](https://cloud.google.com/bigquery-ml/pricing)   
- [Pricing | BigQuery: Cloud Data Warehouse](https://cloud.google.com/bigquery/pricing?hl=ko#flex-slots-pricing)
- [추천시스템 협업필터링 - Matrix Factorization : 네이버 블로그](https://m.blog.naver.com/car9380/221175862829)   
- [Matrix Factorization ALS SGD](https://m.blog.naver.com/car9380/221182254937)   
- [#5 행렬 인수분해(Matrix Factorization)](https://alsoj.tistory.com/268)
