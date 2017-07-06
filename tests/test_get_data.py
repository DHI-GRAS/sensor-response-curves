import pandas as pd
import sensor_response_curves as srcurves

def test_get_data_raw():
    for sensor in srcurves._supported_sensors:
        df = srcurves.get_data_raw(sensor)
        assert isinstance(df, pd.DataFrame)


def test_get_data_standard_names():
    for sensor in srcurves._supported_sensors:
        df = srcurves.get_data_standard_names(sensor)
        assert 'wavelength' in df.columns
