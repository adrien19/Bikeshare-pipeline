import datetime

from airflow import DAG
from airflow.models import Variable

from airflow.operators.udacity_plugin import (
    FactsCalculatorOperator,
    HasRowsOperator,
    S3ToRedshiftOperator
)

dag_config = Variable.get("bikeshare_configs", deserialize_json=True)
s3_bucket = dag_config["s3_bucket"]
s3_key = dag_config["s3_key"]

#
# Create a DAG which performs the following functions:
#
#       1. Loads Trip data from S3 to RedShift
#       2. Performs a data quality check on the Trips table in RedShift
#       3. Uses the FactsCalculatorOperator to create a Facts table in Redshift
#           a. **NOTE**: to complete this step you must complete the FactsCalcuatorOperator
#              skeleton defined in plugins/operators/facts_calculator.py
#
dag = DAG("bikeshare.bikeshareDag", start_date=datetime.datetime.utcnow())


#
# Load trips data from S3 to RedShift. Use the s3_key
#       "data-pipelines/divvy/unpartitioned/divvy_trips_2018.csv"
#       and the s3_bucket "udacity-dend"
#
copy_trips_task = S3ToRedshiftOperator(
    task_id = 'copy_trips_from_s3_to_redshift',
    dag = dag,
    table = 'trips',
    redshift_conn_id = "redshift",
    aws_credentials_id = "aws_credentials",
    s3_bucket = s3_bucket,
    s3_key = s3_key
)

#
# Perform a data quality check on the Trips table
#
check_trips = HasRowsOperator(
    task_id = "check_trips_table",
    dag = dag,
    redshift_conn_id = "redshift",
    table = 'trips',
)

#
# Use the FactsCalculatorOperator to create a Facts table in RedShift. The fact column should
#       be `tripduration` and the groupby_column should be `bikeid`
#
calculate_facts = FactsCalculatorOperator(
    task_id = "calculate_facts_from_trips_table",
    dag = dag,
    redshift_conn_id="redshift",
    origin_table="trips",
    destination_table="facts",
    fact_column="tripduration",
    groupby_column="bikeid",
)

#
# Define task ordering for the DAG tasks you defined
#
copy_trips_task >> check_trips
check_trips >> calculate_facts
