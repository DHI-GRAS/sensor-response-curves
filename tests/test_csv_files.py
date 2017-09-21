import logging

import pandas as pd
import sensor_response_curves as srcurves


def test_get_csv_file():
    for sensor in srcurves.SUPPORTED_SENSORS:
        logging.info(sensor)
        srcurves._get_csv_file(sensor)


def test_parse_csv_file():
    for sensor in srcurves.SUPPORTED_SENSORS:
        logging.info(sensor)
        csvfile = srcurves._get_csv_file(sensor)
        df = srcurves._parse_csv(csvfile)
        assert isinstance(df, pd.DataFrame)
