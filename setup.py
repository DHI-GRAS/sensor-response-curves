from setuptools import setup, find_packages

setup(
    name='sensor_response_curves',
    version='0.2',
    description='Sensor Response Curves for WV, S2, L8, L7',
    author='Jonas Solvsteen',
    author_email='josl@dhi-gras.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['pandas', 'scipy', 'numpy'])
