from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, DateType
from pyspark.sql.window import Window
import logging

def create_spark_session(app_name="Process Stock Data"):
    return SparkSession.builder \
        .master('local[*]') \
        .appName(app_name) \
        .config('spark.sql.legacy.timeParserPolicy', 'LEGACY') \
        .getOrCreate()


def define_schema():
    """Schema of the expected stock data"""
    return StructType([
        StructField('date', DateType(), False),
        StructField('symbol', StringType(), False),
        StructField('open', DoubleType(), True),
        StructField('high', DoubleType(), True),
        StructField('low', DoubleType(), True),
        StructField('close', DoubleType(), True),
        StructField('adj_close', DoubleType(), True),
         StructField("volume", DoubleType(), True)
    ])

def read_data(spark, input_path, schema):
    try:
        df = spark.read \
            .format('csv') \
            .option('header', 'true') \
            .schema(schema) \
            .load(input_path)
        return df
    except Exception as e:
        logging.error(f"Error reading data: {str(e)}")
        raise


def calculate_basic_metrics(df):
    """Calculate basic trading metrics"""
    return df \
        .withColumn("daily_return", 
            F.round((F.col("close") - F.col("open")) / F.col("open"), 4)) \
        .withColumn("trading_range", 
            F.round(F.col("high") - F.col("low"), 4)) \
        .withColumn("price_change_percentage", 
            F.round(((F.col("close") - F.col("open")) / F.col("open")) * 100, 2))


def calculate_technical_indicators(df):
    window_20 = Window.partitionBy('symbol').orderBy('date').rowsBetween(-19, 0)
    window_5 = Window.partitionBy('symbol').orderBy('date').rowsBetween(-4, 0)

    return df \
        .withColumn('ma_20', F.round(F.avg('close').over(window_20), 2)) \
        .withColumn('ma_5', F.round(F.avg('volume').over(window_5), 0))
   

def add_metadata(df):
     return df \
        .withColumn('processing_timestamp', F.current_date()) \
        .withColumn('data_source', F.lit('yahoo_finance'))   

def validate_data(df):
    
    validation_checks = [
        (F.col('high') >= F.col('low'), 'high_low_check'),
        (F.col('volume') >= 0, 'volume_check'),
        (F.col('open').isNotNull(), 'open_null_check')
    ]

    for check, name in validation_checks:
        invalid_count = df.filter(~check).count()
        if invalid_count > 0:
            logging.warning(f"Validation {name} failed for {invalid_count} records")

        return df

def main():
    logging.basicConfig(level=logging.INFO)
    
    try:
        spark = create_spark_session()
        logging.info("Spark session created successfully")

        schema = define_schema()
        df = read_data(spark, 'raw_stocks.csv', schema)
        logging.info(f"Loaded {df.count()} records")

        # Apply transformations
        df = calculate_basic_metrics(df)
        df = calculate_technical_indicators(df)
        df = add_metadata(df)
        
        # Validate results
        df = validate_data(df)

        # Show sample results
        df.show(20)

   
        df.write.mode('overwrite').parquet('processed_stocks')
        
        logging.info("Processing completed successfully")

    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
