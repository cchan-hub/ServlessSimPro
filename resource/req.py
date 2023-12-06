# -*- coding: utf-8 -*-
from functools import cmp_to_key


class Req:
    def __init__(self, app, func, end, dura):
        self.id = -1
        self.appId = app
        self.funcId = func
        self.run_end_timestamp = end
        self.duration = dura
        self.start_timestamp = end - dura
        self.containerId = -1
        self.end_timestamp = -1
        self.isRejected = False


def cmp_by_start_timestamp(a, b):
    if a.start_timestamp <= b.start_timestamp:
        return -1
    else:
        return 1


def getReqList():
    reqList = []
    line_num = 0
    with open('Trace/AzureFunctionsInvocationTraceForTwoWeeksJan2021.txt', 'r') as f:
        for line in f:
            if line_num == 0:
                line_num = 1
                continue
            data = line.split(',')
            tempReq = Req(data[0], data[1], float(data[2]), float(data[3].strip()))
            reqList.append(tempReq)
    appDict = {}
    funcDict = {}
    appNum = 0
    funcNum = 0

    for i in range(len(reqList)):
        if reqList[i].appId not in appDict.keys():
            appDict[reqList[i].appId] = appNum
            appNum += 1
        if reqList[i].funcId not in funcDict.keys():
            funcDict[reqList[i].funcId] = funcNum
            funcNum += 1
    for i in range(len(reqList)):
        reqList[i].appId = appDict[reqList[i].appId]
        reqList[i].funcId = funcDict[reqList[i].funcId]
    reqList.sort(key=cmp_to_key(cmp_by_start_timestamp))
    for i in range(len(reqList)):
        reqList[i].id = i
    return reqList
