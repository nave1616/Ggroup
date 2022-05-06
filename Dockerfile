FROM ubuntu
RUN apt-get update
RUN apt-get install git\
                            python3-pyqt5\
                            python3\ 
                            python3-pip\
                            python3-dev -y 

WORKDIR /home/Ggroup/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./Ggrups.py" ]