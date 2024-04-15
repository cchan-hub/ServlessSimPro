# -*- coding: utf-8 -*-
# @Author  : CaoHan
# @Time    : 2022/11/15 15:30

import json
import heapq
import logging
from resource.container import Container
from resource.pm import PM, CPU
from resource.app import App, APP_NUM
import resource.req
import resource.app
from schedulingInterface.ContainerPlacement import FirstFit, MinVectorDist
from schedulingInterface.RequestAllocation import EarliestKilled, LatestKilled, RandomSelection
from schedulingInterface.ContainerConsolidation import MinPmNum
from schedulingInterface.PopQueue import FCFS, SJF, HRRN
from enumClass.enumClass import ReqAllocAlgo, ConPlaceAlgo, ConConsAlgo, PopQueueAlgo, Task, ContainerState

# ####################### Simulation Parameters(Adjustable) #######################
req_num = 200000
P_idle = 92.61
P_max = 259.67
P_mid = 94.8
cs_factor = 0.52

reuseTimeWindow = 600

USE_CONSOLIDATION = False
CONSOLIDATION_TIME_INTERVAL = 300
CONSOLIDATION_THRESHOLD = 0.38

LOG_TIME_INTERVAL = 50

APP_CONF_RANDOM = False

USE_QUEUE = True
PARAM1 = 50
PARAM2 = 50
QUEUE_THRESHOLD = [PARAM1] * APP_NUM
MAX_QUEUE_LENGTH = [PARAM2] * APP_NUM

# ####################### Strategies(Adjustable) #######################

ContainerPlacementStrategy = ConPlaceAlgo.FIRST_FIT
RequestAllocationStrategy = ReqAllocAlgo.EARLIEST_KILLED
ContainerConsolidationStrategy = ConConsAlgo.MIN_PM_NUM
PopQueueStrategy = PopQueueAlgo.FCFS

# log file name in /logs/plotFigs
LOG_STRATEGY = RequestAllocationStrategy
# ####################### Global Variables #######################
max_energy = 0
max_latency = 0
max_clodStartTimes = req_num
cold_start_times = 0
total_latency = 0
total_energy = 0
reject_num = 0
consolidation_num = 1
log_num = 1
seq = 0
cpu_pm = CPU
reqList = []
appList = []
consolidation_num_list = []
log_num_list = []
containerList = []
pmList = []
activeContainers = {}
jobList = []
appWaitingQueue = {}
migration_num = 0
logger = logging.getLogger(__name__)
energy_list = []
latency_list = []
rej_list = []
cold_start_times_list = []
migration_list = []
u_cpu_list = []
u_mem_list = []
max_concur_list = []
cold_start_list = []
run_list = []
spare_list = []
kill_list = []
activePm_list = []
time_series_data = {}
time_series = []


# ####################### Task Layer #######################


def createContainer(req, createTime):
    container = Container(appList[req.appId], createTime)
    containerList.append(container)
    activeContainers[container.appId].append(container.id)
    req.containerId = container.id
    if ContainerPlacementStrategy == ConPlaceAlgo.FIRST_FIT:
        noAvailablePM = FirstFit(pmList, container)
    elif ContainerPlacementStrategy == ConPlaceAlgo.MIN_VEC_DIST:
        noAvailablePM = MinVectorDist(pmList, container)
    else:
        logger.error("No container placement strategy is selected!")
        assert 1 == 0
    if noAvailablePM:
        pm0 = PM(createTime)
        pm0.remainMem -= container.mem
        pm0.remainCpu -= container.cpu
        pm0.containerIdList.append(container.id)
        pmList.append(pm0)


def containerKill(req, time):
    container = containerList[req.containerId]
    container.kill()
    activeContainers[container.appId].remove(container.id)
    for pm in pmList:
        if container.id in pm.containerIdList:
            pm.containerIdList.remove(container.id)
            pm.remainMem += container.mem
            pm.remainCpu += container.cpu
            if len(pm.containerIdList) == 0:
                pm.alive = False
                pm.start_end_time[1] = time
            break


