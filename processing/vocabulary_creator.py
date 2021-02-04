from pyspark.sql.functions import explode, lit, lower, regexp_replace, split


class VocabCreator:
    def __init__(self, path: str, spark):
        self.spark = spark
        self.df = spark.read.csv(path)

    def __call__(self):
        self.df = self.df.withColumnRenamed("_c1", "overall")
        self.df = self.df.withColumnRenamed("_c0", "reviewText")

        self.df = self.df.withColumn("dummy_col", lit(1))

        self.df = self.df.withColumn("array_col", split("reviewText", " "))
        words = self.df.withColumn("explode_col", explode("array_col"))

        words = words.drop("overall").drop("array_col").drop("reviewText")
        words = words.groupBy("explode_col").sum("dummy_col")
        words = words.select(
            "explode_col",
            "sum(dummy_col)",
            (
                lower(regexp_replace("explode_col", "[^a-zA-Z\\s]", "")).alias(
                    "text"
                )
            ),
        )
        words = words.drop("explode_col")
        words = words.filter(words["sum(dummy_col)"] > 20).orderBy(
            "sum(dummy_col)"
        )  # noqa E501

        words.show()

        words.repartition(1).write.format("com.databricks.spark.csv").save(
            "vocab.csv"
        )
