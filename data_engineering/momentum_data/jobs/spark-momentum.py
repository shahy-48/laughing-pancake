from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType, IntegerType
from pyspark.sql.functions import from_json, col
from pyspark.sql import DataFrame
from config import configuration

def main():
    spark = SparkSession.builder.appName('momentum_stream')\
    .config("spark.jars.packages",
            "org.apache.commons:commons-pool2:2.8.0,"
            "org.apache.kafka:kafka-clients:2.5.0,"
            "org.apache.spark:spark-streaming-kafka-0-10-assembly_2.12:3.0.0-preview2,"
            "org.apache.spark:spark-token-provider-kafka-0-10_2.13:3.5.0,"
            "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0,"
            "org.apache.hadoop:hadoop-aws:3.3.1,"
            "com.amazonaws:aws-java-sdk:1.11.469")\
    .config("spark.hadoop.fs.s3a.impl","org.apache.hadoop.fs.s3a.S3AFileSystem")\
    .config("spark.hadoop.fs.s3a.access.key",configuration['AWS_ACCESS_KEY'])\
    .config("spark.hadoop.fs.s3a.secret.key",configuration['AWS_SECRET_KEY'])\
    .config("spark.hadoop.fs.s3a.aws.credentials.provider",'org.apache.hadoop.fs.s3a.impl.SimpleAWSCredentialsProvider')\
    .getOrCreate()

# adjust the log level to minimize the console output on executors
    spark.sparkContext.setLogLevel('WARN')

    # vehicle schema
    vehicle_schema = StructType([
        StructField('id', StringType(), True),
        StructField('device_id', StringType(), True),
        StructField('timestamp', TimestampType(), True),
        StructField('location', StringType(), True),
        StructField('speed', DoubleType(), True),
        StructField('direction', StringType(), True),
        StructField('vehicle make', StringType(), True),
        StructField('vehicle model', StringType(), True),
        StructField('model year', IntegerType(), True),
        StructField('battery type', StringType(), True)
    ])

    # gps schema
    gps_schema = StructType([
        StructField('id', StringType(), True),
        StructField('device_id', StringType(), True),
        StructField('timestamp', TimestampType(), True),
        StructField('speed', DoubleType(), True),
        StructField('direction', StringType(), True),
        StructField('vehicle type', StringType(), True)
    ])

    # traffic schema
    traffic_schema = StructType([
        StructField('id', StringType(), True),
        StructField('device_id', StringType(), True),
        StructField('camera_id', StringType(), True),
        StructField('timestamp', TimestampType(), True),
        StructField('location', StringType(), True),
        StructField('snapshot', DoubleType(), True)
    ])

    # weather scehma
    weather_schema = StructType([
        StructField('id', StringType(), True),
        StructField('device_id', StringType(), True),
        StructField('timestamp', TimestampType(), True),
        StructField('location', StringType(), True),
        StructField('temperature', DoubleType(), True),
        StructField('weather condition', StringType(), True),
        StructField('precipitation', DoubleType(), True),
        StructField('wind speed', DoubleType(), True),
        StructField('humidity', IntegerType(), True),
        StructField('air quality index', DoubleType(), True)
    ])

    # emergency schema
    emergency_schema = StructType([
        StructField('id', StringType(), True),
        StructField('device_id', StringType(), True),
        StructField('timestamp', TimestampType(), True),
        StructField('location', StringType(), True),
        StructField('incident_id', StringType(), True),
        StructField('type', StringType(), True),
        StructField('status', StringType(), True),
        StructField('description', StringType(), True)
    ])

    def read_kafka_topic(topic, schema):
        return (spark.readStream
                .format('kafka')
                .option('kafka.bootstrap.servers', 'kafka:9092')
                .option('subscribe', topic)
                .option('startingOffsets','earliest')
                .load()
                .selectExpr('CAST(value AS STRING')
                .select(from_json(col('value'), schema)).alias('data')
                .select('data.*')
                .withWatermark('timestamp','2 minutes')
                )
    
    def stream_writer(input:DataFrame, checkpoint_folder, output):
        return(
            input.writeStream
            .format('parquet')
            .option('checkpoint_location', checkpoint_folder)
            .option('path', output)
            .outputMode('append')
            .start()
        )

    vehicle_df = read_kafka_topic('vehicle_data', vehicle_schema).alias('vehicle')
    gps_df = read_kafka_topic('gps_data', gps_schema).alias('gps')
    traffic_df = read_kafka_topic('traffic_data', traffic_schema).alias('traffic')
    weather_df = read_kafka_topic('weather_data', weather_schema).alias('weather')
    emergency_df = read_kafka_topic('emergency_data', emergency_schema).alias('emergency')

    # write vehicle data into S3
    query_1 =stream_writer(vehicle_df,
                  's3a://streaming-momentum-bucket/checkpoints/vehicle_data', 
                  's3a://streaming-momentum-bucket/data/vehicle_data')
    
    # write gps data into S3
    query_2 =stream_writer(gps_df,
                  's3a://streaming-momentum-bucket/checkpoints/gps_data', 
                  's3a://streaming-momentum-bucket/data/gps_data')
    
    # write traffic data into S3
    query_3 =stream_writer(traffic_df,
                  's3a://streaming-momentum-bucket/checkpoints/traffic_data', 
                  's3a://streaming-momentum-bucket/data/traffic_data')
    
    # write weather data into S3
    query_4 =stream_writer(weather_df,
                  's3a://streaming-momentum-bucket/checkpoints/weather_data', 
                  's3a://streaming-momentum-bucket/data/weather_data')
    
    # write emergency data into S3
    query_5 =stream_writer(emergency_df,
                  's3a://streaming-momentum-bucket/checkpoints/emergency_data', 
                  's3a://streaming-momentum-bucket/data/emergency_data')
    
    query_5.awaitTermination()


if __name__ == "__main__":
    main()