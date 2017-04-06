#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

import numpy as np
import pandas as pd
import netCDF4 as nc
from datetime import datetime
import pygrib
from ncepgrib2 import Grib2Decode, Grib2Encode


#inputDir = "E:\\work\\IBM\\wrf\\data\\sample_2015070200.nc"
inputDir = "/home/enso/max_micaps/wrf/data/"

def read_wrf(fn):
    fh = nc.Dataset(fn, mode='r')

    #lons = fh.variables['LONGITUDE'][:]
    #lats = fh.variables['LATITUDE'][:]
    #td2 = fh.variables['RH'][:]
    td2 = fh.variables['VV'][:, 1, :, :]

    data =  np.mat(np.reshape(td2, (420, 500)))
    #data = np.mat(np.ones((420, 500)))

    #lons = lons[::-1, :]
    return  data

# grbo = Grib2Encode(discipline_code, identification_section)
discipline_code = 0  # 0 for meteorlogical, 1 for hydrological, 2 for land surface, 3 for space, 10 for oceanographic products
identification_section = [
    7,           #@ 7 for NCEP, 38 for Beijing, 98 for ECMWF. http://www.nws.noaa.gov/tg/GRIB_C1.php
    0,           # Id of orginating sub-centre (local table)
    2,           # GRIB Master Tables Version Number
    1,           # http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_table1-1.shtml
    1,           #@ 1 for Start of Forecast. 
    2011,        #@ year
    1,           #@ month
    10,          #@ day
    12,          #@ hour
    0,           # minute
    0,           # second
    0,           #@ 0 for Operational Products. http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_table1-3.shtml
    1            #@ 1 for Forecast Products. http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_table1-4.shtml
]

# grbo.addgrid(grid_definition_info, grid_definition_template)
grid_definition_info = [
    0,           #@ 0 for Latitude/Longitude. http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_table3-1.shtml
    210000,       #@ Number of grid points in the defined grid
    0,           #@ 0 for regular grids. Number of octets needed for each additional grid points defn. Used to define number of points in each row for non-reg grids (=0 for regular grid).
    0,           # http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_table3-11.shtml
    30            #@ 0 for Latitude/Longitude. http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_table3-1.shtml
]
grid_definition_template = [
    4,           #@ 6 for Earth assumed spherical with radius = 6,371,229.0 m. Shape of the Earth (See Code Table 3.2)
    0,           # Scale Factor of radius of spherical Earth
    0,           # Scale value of radius of spherical Earth
    0,           # Scale factor of major axis of oblate spheroid Earth
    0,           # Scaled value of major axis of oblate spheroid Earth
    0,           # Scale factor of minor axis of oblate spheroid Earth
    0,           # Scaled value of minor axis of oblate spheroid Earth
    500,         #@ Ni?number of points along a parallel
    420,         #@ Nj?number of points along a meridian
    8600000,           
    82600000,
    0,
    35000000,
    110000000,
    12000000,   
    12000000,
    0,
    0,
    30000000,
    60000000,
    0,
    0
]

# grbo.addfield(product_definition_template_number, product_definition_template, data_representation_template_number, data_representation_template, data)
product_definition_template_number = 0  # http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_table4-0.shtml
product_definition_template = [
    0,          #@ Parameter category (see Code table 4.1)
    0,          #@ Parameter number (see Code table 4.2)
    2,          #@ 2 for Forecast. Type of generating process (see Code table 4.3)
    0,          # Background generating process identifier (defined by originating centre)
    96,         # Analysis or forecast generating process identified (see Code ON388 Table A)
    0,          # Hours of observational data cutoff after reference time (see Note)
    0,          # Minutes of observational data cutoff after reference time (see Note)
    1,          #@ 1 for hour. Indicator of unit of time range (see Code table 4.4)
    120,        #@ fcst valid for 120 hours. Forecast time in units defined by octet 18
    100,        #@ 100 for isobar, 1 for Ground or water surface, 103 for height about ground. Type of first fixed surface (see Code table 4.5)
    0,          #@ Scale factor of first fixed surface
    1000,       #@ 1000 for 1000hPa. Scaled value of first fixed surface
    255,        # Type of second fixed surfaced (see Code table 4.5)
    0,          # Scale factor of second fixed surface
    0           # Scaled value of second fixed surfaces
]
data_representation_template_number = 3
data_representation_template = [1156603904, 0, 1, 8, 0, 1, 0, 0, 0, 696, 0, 3, 1, 1, 32, 5, 1, 1]


def test(
        discipline_code = discipline_code,
        identification_section = identification_section,
        grid_definition_info = grid_definition_info,
        grid_definition_template = grid_definition_template,
        product_definition_template_number = product_definition_template_number,
        product_definition_template = product_definition_template,
        data_representation_template_number = data_representation_template_number,
        data_representation_template = data_representation_template):


    files = os.listdir(inputDir)
    files = sorted(files, key=lambda i:int(i.split('_')[1][0:10]))
    count = 0
    for ff in files:
        fn = os.path.join(inputDir, ff)
        data = read_wrf(fn)

        identification_section[0] = 98
        identification_section[5] = 2015
        identification_section[6] = 7
        identification_section[7] = 2
        identification_section[8] = 0

        grid_definition_info[1] = 500* 420

        grid_definition_template[7] = 500
        grid_definition_template[8] = 420

        product_definition_template[0] = 2
        product_definition_template[1] = 3
        product_definition_template[8] = count
        product_definition_template[9] = 103
        product_definition_template[10] = 0
        product_definition_template[11] = 10

        (
            identification_section,
            grid_definition_info,
            grid_definition_template,
            product_definition_template,
            data_representation_template
        ) = [np.array(_, dtype=np.int64) for _ in [
            identification_section,
            grid_definition_info,
            grid_definition_template,
            product_definition_template,
            data_representation_template
        ]]

        if count < 10:
            tt = '0%s' %count
        else:
            tt =count
        fn = "2015070200%s_WRF-10mVWIND_CHINA_12km" %tt 
        f=open(fn + '.grib2','wb')
        grbo = Grib2Encode(
            discipline_code,
            identification_section)
        grbo.addgrid(
            grid_definition_info,
            grid_definition_template)
        grbo.addfield(
            product_definition_template_number,
            product_definition_template,
            data_representation_template_number,
            data_representation_template,
            data)
        grbo.end()
        f.write(grbo.msg)
        f.close()
        count +=1

if __name__ == '__main__':
    test()

