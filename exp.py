#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from psychopy import visual, core, event, clock, monitors
from generate_data import *
from trial_func import *


name = input("请输入姓名：")
sex = input("请输入性别(男：1; 女：0)：")
age = input("请输入年龄：")

w, h = (1280, 720)  # 显示器像素
distance = 50
width = 29.3
height = width*h/w
mon = monitors.Monitor(
    name='my_monitor',
    width=29.3,
    distance=50,    # 被试距显示器距离，单位cm
    gamma=1,        # gamma值
    verbose=False)  # 是否输出详细信息
# mon.setSizePix((3200, 1800))  # 设置显示器分辨率
mon.setSizePix((1280, 720))  # 设置显示器分辨率
mon.save()  # 保存显示器信息

# stim_size = [0.2, 0.4, 0.6, 0.8, 1, 1.2]  # 刺激半径大小，cm
stim_size = [0.15, 0.3, 0.45, 0.6, 0.75, 0.9]
theta = [45, 90, 135]  # 刺激角度，三个水平
r =10  # 刺激距起始点距离，半径，cm, 10
repeat = 5  # 每个条件重复次数
stp_size = 0.5  # 起始点大小，半径，单位cm
stp_pos_y = -3  # 起始点纵坐标，以屏幕中心点为原点，下方为负，横坐标为0，单位cm
# 生成trial
df = generate(stim_size, theta, r, repeat, stp_size, stp_pos_y)
df.to_csv('trial.csv')

result = {'x0': [], 'y0': [], 'x1': [], 'y1': [], 'p': [], 't_p': [], 'rt': [], 'resp': [], 'soa': []}

win = visual.Window(size=(w, h), fullscr=True, units='cm', color=[0, 0, 0], monitor=mon)
fix = visual.ImageStim(win, pos=(0, 0), image='icon/fix.png')
stim = visual.Circle(win, radius=0.2, fillColor=[0.5, 0.5, 0.5], lineColor=[0.5, 0.5, 0.5])
stp = visual.Circle(win, radius=0.5, fillColor=[0.5, 0.5, 0.5], lineColor=[0.5, 0.5, 0.5])
slider = visual.Slider(win, ticks=range(101), labels=list(np.arange(11) * 10),
                       pos=(0, -5), size=(16, 0.5), granularity=0, style='triangleMarker')

hit_text = visual.TextStim(win, bold=True, color='yellow', text=u'击中')
miss_text = visual.TextStim(win, bold=True, color='purple', text=u'未击中')
no_response_text = visual.TextStim(win, bold=True, color='purple', text=u'超时')
text_p = visual.TextStim(win, text=u'请估计你击中该目标的概率%s%%' % "?", pos=(-4.5, -4), height=0.5)
txt = {'hit': hit_text, 'miss': miss_text, 'no_response': no_response_text}
# r = 0.4*h
myMouse = event.Mouse()

# 指导语
visual.TextStim(win, bold=True, text='阶段一，点击鼠标开始', height=1).draw()
win.flip()
while sum(myMouse.getPressed(getTime=True)[0]) == 0:
    continue
# 实验
clk = clock.Clock()
clk.reset()
for i in range(len(df)):
    print(i)
    win.flip()
    pos_start = (0, stp_pos_y)
    slider.reset()
    p_i, t_p_i, x0_i, y0_i, x1_i, y1_i, resp_i, rt_i, t_soa_i = run_trial(i, win, df, clk, slider, stim, stp, text_p, txt, pos_start)
    result['p'].append(p_i)
    result['t_p'].append(t_p_i)
    result['x0'].append(x0_i)
    result['x1'].append(x1_i)
    result['y0'].append(y0_i)
    result['y1'].append(y1_i)
    result['rt'].append(rt_i)
    result['resp'].append(resp_i)
    result['soa'].append(t_soa_i)
    win.flip()
    key = event.waitKeys(maxWait=0.2, keyList=['escape'])
    if key:
        core.wait(0.2)
        win.close()
        core.quit()
    event.clearEvents()
df['p'] = result['p']
df['t_p'] = result['t_p']
df['x0'] = result['x0']
df['y0'] = result['y0']
df['x1'] = result['x1']
df['y1'] = result['y1']
df['rt'] = result['rt']
df['response'] = result['resp']
df['soa'] = result['soa']

df['name'] = [name]*len(df)
df['sex'] = [sex]*len(df)
df['age'] = [age]*len(df)
df['distance'] = [distance]*len(df)
df.to_csv('exp_data\\%s_%s.csv' % (name, time.strftime("%H-%M-%S")))
visual.TextStim(win, text='本次实验结束').draw()
win.flip()
core.wait(2)
win.close()
core.quit()