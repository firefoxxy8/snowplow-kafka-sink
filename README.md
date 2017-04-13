# snowplow-kafka-sink

Monitor kafka topic. Publish to snowplow collector.

# Sample Docker RUN

```
$ docker run -d --name=spks --hostname=spks -e APP_ID=myapp -e OPERATOR_ID=com.rbox24 -e SP_COLLECTOR_URI=example.com -e SP_COLLECTOR_PROTOCOL=https -e SP_COLLECTOR_PORT=443 -e SP_COLLECTOR_METHOD=post -e KAFKA_BOOTSTRAP_SRVS=localhost:9092 -e KAFKA_GROUP_ID=myappgrid -e KAFKA_SOURCE_TOPIC=myapptopic goliasz/snowplow-kafka-sink
```

# License
Apache License, Version 2.0
