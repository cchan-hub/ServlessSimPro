from resource.pm import PM
import copy


def MinPmNum(time, pmList, containerList, CONSOLIDATION_THRESHOLD):

    underThreshPMsConList = []
    pmListCopy = copy.deepcopy(pmList)
    for pm in pmList:
        if (pm.cpu - pm.remainCpu) < CONSOLIDATION_THRESHOLD * pm.cpu and pm.alive:
            underThreshPMsConList.extend(pm.containerIdList)
            pm.containerIdList = []
            pm.remainCpu = pm.cpu
            pm.remainMem = pm.mem

    Rpast = []
    for c_id in underThreshPMsConList:
        Rpast.append(containerList[c_id])
    Rpast.sort(key=lambda x: x.csTime[-1].start, reverse=False)
    migrationConList = []

    for container in Rpast:
        find = False
        for pm in pmList:
            if pm.remainMem >= container.mem and pm.remainCpu >= container.cpu and pm.alive:
                if pm.id >= len(pmListCopy) or container.id not in pmListCopy[pm.id].containerIdList:
                    migrationConList.append(container)
                pm.remainMem -= container.mem
                pm.remainCpu -= container.cpu
                pm.containerIdList.append(container.id)
                find = True
                break
        if not find:
            new_pm = PM(time)
            new_pm.remainMem -= container.mem
            new_pm.remainCpu -= container.cpu
            new_pm.containerIdList.append(container.id)
            pmList.append(new_pm)
            migrationConList.append(container)
    return migrationConList
