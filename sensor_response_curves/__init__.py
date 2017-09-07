from __future__ import division
import os

import pandas as pd
import numpy as np
import scipy.interpolate

_here = os.path.abspath(os.path.dirname(__file__))
_csvdir = os.path.join(_here, 'data')

_sensor_groups = {
        'WV2': 'WV',
        'WV3': 'WV',
        'PHR1A': 'PHR',
        'PHR1B': 'PHR',
        'SPOT6': 'PHR',
        'L7': 'L7',
        'L8': 'L8',
        'S2': 'S2'}

_supported_sensors = sorted(list(_sensor_groups))

_cols_to_bands = {
        'S2': {
            'wavelength': 'SR_WL',
            'coastal': 'SR_AV_B1',
            'blue': 'SR_AV_B2',
            'green': 'SR_AV_B3',
            'red': 'SR_AV_B4',
            'rededge': 'SR_AV_B5',
            'rededge2': 'SR_AV_B6',
            'rededge3': 'SR_AV_B7',
            'nir1': 'SR_AV_B8',
            'nir2': 'SR_AV_B8A',
            'nir3': 'SR_AV_B9',
            'swir1': 'SR_AV_B10',
            'swir2': 'SR_AV_B11',
            'swir3': 'SR_AV_B12'},
        'WV': {
            'wavelength': 'Wavelength',
            'pan': 'Panchromatic',
            'coastal': 'Coastal',
            'blue': 'Blue',
            'green': 'Green',
            'yellow': 'Yellow',
            'red': 'Red',
            'rededge': 'Red Edge',
            'nir1': 'NIR1',
            'nir2': 'NIR2'},
        'PHR': {
            'wavelength': 'Wavelength',
            'green': 'B1Blue',  # the order of Pleadis bands is like below (RGBN),
            'blue': 'B2Green',  # not like indicated in the metadata file (BGRN)
            'red': 'B3Red',
            'nir1': 'B4NIR'},
        'L8': {
            'wavelength': 'Wavelength',
            'coastal': 'L8B1Coast',
            'blue': 'L8B2Blue',
            'green': 'L8B3Green',
            'red': 'L8B4Red',
            'nir1': 'L8B5NIR',
            'pan': 'L8B8Pan'},
        'L7': {
            'wavelength': 'Wavelength',
            'blue': 'L7B1Blue',
            'green': 'L7B2Green',
            'red': 'L7B3Red',
            'nir1': 'L7B4NIR',
            'nir2': 'L7B5NIR',
            'pan': 'L7B8Pan'}}

_common_bands = ['red', 'green', 'blue', 'nir1']

_bands_to_cols = {sk: {v: k for k, v in _cols_to_bands[sk].items()} for sk in _cols_to_bands}

_default_bands = {
        'S2': [
            'coastal', 'blue', 'green', 'red',
            'rededge', 'rededge2', 'rededge3', 'nir1', 'nir2'],
        'WV': [
            'coastal', 'blue', 'green', 'yellow',
            'red', 'rededge', 'nir1', 'nir2'],
        'PHR': [
            'red', 'blue', 'green', 'nir1'],
        'L8': [
            'coastal', 'blue', 'green', 'red', 'nir1'],
        'L7': [
            'blue', 'green', 'red', 'nir1']}


def _check_supported_sensor(sensor):
    if sensor not in _supported_sensors:
        raise ValueError(
                'Sensor \'{}\' is not supported. Choose from {}.'
                ''.format(sensor, _supported_sensors))


def _parse_csv(infile):
    return pd.read_csv(infile)


def _get_sensor_columns(df, sensor):
    sensorgroup = _sensor_groups[sensor]
    colmap = _bands_to_cols[sensorgroup]
    colmap_inverse = _cols_to_bands[sensorgroup]
    df_renamed = df.rename(columns=colmap)
    if set(df_renamed.columns) != set(colmap_inverse):
        raise ValueError(
                'Expecting to have renamed all existing columns. '
                'But the result is {} and the set to rename was {}.'
                ''.format(list(df_renamed.columns), list(colmap_inverse)))
    return df_renamed


def _get_default_bands(sensor):
    sensorgroup = _sensor_groups[sensor]
    bandkeys = _default_bands[sensorgroup]
    return bandkeys


def _get_columns(df, *colnames):
    return [df[colname].values for colname in colnames]


def _get_csv_file(sensor):
    """Get CSV file for given sensor

    Parameters
    ----------
    sensor : str in _supported_sensors
        sensor name
    """
    _check_supported_sensor(sensor)
    fname = sensor + '.txt'
    csvfile = os.path.join(_csvdir, fname)
    if not os.path.isfile(csvfile):
        raise ValueError(
                'CSV file missing from package: \'{}\'.'.format(csvfile))
    return csvfile


def get_data_raw(sensor):
    """Get sensor response curve data for sensor

    Parameters
    ----------
    sensor : str in _supported_sensors
        sensor name

    Returns
    -------
    pandas.DataFrame
    """
    _check_supported_sensor(sensor)
    infile = _get_csv_file(sensor)
    df = _parse_csv(infile)
    return df


def get_data_standard_names(sensor):
    """Get sensor response curve data for sensor with renamed columns

    Parameters
    ----------
    sensor : str in _supported_sensors
        sensor name

    Returns
    -------
    pandas.DataFrame : data with standard names
        column order corresponds to band order
    """
    df = get_data_raw(sensor)
    df_renamed = _get_sensor_columns(df, sensor)
    if 'wavelength' not in df_renamed.columns:
        raise RuntimeError(
                'Renaming seems to have failed.')
    return df_renamed


def get_response_curves(
        sensor, pan_only=False, bandkeys=None, band_ids=None):
    """Read response curves for given sensor

    Parameters
    ----------
    sensor : str in _supported_sensors
        sensor name
    pan_only : bool
        whether to get pan band only
    bandkeys : list of str, optional
        list of bands to get curves for
        default: _default_bands for the
                 given sensor group
    band_ids : list of int, optional
        list of band numbers to get curves for
        default: as bandkeys

    Returns
    -------
    float, float : wavelength start, wavelength end
    ndarray : sensor response curve
    """
    df = get_data_standard_names(sensor)
    wavelength = df['wavelength'].values
    start_wv = wavelength[0]
    end_wv = wavelength[-1]
    # collect bands specific for each sensor and start and end wavelenghts
    if bandkeys is not None:
        pass
    elif band_ids is not None:
        bandkeys = [df.columns[i] for i in band_ids]
    elif pan_only:
        bandkeys = ['pan']
    else:
        bandkeys = _get_default_bands(sensor)
    return start_wv, end_wv, _get_columns(df, *bandkeys)


def resample_response_curves(
        rcurve, start_wv, end_wv, resolution, kind='slinear'):
    """Resample the given response curve to specified spectral resolution

    Parameters
    ----------
    rcurve : ndarray
        sensor response curve
    start_wv, end_wv : float
        start and end wavelengths
    resolution : float
        resolution to interpolate to
    kind : str
        interpolation algorithm for
        scipy.interpolate.interp1d
    """
    x = np.linspace(start_wv, end_wv, len(rcurve))
    f = scipy.interpolate.interp1d(x, rcurve, kind=kind)
    xnew = np.linspace(start_wv, end_wv, (end_wv-start_wv) // resolution + 1)
    return f(xnew)