def handleReq(req, time):
    if not USE_QUEUE:
        requestAlloc(req, time)
    else:
        if len(appWaitingQueue[req.appId]) == 0:
            hasSpareCon = False
            for c_id in activeContainers[req.appId]:
                if ContainerState(containerList[c_id].state.value) == ContainerState.SPARE:
                    hasSpareCon = True
                    break
            if hasSpareCon or len(activeContainers[req.appId]) < QUEUE_THRESHOLD[req.appId]:
                requestAlloc(req, time)
            else:
                appWaitingQueue[req.appId].append(req)
        else:
            if len(appWaitingQueue[req.appId]) < MAX_QUEUE_LENGTH[req.appId]:
                appWaitingQueue[req.appId].append(req)
            else:
                req.isRejected = True
                global reject_num
                reject_num += 1


def requestAlloc(req, time):
    spareCon2ThisReq = []
    for containerId in activeContainers[req.appId]:
        con = containerList[containerId]
        if ContainerState(con.state.value) == ContainerState.SPARE:
            spareCon2ThisReq.append(con)

    if RequestAllocationStrategy == ReqAllocAlgo.EARLIEST_KILLED:
        container = EarliestKilled(spareCon2ThisReq)
    elif RequestAllocationStrategy == ReqAllocAlgo.LATEST_KILLED:
        container = LatestKilled(spareCon2ThisReq)
    elif RequestAllocationStrategy == ReqAllocAlgo.RANDOM:
        container = RandomSelection(spareCon2ThisReq)
    else:
        logger.error("No request allocation strategy is selected!")
        assert 1 == 0
    global seq
    seq += 1
    if container is not None:
        killIndex = -1
        for ii in range(len(jobList)):
            if jobList[ii][2] == Task.CON_KILL and jobList[ii][3].containerId == container.id:
                killIndex = ii
                break
        jobList[killIndex] = jobList[-1]
        jobList.pop()
        if killIndex < len(jobList):
            heapq._siftup(jobList, killIndex)
            heapq._siftdown(jobList, 0, killIndex)
        req.containerId = container.id
        container.run(time)
        heapq.heappush(jobList, (req.run_end_timestamp, seq, Task.CON_SPARE, req))
        addPeriodicJob(req, req.run_end_timestamp)
    else:
        createContainer(req, time)
        heapq.heappush(jobList, (containerList[-1].coldStartEndTime, seq, Task.CON_RUN, req))
        addPeriodicJob(req, containerList[-1].coldStartEndTime)
        global cold_start_times
        cold_start_times += 1


def containerRun(req, time):
    c = containerList[req.containerId]
    c.run(time)
    global seq
    seq += 1
    heapq.heappush(jobList, (time + req.duration, seq, Task.CON_SPARE, req))
    addPeriodicJob(req, time + req.duration)


def containerSpare(req, time):
    req.end_timestamp = time
    if USE_QUEUE and len(appWaitingQueue[req.appId]) > 0:
        if PopQueueStrategy == PopQueueAlgo.FCFS:
            selectedReq = FCFS(appWaitingQueue[req.appId])
        elif PopQueueStrategy == PopQueueAlgo.SJF:
            selectedReq = SJF(appWaitingQueue[req.appId])
        elif PopQueueStrategy == PopQueueAlgo.HRRN:
            selectedReq = HRRN(appWaitingQueue[req.appId], time)
        else:
            logger.error("No pop queue strategy is selected!")
            assert 1 == 0
        selectedReq.containerId = req.containerId
        containerRun(selectedReq, time)
    else:
        c = containerList[req.containerId]
        c.spare(time, reuseTimeWindow)
        global seq
        seq += 1
        heapq.heappush(jobList, (time + reuseTimeWindow, seq, Task.CON_KILL, req))
        addPeriodicJob(req, time + reuseTimeWindow)


def addPeriodicJob(req, time):
    global consolidation_num, seq, log_num
    # consolidation periodic task
    if USE_CONSOLIDATION:
        while time > (
                CONSOLIDATION_TIME_INTERVAL * consolidation_num) and consolidation_num not in consolidation_num_list:
            consolidation_num_list.append(consolidation_num)
            seq += 1
            heapq.heappush(jobList, (CONSOLIDATION_TIME_INTERVAL * consolidation_num, seq, Task.CONSOLIDATION, req))
            consolidation_num += 1
    # system log periodic task
    while time > (LOG_TIME_INTERVAL * log_num) and log_num not in log_num_list:
        log_num_list.append(log_num)
        seq += 1
        heapq.heappush(jobList, (LOG_TIME_INTERVAL * log_num, seq, Task.SYS_LOG, req))
        log_num += 1


