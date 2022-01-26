import os
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