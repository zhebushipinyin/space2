#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from psychopy import visual, core, event, clock, monitors, iohub
from generate_data import *
from target import *


#: Constant for a Mouse Button Press Event.
MOUSE_BUTTON_PRESS = 32

#: Constant for a Mouse Button Release Event.
MOUSE_BUTTON_RELEASE = 33

w, h = (1280, 720)  # 显示器像素
distance = 50
width = 29.3
height = width * h / w
mon = monitors.Monitor(
    name='my_monitor',
    width=29.3,
    distance=50,  # 被试距显示器距离，单位cm
    gamma=1,  # gamma值
    verbose=False)  # 是否输出详细信息
# mon.setSizePix((3200, 1800))  # 设置显示器分辨率
mon.setSizePix((1280, 720))  # 设置显示器分辨率
mon.save()  # 保存显示器信息
win = visual.Window(size=(w, h), fullscr=True, units='cm', color=[0, 0, 0], monitor=mon)
shape = visual.ShapeStim(win, lineWidth=1.5, fillColor=[0, -1, 0])

stim = visual.Rect(win, width=0.4, height=1.6, pos=get_xy(12.8, 45, (0, -6.4)), ori=45
                   , fillColor=[-0.5, -0.5, 1], lineColor=[-0.5, -0.5, 1])
fix = visual.ImageStim(win, pos=get_xy(12.8, 45, (0, -6.4)), image='icon/fix.png', ori=45,size=0.4)

stp = visual.Circle(win, lineWidth=5, radius=0.5, fillColor=[0, 0, 0], lineColor=[0.5, 0.5, 0.5])
stp.pos = (0, -6.4)
slider = visual.Slider(win, ticks=range(101), labels=list(np.arange(11) * 10),
                       pos=(0, -4), size=(16, 0.5), granularity=0, style='rating')
myMouse = event.Mouse()
io = iohub.launchHubServer()
mouse = io.devices.mouse
# tar = Target(shape, r=6, h=0.5, theta0=0, size=60)
while True:
    # stim.pos = myMouse.getPos()
    stim.draw()
    stp.draw()
    fix.draw()
    slider.draw()
    win.flip()
    if mouse.getEvents(event_type=MOUSE_BUTTON_RELEASE):
        print(1)
    if (slider.getRating() is not None) & (myMouse.isPressedIn(stp)):
        break
    elif stp.contains(myMouse):
        stp.fillColor = [0.5, 0, -0.5]
    elif not stp.contains(myMouse):
        stp.fillColor = [1, 0, -1]
stp.fillColor = [0.5, 0, -0.5]
# stim.draw()
stp.draw()
fix.draw()
win.flip()
print(slider.getRating(), slider.getRT(), slider.getMouseResponses())
win.flip()
core.wait(0.2)
event.clearEvents()
stp.fillColor = [0.5, 0.5, 0.5]
while True:
    stim.draw()
    stp.draw()
    fix.draw()
    win.flip()
    buttons = myMouse.getPressed(getTime=True)
    if myMouse.isPressedIn(stim):
        print(buttons)
        break
    elif sum(buttons[0]):
        break
visual.TextStim(win, text='您本试实验估计正确率为：%s%%' % np.round(34.56, 1), pos=(0, 1)).draw()
visual.TextStim(win, text='您本试实验实际正确率为：%s%%' % np.round(90.45, 1), pos=(0, -1)).draw()
visual.TextStim(win, text='本次实验结束', pos=(-8, 4)).draw()
win.flip()
core.wait(2)
win.close()
core.quit()
