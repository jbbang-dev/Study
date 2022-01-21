<< BigQuery Machine Learning >>
===

# 1. Recommendation System
> - 정보 필터링 기술의 일종으로, 특정 사용자가 관심을 가질만한 정보(영화, 음악, 책, 뉴스, 이미지, 웹페이지 등)을 추천
> - 등급 또는 과거 구매를 기반으로 다음 제품을 권장
> - ***Collaborative Filtering(협업 필터링)*** 방식과 ***Content-based Filtering(컨텐츠 기반 필터링)*** 방식을 통해 추천 목록을 구성

## 1.1. Collaborative filtering
- 예시 : 영화 추천 시스템
- 다음 항목을 이용하여 영화를 추천
  - 각 행은 사용자
  - 각 열은 항목(영화)
  - 사용자가 과거에 좋아했던 영화와의 유사성    
  - 유사한 사용자가 좋아한 영화

- 1D Embedding
  - 영화가 어린이용인지(-1, 부정적 가치) 성인용인지(1, 긍정적 가치)로 [-1, 1] 범위
  - 사용자가 어린이영화에 관심(-1, 부정적 가치) 성인용영화 관심(1, 긍정적 가치)로 [-1, 1] 범위
![image](https://user-images.githubusercontent.com/77611557/150443399-549f4087-2cd3-4639-bc54-1cf91a9a10da.png)



![image](https://user-images.githubusercontent.com/77611557/150443461-476d3fd4-13cf-4883-bbfd-4924d66de704.png)



![image](https://user-images.githubusercontent.com/77611557/150443499-f708dbb6-47cf-4125-89c4-0d7e035220b3.png)



![image](https://user-images.githubusercontent.com/77611557/150443518-ac335d94-d2de-40ef-af63-8cf967780385.png)



![image](https://user-images.githubusercontent.com/77611557/150443563-4c52517f-4d68-4a41-b9c4-16f2c6bd3825.png)



![image](https://user-images.githubusercontent.com/77611557/150443621-e80e1b0d-c629-4640-aef1-1faa0c4bb905.png)




![image](https://user-images.githubusercontent.com/77611557/150443707-1375cc50-ba47-4231-9c63-063eddb7c910.png)
