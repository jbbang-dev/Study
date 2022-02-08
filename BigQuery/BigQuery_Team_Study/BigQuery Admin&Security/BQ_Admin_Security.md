<< BigQuery Administration & Security >>
===


# 1. 인프라스트럭쳐 보안
- GCP에서 데이터는 유휴상태와 전송 중 상태에도 암호화되며, API를 서비스하는 인프라스트럭처는 암호화된 채널을 통해서만 접근 가능

# 2. 계정 및 접근관리
## 2.1. 계정
- 권한 부여시 개별 계정보다는 그룹으로 권한 할당
- allAuthenticatedUsers
    - 구글 계정이나 서비스 계정으로 인증을 받은 모든 사용자를 의미하는 특별한 식별자
    - 공개 데이터셋을 발행할 때 이 식별자를 주로 사용

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

- ***_basic roll_***  
BigQuery의 데이터 세트 수준 기본 역할은 IAM 도입 전에도 존재했던 역할이며, 기본 역할의 사용을 최소화하는 것이 좋음   
  - 프로젝트 기본역할
    - Viewer : bigquery.dataViewer
    - Editor : bigquery.dataEditor
    - Owner : bigquery.dataOwner
  - 데이터세트 기본역할
    - READER : bigquery.dataViewer
    - WRITER : bigquery.dataEditor
    - OWNER : bigquery.dataOwner

# 3. 빅쿼리 관리
## 3.1. 작업관리
>- 3가지의 상태 부여
>   - PENDING : 작업이 예약되었지만 아직 시작되지 않은 상태
>   - RUNNING : 작업이 시작되었음
>   - SUCCESS & FAILURE : 작업 결과에 따른 반환값

```bash
# 지난 24시간 내에 생성된 작업을 확인하는 명령
# bc : 밀리초 변환
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
>7일 이내 데이터 복구 가능  
삭제된 테이블은 2일 이내 복구 가능

- 테이블 복구
```sql
– 테이블의 상태를 24시간 전의 상태로 복구하려면 SYSTEM_TIME AS OF 문을 사용
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

