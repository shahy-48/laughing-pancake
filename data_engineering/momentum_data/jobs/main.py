from confluent_kafka import SerializingProducer
from datetime import datetime, timedelta
import os
import random
import simplejson as json
import sys
import uuid

london_coordinates = {"latitude": 51.5074,"longitude": -0.1278}
birmingham_coordinates = {"latitude": 52.4862,"longitude": -1.8904}

# calculate the movement increments
latitude_increment = (birmingham_coordinates['latitude'] - london_coordinates['latitude'])/100
longitude_increment = (birmingham_coordinates['longitude'] - london_coordinates['longitude'])/100

# Environment variables for configuration
kafka_bootstrap_server = os.getenv('kafka_bootstrap_servers', 'localhost:29092')
vehicle_topic = os.getenv('vehicle_topic','vehicle_data')
gps_topic = os.getenv('gps_topic','gps_data')
traffic_topic = os.getenv('traffic_topic','traffic_data')
weather_topic = os.getenv('weather_topic','weather_data')
emergency_topic = os.getenv('emergency_topic','emergency_data')


start_time = datetime.now()
start_location = london_coordinates.copy()

def get_next_time():
    global start_time
    start_time += timedelta(seconds=random.randint(30,60)) # update frequency
    return start_time

def simulate_vehicle_movement():
    global start_location

    # move towrads destination
    start_location['latitude'] += latitude_increment
    start_location['longitude'] += longitude_increment

    # add some randomeness to the movement
    start_location['latitude'] += random.uniform(-0.0005, 0.0005)
    start_location['latitude'] += random.uniform(-0.0005, 0.0005)

    return start_location

def generate_vehicle_data(device_id):
    new_location = simulate_vehicle_movement()
    return {
        'id': uuid.uuid4(),
        'device_id': device_id,
        'timestamp': get_next_time().isoformat(),
        'location': (new_location['latitude'], new_location['longitude']),
        'speed': random.uniform(5,15),
        'direction': 'North-East',
        'vehicle make': 'Ninebot',
        'vehicle model':'C500',
        'model year': 2020,
        'battery type': 'Lithium Ion' 
    }

def generate_gps_data(device_id, timestamp, vehicle_type = 'Escooter'):
    return {
        'id': uuid.uuid4(),
        'device_id': device_id,
        'timestamp': timestamp,
        'speed': random.uniform(5,15),
        'direction': 'North-East',
        'vehicle type': vehicle_type
    }

def generate_traffic_camera_data(device_id, timestamp, camera_id, location):
    return {
        'id': uuid.uuid4(),
        'device_id': device_id,
        'camera id':camera_id,
        'timestamp': timestamp,
        'location': location,
        'snapshot': 'Base64EncodedString'
    }

def generate_weather_data(device_id, timestamp, location):
    return {
        'id': uuid.uuid4(),
        'device_id': device_id,
        'timestamp': timestamp,
        'location': location,
        'temperature': random.uniform(0,25),
        'weather condition': random.choice(['Sunny','Rain','Cloudy','Snow']),
        'precipitation': random.uniform(0,25),
        'wind speed': random.uniform(0,15),
        'humidity': random.randint(0,100),
        'air quality index': random.uniform(0,100)
    }

def generate_emergency_incident_data(location, timestamp, device_id):
    return {
        'id': uuid.uuid4(),
        'device_id': device_id,
        'timestamp': timestamp,
        'location': location,
        'incident id': uuid.uuid4(),
        'type': random.choice(['Accident','Fire','Medical','Police','None']),
        'status': random.choice(['Active','Resolved']),
        'description': 'description'
    }

def json_serializer(object):
    if isinstance(object, uuid.UUID):
        return str(object)
    raise TypeError(f'object of type {object.__class__.__name__} is not JSON serializable')

def delivery_report(err,msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def produce_data_to_kafka(producer, topic, data):
    producer.produce(
        topic,
        key = str(data['id']),
        value = json.dumps(data, default=json_serializer).encode('utf-8'), # default value in case of no uuid to avoid breaking system data producer
        on_delivery = delivery_report
    )
    producer.flush()

def simulate_journey(producer, device_id):
    while True:
        vehicle_data = generate_vehicle_data(device_id)
        gps_data = generate_gps_data(device_id, vehicle_data['timestamp'])
        traffic_camera_data = generate_traffic_camera_data(device_id, vehicle_data['timestamp'], 'cam123', vehicle_data['location'])
        weather_data = generate_weather_data(device_id, vehicle_data['timestamp'], vehicle_data['location'])
        emergency_incident_data = generate_emergency_incident_data(vehicle_data['location'], vehicle_data['timestamp'], device_id)

        if vehicle_data['location'][0] >= birmingham_coordinates['latitude'] and vehicle_data['location'][0] >= birmingham_coordinates['longitude']:
            break

        produce_data_to_kafka(producer, vehicle_topic, vehicle_data)
        produce_data_to_kafka(producer, gps_topic, gps_data)
        produce_data_to_kafka(producer, traffic_topic, traffic_camera_data)
        produce_data_to_kafka(producer, weather_topic, weather_data)
        produce_data_to_kafka(producer, emergency_topic, emergency_incident_data)


if __name__ == '__main__':
    producer_config = {
        'bootstrap.servers': kafka_bootstrap_server,
        'error_cb': lambda err: print(f'kafka error: {err}')
    }
    producer = SerializingProducer(producer_config)

    try:
        simulate_journey(producer, 'Vehicle-Escooter-123')
    except KeyboardInterrupt:
        print('Simulation ended by the user')
    except Exception as e:
        print(f'Unexpected error occured:{e}')