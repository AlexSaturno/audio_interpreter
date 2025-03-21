FROM python:3.11

WORKDIR /work
RUN apt update && apt install -y python3-pip ffmpeg libsm6 libxext6 libegl1 python3-opencv libgl1-mesa-glx
COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8501

CMD ["/usr/local/bin/streamlit", "run", "/work/main.py"]
