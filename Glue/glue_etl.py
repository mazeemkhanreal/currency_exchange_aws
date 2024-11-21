import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import boto3  # Import boto3 for SES
from pyspark.sql.functions import col, max as max_
from pyspark.sql.types import DateType

# Parse job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

try:
    # Load data from S3
    print("Loading data from S3...")
    AmazonS3_node1731924571927 = glueContext.create_dynamic_frame.from_options(
        format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False},
        connection_type="s3",
        format="csv",
        connection_options={"paths": ["s3://etlpipeline/currency_exchange_raw/"], "recurse": True},
        transformation_ctx="AmazonS3_node1731924571927"
    )

    # Convert DynamicFrame to DataFrame
    print("Converting DynamicFrame to DataFrame...")
    df = AmazonS3_node1731924571927.toDF()

    # Convert `date` column to DateType
    print("Casting date column to DateType...")
    df = df.withColumn("date", col("date").cast(DateType()))

    # Filter for the latest date and currency 'EURO'
    print("Filtering for latest date and currency 'EURO'...")
    latest_date = df.select(max_("date")).collect()[0][0]  # Get the latest date
    euro_data = df.filter((col("currency") == "EURO") & (col("date") == latest_date))

    # Log data
    print(f"Latest date: {latest_date}")
    euro_data.show()

    # Check condition for alert
    print("Checking threshold condition for EURO...")
    below_threshold_count = euro_data.filter(col("converted_rate") < 300).count()
    print(f"Records below threshold: {below_threshold_count}")

    if below_threshold_count > 0:
        # Send Email Alert using SES
        ses = boto3.client('ses', region_name='us-east-1')  # Specify your AWS region
        try:
            response = ses.send_email(
                Source='mazeemkhanq@gmail.com',  # Replace with your SES verified email
                Destination={'ToAddresses': ['mazeemkhanq@gmail.com']},  # Replace with your recipient email
                Message={
                    'Subject': {'Data': 'Currency Alert: EURO Rate Below Threshold'},
                    'Body': {
                        'Text': {
                            'Data': f"The EURO currency rate is below 300 for the latest date: {latest_date}."
                        }
                    }
                }
            )
            print(f"SES Response: {response}")
            print("Email alert sent successfully.")
        except Exception as ses_error:
            print(f"Error while sending email: {ses_error}")
    else:
        print("No alert triggered: EURO rate is above threshold.")

    # Transform and write data back to S3
    print("Writing transformed data back to S3...")
    AmazonS3_node1732003914952 = glueContext.write_dynamic_frame.from_options(
        frame=AmazonS3_node1731924571927,
        connection_type="s3",
        format="glueparquet",
        connection_options={"path": "s3://etlpipeline/currency_exchange_transformed/", "partitionKeys": []},
        format_options={"compression": "uncompressed"},
        transformation_ctx="AmazonS3_node1732003914952"
    )

except Exception as e:
    print(f"Error occurred: {e}")
    raise e

# Commit job
print("Committing the job...")
job.commit()
