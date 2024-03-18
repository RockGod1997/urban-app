import MacTmp
import time
import boto3
aws_access_key = ""
aws_secret_key = ""
s3_bucket_name = "meribaaaalti"
s3_object_key = "cpu_temperature_data.csv"
def get_cpu_temperature():
    temp = MacTmp.CPU_Temp()
    return temp
result=[]

def save_temperature_to_csv(temperatures):
       
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        temperatures= temperatures + "°C"

        result.append([current_time,temperatures])
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
        updated_data="\n".join([",".join(entry) for entry in result])
        # Upload the updated data to AWS S3
        s3.put_object(Bucket=s3_bucket_name, Key=s3_object_key, Body=updated_data)

csv_file = 'Device.csv' #Name it uniquely according to your choice

temperatures = get_cpu_temperature()
save_temperature_to_csv(temperatures)
time.sleep(60)  # Sleep for 60s