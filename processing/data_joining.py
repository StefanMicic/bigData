# from loguru import logger as log
from pyspark.sql.functions import col, lit, translate


class Reader:
    def __init__(
        self, path_to_json: str, path_to_csv: str, path_to_txt: str, spark
    ):
        self.json = path_to_json
        self.csv = path_to_csv
        self.txt = path_to_txt
        self.spark = spark

    def __call__(self):
        return self.read_json(), self.read_csv(), self.read_txt()

    def read_json(self):
        print(self.json)
        print("AAAAAAAAAAAAAa")
        df = self.spark.read.json(self.json)
        print("BBBBBBBBBBBBBB")

        data_json = df.select(df["reviewText"], df["overall"])

        data_json = data_json.withColumn(
            "overall", translate("overall", "0", "0")
        )
        data_json = data_json.withColumn(
            "overall", translate("overall", "1", "0")
        )
        data_json = data_json.withColumn(
            "overall", translate("overall", "2", "0")
        )
        data_json = data_json.withColumn(
            "overall", translate("overall", "3", "1")
        )
        data_json = data_json.withColumn(
            "overall", translate("overall", "4", "1")
        )
        data_json = data_json.withColumn(
            "overall", translate("overall", "5", "1")
        )
        # log.info("Json files parsed")
        return data_json

    def read_csv(self):
        df = self.spark.read.csv(self.csv)
        data_csv = df.select(df["_c5"], df["_c0"])
        data_csv = data_csv.withColumn("_c0", translate("_c0", "4", "1"))

        data_csv = data_csv.withColumnRenamed("_c0", "overall")
        data_csv = data_csv.withColumnRenamed("_c5", "reviewText")
        # log.info("CSV files parsed")
        return data_csv

    def read_txt(self):
        data_text = self.spark.read.text(self.txt)
        data_text = data_text.filter(~col("value").like("%P%"))
        data_text = data_text.filter(~col("value").like("%-%"))

        data_text = data_text.withColumnRenamed("value", "reviewText")
        data_text = data_text.withColumn("overall", lit("1"))
        # log.info("Text files parsed")
        return data_text
