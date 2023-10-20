import datetime
import json
import os
import warnings

import dotenv
import pandas as pd
import requests

from app.utils.db import get_db_adapter
from app.utils.logger import getLogger

warnings.simplefilter("error")

# 環境変数の読み込み
dotenv.load_dotenv("./.env.local")

# 関東自動車（GTFS-RT）
# 公共交通データHUBシステムから取得
# https://www.ptd-hs.jp/
if __name__ == "__main__":
    logger = getLogger(__name__)
    db_adapter = get_db_adapter()

    API_KEY = os.environ.get("PTD_HS_KEY")

    with requests.get(
        f"https://www.ptd-hs.jp/GetTripUpdate?uid={API_KEY}&agency_id=0904&output=json"
    ) as response:
        t_d = json.loads(response.text)

    res = []
    for temp in [
        x["tripUpdate"]
        for x in t_d["entity"]
        if x["tripUpdate"]["trip"]["scheduleRelationship"] == "SCHEDULED"
    ]:
        trip_id = temp["trip"]["tripId"]
        route_id = temp["trip"]["routeId"]

        for temp2 in temp["stopTimeUpdate"]:
            res.append(
                {
                    "trip_id": temp["trip"]["tripId"],
                    "stop_sequence": temp2["stopSequence"],
                    "stop_id": temp2["stopId"][:-5],
                    "delay": temp2["arrival"].get("delay"),
                    "arrival_time": datetime.datetime.fromtimestamp(
                        int(temp2["arrival"]["time"])
                    ).strftime("%H:%M:%S"),
                    "departure_time": datetime.datetime.fromtimestamp(
                        int(temp2["arrival"]["time"])
                    ).strftime("%H:%M:%S"),
                    "updated_at": datetime.datetime.fromtimestamp(
                        int(temp["timestamp"])
                    ),
                }
            )
    tripupdate_df = pd.DataFrame(res)

    with db_adapter.engine.connect() as con:
        tripupdate_df.to_sql(
            "tripupdate_db", con, if_exists="replace", index=False, method="multi"
        )
        con.commit()

        trips_df = pd.read_sql("""select * from trips_df""", con=con)

    temp_df = tripupdate_df.merge(trips_df, how="left", on="trip_id")

    res = []
    for trip_id, g in temp_df.groupby(by="trip_id"):
        temp = []
        tt = []
        d = ""
        for _, r in g.iterrows():
            # 前の発時刻と、次の着時刻が同様の場合には、スキップする
            if d == r["arrival_time"]:
                continue

            if r["stop_sequence"] == 0:
                tt.append({"d": r["departure_time"], "s": r["stop_id"]})
            else:
                tt.append(
                    {
                        "a": r["arrival_time"],
                        "d": r["departure_time"],
                        "s": r["stop_id"],
                        "delay": r["delay"],
                    }
                )
            d = r["departure_time"]
        res.append(
            {"trip_id": trip_id, "shape_id": r["shape_id"], "tt": json.dumps(tt)}
        )

    with db_adapter.engine.connect() as con:
        pd.DataFrame(res).to_sql(
            "timetable_db", con, if_exists="replace", index=False, method="multi"
        )
        con.commit()
