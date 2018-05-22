import pytest

from sensor_response_curves import SUPPORTED_SENSORS


@pytest.fixture(params=SUPPORTED_SENSORS)
def sensor(request):
    return request.param
