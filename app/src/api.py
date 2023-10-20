import pandas as pd
from fastapi import FastAPI

from app.utils.db import get_db_adapter
from app.utils.logger import getLogger

app = FastAPI()
logger = getLogger(__name__)
db_adapter = get_db_adapter()


@app.get("/get_trip_update")
async def get_trip_update():
    with db_adapter.engine.connect() as con:
        df = pd.read_sql(
            """
            select *
            from timetable_db
            """,
            con=con
        )

    return df.to_dict(orient="records")


@app.get("/test")
async def test():
    return "こんにちは。これはGTFS-RTの遅延データを配信するサーバーです。"
