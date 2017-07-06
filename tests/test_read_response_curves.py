import sensor_response_curves as srcurves


def test_get_response_curves():
    for sensor in srcurves._supported_sensors:
        wv0, wv1, rcurves = srcurves.get_response_curves(
                sensor, pan_only=False, bandkeys=None, bandids=None)
        assert len(rcurves) > 1


def test_get_pan():
    npassed = 0
    for sensor in srcurves._supported_sensors:
        sensorgroup = srcurves._sensor_groups[sensor]
        if 'pan' not in srcurves._cols_to_bands[sensorgroup]:
            continue
        wv0, wv1, rcurves = srcurves.get_response_curves(sensor, pan_only=True, bandkeys=None)
        assert len(rcurves) == 1
        npassed += 1
    assert npassed > 0


def test_get_custom():
    bandkeys = ['red', 'green', 'blue']
    for sensor in srcurves._supported_sensors:
        wv0, wv1, rcurves = srcurves.get_response_curves(
                sensor, pan_only=False, bandkeys=bandkeys)
        assert len(rcurves) == len(bandkeys)
