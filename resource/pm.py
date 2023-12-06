# -*- coding: utf-8 -*-
# @Author  : CaoHan
# @Time    : 2022/11/15 10:16
import random

tempId = 0
MEM = 192
CPU = 64


class PM:
    def __init__(self, startTime):
        global tempId
        self.id = tempId
        self.mem = MEM
        self.remainMem = self.mem
        self.cpu = CPU  # 同构
        self.remainCpu = self.cpu
        self.containerIdList = []
        self.start_end_time = [startTime, -1]
        self.alive = True
        tempId += 1

    @staticmethod
    def resetId():
        global tempId
        tempId = 0
