<< BigQuery Administration & Security >>
===

# 1. Infrastructure 보안
- GCP에서 데이터는 유휴상태와 전송 중 상태에도 암호화되며, API를 서비스하는 인프라스트럭처는 암호화된 채널을 통해서만 접근 가능

# 2. 계정 및 접근관리
## 2.1. 계정
- 권한 부여시 개별 계정보다는 그룹으로 권한 할당
- allAuthenticatedUsers
    - 구글 계정이나 서비스 계정으로 인증을 받은 모든 사용자를 의미하는 특별한 식별자
    - 공개 데이터셋을 발행할 때 이 식별자를 주로 사용
    
    ![image](https://user-images.githubusercontent.com/77611557/154378575-7252783d-da26-48a9-815b-cadfb899092c.png)

## 2.2. 역할
- ***_predefined roll_***  
상세 이름 : roles/bigquery.[rollname]   
[Access control with IAM | BigQuery | Google Cloud](https://cloud.google.com/bigquery/docs/access-control)

  - metadataViewer : 데이터셋, 테이블 및 뷰의 메타데이터에만 접근할 수 있는 퍼미션
  - dataViewer : 메타데이터는 물론 데이터를 읽을 수 있는 퍼미션 제공
  - dataEditor : 데이터셋을 읽을 수 있는 퍼미션은 물론 데이터셋 안의 테이블 목록 확인, 생성, 갱신, 읽기 및 삭제가 가능한 모든 퍼미션
  - dataOwner : dataEditor + 데이터셋을 삭제할 수 있는 퍼미션 포함
  - readSessionUser : 프로젝트에 요금이 청구되는 빅쿼리 스토리지 API에 대한 접근 퍼미션까지 제공
  - jobUser : 쿼리를 포함한 작업을 실행할 수 있으며, 프로젝트에 요금이 청구
  - user : 작업을 실행할 수 있으며, 프로젝트에 요금이 청구될 수 있는 스토리지에 데이터셋 생성 가능
  - admin : 프로젝트 내의 모든 데이터를 관리할 수 있으며 다른 사용자의 작업을 취소할 수 있음
  
  ![image](https://user-images.githubusercontent.com/77611557/154378983-b3fdee59-b75b-4401-b90b-e26977ee0f08.png)
  
- ***_basic roll_***  
BigQuery의 데이터 세트 수준 기본 역할은 IAM 도입 전에도 존재했던 역할이며, 기본 역할의 사용을 최소화하는 것이 좋음   
  - 프로젝트 기본역할
    - Viewer : bigquery.dataViewer
    - Editor : bigquery.dataEditor
    - Owner : bigquery.dataOwner
    
    ![image](https://user-images.githubusercontent.com/77611557/154379056-65f154b8-a53f-4b57-862b-2b8b5c3a7b13.png)

# 3. 빅쿼리 관리
## 3.1. 작업관리

- 3가지의 상태 부여
   - PENDING : 작업이 예약되었지만 아직 시작되지 않은 상태
   - RUNNING : 작업이 시작되었음
   - SUCCESS & FAILURE : 작업 결과에 따른 반환값

```bash
# 지난 24시간 내에 생성된 작업을 확인하는 명령
# bc : 밀리초 변환수행, shell basic calculator
NOW=$(date +%s)
START_TIME=$(echo "($NOW - 24*60*60)*1000" | bc)

# 작업을 확인한 후 작업 ID를 얻음
bq --location=US ls -j -all --min_creation_time $START_TIME
```
![image](https://user-images.githubusercontent.com/77611557/152890872-47114cfa-0e45-41e0-9f33-6f8723fc5ee9.png)

```bash
# 실행 중인 작업을 취소하는 명령
bq --location=US cancel bquxjob_180ae24c_16b04a8d28d

# 지역을 생략한 채 작업을 취소하는 명령
bq cancel someproject:US.bquxjob_180ae24c_16b04a8d28d
```
## 3.2. 삭제된 레코드와 테이블의 복구
>- 7일 이내 데이터 복구 가능  
>- 삭제된 테이블은 2일 이내 복구 가능

- 테이블 복구
```sql
-- 테이블의 상태를 24시간 전의 상태로 복구하려면 SYSTEM_TIME AS OF 문을 사용
CREATE OR REPLACE TABLE ch10eu.restored_cycle_stations AS
SELECT 
  * 
FROM `bigquery-public-data`.london_bicycles.cycle_stations
FOR SYSTEM_TIME AS OF 
    TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
```

- 테이블 삭제-복구
```bash
# 테이블 삭제
bq rm ch10eu.restored_cycle_stations

# 120초 전의 스냅샷을 이용해 복구
NOW=$(date +%s)
SNAPSHOT=$(echo "($NOW - 120)*1000" | bc) 
bq --location=EU cp \
   ch10eu.restored_cycle_stations@$SNAPSHOT \
   ch10eu.restored_table
```

## 3.3. CI/CD
>SQL 쿼리의 버전을 관리해서 특정 시점의 스크립트를 확보하거나 시간이 지나면서 변경된 스크립트 추적할 경우

- _```Cloud Source Repository```_ 및 _```Cloud Function(Cloud Run)```_ 을 이용해 쿼리 실행
- Cloud Function에서 빅쿼리 호출
    - Cloud Source Repository에 빅쿼리 SQL 파일과 cloud function을 구현한 python 파일을 버전 관리 시스템에 등록  
    [Cloud Source Repository](https://source.cloud.google.com/looker-data-grfit/looker-bq-test-repo)
    - Cloud Function & Cloud Scheduler로 쿼리 예약 대신 사용 가능  
    [Cloud function](https://console.cloud.google.com/functions/details/asia-northeast3/function-bq-study-jsyoo-01?env=gen1&orgonly=true&project=looker-data-grfit&supportedpurview=organizationId&tab=metrics&pli=1)
    ```python
    from google.cloud import bigquery

    def bq_cloudfunc01(request):
        client = bigquery.Client()

        query_job = client.query("""
            SELECT CURRENT_DATETIME() AS Now, 'BigQuery Cloud Func Test' as test
        """)
        query_job.result()

        extract_job = client.extract_table(
            query_job.destination, 
            "gs://bq_sample_study_jsyoo/file.csv"
            )
        extract_job.result()

        return "Data Inserted!!"
    ```

# 4. 슬롯 예약(비용)
별도로 정리  
[***```BigQuery Pricing```***](https://github.com/jbbang-dev/Study/blob/master/BigQuery/BigQuery_Team_Study/BigQuery%20Pricing/BQ_Pricing.md)
# 5. 가용성과 재해 복구, 암호화
## 5.1. 존, 리전, 멀티리전
### 5.1.1. Zone
- Compute Cluster이며 보통 하나의 건물에 위치
- HA 지원하지만 H/W 장애 시 존 전체의 오프라인 가능성
### 5.1.2. Region
- 여러 zone으로 구성, 대형 캠퍼스 안의 여러 건물에 걸쳐 구성됨
- 예측 불가능한 자연재해로 데이터 유실 가능
### 5.1.3. Multi Region
- 다중 지역(국가수준)의 여러 데이터센터에 걸쳐 구성

## 5.2. 장애처리
### 5.2.1. 디스크 장애
- 회전형 디스크는 물리적인 장애 발생 가능
- 콜로서스는 디스크의 장애를 탐지하면 데이터를 다른 디스크로 복제
### 5.2.2. 머신 장애
- 구글의 데이터센터는 언제든지 장애 발생을 가정하여, 문제를 처리할 수 있는 소프트웨어를 개발
- 맵리듀스, 콜로서스, 드레멜 같은 확장형 분산 시스템 개발
- 데이터센터의 클러스터 규모가 워낙 방대하여 일부만 영향을 받음
### 5.2.3. Zone 장애
- 장애 회복을 할 수있도록 구성되어 있지만, 물리적인 장애 발생 가능
- 소프트한 장애 : 빅쿼리의 모든 클라우드 프로젝트는 1차 지역과 2차 지역을 갖고, 자동으로 이전
- 하드한 장애 : 기존의 쿼리가 취소되고 새로운 존에서 다시 시작하지만 2차 존으로 데이터가 복제되지 않는다면 쿼리의 실패
### 5.2.4. Region 장애
- 거의 발생가능성 없음
- 미리 예측한 장애 상황에 대비하여 데이터센터 셧다운 및 데이터 보호 가능
- 심각한 자연재해의 경우 데이터 유실 가능성 있음
- 멀티Region의 경우 백업본을 사용하는데 시간이 걸릴 수 있음
### 5.2.5. 내구성과 백업, 재해복구
- 멀티리전 데이터는 최소 두 리전으로 복제
- 모든 데이터는 2개의 가용 존에 복제
- 한 가용존 내의 데이터는 이레이저 인코딩을 이용해 관리
>***erasure coding***   
>- 최대 K개의 데이터가 손실 되어도 N개의 데이터만 살아 있으면 원본 데이터가 복구 가능한 방식   
>- RAID나 Mirroring에 비해서 성능에 영향이 큼 -> 주요 Cloud Storage 서비스에서 사용

- 데이터 복구
  - 실수로 지운 데이터에 대하여 7일간 복구 가능
  - 테이블은 2일간 복구 가능
### 5.2.6. 개인정보 보호와 암호화
- 다중 암호화 수행
  - 빅쿼리의 모든 데이터는 유휴 시 암호화와 네트워크를 통한 전송 시 암호화를 통해 암호화
  - 디스크의 데이터는 콜로서스 파일 암호화를 통해 암호화
  - 스트리밍 데이터는 빅테이블이나 로그 파일에 기록될 때 암호화
  - 메타데이터는 스패너에서 암호화
  - 네트워크 트래픽은 구글의 내부 원격 프로시저 호출 프로토콜을 통해 암호화
- 접근 투명성
  - 데이터에 누군가가 접근 시 감사 로그 레코드를 통해 알림을 받게 됨
- 가상 사설 클라우드 서비스 제어(VPC Service Control)
  - 사내에서만 빅쿼리 접근하도록 제한 가능
  - 타 서비스(GCS 등)에서 데이터의 흐름 제어 가능
- 고객 관리형 암호화 키(Customer Managed Encryption Keys)
  - 고객이 소유한 키를 이용한 암호화 방법
  - CMEK 또한 KMS(Key Managed Service)를 통해 관리  
  ![image](https://user-images.githubusercontent.com/77611557/154392652-60c8bd27-8871-4622-998e-dea1ed73f2c9.png)  
  ![image](https://user-images.githubusercontent.com/77611557/154392700-63341094-da33-4f4c-8031-69cfe33dc607.png)  
  ![image](https://user-images.githubusercontent.com/77611557/154392773-d9274db7-cc46-4945-bcd8-05ec7b111bd8.png)

## 5.3. 규제의 준수
### 5.3.1. 데이터 지역성
- 대부분의 국가는 데이터 저장 지역에 제한을 둠
- 데이터는 해당 지역의 실행위치에서만 접근 가능
- 데이터를 리전간에 이동하기 위해서는 BigQuery Data Transfer Service(Dataset Copy)를 이용할 때만 가능하고, GCS에서 BigQuery Dataset에 복사할 경우에는 동일 지역의 버킷이어야 함(예외적으로 US 멀티리전의 경우 어느 지역으로도 데이터 이동 가능)  
![image](https://user-images.githubusercontent.com/77611557/154388439-51052ec0-9ddf-4d75-9c2d-422a1b45c67c.png)

- 안될경우 GCS로 이전 후 destination location bucket으로 이동 및 다시 bigquery ds로 이전
### 5.3.2. 데이터 서비스에 대한 접근 제한
- 허가된 Dataset / Routine / View(Sharing Authorized ...)
  - 기본적으로 Dataset / Table 단위로 공유 권한을 부여하지 않으면 접근 제한 오류 발생
  - 권한을 부여하지 않은 테이블을 활용하는 Dataset / Routine / View에 대하여 데이터 접근 권한을 부여하는 형태
- 컬럼 수준 보안
  - Cloud Data Catalog를 활용하여 컬럼별 접근제어 설정 적용 가능  
  ![image](https://user-images.githubusercontent.com/77611557/154390125-2232f979-1199-4370-a101-1a131ed664fe.png)  

  ![image](https://user-images.githubusercontent.com/77611557/154389972-5c6535d8-2e56-4e8d-810b-b4280e9fb1be.png)  

- 테이블 접근 제어
  - 특정 테이블과 뷰만 공유 가능
- 사용자 기반 동적 필터
  - 로그인한 사용자를 기준으로 테이블의 행에 필터 적용
  ```sql
  SELECT …
  …
  WHERE REGEXP_EXTRACT(visitorEmailAddress, r’@(.+)’) = REGEXP_EXTRACT(SESSION_USER(), r’@(.+)’)
  ```
### 5.3.3. 개인과 관련된 모든 트랜잭션 제거하기
- DML 활용
```sql
DELETE DATASET.user_transactions
WHERE userId = ‘user id’
```
- Crpyo-shredding(크립토슈레딩)
  - userId 별로 고유한 암호화 키를 할당하고 모든 민감한 데이터를 해당 사용자의 암호화 키로 암호화 함
  - 암호화 키를 삭제하면 사용자의 데이터 사용 불가
```sql
-- 고유한 bike_id 컬럼 값을 저장할 테이블을 생성하는 쿼리
CREATE OR REPLACE TABLE ch10eu.encrypted_bike_keys AS
WITH bikes AS (
  SELECT
    DISTINCT bike_id
  FROM
    `bigquery-public-data`.london_bicycles.cycle_hire
)
SELECT 
  bike_id, KEYS.NEW_KEYSET('AEAD_AES_GCM_256') AS keyset 
FROM
  bikes
```
```sql
-- 키를 암호화할 함수를 구현하는 쿼리
CREATE TEMPORARY FUNCTION encrypt_int(keyset BYTES, data INT64, trip_start TIMESTAMP) AS (
  AEAD.ENCRYPT(keyset, CAST(data AS STRING), CAST(trip_start AS STRING)) 
);
CREATE TEMPORARY FUNCTION encrypt_str(keyset BYTES, data STRING, trip_start TIMESTAMP) AS (
  AEAD.ENCRYPT(keyset, data, CAST(trip_start AS STRING)) 
);
```
```sql
-- 암호화를 수행하고 그 결과를 테이블로 생성하는 쿼리
CREATE OR REPLACE TABLE ch10eu.encrypted_cycle_hire AS
SELECT
    cycle_hire.* EXCEPT(start_station_id, end_station_id, start_station_name, end_station_name)
    , encrypt_int(keyset, start_station_id, start_date) AS start_station_id
    , encrypt_int(keyset, end_station_id, start_date) AS end_station_id
    , encrypt_str(keyset, start_station_name, start_date) AS start_station_name
    , encrypt_str(keyset, end_station_name, start_date) AS end_station_name    
FROM
    `bigquery-public-data`.london_bicycles.cycle_hire
JOIN
    ch10eu.encrypted_bike_keys
USING (bike_id)
```
```sql
-- 데이터 복호화 함수
CREATE TEMPORARY FUNCTION 
decrypt(keyset BYTES, encrypted BYTES, trip_start TIMESTAMP) AS (
   AEAD.DECRYPT_STRING(keyset, encrypted, CAST(trip_start AS STRING)) 
);
```
```sql
-- 자전거 대여 시간이 가장 길었던 대여소를 찾는 쿼리
WITH duration_by_station AS (
  SELECT
      duration
      , decrypt(keyset, start_station_name, start_date) AS start_station_name
  FROM
      ch10eu.encrypted_cycle_hire
  JOIN
      ch10eu.encrypted_bike_keys
  USING (bike_id)
)
SELECT 
  start_station_name
  , AVG(duration) AS duration
FROM
  duration_by_station
GROUP BY
  start_station_name
ORDER BY duration DESC
LIMIT 5
```
```sql
-- 컬럼값에 대한 암호화 적용으로 distinct 불가
-- 전체 데이터 조회
SELECT COUNT (DISTINCT start_station_name)
FROM ch10eu.encrypted_cycle_hire
```
```sql
-- 키 값으로 데이터 삭제
DELETE ch10eu.encrypted_bike_keys
WHERE bike_id = 300
```

### 5.3.4. 데이터 유실 방지
- 민감한 데이터를 전체 스캔하여 노출 위험을 줄일 수 있음
    - 신용카드 번호
    - 회사 비밀 프로젝트 코드
    - 의료 정보 등..
- Cloud DLP(데이터 유실 방지)를 이용하여 BigQuery를 스캔하고 민감정보 보호 가능
  - Table EXPORT > Scan with DLP  
  ![image](https://user-images.githubusercontent.com/77611557/154391363-ecf3dd0b-fc38-47b2-8485-6c1ca3f0b4e3.png)

