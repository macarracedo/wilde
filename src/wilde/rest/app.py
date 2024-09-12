import sys
from pathlib import Path
from typing import Final

from flask import Flask, request, make_response, send_from_directory
from sqlalchemy import create_engine, Engine

from wilde.Facade import Facade
from wilde.database.entity import Base
from wilde.model import LocationData
from wilde.plugin.PluginManager import PluginManager
from wilde.rest.mapper.LocationDataMapper import LocationDataMapper
from wilde.rest.mapper.MonitoringConfigurationMapper import MonitoringConfigurationMapper
from wilde.rest.mapper.ScheduleMapper import ScheduleMapper
from wilde.scheduler.Scheduler import Scheduler

if sys.argv.__len__() != 2:
    sys.argv.append("sqlite:///wilde.db")

_CONNECTION_STRING: Final[str] = sys.argv[1]

_DB_ENGINE: Final[Engine] = create_engine(_CONNECTION_STRING)
Base.metadata.create_all(_DB_ENGINE)

_FACADE: Final[Facade] = Facade(plugin_manager=PluginManager(), scheduler=Scheduler(start=True, engine=_DB_ENGINE))
_PAGES_PATH: Final[Path] = Path(__file__).parent.resolve() / "pages"
_LOCATION_DATA_MAPPER: Final[LocationDataMapper] = LocationDataMapper()
_MONITORING_CONFIGURATION_MAPPER: Final[MonitoringConfigurationMapper] = MonitoringConfigurationMapper(_FACADE)
_SCHEDULE_MAPPER: Final[ScheduleMapper] = ScheduleMapper()

app: Final[Flask] = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome():
    return send_from_directory(_PAGES_PATH, "welcome.html", mimetype="text/html")


@app.route("/watch", methods=["POST"])
def schedule_watch():
    _FACADE.schedule(_MONITORING_CONFIGURATION_MAPPER.map(request.json))

    response = make_response()
    response.status_code = 201
    return response


@app.route("/data/<plugin>/<operation>", methods=["GET"])
def get_data(plugin: str, operation: str):
    location: str | None = request.args.to_dict().pop("location", None)

    if location is None:
        response = make_response("Missing location argument")
        response.status_code = 400

        return response

    location_data = LocationData(location=location, data={})

    location_data = _FACADE.get_data(plugin_id=plugin, operation_id=operation,
                                     params=request.args.to_dict(), location_data=location_data)

    return _LOCATION_DATA_MAPPER.map(location_data)


@app.route("/watches", methods=["GET"])
def list_watches():
    monitors = _FACADE.list_watches()

    return _SCHEDULE_MAPPER.map(monitors)


def main():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