def containerConsolidate(time):
    if ContainerConsolidationStrategy == ConConsAlgo.MIN_PM_NUM:
        migrationConList = MinPmNum(time, pmList, containerList, CONSOLIDATION_THRESHOLD)
    else:
        logger.error("No container consolidation strategy is selected!")
        assert 1 == 0

    if len(migrationConList) > 0:
        global migration_num
        migration_num += len(migrationConList)
    for pm in pmList:
        if len(pm.containerIdList) == 0 and pm.alive:
            pm.alive = False
            pm.start_end_time[1] = time
    for container in migrationConList:
        container.coldStart(time, appList[container.appId].coldStartTime)
    for container in migrationConList:
        killIndex = -1
        reqId = -1
        for ii in range(len(jobList)):
            if jobList[ii][2] != Task.CONSOLIDATION and jobList[ii][2] != Task.SYS_LOG \
                    and jobList[ii][3].containerId == container.id:
                killIndex = ii
                reqId = jobList[ii][3].id
                break
        jobList[killIndex] = jobList[-1]
        jobList.pop()
        if killIndex < len(jobList):
            heapq._siftup(jobList, killIndex)
            heapq._siftdown(jobList, 0, killIndex)
        # add job
        global seq
        seq += 1
        heapq.heappush(jobList, (container.coldStartEndTime, seq, Task.CON_RUN, reqList[reqId]))
        global cold_start_times
        cold_start_times += 1


# ######################################## Metrics ########################################


def updateLatency(time):
    global total_latency
    latency = 0
    for i in range(req_num):
        req = reqList[i]
        if time < req.start_timestamp:  # not start yet
            continue
        if not req.isRejected:
            if req.end_timestamp == -1:
                latency += time - req.start_timestamp
            else:
                latency += req.end_timestamp - req.start_timestamp
    total_latency = latency


def updateEnergy(time):
    global total_energy
    cpu_i = []
    t_i_cs = []
    t_i_run = []
    t_i_total = []
    for container in containerList:
        cpu_i.append(container.cpu)
        t_cs = 0
        for slot in container.csTime:
            if slot.end == -1:
                t_cs += time - slot.start
            else:
                t_cs += slot.end - slot.start
        t_i_cs.append(t_cs)

        t_run = 0
        for slot in container.runTime:
            if slot.end == -1:
                t_run += time - slot.start
            else:
                t_run += slot.end - slot.start
        t_i_run.append(t_run)

        if container.killedTime != -1:
            t_total = container.killedTime - container.createTime
        else:
            t_total = time - container.createTime
        t_i_total.append(t_total)

    sum_cs, sum_running, sum_total = 0, 0, 0
    for i in range(len(cpu_i)):
        sum_cs += cpu_i[i] * t_i_cs[i]
        sum_running += cpu_i[i] * t_i_run[i]
        sum_total += cpu_i[i] * t_i_total[i]
    t_pm = 0
    for pm in pmList:
        if pm.start_end_time[1] == -1:
            t_pm += time - pm.start_end_time[0]
        else:
            t_pm += pm.start_end_time[1] - pm.start_end_time[0]
    total_energy = P_idle * t_pm + (P_max - P_mid) * sum_running / cpu_pm + cs_factor * (
            P_max - P_mid) * sum_cs / cpu_pm + (P_mid - P_idle) * sum_total / cpu_pm


def getEnergyRate(time):
    updateEnergy(time)
    return total_energy / max_energy


def getLatencyRate(time):
    updateLatency(time)
    return total_latency / max_latency


def getLatency(time):
    updateEnergy(time)
    return total_latency


def getEnergy(time):
    updateEnergy(time)
    return total_energy


