from flask import Flask, request, Response, render_template
from flask_influxdb import InfluxDB
import json

app = Flask(__name__)
app.config.from_pyfile("config.cfg")
influxdb = InfluxDB(app=app)

@app.route('/webhook', methods=['POST'])
def respond():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr

    if not request.content_type.startswith('application/json'):
        print(request.content_type)
        print(request.data)
        return Response(status=400)
    else:
        print("OK:", request.json, "|", ip, sep=" ") 

        influxdb.write_points(
            [
                {
                    "fields": {
                    "action": request.json['action'],
                    "source": request.json['source'],
                    "ticker": request.json['ticker'],
                    "exchange": request.json['exchange'],
                    "interval": request.json['interval'],
                    "close": float(request.json['close'])
                    },
                    "measurement": "tv_webhook_data",
                }
            ]
        )
        return Response(status=200)
    

@app.route('/')
def home():
    return render_template("home.html", content="Helloooowww")

@app.route('/history')
def history():
    return 'history comes here'

@app.route('/table') 
def table():
    data_measurement = "tv_webhook_data"
    # OK: {'action': 'buy', 'source': 'mdx', 'user': 'jaco', 'ticker': 'BTCUSD', 'exchange': 'BYBIT', 'interval': '15', 'close': 57752} | 52.32.178.7
    data_tags = ["time", "source", "ticker", "ticker", "exchange", "interval", "close"]

    tabledata = influxdb.query(
        "SELECT {0} from {1}".format(", ".join(data_tags), data_measurement)
    )

    data_points = []
    for measurement, tags in tabledata.keys():
        for p in tabledata.get_points(measurement=measurement, tags=tags):
            data_points.append(p)

    return render_template(
        "table.html",
        measurement=data_measurement,
        columns=data_tags,
        points=data_points,
        )    



if __name__ == "__main__":
    app.run(debug=True)
