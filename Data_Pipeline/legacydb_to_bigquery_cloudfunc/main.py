# 2021.12.03
# 내부 Server hosting 된 DB(MariDB)에서 데이터를 추출하여 pubsub으로 메세지 전달
import pymysql, os, pandas as pd
from google.cloud import pubsub_v1

# 프로젝트/topic 선언
project_id = "looker-data-grfit"
topic_id = "datapipelining-sample-topic"
# 인증정보 설정
credential_path = "..\..\..\GCP Json Key\looker-data-grfit-536efecf194c.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# json topic 설정 가져오기
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# 내부 db연결 및 query 전달
conn = pymysql.connect(host='localhost', user='looker', password='looker', db='gurufit_to_looker', charset='utf8')
curs = conn.cursor()
sql = "select cateNm, cateCd from es_categoryBrand WHERE cateCd in ('030', '031')"
df = pd.read_sql(sql, conn)

# json 포멧으로 변환
data = df.to_json(orient='records')
message_bytes = data.encode(encoding="utf-8")

try:
    # 최종 메세지 전달
    publish_future = publisher.publish(topic_path, data=message_bytes)
    # 성공적으로 전달되었는지 확인
    publish_future.result() 
except Exception as e:
    print("error")
    print(e)
