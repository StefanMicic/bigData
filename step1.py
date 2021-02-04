import os

# from loguru import logger as log
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

from processing.data_joining import Reader


def quiet_logs(sc):
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org").setLevel(logger.Level.ERROR)
    logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)


def main():
    HDFS_NAMENODE = os.environ["CORE_CONF_fs_defaultFS"]

    conf = (
        SparkConf().setAppName("Step 1").setMaster("spark://spark-master:7077")
    )
    sc = SparkContext(conf=conf)
    spark = SparkSession(sc)

    quiet_logs(spark)
    reader = Reader(
        HDFS_NAMENODE + "/home/jsons",
        HDFS_NAMENODE + "/home/train.csv",
        HDFS_NAMENODE + "/home/en",
        spark,
    )
    data_json, data_csv, data_text = reader()
    # log.info("Data reading finished")
    data = data_csv.union(data_json)
    data = data.union(data_text)
    try:
        data.repartition(1).write.format("com.databricks.spark.csv").save(
            HDFS_NAMENODE + "/home/output.csv"
        )
    except:  # noqa E722
        pass
    #     log.info("Output already created!")
    # log.info("Data saved")


if __name__ == "__main__":
    main()
