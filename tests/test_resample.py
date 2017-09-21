import sensor_response_curves as srcurves
import sensor_response_curves.resample as srresample


def test_resample_response_curves():
    sensor = 'S2A'
    wavelength, rcurves = srcurves.get_response_curves(sensor)
    wavelength, rcurves = srresample.resample_response_curves(wavelength, rcurves, resolution=5)
