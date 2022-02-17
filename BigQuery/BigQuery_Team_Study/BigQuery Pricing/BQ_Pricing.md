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
- SQL 쿼리를 실행하기 위해 BigQuery에서 사용되는 ```가상 CPU```
- 쿼리 크기와 복잡성에 따라 각 쿼리에 필요한 슬롯 수를 자동으로 계산
- On-demand pricing(주문형 가격 책정 모델) / Flat-rate pricing(정액제 가격 책정 모델) 둘다 슬롯은 사용되며, 정액제는 슬롯 및 분석 용량을 명시할 수 있음(예, 2000개의 슬롯 구매 시 2000개 이하의 가상 CPU만 사용되도록 제한)
- 사용되는 슬롯 수는 Cloud Monitoring에서 확인 가능

## 2.2. slot을 활용한 쿼리 실행
- 분산 병렬 아키텍처로 쿼리를 실행하며, 각 스테이지는 worker가 동시에 실행할 수 있는 작업 단위 모델링
- 각 스테이지는 분산 셔플 아키텍처를 통해 통신하며, 동적 DAG(Directed Acyclic Graph - 방향 비순환 그래프) 형태로 실행됨
    - DAG(Directed Acyclic Graph) : 엑셀 스프레드 시트에서 셀마다 함수를 연계하여 사용하는 형태의 그래프
- BQ slot은 쿼리의 각 스테이지별로 개별 작업 단위를 실행
    - 예를 들어, 자동으로 스테이지의 최적 동시 처리 계수를 10으로 결정하면 해당 스테이지 처리를 위해 10개의 슬롯 요청하는 형태
