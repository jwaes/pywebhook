from flask import Flask
from flask_influxdb import InfluxDB

influx_db = InfluxDB()

app = Flask(__name__)
app.config.from_pyfile("config.cfg")
influxdb.init_app(app=app)

@app.route('/webhook', methods=['POST'])
def respond():
    print(request.json);
    influx_db.write_points(
        [
            {
                "fields": {"raw":request.json},
                "measurement": "tv_webhook_raw",
            }
        ]
    )
    return Response(status=200)

if __name__ == "__main__":
    app.run(debug=True)
