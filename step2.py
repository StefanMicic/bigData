import os

# from loguru import logger as log
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

from processing.vocabulary_creator import VocabCreator


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

    vocabCreator = VocabCreator(HDFS_NAMENODE + "/home/output.csv", spark)
    vocabCreator()
    # log.info("Vocab created")


if __name__ == "__main__":
    main()
