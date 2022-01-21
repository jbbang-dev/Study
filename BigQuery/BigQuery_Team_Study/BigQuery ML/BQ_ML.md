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
```단일 feature로 설명되지 않는 값 존재```

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

    1. Observed Only MF
    - 제곱 오차 합계를 최소화 하기 위한 Squared distance
    - 관찰되지 않은 값을 0으로 처리하고, 행렬의 모든 항목에 대한 합계 계산
    - not good idea : 효과적인 추천을 할 수 없고 일반화되지 않음   
    
    2. SVD(Single Value Decomposition) 계산
    - Single Value Decomposition => sparse matrix ~ approximation = User factor * Item factor
    - 3개 행렬로 나누고(User, 속성들의 가중치, Item)
    - https://m.blog.naver.com/car9380/221175862829   
    
    3. Weighted Matrix Factorization
    - 관찰된 항목에 대한 합계와 관찰되지 않은 항목에 대한 합계(0으로 처리)로 두가지로 분해
    - 두 항에 하이퍼파라미터로 가중치 부여하여 

  - 목적 함수의 최소화 알고리즘 적용 -> 학습속도 향상을 위해
    - Stochastic Gradient Descent(확률적 경사 하강법)
      - 행렬의 일부 값을 랜덤으로 추출하여 U,V 행렬의 성분을 조정 반복
    - Weighted Alternating Least Squares(W-ALS)
      - V매트릭스에만 값을 채우고 U매트릭스 최적화, 반대로 수행하면서 반복
    - https://m.blog.naver.com/car9380/221182254937
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

***matrix_factorization*** : 사용자 팩터와 아이템 팩터의 2개의 벡터로 분해하는 협업 필터링 기술
기본 설정으로는 학습 시간 오래걸림

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
- 최종 평가손실 : 174.4057
- 총 시간 : 1시간


***l2_reg*** : 

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
- 최종 평가손실 : 1.4596
- 총 시간 : 35분

***num_factors :***
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
- 최종 평가손실 : 0.97

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
- ML.PREDICT 함수를 호출할 때 학습된 추천 모델을 전달하고 예측 수행에 필요한 일련의 MOVIEiD 및 uSERiD를 제공

## 2.3. BigQuery ML 요금제
### 2.3.1. On-Demand 요금제

![image](https://user-images.githubusercontent.com/77611557/150450797-4d83938c-e08b-4ade-98b0-411955de60ab.png)




![image](https://user-images.githubusercontent.com/77611557/150450702-0d296505-e31d-43ef-862c-98b04dede333.png)

