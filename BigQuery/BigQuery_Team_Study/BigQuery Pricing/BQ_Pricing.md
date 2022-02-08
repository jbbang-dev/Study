<< BigQuery 가격 책정 >>
===

# 1. 빅쿼리 가격정책표

  |분류1|분류2|분류3
  |:---|:---|:---|
  |분석 가격 책정 모델|주문형 가격 책정||
  ||정액제|가변슬롯|
  |||월간|
  |||연간|
  |||BigQuery Omni|
  |BigQuery Omni 가격 책정|||
  |저장소 가격|활성 스토리지||
  ||장기 스토리지||
  |데이터 수집 가격|batch||
  ||streaming||
  |무료 가격|||
  |Free usage tier|||


# 2. Slot
## 2.1. 개요
- SQL 쿼리를 실행하기 위해 BigQuery에서 사용되는 가상 CPU
- 쿼리 크기와 복잡성에 따라 각 쿼리에 필요한 슬롯 수를 자동으로 계산
- On-demand pricing(주문형 가격 책정 모델) / Flat-rate pricing(정액제 가격 책정 모델) 둘다 슬롯은 사용되며, 정액제는 슬롯 및 분석 용량을 명시할 수 있음(예, 2000개의 슬롯 구매 시 2000개 이하의 가상 CPU만 사용되도록 제한)
- 사용되는 슬롯 수는 Cloud Monitoring에서 확인 가능

## 2.2. slot을 활용한 쿼리 실행
- 분산 병렬 아키텍처로 쿼리를 실행하며, 각 스테이지는 worker가 동시에 실행할 수 있는 작업 단위 모델링
- 각 스테이지는 분산 셔플 아키텍처를 통해 통신하며, 동적 DAG(Directed Acyclic Graph - 방향 비순환 그래프) 형태로 실행됨
    - DAG(Directed Acyclic Graph) : 엑셀 스프레드 시트에서 셀마다 함수를 연계하여 사용하는 형태의 그래프
- BQ slot은 쿼리의 각 스테이지별로 개별 작업 단위를 실행, 자동으로 스테이지의 최적 동시 처리 계수를 10으로 결정하면 해당 스테이지 처리를 위해 10개의 슬롯 요청하는 형태
- 슬롯 리소스 절약 모드
    - 쿼리 실행 시 특정 스테이지에 대해 아무리 많은 슬롯이라도 요청 가능하며, 주문형이어도 개별 작업 단위를 큐에 임시로 두고 슬롯이 확보되면 큐의 작업단위를 가져와서 실행되는 형태 -> 아마도 자동
        1. 1000개의 슬롯만 사용 가능하나, 2000개의 슬롯을 사용해야 하는 쿼리 스테이지일 경우
        2. 1000개의 슬롯은 모두 사용하고, 1000개의 슬롯(남은 작업단위)은 큐에 추가
        3. 일부 100개 슬롯 작업이 완료되면 큐의 100개만 동적으로 선택되고 900개의 작업이 남음
        4. 500개의 슬롯 작업이 완료되면 900개의 작업 중 500개를 동적 선택하여 400개의 작업 남음

![image](https://user-images.githubusercontent.com/77611557/152895904-64bd638f-a56b-4c5e-b823-6072780ef9f8.png)



![image](https://user-images.githubusercontent.com/77611557/152895937-03ad2abb-a209-4cb3-95d5-117b59b86bec.png)



![image](https://user-images.githubusercontent.com/77611557/152895967-b66c153a-07b8-425a-a519-dd487f918c99.png)



![image](https://user-images.githubusercontent.com/77611557/152895994-53d94e22-c07b-4e41-b163-04aa0d9baa92.png)



![image](https://user-images.githubusercontent.com/77611557/152896051-9342bdfe-8b5b-4673-9d9a-b98842a7402f.png)


![image](https://user-images.githubusercontent.com/77611557/152896082-387353ef-794c-4d8d-a89a-20c43a5cbacf.png)


![image](https://user-images.githubusercontent.com/77611557/152896117-e708d98e-43b0-41db-8155-120b6e9d89db.png)


![image](https://user-images.githubusercontent.com/77611557/152896163-3e4a520f-8be4-4cd9-8f45-ee45f7e29045.png)


![image](https://user-images.githubusercontent.com/77611557/152896191-2caf62ee-b1ad-4bb1-9232-091c45e99e4a.png)


![image](https://user-images.githubusercontent.com/77611557/152896241-286d58dd-fcfb-4e9f-9ebf-04461b959494.png)


![image](https://user-images.githubusercontent.com/77611557/152896275-62095e00-eff9-4812-9801-182ae74dfc91.png)


![image](https://user-images.githubusercontent.com/77611557/152896331-e28f3e3d-653e-47b2-865b-042d73b88694.png)


![image](https://user-images.githubusercontent.com/77611557/152896359-201cb80d-a915-42a6-9fc9-5acbaacae1f2.png)











