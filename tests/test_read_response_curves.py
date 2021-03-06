

def test_get_response_curves(sensor):
    import sensor_response_curves as srcurves
    wavelength, rcurves = srcurves.get_response_curves(
            sensor, pan_only=False, bandkeys=None, band_ids=None)
    assert rcurves.shape[0] > 1


def test_get_pan(sensor):
    import sensor_response_curves as srcurves
    sensorgroup = srcurves.SENSOR_GROUPS[sensor]
    if 'pan' not in srcurves.BANDS_TO_COLS[sensorgroup]:
        return
    wavelength, rcurves = srcurves.get_response_curves(sensor, pan_only=True, bandkeys=None)
    assert rcurves.shape[0] == 1


def test_get_bandkeys(sensor):
    import sensor_response_curves as srcurves
    bandkeys = ['red', 'green', 'blue']
    wavelength, rcurves = srcurves.get_response_curves(
        sensor, pan_only=False, bandkeys=bandkeys)
    assert rcurves.shape[0] == len(bandkeys)


def test_get_band_ids(sensor):
    import sensor_response_curves as srcurves
    band_ids = [3, 2, 1]
    wavelength, rcurves = srcurves.get_response_curves(
        sensor, pan_only=False, band_ids=band_ids)
    assert rcurves.shape[0] == len(band_ids)
