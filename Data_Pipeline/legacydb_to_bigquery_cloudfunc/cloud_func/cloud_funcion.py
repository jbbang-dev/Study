# 2021.12.03
# GCP pubsub topic에 신규 데이터 전달 시 subscription triggering으로 실행되는 cloud function
import base64
import io, os, json
from google.cloud import bigquery

def bigquery_push(event, context):
    # 전달 message decoding 
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')

    # json object로 변환
    json_object = json.loads(pubsub_message)

    # BigQuery client object 설정
    client = bigquery.Client()

    # destination 지정
    table_id = "looker-data-grfit.pipelining_sample.pipelining_data"
    location = "asia-northeast3"
    
    # bigquery 업로드 작업 설정
    job_config = bigquery.LoadJobConfig(
         schema=[
              bigquery.SchemaField("cateNm", "STRING"),
              bigquery.SchemaField("cateCd", "STRING"),
         ],
         source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )

    # 전송 작업 호출
    load_job = client.load_table_from_json(
         json_rows=json_object,
         destination=table_id,
         location=location,
         job_config=job_config,
    ) 
    
    # 전송작업 및 결과 대기
    load_job.result()  

    # 작업결과 확인
    destination_table = client.get_table(table_id)
    print("Loaded {} rows.".format(destination_table.num_rows))