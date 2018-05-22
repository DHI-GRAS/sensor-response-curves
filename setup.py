from setuptools import setup, find_packages
import versioneer

setup(
    name='sensor_response_curves',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Sensor Response Curves for WV, GE, S2, L8, L7',
    author='Jonas Solvsteen',
    author_email='josl@dhigroup.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['scipy', 'numpy'])
