# -*- coding: utf-8 -*-
# @Author  : CaoHan
# @Time    : 2022/11/15 10:02

from enumClass.enumClass import ContainerState

tempId = 0


class TimeSlot:
    def __init__(self, start):
        self.start = start
        self.end = -1


class Container:
    def __init__(self, app, coldStartStartTime):
        global tempId
        self.id = tempId
        tempId += 1
        self.appId = app.id
        self.mem = app.mem
        self.cpu = app.cpu
        self.state = ContainerState.COLD_START
        self.createTime = coldStartStartTime
        self.killedTime = -1
        self.coldStartEndTime = coldStartStartTime + app.coldStartTime
        self.runTime = []
        self.csTime = []
        self.csTime.append(TimeSlot(coldStartStartTime))

    def coldStart(self, time, duration):  # consolidation
        if self.state == ContainerState.COLD_START:
            self.csTime[-1].end = time
        elif self.state == ContainerState.RUN:
            self.runTime[-1].end = time
        self.state = ContainerState.COLD_START
        self.csTime.append(TimeSlot(time))
        self.killedTime = -1
        self.coldStartEndTime = time + duration

    def run(self, time):
        # if self.state == ContainerState.RUN:  # queue + reuse
        #     do nothing
        if self.state == ContainerState.COLD_START:  # run
            self.csTime[-1].end = time
            self.runTime.append(TimeSlot(time))
        elif self.state == ContainerState.SPARE:  # reuse
            self.runTime.append(TimeSlot(time))
            self.killedTime = -1
        self.state = ContainerState.RUN

    def spare(self, time, reuseTimeWindow):
        self.killedTime = time + reuseTimeWindow
        self.runTime[-1].end = time
        self.state = ContainerState.SPARE

    def kill(self):
        self.state = ContainerState.KILL

    @staticmethod
    def resetId():
        global tempId
        tempId = 0
