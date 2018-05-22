import logging


def test_get_csv_file(sensor):
    import sensor_response_curves as srcurves
    logging.info(sensor)
    srcurves._get_csv_file(sensor)


def test_parse_csv_file(sensor):
    import numpy as np
    import sensor_response_curves as srcurves
    logging.info(sensor)
    csvfile = srcurves._get_csv_file(sensor)
    data = srcurves._parse_csv(csvfile)
    assert isinstance(data, np.ndarray)
