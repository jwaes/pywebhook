from flask import Flask, request, Response
from flask_influxdb import InfluxDB
import json

influxdb = InfluxDB()

app = Flask(__name__)
app.config.from_pyfile("config.cfg")
influxdb.init_app(app=app)

@app.route('/webhook', methods=['POST'])
def respond():
    if request.content_type != 'application/json':
        print(request.content_type)
        print(request.data)
        return Response(status=400)
    else
        print(request.json) 

        influxdb.write_points(
            [
                {
                    "fields": {"raw":json.dumps(request.json)},
                    "measurement": "tv_webhook_raw",
                }
            ]
        )
        return Response(status=200)
    

if __name__ == "__main__":
    app.run(debug=True)
