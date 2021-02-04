# from loguru import logger as log
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import CountVectorizer
from pyspark.sql.functions import lower, regexp_replace, split
from pyspark.sql.types import IntegerType

# apk update
# apk add make automake gcc g++ subversion python3-dev
# pip3 install numpy

# hdfs dfs -mkdir /home
# hdfs dfs -put /home/ /home/

#     docker container prune
#     docker volume prune


class ModelTrain:
    def __init__(self, spark, HDFS_NAMENODE):
        self.spark = spark
        self.hdfs = HDFS_NAMENODE

    def __call__(self):
        df = self.spark.read.csv(self.hdfs + "/home/output.csv")
        df = df.withColumnRenamed("_c1", "overall")
        df = df.withColumnRenamed("_c0", "reviewText")
        df = df.select(
            "reviewText",
            "overall",
            (
                lower(regexp_replace("reviewText", "[^a-zA-Z\\s]", "")).alias(
                    "text"
                )
            ),
        )
        df = df.drop("reviewText")

        df = df.withColumnRenamed("overall", "label")
        df = df.withColumn("feature", split("text", " "))
        df = df.drop("text")

        df = df.na.drop()

        cv = CountVectorizer(
            inputCol="feature", outputCol="features", vocabSize=150, minDF=50.0
        )

        model = cv.fit(df)

        result = model.transform(df)

        result = result.withColumn("label", df["label"].cast(IntegerType()))
        lr = LogisticRegression(maxIter=2, regParam=0.01)

        # log.info("Training started.")

        model1 = lr.fit(result)
        # log.info("Model successfully trained.")
        model1.write().overwrite().save(self.hdfs + "/user/test/titanic-model")
        return model1
