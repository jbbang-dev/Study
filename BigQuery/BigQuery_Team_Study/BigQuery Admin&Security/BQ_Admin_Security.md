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
- 3가지의 상태 부여
  - PENDING : 작업이 예약되었지만 아직 시작되지 않은 상태
  - RUNNING : 작업이 시작되었음
  - SUCCESS & FAILURE : 작업 결과에 따른 반환값

```bash
# 지난 24시간 내에 생성된 작업을 확인하는 명령
# bc : 밀리초 변환
NOW=$(date +%s)
START_TIME=$(echo "($NOW - 24*60*60)*1000" | bc)
```

# 작업을 확인한 후 작업 ID를 얻음
bq --location=US ls -j -all --min_creation_time $START_TIME

# 실행 중인 작업을 취소하는 명령
bqmin_creation_timebcbq --location=US cancel bquxjob_180ae24c_16b04a8d28d

# 지역을 생략한 채 작업을 취소하는 명령
bq cancel someproject:US.bquxjob_180ae24c_16b04a8d28d
```