- 슬롯 리소스 절약 모드
    - 쿼리 실행 시 특정 스테이지에 대해 아무리 많은 슬롯이라도 요청 가능하며, 주문형이어도 개별 작업 단위를 큐에 임시로 두고 슬롯이 확보되면 큐의 작업단위를 가져와서 실행되는 형태 -> 아마도 자동
        1. 1000개의 슬롯만 사용 가능하나, 2000개의 슬롯을 사용해야 하는 쿼리 스테이지일 경우
        2. 1000개의 슬롯은 모두 사용하고, 1000개의 슬롯(남은 작업단위)은 큐에 추가
        3. 일부 100개 슬롯 작업이 완료되면 큐의 100개만 동적으로 선택되고 900개의 작업이 남음
        4. 500개의 슬롯 작업이 완료되면 900개의 작업 중 500개를 동적 선택하여 400개의 작업 남음
        ![image](https://user-images.githubusercontent.com/77611557/152895904-64bd638f-a56b-4c5e-b823-6072780ef9f8.png)
    - slot은 여러 프로젝트 간 프로젝트 내 여러 작업 내에 균등하게 배포됨, 모든 쿼리는 언제든지 사용 가능한 모든 슬롯에 액세스 가능하며 동적으로 자동 재할당됨

## 2.3. 워크로드 관리
- 별도의 프로젝트를 구성하여(추천 프로젝트 명 : ***bq-COMPANY_NAME-admin***) 중앙에서 슬롯을 관리하게 하고, 프로젝트/부서/팀별로 슬롯 할당 및 용량 분산 관리 가능  
![image](https://user-images.githubusercontent.com/77611557/152895937-03ad2abb-a209-4cb3-95d5-117b59b86bec.png)
    
## 2.4. 예약 사용하기
### 2.4.1. Buy slots
![image](https://user-images.githubusercontent.com/77611557/154381107-88f07ee6-8096-43d7-8336-296e19f37b0a.png)
![image](https://user-images.githubusercontent.com/77611557/154381146-e954c3e6-9e21-4e42-9906-30dc2295473d.png)

### 2.4.2. Create reservation 
![image](https://user-images.githubusercontent.com/77611557/154381261-ba4e7776-84ab-4de7-a2cc-8d94714982a7.png)

### 2.4.3. Create assignment
![image](https://user-images.githubusercontent.com/77611557/154381651-595c0e81-844a-41fe-bb02-285fc5af4164.png)

# 3. 가격 책정 모델
## 3.1. 분석 가격 책정
>SQL, UDF 스크립트, DML, DDL을 포함한 쿼리를 처리할 때 발생하는 비용   

### 3.1.1. 주문형 가격 책정 모델
- 쿼리에서 처리된 바이트 수에 대한 요금 부과, 사용한 만큼만 지불
- 쿼리는 공유 슬롯 풀을 사용하므로 실행시 마다 성능이 다를 수 있음
- 테이블당 데이터 처리량은 최소 10MB로 간주함
- 일반적으로 단일 프로젝트에서 모든 쿼리 간에 공유되는 최대 2000개의 동시 슬롯 이용 가능
![image](https://user-images.githubusercontent.com/77611557/152895967-b66c153a-07b8-425a-a519-dd487f918c99.png)
- 컬럼 기반 데이터 구조에서 열의 총 데이터 처리량을 기준으로 요금 청구되며, 열의 데이터 유형에 따로 계산
![image](https://user-images.githubusercontent.com/77611557/152895994-53d94e22-c07b-4e41-b163-04aa0d9baa92.png)

### 3.1.2. 정액제
- 가상 CPU인 슬롯을 구매하고, 이 용량을 소비하여 처리한 바이트에 대해서는 요금이 청구되지 않음
- 장기 약정에 대해 할인된 가격으로 보장된 용량을 구매 가능
- 예측가능 : 몇개의 슬롯을 구매하면 몇개의 쿼리를 실행하든 같은 가격을 지불하므로, 비용을 예상하기를 원하는 기업에 적합
- 최소 100개 구매 가능
- 구입한 슬롯 및 유휴 용량 또한 다른 조직과 공유 안됨
- 종류
    - 월간
    ![image](https://user-images.githubusercontent.com/77611557/152896051-9342bdfe-8b5b-4673-9d9a-b98842a7402f.png)
    - 연간(장기 약정)
    ![image](https://user-images.githubusercontent.com/77611557/152896082-387353ef-794c-4d8d-a89a-20c43a5cbacf.png)
    - 가변슬롯(초단기 약정)
        - 가변 슬롯은 특수 약정 유형
        - 약정이 활성화된 후 60초까지는 가변 슬롯 약정을 삭제할 수 없습니다.
        - 60초가 지나면 언제든지 취소할 수 있으며 약정이 활성화된 시간(초)에 대해서만 요금이 청구됩니다.
        - 예를 들면 다음과 같습니다.  
        10월 5일 6:00:00에 약정을 구매하는 경우 해당 순간에 요금이 청구되기 시작합니다.  
        10월 5일 6:01:00까지는 삭제할 수 없습니다.  
        10월 5일 6:01:01에 삭제하는 경우 61초로 청구됩니다(10월 5일 6:00:00 ~ 10월 5일 6:01:01).  
        - 약정을 삭제하지 않으면 요금이 계속 청구됩니다.
    ![image](https://user-images.githubusercontent.com/77611557/152896117-e708d98e-43b0-41db-8155-120b6e9d89db.png)

## 3.2. BigQuery Omni 가격 책정
- 멀티 클라우드로 스토리지(데이터)가 분산되어있는 각 클라우드 내에서 빅쿼리 처리 수행되는 형태
  - AWS : S3 Storage
  - Azure : Blob Storage
- https://cloud.google.com/bigquery-omni/docs/introduction
- 현재 US-east-1 밖에 없음
- 월간 정액제 가격 예시
  - AWS  
  ![image](https://user-images.githubusercontent.com/77611557/154382870-7375ad82-982a-46cd-be14-2ea46cc7646e.png)

  - Azure  
  ![image](https://user-images.githubusercontent.com/77611557/154382926-26680710-9316-48af-a543-56fc538c8ebd.png)
  
## 3.3. 스토리지 가격 책정
>BigQuery에 로드한 데이터를 저장하는 데 드는 비용  

- 활성 스토리지 
    - 지난 90일 동안 수정된 모든 테이블 또는 테이블 파티션 포함
- 장기 스토리지
    - 연속으로 90일 동안 수정되지 않은 모든 테이블 또는 테이블 파티션  
    - 자동으로 50% 인하되며, 활성 스토리지와 성능차이 없음
- 비용
![image](https://user-images.githubusercontent.com/77611557/152896163-3e4a520f-8be4-4cd9-8f45-ee45f7e29045.png)
- 다음 작업을 수행할 경우, 활성 90일 카운트로 전환
![image](https://user-images.githubusercontent.com/77611557/152896191-2caf62ee-b1ad-4bb1-9232-091c45e99e4a.png)

## 3.4. 데이터 수집 가격 책정
![image](https://user-images.githubusercontent.com/77611557/152896241-286d58dd-fcfb-4e9f-9ebf-04461b959494.png)

## 3.5. 데이터 추출 가격 책정
![image](https://user-images.githubusercontent.com/77611557/152896275-62095e00-eff9-4812-9801-182ae74dfc91.png)

## 3.6. 무료 작업
![image](https://user-images.githubusercontent.com/77611557/152896331-e28f3e3d-653e-47b2-865b-042d73b88694.png)

## 3.7. 무료 사용량 등급
![image](https://user-images.githubusercontent.com/77611557/152896359-201cb80d-a915-42a6-9fc9-5acbaacae1f2.png)

# 4. Biiling Export
- Billing Export 메뉴에서 빅쿼리 내보내기를 선택하여 정기적으로 데이터 전달
```sql
SELECT
  invoice.month
  , product
  , ROUND(SUM(cost)
         + SUM(IFNULL((SELECT SUM(c.amount) FROM UNNEST(credits) c),
               0))
         , 2) AS monthly_cost
FROM ch10eu.gcp_billing_export_v1_XXXXXX_XXXXXX_XXXXXX
GROUP BY 1, 2
ORDER BY 1 ASC, 2 ASC
```
- [PUBLIC - GCP Advanced Billing Dashboard](https://datastudio.google.com/u/0/reporting/1MJ0GHVvcHI6cRHwMKyeSK3r7UoabEHOH/page/WXzW)

- label
    - 데이터셋에 레이블을 정의하여 요금 보고서 분류
    - label key/value값을 셋팅하고 export 된 데이터 셋에서 labels 속성을 이용해 구분지어 확인 가능
    ```sql
    SELECT
        invoice.month
        , label.value
        , ROUND(SUM(cost)
                + SUM(IFNULL((SELECT SUM(c.amount) FROM UNNEST(credits) c),
                    0))
                , 2) AS monthly_cost
    FROM 
        ch10eu.gcp_billing_export_v1_XXXXXX_XXXXXX_XXXXXX
        , UNNEST(labels) AS label
    WHERE
        label.key = 'environment'
    GROUP BY 1, 2
    ORDER BY 1 ASC, 2 ASC
    ```

# Reference 
- [Pricing | BigQuery: Cloud Data Warehouse](https://cloud.google.com/bigquery/pricing)
- [Introduction to Reservations | BigQuery | Google Cloud](https://cloud.google.com/bigquery/docs/reservations-intro)
- [Understand slots | BigQuery | Google Cloud](https://cloud.google.com/bigquery/docs/slots)
- [Capacity commitment plans | BigQuery | Google Cloud](https://cloud.google.com/bigquery/docs/reservations-details#commitment-plans)
- [Workload management using Reservations | BigQuery | Google Cloud](https://cloud.google.com/bigquery/docs/reservations-workload-management)
- [Purchase and manage slot capacity | BigQuery | Google Cloud](https://cloud.google.com/bigquery/docs/reservations-commitments)
- [What is BigQuery Omni? | Google Cloud](https://cloud.google.com/bigquery-omni/docs/introduction)
- [Cloud Billing 데이터를 BigQuery로 내보내기  |  Google Cloud](https://cloud.google.com/billing/docs/how-to/export-data-bigquery?hl=ko)
- [Google 데이터 스튜디오로 시간별 지출 시각화  |  Cloud Billing  |  Google Cloud](https://cloud.google.com/billing/docs/how-to/visualize-data?hl=ko)
