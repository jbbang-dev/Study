# 패키지 설치
# install.packages("bigrquery", dependencies=TRUE)

# 라이브러리 불러오기
library(bigrquery)
library(grid)
library(gridExtra)

bq_auth(path = "looker-data-grfit-6cd8aea2ca15.json")

# bigquery 데이터 조회
project <- 'looker-data-grfit'
sql <- "SELECT 
          START_STATION_NAME,
          AVG(DURATION) AS DURATION,
          COUNT(DURATION) AS NUM_TRIPS
        FROM `bigquery-public-data.london_bicycles.cycle_hire`
        GROUP BY START_STATION_NAME
        ORDER BY NUM_TRIPS DESC
        LIMIT 10
        "
# 쿼리 수행 및 data frame으로 데이터 반환
result <- bq_project_query(project,  sql)
df <- bq_table_download(result, n_max=100)
# 조회 내역 확인
grid.table(df)
plot.ts(df$NUM_TRIPS)
