# Requirements
- This project must be run on a Ubuntu machine (eg. Ubuntu 20.04 LTS)
- python, pip and npm
# Installation
## For the web
- `pip install django` in /server
- run `npm install` in /client
## For Kafka
- install Java by `sudo apt install openjdk-8-jdk -y`
- `wget https://downloads.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz` in the project directory
- `tar xvf kafka_2.13-3.7.0.tgz`
- `sudo mv kafka_2.13-3.7.0 /opt/kafka`
- `echo 'export KAFKA_HOME=/opt/kafka' >> ~/.bashrc`
- `echo 'export PATH=$PATH:$KAFKA_HOME/bin' >> ~/.bashrc`
- `source ~/.bashrc` to apply the change
- `kafka-topics.sh --version` to verify the installation
# Start demo
- start Django by `python manage.py runserver` in /server
- start React front-end by `npm run start` in /client
- start zookeeper `zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties
` start kafka server `kafka-server-start.sh /opt/kafka/config/server.properties`
- create a topic named prediction `kafka-topics.sh --create --topic prediction --bootstrap-server localhost:9092`
- `python resetMongoDB.py`
- navigate to /server/server/utils and `python consumer.py`, submit the video url in front-end then in another terminal run `python producer.py`
