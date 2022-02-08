<< BigQuery With Development >>
===

# 1. REST API
## 1.1. REST API?
  - [HTTP - 위키백과, 우리 모두의 백과사전](https://ko.wikipedia.org/wiki/HTTP)
  - [REST - 위키백과, 우리 모두의 백과사전](https://ko.wikipedia.org/wiki/REST)

## 1.2. REST API 사용
  - BigQuery API | Google Cloud
  - Cloud SDK 설치 : Quickstart: Getting started with Cloud SDK
  - GCP 인증 : Getting started with authentication
  - 샘플 api : Method: tables.list | BigQuery | Google Cloud
    - 인증정보 설정
      - Option 1 - Service Account Key Pair 사용
        ```bash
        set GOOGLE_APPLICATION_CREDENTIALS="looker-data-grfit-536efecf194c.json"
        ```
      - Option 2 - browser를 통한 login 인증
        ```bash
        gcloud auth application-default login
        ```
    - API 호출
    ```bash
    PROJECT=$(gcloud config get-value project)
    access_token=$(gcloud auth application-default print-access-token)
    curl -H "Authorization: Bearer $access_token" -H "Content-Type: application/json" -X GET "https://www.googleapis.com/bigquery/v2/projects/$PROJECT/datasets/pipelining_sample/tables"
    ```
    
## 1.3. SQL 사용
  - Query를 이용하여 스키마 정보 확인
  - SQL로 가능한 BigQuery 관련 정보들
    - CREATE / ALTER / DROP TABLE
    - INSERT / DELETE / UPDATE / MERGE
    - Dataset Metadata
      - INFORMATION_SCHEMA.SCHEMATA
      - INFORMATION_SCHEMA.SCHEMATA_OPTIONS
    - Table(View) Metadata
      - INVORMATION_SCHEMA.TABLES
      - INVORMATION_SCHEMA.TABLE_OPTIONS
      - INVORMATION_SCHEMA.COLUMNS
      - INVORMATION_SCHEMA.COLUMN_OPTIONS
    - Job Metadata
      - NFORMATION_SCHEMA.JOBS_BY_USER
      - INFORMATION_SCHEMA.JOBS_BY_PROJECT
      - INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION
    - 도구 사용과 숙련도 차원에서 SQL을 사용하는 것이 더 나은 경우도 있음
  - 쿼리를 API로 수행
    ```bash
    request.json 
    curl -H "Authorization: Bearer $access_token"   -H "Content-Type: application/json"   -X POST   -d @request.json   "https://www.googleapis.com/bigquery/v2/projects/$PROJECT/queries"
    ```
  - API 옵션(제약사항)
    ```json
    {
      "useLegacySql": false,
      "timeoutMs": 0,
      "useQueryCache": false,
      "query": \"${QUERY_TEXT}\"
    }
    ```

# 2. Google Cloud Client Library(with Python, Jupyter)
## 2.1. Python / Virtual Environment / Jupyter notebook 사용 환경 설정
  - [Python / Virtual Environment / Jupyter notebook 사용 환경 설정](https://github.com/jbbang-dev/Study/blob/master/BigQuery/BigQuery_Team_Study/BigQuery%20With%20Development/exercise/Jupyter%20notebook%20%EC%82%AC%EC%9A%A9%20%ED%99%98%EA%B2%BD%20%EC%84%A4%EC%A0%95.md)
  - Python notebook 아래부터 실습 진행(With Jupyterlab)
<br></br>


# 3. 다양한 도구로 BigQuery 개발 활용
## 3.1. jupyter magic(With Jupyterlab)
  1. jupyter-lab에서 jupyter magic 키워드 사용 개발(%, %%)
     - [Built-in magic commands — IPython 7.30.1 documentation](https://ipython.readthedocs.io/en/stable/interactive/magics.html)
  2. %load_ext : 클라이언트 라이브러리에서 bigquery magic 라이브러리 호출
  3. %%bigquery : 쿼리 조회 및 결과를 Pandas Dataframe으로 반환
  4. [Visualizing BigQuery data in a Jupyter notebook | Google Cloud](https://cloud.google.com/bigquery/docs/visualize-jupyter)

## 3.2. R(With R Studio)
  1. R 설치
     - [The Comprehensive R Archive Network](https://cran.rstudio.com/)
     - [Download the RStudio IDE](https://www.rstudio.com/products/rstudio/download/)
  2. bigrquery 패키지 설치 및 라이브러리 적용
     - https://bigrquery.r-dbi.org/reference/index.html
  3. Service Account Key 설정
     - https://bigrquery.r-dbi.org/reference/bq_auth.html
  4. bigquery project 설정 및 데이터 활용

## 3.3. Dataflow(with VS Code)
  1. [Apache Beam](https://beam.apache.org/) : An advanced unified programming model
  2. Dataflow(Fully-Managed)에 기반이 되는 apache beam SDK를 이용
     - apache-beam[gcp] 패키지 설치
     - https://beam.apache.org/get-started/quickstart-py/
  3. Runner : 분산처리 백엔드 엔진 : Dataflow 활용
  ```python
  RUNNER = 'DataflowRunner'
  ```
  4. beam pipeline : 데이터 추출 -> 원하는 데이터 형태로 변형 -> 결과 데이터 다시 입력
  
  |제목|내용|
  |:---:|:---|
  |source|SELECT chapter, title FROM pipelining_sample.db_dataflow_test|
  |destination|SELECT chapter, title FROM bq_lib_ch05_jsyoo.temp_table|
  
  참고 : [GCP - Apache Beam 알아보기](https://jaemunbro.medium.com/gcp-dataflow-apache-beam-%EC%95%8C%EC%95%84%EB%B3%B4%EA%B8%B0-a4f5f09b98d1)
> ※ 기타 : python 3.8 버전에서 apache-beam 라이브러리 설치 원활

## 3.4. jdbc / odbc driver
  1. Java 혹은 .Net에서 사용하는 Database Connection API(Connection String)
  2. [ODBC and JDBC drivers for BigQuery | Google Cloud](https://cloud.google.com/bigquery/docs/reference/odbc-jdbc-drivers)
     - 여러 연결 방법 중 odbc data source administrator 에서 설정 후 적용하는 방법(dsn connection string 방법 등 존재)
     - ODBC 설치(32bit)
     - ODBC Data Source Administrator 에서 인증 키 설정
     - 사용할 프로그램에서 설정

## 3.5. google apps script
  1. bigquery 데이터를 workspace에 연동하여 개발 수행
     - [Script Google](https://script.google.com/)
     - bigquery project 설정
     - bigquery 서비스 포함
     - [BigQuery Service | Apps Script | Google Developers](https://developers.google.com/apps-script/advanced/bigquery)

## 3.6. bq command line
  1. Google Cloud SDK(Software Development Kit)에서 제공하는 도구이며, CLI(Command Line Interface)에서 빅쿼리 작업 수행 가능
  2. SDK는 Google Cloud VM(Compute Engine)과 Cluster에 기본 설치되어 있고, on-premises에서는 다운받아 설치 후 수행 가능
  3. BigQuery 콘솔 UI에서 수행할 수 있는 모든 작업들 수행 가능(당연히..)
  4. [Using the bq command-line tool | BigQuery | Google Cloud](https://cloud.google.com/bigquery/docs/bq-command-line-tool)
  5. [bq command-line tool reference | BigQuery | Google Cloud](https://cloud.google.com/bigquery/docs/reference/bq-cli-reference)

# 4. 기타
> ***※ key.json 파일은 github 등을 사용할 때 public으로 올려놓게 되면 매우 위험하므로 주의 필요!***   
   
   
# Reference
- [ 구글 빅쿼리 완벽 가이드: 발리아파 락쉬마난, 조던 티가니 저/변성윤, 장현희 역, 책만, 2020 ]