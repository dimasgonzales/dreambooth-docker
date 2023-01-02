FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-devel

RUN apt-get update && apt-get install -y git

ENV SOURCE_PATH /opt/source
ENV LOCAL_PATH ./

COPY ${LOCAL_PATH}/main.py ${SOURCE_PATH}/main.py
COPY ${LOCAL_PATH}/requirements.txt ${SOURCE_PATH}/requirements.txt

RUN pip install -r ${SOURCE_PATH}/requirements.txt
WORKDIR ${SOURCE_PATH}
CMD ["python", "main.py", "2"]
