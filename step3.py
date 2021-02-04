import os

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

from processing.lr_model_train import ModelTrain


def quiet_logs(sc):
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org").setLevel(logger.Level.ERROR)
    logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)


def main():
    HDFS_NAMENODE = os.environ["CORE_CONF_fs_defaultFS"]

    conf = (
        SparkConf()
        .setAppName("example join")
        .setMaster("spark://spark-master:7077")
    )
    sc = SparkContext(conf=conf)
    spark = SparkSession(sc)

    quiet_logs(spark)

    model = ModelTrain(spark, HDFS_NAMENODE)
    model()


if __name__ == "__main__":
    main()
