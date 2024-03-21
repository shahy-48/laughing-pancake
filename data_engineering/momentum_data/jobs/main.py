import os
from confluent_kafka import SerializingProducer
import simplejson as json

london_coordinates = {"latitude": 51.5074,"longitude": -0.1278}
birmingham_coordinates = {"latitude": 52.4862,"longitude": -1.8904}

# calculate the movement increments
latitude_increment = (birmingham_coordinates['latitude'] - london_coordinates['latitude'])/100
longitude_increment = (birmingham_coordinates['longitude'] - london_coordinates['longitude'])/100