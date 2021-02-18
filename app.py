from flask import Flask, request, Response
from flask_influxdb import InfluxDB
import json

influxdb = InfluxDB()

app = Flask(__name__)
app.config.from_pyfile("config.cfg")
influxdb.init_app(app=app)

@app.route('/webhook', methods=['POST'])
def respond():
    if not request.content_type.startswith('application/json'):
        print(request.content_type)
        print(request.data)
        return Response(status=400)
    else:
        print("OK:", request.json, sep=" ") 

        influxdb.write_points(
            [
                {
                    "fields": {
                    "action": request.json.action,
                    "source": request.json.source,
                    "ticker": request.json.ticker,
                    "exchange": request.json.exchange,
                    "interval": request.json.interval,
                    "close": request.json.close
                    },
                    "measurement": "tv_webhook_data",
                }
            ]
        )
        return Response(status=200)
    

if __name__ == "__main__":
    app.run(debug=True)
