#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


def generate(stim_size=[0.4, 0.6, 1], ratio=4, theta=[45, 135], ori=[1, 0],  r=10, repeat=5, stp_size=0.5, stp_pos_y=-5,
             jitter=0):
    """
    生成实验的数据
    :param stim_size: 刺激宽度大小，3个水平，单位cm
    :param ratio: 长宽比，默认4
    :param theta: 方位角度
    :param ori: 刺激与方位角的关系，ori=1表示刺激长轴与方位角一致；反之代表刺激长轴垂直于方位角
    :param r: 运动半径，cm
    :param repeat: 每种条件重复次数
    :param stp_size: 起始点大小，半径，单位cm
    :param stp_pos_y: 起始点纵坐标，以屏幕中心点为原点，下方为负，横坐标为0，单位cm
    :param jitter: 角度随机范围，+-10°
    return: DataFrame
    """
    df = pd.DataFrame()
    n = len(stim_size) * len(theta) * len(ori) * repeat
    df['theta'] = theta * len(stim_size) * len(ori) * repeat
    df['target_x'] = r * np.cos(df.theta * np.pi / 180)
    df['target_y'] = r * np.sin(df.theta * np.pi / 180) + stp_pos_y
    df['jitter'] = jitter
    # df['theta'] = df['theta0'] + np.random.randint(-jitter, jitter+1, len(df['theta0']))
    theta_ = stim_size * len(theta)
    theta_.sort()
    df['size_r'] = theta_ * len(ori) * repeat
    df['width'] = df['size_r'].values
    df['height'] = df['size_r'].values*ratio
    ori_ = ori * len(stim_size) * len(theta)
    ori_.sort()
    df['ori'] = ori_ * repeat
    df['r'] = [r] * n
    df['stp_size'] = [stp_size] * n
    df['stp_pos_y'] = [stp_pos_y] * n

    df = df.sample(frac=1)
    df.index = range(len(df))
    return df


if __name__ == '__main__':
    df = generate()
    df.to_csv('trial.csv')
