# 2021.12.23 기준 apache-beam 라이브러리 정상 설치를 위하여 python version 3.9 미만버전 사용 권장(테스트는 3.8버전)
# [py -3.8 -m venv venv] 로 가상환경 버전 설정
# pip install apache-beam[gcp]
# pip install scipy
import apache_beam as beam
import os
from apache_beam.options.pipeline_options import PipelineOptions

# project 전역 설정
PROJECT = "looker-data-grfit"
RUNNER = 'DataflowRunner'
JOB_NAME = 'jsyoo-job-name-4'
TEMP_LOCATION = 'gs://datapipeline-sample-bucket/temp'
REGION = 'asia-northeast3'

# service account json key pair 환경변수 설정
# json 파일 경로 작성
credential_path = "looker-data-grfit-6cd8aea2ca15.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# 빅쿼리의 row를 입력받아 원하는 형태로 조정하여 결과행을 보내는 함수
def compute_fit(row):
    from scipy import stats
    result = {}
    result['chapter'] = int(row['chapter']) + 2
    result['title'] = str(row['title']) + '!!!'
    return result

# beam 설정값 셋팅
opts = PipelineOptions(
    runner=RUNNER,
    project=PROJECT,
    job_name=JOB_NAME,
    temp_location=TEMP_LOCATION,
    region=REGION
    )

# 입력 쿼리 설정
query = """
    SELECT chapter, title
    FROM pipelining_sample.db_dataflow_test
"""

# beam 파이프라인 작업 설정
with beam.Pipeline(RUNNER, options=opts) as p:
    (p
    | 'QueryTable' >> beam.io.Read(beam.io.ReadFromBigQuery(query=query))
    | 'compute_fit' >> beam.Map(compute_fit)
    | 'write_bq' >> beam.io.WriteToBigQuery(
        'bq_lib_ch05_jsyoo.temp_table', 
        schema='chapter:INTEGER, title:STRING',
        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
    )
)