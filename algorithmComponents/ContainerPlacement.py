# -*- coding: utf-8 -*-
# @Author  : zhangjq
# @Time    : 2023/4/11 09:52

def FirstFit(pmList, container):
    noAvailablePM = True
    for pm in pmList:
        if pm.remainMem >= container.mem and pm.remainCpu >= container.cpu and pm.alive:
            pm.remainMem -= container.mem
            pm.remainCpu -= container.cpu
            pm.containerIdList.append(container.id)
            noAvailablePM = False
            break
    return noAvailablePM


def MinVectorDist(pmList, container):
    y_cpu = container.cpu/(container.mem + container.cpu)
    y_mem = container.mem/(container.mem + container.cpu)
    minVectorDist = 1000000
    bestPm = None
    for pm in pmList:
        if pm.remainMem >= container.mem and pm.remainCpu >= container.cpu and pm.alive:
            x_cpu = pm.remainCpu/(pm.remainCpu + pm.remainMem)
            x_mem = pm.remainMem/(pm.remainCpu + pm.remainMem)
            dist = (x_cpu-y_cpu)*(x_cpu-y_cpu) + (x_mem-y_mem)*(x_mem-y_mem)
            if dist < minVectorDist:
                minVectorDist = dist
                bestPm = pm
    if bestPm is None:
        return True
    else:
        bestPm.remainMem -= container.mem
        bestPm.remainCpu -= container.cpu
        bestPm.containerIdList.append(container.id)
        return False
