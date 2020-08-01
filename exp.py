#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from psychopy import visual, core, event, clock, monitors, gui
from generate_data import *
from trial_func import *


# GUI
myDlg = gui.Dlg(title=u"实验")
myDlg.addText(u'被试信息')
myDlg.addField('name:')
myDlg.addField('sex:', choices=['male', 'female'])
myDlg.addField('age:', 21)
ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
if not myDlg.OK:
    core.quit()
name = ok_data[0]
sex = ok_data[1]
age = ok_data[2]


w, h = (3200, 1800)  # 显示器像素
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
mon.setSizePix((w, h))  # 设置显示器分辨率
mon.save()  # 保存显示器信息

# stim_size = [0.2, 0.4, 0.6, 0.8, 1, 1.2]  # 刺激半径大小，cm
# stim_size = [0.15, 0.3, 0.45, 0.6, 0.75, 0.9]
# 刺激大小（宽度）改为等比数列，三个水平，对应长度为宽度*4
stim_size = [0.24, 0.36, 0.48]
ratio = 4  # 长宽比
# theta = [45, 90, 135]
theta = [45, 135]  # 刺激角度，2个水平
ori = [1, 0]  # 刺激与方位角的关系，ori=1表示刺激长轴与方位角一致
r = 12.8  # 刺激距起始点距离，半径，cm, 10
repeat = 5  # 每个条件重复次数
stp_size = 0.5  # 起始点大小，半径，单位cm
stp_pos_y = -6.4  # 起始点纵坐标，以屏幕中心点为原点，下方为负，横坐标为0，单位cm
jitter = 0  # 角度随机范围，整数，默认0
t_bound = 0.6  # 反应时间上限， 600ms
sound_file = ['sound\\right.wav', 'sound\\wrong.wav', 'sound\\no_resp.wav']
# 生成trial
df = generate(stim_size, ratio, theta, ori,  r, repeat, stp_size, stp_pos_y)

df.to_csv('trial.csv')

result = {'id': [], 'x0': [], 'y0': [], 'x1': [], 'y1': [], 'dr': [],
          'p': [], 't_p': [], 'rt': [], 'resp': [], 'soa': [], 'points': []}

win = visual.Window(size=(w, h), fullscr=True, units='cm', color=[0, 0, 0], monitor=mon)
fix = visual.ImageStim(win, pos=(0, 0), image='icon/fix.png')
stim = visual.Rect(win, width=0.8, height=2.4, fillColor=[1, 0, -1], lineColor=[1, 1, 1], ori=45)
stp = visual.Circle(win, lineWidth=5, radius=0.5, fillColor=[0, 0, 0], lineColor=[0.5, 0.5, 0.5])
slider = visual.Slider(win, ticks=range(101), labels=list(np.arange(11) * 10),
                       pos=(0, -4), size=(16, 0.5), granularity=0, style='rating')
slider.marker.setColor([1, 0, -1], 'rgb')
hit_text = visual.TextStim(win, bold=True, color='yellow', text=u'击中')
miss_text = visual.TextStim(win, bold=True, color='purple', text=u'未击中')
no_response_text = visual.TextStim(win, bold=True, color='purple', text=u'超时')
text_p = visual.TextStim(win, text=u'请估计你击中该目标的概率: %s%%' % "?", pos=(-4.5, -3), height=0.5)
fix = visual.ImageStim(win, pos=(0, 0), image='icon/fix.png')
aim = visual.ImageStim(win, image='icon/fix.png', size=min(stim_size))
txt = {'hit': hit_text, 'miss': miss_text, 'no_response': no_response_text}
# r = 0.4*h
myMouse = event.Mouse()

# 指导语
visual.TextStim(win, bold=True, text='双击屏幕或点击鼠标开始实验', height=1).draw()
win.flip()
while sum(myMouse.getPressed(getTime=True)[0]) == 0:
    continue
# 实验
clk = clock.Clock()
clk.reset()
for i in range(len(df)):
    print(i)
    if i == len(df)//2:
        visual.TextStim(win, bold=True, text='请休息一下，双击屏幕或点击鼠标继续', height=1).draw()
        win.flip()
        while sum(myMouse.getPressed(getTime=True)[0]) == 0:
            continue
    win.flip()
    pos_start = (0, stp_pos_y)
    slider.reset()
    fix.draw()
    win.flip()
    core.wait(0.2)
    p_i, t_p_i, x0_i, y0_i, x1_i, y1_i, resp_i, rt_i, t_soa_i, point_i = run_trial(i, win, df, clk, slider, stim, stp,
                                                                                   aim, text_p, txt, sound_file,
                                                                                   pos_start, t_bound)
    result['id'].append(i)
    result['p'].append(p_i)
    result['t_p'].append(t_p_i)
    result['x0'].append(x0_i)
    result['x1'].append(x1_i)
    result['y0'].append(y0_i)
    result['y1'].append(y1_i)
    result['rt'].append(rt_i)
    result['resp'].append(resp_i)
    result['soa'].append(t_soa_i)
    result['points'].append(point_i)
    # result['resp_start'].append(rt_StartMove_i)

    win.flip()
    key = event.waitKeys(maxWait=0.2, keyList=['escape'])
    if key:
        core.wait(0.2)
        win.close()
        core.quit()
    event.clearEvents()
df['id'] = result['id']
df['p'] = result['p']
df['t_p'] = result['t_p']
df['x0'] = result['x0']
df['y0'] = result['y0']
df['x1'] = result['x1']
df['y1'] = result['y1']
df['rt'] = result['rt']
df['response'] = result['resp']
df['soa'] = result['soa']
df['points'] = result['points']

df['name'] = [name]*len(df)
df['sex'] = [sex]*len(df)
df['age'] = [age]*len(df)
df['distance'] = [distance]*len(df)
df['t_bound'] = [t_bound]*len(df)
df.to_csv('exp_data\\%s_%s.csv' % (name, time.strftime("%y-%m-%d-%H-%M")))
visual.TextStim(win, text='您本试实验估计正确率为：%s%%' % np.round(df.p.mean(), 1), pos=(0, 1)).draw()
visual.TextStim(win, text='您本试实验实际正确率为：%s%%' % np.round(len(df[df.response == 'hit'])*100/len(df), 1), pos=(0, -1)).draw()
visual.TextStim(win, text='本次实验结束', pos=(-8, 4)).draw()
win.flip()
core.wait(5)
win.close()
core.quit()
