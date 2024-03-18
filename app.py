
import boto3
from flask import Flask, render_template
import requests
from io import StringIO
import pandas as pd

app = Flask(__name__)
#Open Weather API
api_key = ''
api_endpoint = 'http://api.openweathermap.org/data/2.5/weather'
default_city = 'Dublin'
default_country = 'IE'

#AWS instance details
aws_access_key_id = ''
aws_secret_access_key = ''
bucket_name = 'meribaaaalti'
object_key =['Device1.csv','Device2.csv'] # More csv files can be added here depending on the number of devices

def fetch_s3_data():
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    last_item=[]
    for key in object_key:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        csv_content = response['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_content),header=None)
        last_row = df.iloc[-1].to_dict()
        last_item.append([key,last_row])
    return last_item
@app.route('/')
def index():
    params = {'q': f'{default_city},{default_country}', 'appid': api_key}
    response = requests.get(api_endpoint, params=params)
    weather_data = response.json()

    city = weather_data['name']
    country = weather_data['sys']['country']
    temperature = weather_data['main']['temp']
    description = weather_data['weather'][0]['description']
    data = fetch_s3_data()
    #print(data)
    return render_template('index.html', city=city, country=country, temperature=float("{:.2f}".format(temperature-273.15)), description=description,last_items=data)



if __name__ == '__main__':
    app.run(debug=True)
