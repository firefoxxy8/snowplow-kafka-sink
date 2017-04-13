
#!/usr/bin/python

# Copyright KOLIBERO under one or more contributor license agreements.  
# KOLIBERO licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#from flask import Flask, jsonify, request, Response, abort
#from functools import wraps

import json
import time
import requests
import os
from snowplow_tracker import Subject, Emitter, Tracker, SelfDescribingJson
import uuid
import argparse
from datetime import datetime
from kafka import KafkaConsumer, SimpleConsumer

def listen():
  print "attach"

  # Kafka
  consumer = KafkaConsumer(bootstrap_servers=os.environ["KAFKA_BOOTSTRAP_SRVS"], group_id=os.environ["KAFKA_GROUP_ID"])
  consumer.subscribe([os.environ["KAFKA_SOURCE_TOPIC"]])

  # Snowplow
  e = Emitter(os.environ["SP_COLLECTOR_URI"],protocol=os.environ["SP_COLLECTOR_PROTOCOL"],port=int(os.environ["SP_COLLECTOR_PORT"]),method=os.environ["SP_COLLECTOR_METHOD"])
  t = Tracker(emitters=e,namespace="cf",app_id=str(os.environ["APP_ID"]),encode_base64=True)

  for msg in consumer:
    #
    indata = json.loads(msg.value)

    s1 = Subject()
    s1.set_platform("app")
    s1.set_user_id("??")
    s1.set_lang("??")
    s1.set_ip_address("0.0.0.0")
    s1.set_useragent("??")

    t.set_subject(s1)

    t.track_self_describing_event(SelfDescribingJson("iglu:com.snowplowanalytics.snowplow/unstruct_event/jsonschema/1-0-0",{
      "data":{
        "data": indata
      },
      "schema": "iglu:"+os.environ["OPERATOR_ID"]+"/"+os.environ["APP_ID"]+"/jsonschema/1-0-0"
    }))

    t.flush()
  
if __name__ == '__main__':
  listen()
