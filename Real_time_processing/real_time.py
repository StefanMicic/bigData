r"""
 Run the example
    `
    $SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.4 $SPARK_HOME/real_time.py zoo1:2181 subreddit-politics subreddit-worldnews
    `
"""  # noqa W291
from __future__ import print_function

import sys
from random import random

from pyspark import SparkContext
from pyspark.sql import Row, SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


def getSparkSessionInstance(sparkConf):
    if "sparkSessionSingletonInstance" not in globals():
        globals()[
            "sparkSessionSingletonInstance"
        ] = SparkSession.builder.config(conf=sparkConf).getOrCreate()
    return globals()["sparkSessionSingletonInstance"]


def quiet_logs(sc):
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getRootLogger().setLevel(logger.Level.ERROR)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: kafka_wordcount.py <zk> <topic1> <topic2>", file=sys.stderr
        )
        sys.exit(-1)

    sc = SparkContext(appName="SparkStreamingKafkaWordCount")
    quiet_logs(sc)
    ssc = StreamingContext(sc, 3)

    ssc.checkpoint("stateful_checkpoint_direcory")

    zooKeeper, topic1, topic2 = sys.argv[1:]
    kvs = KafkaUtils.createStream(
        ssc, zooKeeper, "spark-streaming-consumer", {topic1: 1, topic2: 1}
    )

    lines = kvs.map(lambda x: x[1])

    def updateFunc(new_values, last_sum):
        if last_sum is None:
            last_sum = 0
        return sum(new_values, last_sum)

    counts = (
        lines.map(lambda line: ("len_" + str(len(line.split())), 1))
        .reduceByKey(lambda a, b: a + b)
        .updateStateByKey(updateFunc)
    )

    counts.pprint()

    sent_len = lines.map(lambda line: (line, len(line.split()), random()))

    sent_len.pprint()

    def process(time, rdd):
        print("========= %s USAO =========" % str(time))

        try:

            # Get the singleton instance of SparkSession
            spark = getSparkSessionInstance(rdd.context.getConf())

            # Convert RDD[String] to RDD[Row] to DataFrame
            rowRdd = rdd.map(lambda w: Row(word=w[0], sentiment=w[2]))
            wordsDataFrame = spark.createDataFrame(rowRdd)

            # Creates a temporary view using the DataFrame.
            wordsDataFrame.createOrReplaceTempView("words")

            # Do word count on table using SQL and print it
            wordCountsDataFrame = spark.sql(
                "select word, sentiment from words where sentiment >= 0.5 \
                order by sentiment asc"
            )
            wordCountsDataFrame.show()
        except:
            pass

    sent_len.foreachRDD(process)
    ssc.start()
    ssc.awaitTermination()
