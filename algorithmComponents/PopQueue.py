def FCFS(waitingQueue):
    req = waitingQueue[0]
    del waitingQueue[0]
    return req


def SJF(waitingQueue):
    shortestReq = waitingQueue[0]
    del_id = 0
    for i in range(len(waitingQueue)):
        if waitingQueue[i].duration < shortestReq.duration:
            shortestReq = waitingQueue[i]
            del_id = i
    req = shortestReq
    del waitingQueue[del_id]
    return req


def HRRN(waitingQueue,time):
    HRR = 1 + (time - waitingQueue[0].start_timestamp)/waitingQueue[0].duration
    del_id = 0
    for i in range(len(waitingQueue)):
        RR = 1 + (time - waitingQueue[i].start_timestamp)/waitingQueue[i].duration
        if RR > HRR:
            del_id = i
    req = waitingQueue[del_id]
    del waitingQueue[del_id]
    return req
