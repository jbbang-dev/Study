# ch.05 빅쿼리를 활용한 개발

윈도우 CMD(Command Line) 기준 설명 자료입니다.

### 1. 파이썬/pip 설치 확인

```powershell
C:￦> python --version
C:￦> pip --version
```

### 2. jupyter notebook 설치
#### [![텍스트](https://jupyter.org/assets/logos/rectanglelogo-greytext-orangebody-greymoons.svg)](https://jupyter.org/install)

```powershell 
C:￦> pip install jupyterlab 
```

### 3. 개발 폴더 설정 및 이동

개인 실습 폴더 위치는 편한대로..

예) d:\python_dev\ch05

```powershell
C:￦> d:
D:￦> cd d:\python_dev\ch05
```

### 4. 개발 폴더 내 python virtual environment 설정

```powershell
D:￦python_dev￦ch05> python -m venv venv
```

### 5. 가상 환경 활성화 실행

```powershell
D:￦python_dev￦ch05> venv\Scripts\activate.bat
```

실행하면 화면 Clear 이후 아래와 같이 (venv)가 앞에 붙음

```powershell
(venv) D:￦python_dev￦ch05>
```

### 6. 의존성 패키지 라이브러리 미리 설치(google-cloud-bigquery, pandas, pyarrow)

```powershell
(venv)￦> pip install google-cloud-bigquery
(venv)￦> pip install pandas
(venv)￦> pip install pyarrow
```

### 7. jupyter 의존성 및 가상 kernel 추가

```powershell
(venv)￦> pip install ipykernel
(venv)￦> python -m ipykernel install --user --name venv --display-name "bq-python-kernel"
```

### 8. jupyter 잘 설치되었는지 실행

```powershell
(venv)￦> jupyter-lab
```

### 9. 종료할때는 Shut Down으로 종료

 - CMD 창에 프롬프트로 나오지 않는다면 [ctrl+c]

### 10. 가상환경 빠져나오기

```powershell
(venv)￦> venv\Scripts\deactivate.bat
```

아래와 같이 (venv) 없어짐

```powershell
￦>
```

### 11. GCP Service Account 및 key pair(json) 생성

부터는 같이 실습~
