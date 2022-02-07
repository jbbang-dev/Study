from google.cloud import translate_v2 as translate
import os, time, threading
from subprocess import Popen

_current_dir = "{0}{1}Translate_API\youtube_script_translate\\".format(os.getcwd(), "\\")
_in_txt_file = "{0}input.txt".format(_current_dir)
_out_txt_file = "{0}result.txt".format(_current_dir)

def readWrite():
    text = open(_in_txt_file, mode="r")
    text = text.read().split()
    client = translate.Client()
    result = client.translate(' '.join(text), target_language="ko")
    ko_text = str(result['translatedText']).replace('.', '.\n')
    print(ko_text) 
    f = open(_out_txt_file, "w")
    f.write(ko_text)
# service account json key pair 환경변수 설정
# json 파일 경로 작성
credential_path = "D:\Study\GCP Json Key\json key\looker-data-grfit-6cd8aea2ca15.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
t1 = threading.Thread(target=readWrite)
t1.start()
time.sleep(1)
p = Popen(['notepad.exe', _out_txt_file])
# p.terminate()