def getCpuMemUsage():
    total_cpu = 0
    total_mem = 0
    using_cpu = 0
    using_mem = 0
    for pm in pmList:
        if pm.alive:
            total_cpu += pm.cpu
            total_mem += pm.mem
            using_cpu += pm.cpu - pm.remainCpu
            using_mem += pm.mem - pm.remainMem
    return using_cpu / total_cpu, using_mem / total_mem


def getColdStartProb():
    return cold_start_times / max_clodStartTimes


def getColdStart():
    return cold_start_times


def getConcur4EachApps():
    appConcurLevel = [0] * APP_NUM
    for container in containerList:
        if ContainerState(container.state.value) != ContainerState.KILL:
            appConcurLevel[container.appId] += 1
    return appConcurLevel


def getConcur4AllApps():
    appConcurLevel = getConcur4EachApps()
    concur_max = -1
    for concur in appConcurLevel:
        if concur > concur_max:
            concur_max = concur
    return concur_max


def getReject():
    return reject_num


def getRejectProb():
    return reject_num / req_num


def getMigrationNum():
    return migration_num


def getActivePmNum():
    num = 0
    for pm in pmList:
        if pm.alive:
            num += 1
    return num


def getContainerStateNum():
    cold_start = 0
    run = 0
    spare = 0
    kill = 0
    for container in containerList:
        if ContainerState(container.state.value) == ContainerState.COLD_START:
            cold_start += 1
        elif ContainerState(container.state.value) == ContainerState.RUN:
            run += 1
        elif ContainerState(container.state.value) == ContainerState.SPARE:
            spare += 1
        elif ContainerState(container.state.value) == ContainerState.KILL:
            kill += 1
    return cold_start, run, spare, kill


def getAvg(li):
    return sum(li) / len(li)


# ######################################## logging ########################################
def systemLog(time):
    updateEnergy(time)
    updateLatency(time)

    # Snapshot
    u_cpu, u_mem = getCpuMemUsage()
    max_concur = getConcur4AllApps()
    cold_start, run, spare, kill = getContainerStateNum()
    activePm = getActivePmNum()

    time_series.append(time)
    energy_list.append(total_energy)
    latency_list.append(total_latency)
    rej_list.append(reject_num)
    cold_start_times_list.append(cold_start_times)
    migration_list.append(migration_num)
    u_cpu_list.append(u_cpu)
    u_mem_list.append(u_mem)
    max_concur_list.append(max_concur)
    cold_start_list.append(cold_start)
    run_list.append(run)
    spare_list.append(spare)
    kill_list.append(kill)
    activePm_list.append(activePm)


def logInfo(endTime):
    logger.info("req_num: " + str(req_num))
    logger.info("reuseTimeWindow: " + str(reuseTimeWindow))
    logger.info("USE_CONSOLIDATION: " + str(USE_CONSOLIDATION))
    logger.info("CONSOLIDATION_TIME_INTERVAL: " + str(CONSOLIDATION_TIME_INTERVAL))
    logger.info("CONSOLIDATION_THRESHOLD: " + str(CONSOLIDATION_THRESHOLD))
    logger.info("LOG_TIME_INTERVAL: " + str(LOG_TIME_INTERVAL))
    logger.info("APP_CONF_RANDOM: " + str(APP_CONF_RANDOM))
    logger.info("USE_QUEUE: " + str(USE_QUEUE))
    logger.info("PARAM1: " + str(PARAM1))
    logger.info("PARAM2: " + str(PARAM2))
    logger.info("ContainerPlacementStrategy: "+str(ContainerPlacementStrategy))
    logger.info("RequestAllocationStrategy: "+str(RequestAllocationStrategy))
    logger.info("ContainerConsolidationStrategy: " + str(ContainerConsolidationStrategy))
    logger.info("PopQueueStrategy: " + str(PopQueueStrategy))
    logger.info("LOG_STRATEGY: "+str(LOG_STRATEGY))
    logger.info("-*-*-*-*-*-* metrics -*-*-*-*-*-*")
    logger.info("Total Energy Consumption:" + str(getEnergy(endTime)))
    logger.info("Total Latency:" + str(getLatency(endTime)))
    logger.info("Cold Start Count:" + str(getColdStart()))
    logger.info("Rejection Count:" + str(getReject()))
    logger.info("Average CPU Allocation Rate:" + str(getAvg(u_cpu_list)))
    logger.info("Average memory Allocation Rate:" + str(getAvg(u_mem_list)))
    logger.info("Average Maximum Concurrency:" + str(getAvg(max_concur_list)))
    logger.info("Average Cold Start State Count:" + str(getAvg(cold_start_list)))
    logger.info("Average Running State Count:" + str(getAvg(run_list)))
    logger.info("Average Idle State Count:" + str(getAvg(spare_list)))
    logger.info("Average Dead State Count:" + str(getAvg(kill_list)))
    logger.info("Average Active Physical Machine Count:" + str(getAvg(activePm_list)))
    if LOG_STRATEGY == PopQueueStrategy and USE_QUEUE:
        with open('logs/plotFigs/' + str(LOG_STRATEGY) + '(' + str(PARAM1) + ',' + str(PARAM2) + ').json',
                  mode='w') as file:
            json.dump(time_series_data, file)
    elif LOG_STRATEGY == ContainerConsolidationStrategy and USE_CONSOLIDATION:
        with open('logs/plotFigs/' + str(LOG_STRATEGY) + '(' + str(CONSOLIDATION_TIME_INTERVAL/60) + ').json',
                  mode='w') as file:
            json.dump(time_series_data, file)
    else:
        with open('logs/plotFigs/' + str(LOG_STRATEGY) + '.json', mode='w') as file:
            json.dump(time_series_data, file)


