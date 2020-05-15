# Twitter-Realtime-Analytics
Twitter Streaming obtaining top hashtag and words based on geo-location.
Basically the process it Tweets are ingested to Kafka, then Spark processes and streams as proper table


![Streaming Top Hashtags](https://github.com/arifcanaksoy/Twitter-Realtime-Analytics/blob/master/outputs_spark_query_1.png "Top Hashtags and counts in En")


### Before starting
Install required packages:
  - pip install kafka-python
  - pip install kafka-utils
  - pip install pyspark
 
[Download](https://kafka.apache.org/downloads.html) Kafka and un-tar it. (The version which i am using is 2.5.0)
```sh
$ tar -xzf kafka_2.12-2.5.0.tgz
```

[Download](https://spark.apache.org/downloads.html) Spark and un-tar it. (The version which i am using is 2.4.5)
```sh
$ tar -xzf spark-2.4.5-bin-hadoop2.7.tgz
```

Set Spark Home
```sh
$ export SPARK_HOME="/Users/YOURUSERNAME/Development/Tools/spark-2.4.5-bin-hadoop2.7"
$ export PATH="$SPARK_HOME/bin:$PATH"
```

To test pyspark, run in terminal
```sh
$ pyspark
```
you should see
```sh
   ____              __
  / __/__  ___ _____/ /__
 _\ \/ _ \/ _ `/ __/  '_/
/__ / .__/\_,_/_/ /_/\_\   version 2.4.5
   /_/
```
[Download](https://mvnrepository.com/artifact/org.apache.spark/spark-streaming-kafka-0-8-assembly_2.11) Spark Streaming Kafka Assembly jar (The version which i am using is 2.4.5). We will use it it to stream data from Kafka.
**Important:** The version must match with Spark


### Start Zookeper
switch to folder where you un-tar kafka_2.12-2.5.0 
```sh
$ bin/zookeeper-server-start.sh config/zookeeper.properties
```

### Start Kafka Server
```sh
$ bin/kafka-server-start.bat config/server.properties
```

### Create Topic "topic_twitter"
```sh
$ .bin/kafka-topics.sh --create --zookeeper localhost --replication-factor 1 --partitions 1 --topic topic_twitter
```
### (Optional) To Test Creating Messages in your Topic
```sh
$ bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic topic_twitter
```
### (Optional) To Monitor Incoming Messages via Kafka
```sh
$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic topic_twitter --from-beginning
```
![Monitor on Kafka](https://github.com/arifcanaksoy/Twitter-Realtime-Analytics/blob/master/outputs_from_kafkatopic_consumer.png "Tweets are read through defined kafka topic")


### Reading Tweets via twitter API
run twitter_app.py from this repo to produce messages
```sh
$ python3 twitter_app.py
```

### Streaming Data through Apache Spark
run streamer.py to stream data from Kafka to influxDB via Spark
```sh
$ spark-2.4.5-bin-hadoop2.7/bin/spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.4.5.jar /Users/YOURUSERNAME/git/Twitter-Realtime-Analytics/spark_streaming_twitter.py
```
