#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


def get_xy(r, theta, pos_start=(0, 0)):
    """
    将极坐标转换为直角坐标
    :param r: 极径
    :param theta: 角度
    :param pos_start: 初始点，(x, y)
    :return: 直角坐标(x, y)
    """
    return r * np.array((np.cos(theta * np.pi / 180), np.sin(theta * np.pi / 180))) + np.array(pos_start)


def get_rotate(Δx,  Δy, theta, pos_start=(0, 0)):
    """
    将极坐标转换为直角坐标
    :param Δx: 相对于旋转中心的横坐标
    :param Δy: 相较旋转中心的纵坐标
    :param theta: 旋转角度°
    :param pos_start: 初始点，(x0, y0)
    :return: 直角坐标(x, y)
    """
    ca = np.cos(theta * np.pi / 180)
    sa = np.sin(theta * np.pi / 180)
    return np.array((Δx*ca-Δy*sa, Δx*sa+Δy*ca)) + np.array(pos_start)


def get_pos(r, theta0, omega, mt):
    """
    计算时间 t 时的极坐标
    :param r: 极径
    :param theta0: 初始角度
    :param omega: 角速度
    :param mt: 运动时间
    :return: 新的极坐标(r, theta)
    """
    return r, theta0 + omega * mt


# 扇环对象，包含psychopy形状刺激shape，半径r，高度h，初始角度theta0以及角度大小size
class Target:
    def __init__(self, shape, r, h, theta0, size):
        self.shape = shape
        self.r = r
        self.h = h
        self.theta0 = theta0
        self.size = size

    def get_vert(self, theta):
        vert = []
        for i in range(11):
            vert.append(get_xy(self.r, theta + self.size * i / 10 - 0.5 * self.size))
        for j in range(11):
            vert.append(get_xy(self.r - self.h, theta + self.size * (1 - 0.1 * j) - 0.5 * self.size))
        self.shape.vertices = vert
