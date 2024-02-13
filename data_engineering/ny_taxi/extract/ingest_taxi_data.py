import argparse
import os
import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine


def main():
    # user = params.user
    # password = params.password
    # url = params.url
    # db = params.db
    # port = params.port
    # table_name = params.table_name

    user = "yash"
    password = "yash"
    db = "ny_taxi" 
    port = 5432
    table_name = "yellow_taxi_data"
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
    file_name = "yellow_tripdata_2023-01.parquet"
    
    os.system(f"wget {url}")

    parquet_file = pq.ParquetFile(file_name)
    df  = pd.read_parquet(file_name)
    engine = create_engine(f'postgresql://{user}:{password}@localhost:{port}/{db}')
    # Add headers to the postgres database to create the schema first
    df.head(0).to_sql(name = 'yellow_taxi_data', con=engine, if_exists='replace')
    for batch in parquet_file.iter_batches():
        print("Batch successfully loaded")
        batch_df = batch.to_pandas()
        batch_df.to_sql(name = table_name, con=engine, if_exists='append')

if __name__=="__main__":
    main()
