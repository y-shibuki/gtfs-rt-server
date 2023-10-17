import io
import json
import os
import warnings
import zipfile

import dotenv
import pandas as pd
import requests

from app.utils.db import get_db_adapter

warnings.simplefilter("error")


# 環境変数の読み込み
dotenv.load_dotenv("./.env.local")

# 関東自動車（GTFS-RT）
# 公共交通データHUBシステムから取得
# https://www.ptd-hs.jp/
# 吉田のライセンスキーで取得
if __name__ == "__main__":
    API_KEY = os.environ.get("PTD_HS_KEY")
    db_adapter = get_db_adapter()

    # 最新のバージョンを確認
    with requests.get(
        "https://www.ptd-hs.jp/GetAgencyDetail?agency_id=0904"
    ) as response:
        df = pd.DataFrame(
            json.loads(json.dumps(response.json(), ensure_ascii=False))["Datas"]
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    latest_version = df.sort_values(by="timestamp")["version"].to_list()[-1]
    url = f"https://www.ptd-hs.jp/GetContentData?uid={API_KEY}&agency_id=0904&output=json&type=static&version={latest_version}"

    with (
        requests.get(url) as response,
        io.BytesIO(response.content) as bytes_io,
        zipfile.ZipFile(bytes_io) as zip,
        zip.open("trips.txt") as f,
        db_adapter.engine.connect() as con,
    ):
        columns = f.readline().decode("utf-8-sig").split(",")

        pd.DataFrame(
            [x.decode("utf-8-sig").split(",") for x in f.readlines()],
            columns=columns,
        )[["route_id", "service_id", "trip_id", "shape_id"]].to_sql(
            "trips_df", con=con, if_exists="replace", index=False
        )
