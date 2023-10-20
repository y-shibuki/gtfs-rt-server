import json

import pandas as pd

from app.utils.db import get_db_adapter
from app.utils.logger import getLogger

logger = getLogger(__name__)
db_adapter = get_db_adapter()

with db_adapter.engine.connect() as con:
    df = pd.read_sql(
        """
        select *
        from timetable_db
        """,
        con=con
    )
df["tt"] = df["tt"].apply(json.loads)
logger.info(df.to_dict(orient="records")[0])