# #################################### real-time simulation ####################################

def initEnvironment():
    global reqList, appList, activeContainers, appWaitingQueue, jobList, seq, cpu_pm, P_max, P_mid, P_idle, \
        max_energy, max_latency, logger, time_series_data
    # logger
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('./logs/logMetrics')
    file_handler.setFormatter(logging.Formatter(fmt="%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(message)s",
                                                datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(file_handler)
    # 1980951 REQ
    reqList = resource.req.getReqList()
    # 119 APP
    appList = resource.app.getAppList(APP_CONF_RANDOM)
    # init activeContainers
    for appId in range(APP_NUM):
        activeContainers[appId] = []
        appWaitingQueue[appId] = []
    # init jobList
    num0 = 0
    for req in reqList:
        seq += 1
        jobList.append((req.start_timestamp, seq, Task.HANDLE_REQ, req))
        num0 += 1
        if num0 == req_num:
            break
    num1 = 0
    for req in reqList:
        max_energy += (req.duration + appList[req.appId].coldStartTime) * (P_max - P_idle) * appList[
            req.appId].cpu / cpu_pm + (req.duration + appList[req.appId].coldStartTime + reuseTimeWindow) * P_idle \
                      + reuseTimeWindow * (P_mid - P_idle)
        max_latency += appList[req.appId].coldStartTime
        num1 += 1
        if num1 == req_num:
            break
    time_series_data = {
        'time_series': time_series,
        'energy_list': energy_list,
        'latency_list': latency_list,
        'cold_start_times_list': cold_start_times_list,
        'migration_list': migration_list,
        'u_cpu_list': u_cpu_list,
        'u_mem_list': u_mem_list,
        'max_concur_list': max_concur_list,
        'cold_start_list': cold_start_list,
        'run_list': run_list,
        'spare_list': spare_list,
        'kill_list': kill_list,
        'activePm_list': activePm_list,
        'rej_list': rej_list
    }


def sim():
    logger.info("----------------------------simulation start----------------------------")
    endTime = 0
    while len(jobList) != 0:
        (time, sequence, task, req) = heapq.heappop(jobList)

        if task == Task.HANDLE_REQ:
            handleReq(req, time)
        elif task == Task.CON_RUN:
            containerRun(req, time)
        elif task == Task.CON_SPARE:
            containerSpare(req, time)
        elif task == Task.CONSOLIDATION:
            containerConsolidate(time)
        elif task == Task.SYS_LOG:
            systemLog(time)
        elif task == Task.CON_KILL:
            containerKill(req, time)

        if len(jobList) == 0:
            endTime = time
    updateLatency(endTime)
    logInfo(endTime)
    logger.info("-----------------------------simulation end-----------------------------")


if __name__ == "__main__":
    initEnvironment()
    sim()
