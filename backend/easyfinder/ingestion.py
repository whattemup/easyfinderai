import pandas as pd


def ingest_csv(file) -> list:
df = pd.read_csv(file)
return df.to_dict(orient="records")
