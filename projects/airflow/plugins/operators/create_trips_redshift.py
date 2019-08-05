from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class CreateTripsRedshiftOperator(BaseOperator):
    create_trips_sql = """
    CREATE TABLE IF NOT EXISTS trips (
    trip_id INTEGER NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    bikeid INTEGER NOT NULL,
    tripduration DECIMAL(16,2) NOT NULL,
    from_station_id INTEGER NOT NULL,
    from_station_name VARCHAR(100) NOT NULL,
    to_station_id INTEGER NOT NULL,
    to_station_name VARCHAR(100) NOT NULL,
    usertype VARCHAR(20),
    gender VARCHAR(6),
    birthyear INTEGER,
    PRIMARY KEY(trip_id))
    DISTSTYLE ALL;
    """


    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 *args, **kwargs):

        super(CreateTripsRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Creating trips destination table in Redshift")
        redshift.run(create_trips_sql)
