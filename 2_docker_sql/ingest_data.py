import argparse
import os
import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user=params.user
    password=params.password
    host=params.host
    port=params.port
    db=params.db
    table_name=params.table_name
    url=params.url
    
    data_file_name = 'output.parquet' # this might be qarquet file
    
    os.system(f"wget {url} -O {data_file_name}")
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df = pd.read_parquet(data_file_name)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    print(pd.io.sql.get_schema(df, name = 'yellow_taxi_data', con=engine))

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    # get_ipython().run_line_magic('time', "df.to_sql(name={table_name}, con={engine}, if_exists='append')")
    df.to_sql(name=table_name, con=engine, if_exists='append')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest data into PostgreSQL')
    # use 
    # password
    # host
    # port
    # database name
    # table name
    # url of the data

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the result to')
    parser.add_argument('--url', help='url of the data')

    args = parser.parse_args()
    main(args)


