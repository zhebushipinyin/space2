#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from psychopy import visual, event, core
from target import *
import random
from psychopy.sound import Sound


def run_trial(i, win, df, clk, slider, stim, stp, text_p, txt, sound, pos_start=(0, 0)):
    """
    执行运动能力测量试次，得分矩阵\\
    points = {'phase_1': ['+100', '0', '-300'], 'phase_2': ['+100', '0', '-300']}\\
    index = ['hit', 'miss', 'no_response']
    :param i: 试次编号
    :param win: 窗口，psychopy visual.Window对象
    :param df: dataFrame, 实验trial表格
    :param clk: 时钟，psychopy clock对象
    :param slider: 概率条
    :param stim: 点击对象，visual.Circle()
    :param stp: 初始位置，visual.Circle()
    :param text_p: 概率文本 visual.TextStim()
    :param txt: 文本字典，txt = {'hit':hit_text, 'miss':miss_text, 'no_response': no_response_text}
    :param sound: 声音文件位置sound[0]:正确， sound[1]:错误
    :param pos_start: 初始点，(x, y)
    :return: 返回 概率p, 概率判断时间t_p, 初始位置(x0, y0)，落点位置(x1, y1)，反应resp, 反应时rt, soa
    """
    # soa = [0.1, 0.2, 0.3]
    # soa改为只有一种
    soa = [0.1]
    stim.radius = df.size_r[i]
    # stim.pos = get_xy(df.r[i], 90, pos_start)
    stim.pos = get_xy(df.r[i], df.theta0[i], pos_start)  # 刺激角度，无jitter
    stp.pos = pos_start
    stp.radius = df.stp_size[i]
    myMouse = event.Mouse()
    state = 'onset'
    clk.reset()  # 初始时钟
    feedback = visual.Circle(win, radius=0.2, fillColor=[0.5, 0.5, 0.5], lineColor=[0.5, 0.5, 0.5])
    feedback_sound_hit = Sound(sound[0])
    feedback_sound_miss = Sound(sound[1])
    feedback_sound_no_response = Sound(sound[2])

    while True:
        # 初始状态
        if state == 'onset':
            stim.draw()
            stp.draw()
            win.flip()
            core.wait(0.5)
            state = 'wait'
        elif state == 'wait':
            stim.draw()
            stp.draw()
            slider.draw()
            text_p.draw()
            win.flip()
            if slider.getRating() is not None:
                state = 'rating'
                stp.fillColor = [1, 1, 1]
                stp.lineColor = [1, 1, 1]
        # 评分
        elif state == 'rating':
            stim.draw()
            stp.draw()
            slider.draw()
            p = slider.getRating()
            t_p = slider.getRT()
            text_p.text = u'请估计你击中该目标的概率: %s%%' % int(p)
            text_p.draw()
            win.flip()
            if stp.contains(myMouse.getPos()):
                x0, y0 = myMouse.getPos()
                state = 'running'
                stim.pos = get_xy(df.r[i], df.theta[i], pos_start)  # 刺激角度，有jitter
        # 初始&等待刺激
        elif state == 'running':
            stp.fillColor = [0, 1, 0]
            stp.draw()
            win.flip()
            stp.fillColor = [0, 0, 0]
            stp.lineColor = [0.5, 0.5, 0.5]
            stp.draw()
            t_soa = random.choice(soa)
            core.wait(t_soa)
            win.flip()
            state = 'click'
            stim.fillColor = [1, 0, -1]
            stim.lineColor = [1, 1, 1]
            clk.reset()
        # 开始反应
        elif state == 'click':
            stim.draw()
            stp.draw()
            win.flip()
            buttons = myMouse.getPos()
            t = clk.getTime()
            t_StartMove = clk.getTime()
            if stim.contains(buttons):
                state = 'hit'
                resp = 'hit'
                x1, y1 = myMouse.getPos()
                rt = t
                feedback_sound_hit.play()
            # 超过700ms
            elif t > 0.7:
                state = 'no_response'
                resp = 'no_response'
                x1, y1 = myMouse.getPos()
                rt = t
                feedback_sound_no_response.play()
            elif not (stp.contains(buttons)):
                state = 'miss'
                resp = 'miss'
                x1, y1 = myMouse.getPos()
                rt = t
                feedback_sound_miss.play()
            elif stp.contains(buttons):
                rt_StartMove = t_StartMove
        # 击中
        elif state == 'hit':
            stp.draw()
            stim.draw()
            txt['hit'].pos = (x1-2, y1-2)
            txt['hit'].draw()
            feedback.pos = (x1, y1)
            feedback.draw()
            win.flip()
            state = 'quit'
        # 未击中
        elif state == 'miss':
            stp.draw()
            stim.draw()
            txt['miss'].pos = (x1-2, y1-2)
            txt['miss'].draw()
            feedback.pos = (x1, y1)
            feedback.draw()
            win.flip()
            state = 'quit'
        # 无反应
        elif state == 'no_response':
            stp.draw()
            stim.draw()
            txt['no_response'].pos = (0, 5)
            txt['no_response'].draw()
            feedback.pos = (x1, y1)
            feedback.draw()
            win.flip()
            state = 'quit'
        # 结束本试次
        elif state == 'quit':
            stim.fillColor = [1, 0, -1]
            stim.lineColor = [1, 1, 1]
            stp.fillColor = [0, 0, 0]
            stp.lineColor = [0.5, 0.5, 0.5]
            text_p.text = u'请估计你击中该目标的概率: %s%%' % '?'
            core.wait(0.4)
            feedback_sound_miss.stop()
            feedback_sound_hit.stop()
            feedback_sound_no_response.stop()
            break
    return p, t_p, x0, y0, x1, y1, resp, rt, t_soa