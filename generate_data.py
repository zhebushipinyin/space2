#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd


def generate(stim_size=[0.2, 0.4, 0.6, 0.8, 1, 1.2], theta=[0, 30, 60], r=10, repeat=5, stp_size=0.5, stp_pos_y=-5):
    """
    生成实验的数据
    :param stim_size: 刺激半径大小，6个水平，单位cm
    :param theta: 角度，三个水平，°
    :param r: 运动半径，cm
    :param repeat: 每种条件重复次数
    :param stp_size: 起始点大小，半径，单位cm
    :param stp_pos_y: 起始点纵坐标，以屏幕中心点为原点，下方为负，横坐标为0，单位cm
    :return: DataFrame
    """
    df = pd.DataFrame()
    n = len(stim_size) * len(theta) * repeat
    df['theta'] = theta * len(stim_size) * repeat
    theta_ = stim_size * len(theta)
    theta_.sort()
    df['size_r'] = theta_ * repeat
    df['r'] = [r] * n
    df['stp_size'] = [stp_size] * n
    df['stp_pos_y'] = [stp_pos_y] * n
    df = df.sample(frac=1)
    df.index = range(len(df))
    return df


if __name__ == '__main__':
    df = generate()
    df.to_csv('trial.csv')
