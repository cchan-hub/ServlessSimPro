# -*- coding: utf-8 -*-
# @Author  : CaoHan
# @Time    : 2022/11/15 17:29
import random
import math

APP_NUM = 119


class App:
    def __init__(self, id, mem, cpu, coldStartTime):
        self.id = id
        self.mem = mem
        self.cpu = cpu
        self.coldStartTime = coldStartTime


def getAppList(APP_CONF_RANDOM):
    appList = []
    if APP_CONF_RANDOM == False:
        for i in range(APP_NUM):
            appList.append(App(i, fixedMemList[i], fixedCpuList[i], fixedColdStartTime[i]))
        return appList
    else:
        # 根据阿里云实际设定，随机生成CPU, mem, coldStartTime，
        # CPU:0.05-16,以0.05递增，Memory:128-32768,以64递增，带宽5Gbps。CPU:Memory = 1:1 - 1:4。最大值为16核，32GB，比值为1:2。
        # 裸金属服务器大小为96核，192GB，比值为1:2。
        memList = []
        cpuList = []
        coldStartTime = []
        for i in range(APP_NUM):
            memoryGB = random.randint(2, 512) * 64 / 1024
            memList.append(memoryGB)  # 转化为以GB为单位的计费方式。
            cpu_min, cpu_max = max(0.05, memoryGB / 4), min(16.0, memoryGB)
            cpu_capacity = round(random.randint(math.ceil(cpu_min / 0.05), math.floor(cpu_max / 0.05)) * 0.05, 2)
            cpuList.append(cpu_capacity)
            coldStartTime.append(round(random.uniform(0.1, 10.0), 3))
        for i in range(APP_NUM):
            appList.append(App(i, memList[i], cpuList[i], coldStartTime[i]))
        return appList


# ########################## Fixed Config ######################################

fixedMemList = [10.6875, 18.8125, 3.9375, 3.75, 6.5625, 28.375, 27.5, 29.9375, 7.5, 8.1875, 20.375, 11.6875, 2.75, 7.6875,
           31.9375, 2.6875, 18.5, 16.5, 6.6875, 14.9375, 16.375, 14.375, 11.8125, 22.25, 10.125, 31.0, 13.8125, 9.875,
           27.375, 7.1875, 29.0, 5.5, 1.5625, 1.9375, 17.6875, 19.1875, 24.8125, 9.8125, 29.875, 1.5625, 12.5625, 17.0,
           31.9375, 23.8125, 6.0625, 2.625, 8.6875, 28.875, 4.8125, 23.75, 8.1875, 3.25, 4.875, 9.1875, 14.5, 17.3125,
           27.6875, 25.375, 17.375, 5.375, 18.0625, 8.0, 15.75, 22.9375, 20.875, 5.75, 15.6875, 10.25, 20.75, 19.875,
           13.25, 3.0625, 2.6875, 5.625, 6.875, 12.6875, 11.5, 28.0625, 8.0, 16.5625, 6.0625, 23.3125, 0.75, 6.6875,
           19.0625, 31.8125, 24.75, 22.75, 7.5, 7.0625, 5.5625, 23.875, 20.1875, 22.375, 2.9375, 7.75, 15.6875, 8.5,
           9.1875, 14.9375, 23.375, 14.75, 5.75, 27.1875, 16.8125, 19.5, 31.3125, 23.8125, 14.875, 24.5625, 2.5, 17.1875,
           9.0, 0.6875, 22.4375, 17.875, 20.8125, 31.0, 24.75]
fixedCpuList = [10.5, 10.2, 2.7, 3.5, 4.75, 12.3, 13.85, 15.05, 3.55, 7.7, 10.75, 4.05, 1.2, 5.2, 8.8, 1.75, 9.45, 6.55,
           3.85, 10.9, 7.2, 6.4, 9.25, 13.6, 8.3, 8.8, 9.85, 8.0, 8.85, 4.25, 11.0, 4.75, 0.7, 0.55, 14.6, 10.95, 11.8,
           9.45, 11.65, 1.0, 4.75, 7.15, 12.85, 10.3, 3.05, 2.15, 6.05, 14.8, 3.05, 12.0, 8.05, 2.95, 4.3, 9.0, 11.9,
           9.75, 8.8, 9.3, 10.85, 1.95, 4.95, 6.6, 12.15, 13.05, 7.75, 2.75, 7.6, 8.7, 7.05, 7.55, 10.35, 2.6, 1.9,
           2.45, 3.15, 12.25, 10.8, 9.5, 4.9, 12.15, 4.55, 15.1, 0.55, 3.95, 9.65, 11.1, 15.15, 15.65, 4.2, 3.35, 5.55,
           13.35, 11.9, 6.6, 2.05, 6.3, 9.25, 7.0, 4.9, 6.25, 7.45, 4.35, 3.9, 11.7, 8.15, 5.25, 13.2, 11.95, 10.45,
           9.55, 1.4, 12.2, 8.15, 0.35, 15.75, 14.25, 10.2, 14.1, 10.85]
fixedColdStartTime = [3.857, 2.573, 6.791, 0.726, 3.28, 8.229, 5.188, 6.356, 3.93, 1.426, 1.279, 7.333, 1.082, 4.336, 4.507,
                 8.583, 9.051, 1.148, 7.22, 7.937, 3.445, 5.604, 6.213, 9.219, 4.763, 7.972, 6.7, 8.76, 4.098, 5.552,
                 8.766, 4.099, 6.576, 9.281, 3.963, 5.102, 0.797, 5.38, 2.394, 2.516, 6.271, 2.676, 9.993, 7.832, 2.987,
                 3.722, 3.56, 0.883, 5.242, 4.245, 4.445, 1.301, 8.98, 8.255, 0.637, 9.921, 6.8, 6.668, 8.758, 7.676,
                 3.908, 0.529, 6.677, 4.03, 3.382, 3.599, 8.064, 6.04, 1.355, 8.328, 3.392, 9.628, 5.818, 2.923, 9.149,
                 2.262, 2.101, 7.722, 5.662, 9.866, 7.655, 1.919, 5.864, 3.227, 6.339, 7.579, 7.672, 6.065, 8.99, 3.169,
                 2.613, 9.434, 5.373, 4.014, 3.922, 4.225, 2.325, 3.572, 2.795, 7.653, 7.143, 0.59, 5.493, 4.374, 0.845,
                 1.642, 3.579, 2.723, 4.966, 6.889, 1.389, 6.297, 3.263, 5.01, 5.045, 1.638, 5.089, 5.75, 0.213]
#################################################################
