import pandas as pd
import sensor_response_curves as srcurves


def test_get_csv_file():
    for sensor in srcurves._supported_sensors:
        srcurves._get_csv_file(sensor)

def test_parse_csv_file():
    for sensor in srcurves._supported_sensors:
        csvfile = srcurves._get_csv_file(sensor)
        df = srcurves._parse_csv(csvfile)
        assert isinstance(df, pd.DataFrame)
