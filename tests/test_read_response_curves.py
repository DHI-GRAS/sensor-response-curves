import logging

import sensor_response_curves as srcurves


def test_get_response_curves():
    for sensor in srcurves.SUPPORTED_SENSORS:
        logging.info(sensor)
        wavelength, rcurves = srcurves.get_response_curves(
                sensor, pan_only=False, bandkeys=None, band_ids=None)
        assert len(rcurves) > 1


def test_get_pan():
    npassed = 0
    for sensor in srcurves.SUPPORTED_SENSORS:
        logging.info(sensor)
        sensorgroup = srcurves.SENSOR_GROUPS[sensor]
        if 'pan' not in srcurves.BANDS_TO_COLS[sensorgroup]:
            continue
        wavelength, rcurves = srcurves.get_response_curves(sensor, pan_only=True, bandkeys=None)
        assert len(rcurves) == 1
        npassed += 1
    assert npassed > 0


def test_get_custom():
    bandkeys = ['red', 'green', 'blue']
    for sensor in srcurves.SUPPORTED_SENSORS:
        logging.info(sensor)
        wavelength, rcurves = srcurves.get_response_curves(
                sensor, pan_only=False, bandkeys=bandkeys)
        assert len(rcurves) == len(bandkeys)
