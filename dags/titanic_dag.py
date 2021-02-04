import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    "owner": "test",
    "depends_on_past": False,
    "start_date": datetime(2020, 10, 10),
    "email": ["test@test.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    dag_id="titanic_dag",
    default_args=default_args,
    catchup=False,
    schedule_interval="@once",
)

HDFS_NAMENODE = os.environ["CORE_CONF_fs_defaultFS"]
pyspark_app_home = "/home"


step1 = BashOperator(
    task_id="train_model",
    bash_command="spark-submit --master spark://spark-master:7077 "
    + f"{pyspark_app_home}/step1.py",
    dag=dag,
)

step2 = BashOperator(
    task_id="test_model",
    bash_command="spark-submit --master spark://spark-master:7077 "
    + f"{pyspark_app_home}/step2.py",
    dag=dag,
)

step3 = BashOperator(
    task_id="apply_model",
    bash_command="spark-submit --master spark://spark-master:7077 "
    + f"{pyspark_app_home}/step3.py",
    dag=dag,
)

step1 >> step2 >> step3
