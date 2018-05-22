

def test_get_data_raw(sensor):
    import numpy as np
    import sensor_response_curves as srcurves
    data = srcurves.get_data_raw(sensor)
    assert isinstance(data, np.ndarray)


def test_get_data_standard_names(sensor):
    import sensor_response_curves as srcurves
    data = srcurves.get_data_standard_names(sensor)
    assert 'wavelength' in data.dtype.names
