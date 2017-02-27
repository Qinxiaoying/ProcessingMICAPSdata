#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @Author: QinXY
    @Date  : 2017-2-22
'''

import os
import numpy as np
import pandas as pd

InputDir = "E:\\work\\IBM\\data\\"
OututDir = ''

CityInfo = {
            'HeFei': 58321,
            'BeiJing': 54511,
            'ChongQing': 57516,
            'TaiBei': 58968,
            'Macau': 45011,
            'GuangZhou': 59287,
            'LanZhou': 52889,
            'NanNing': 59431,
            'GuiYang': 57816,
            'ZhengZhou': 57083,
            'WuHan': 57494,
            'ShiJiaZhuang': 53698,
            'HaiKou': 59758,
            'HaErBin': 50953,
            'ChangSha': 57687,
            'ChangChun': 54161,
            'NanJing': 58238,
            'NanChang': 58606,
            'ShenYang': 54342,
            'Hohhot': 53463,
            'YinChuan': 53614,
            'XiNing': 52866,
            'ChengDou': 56294,
            'JiNan': 54823,
            'ShangHai': 58362,
            'TaiYuan': 53772,
            'TianJin': 54527,
            'Urumqi': 51463,
            'Lhasa': 55591,
            'KunMing': 56778,
            'HangZhou': 58457
}

Ele = {
        u'非对流性降水': 'w1',
        u'对流性降水': 'w2'
}


def ReadData():
    for stname, stid in CityInfo.items():
        value, name = [], []
        fds = os.listdir(os.path.abspath(InputDir))
        for fd in fds:
            print stid, stname
            name.append(fd)
            files = os.listdir(os.path.join(os.path.abspath(InputDir), fd))
            for file in files:
                prep = file[10:12]
                df = pd.read_table(os.path.join(os.path.abspath(InputDir), fd, file),
                                   skiprows=2, header=None, delim_whitespace=True)
                ID, LON, LAT = df[0], df[1], df[2]
                idx = ID.tolist()
                if stid in idx:
                    df1 = df[df[0] == stid][4]
                    value.append(df1.tolist())
                else:
                    value.append(np.nan)
                #break
        yield value, name, stname, stid
        break


def Write2CSV():
    for data in ReadData():
        print np.reshape(data[0], (2, 28))[0]


if __name__ == "__main__":
    Write2CSV()
