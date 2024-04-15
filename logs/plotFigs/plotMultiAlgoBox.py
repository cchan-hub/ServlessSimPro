# -*- coding: utf-8 -*-
# @Author  : CaoHan
# @Time    : 2024/4/15 8:40
from matplotlib import pyplot as plt
import json
from enumClass.enumClass import ReqAllocAlgo, ConPlaceAlgo, ConConsAlgo, PopQueueAlgo


def plotCpu(time_series, u_cpu_list, color_list, algoNameList):
    plt.boxplot(u_cpu_list, labels=algoNameList)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.ylabel("CPU Usage Rate", fontweight='bold')
    plt.show()


def plotMem(time_series, u_mem_list, color_list, algoNameList):
    plt.boxplot(u_mem_list, labels=algoNameList)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.ylabel("Memory Usage Rate", fontweight='bold')
    plt.show()


def plotMaxCurr(time_series, max_concur_list, color_list, algoNameList):
    plt.boxplot(max_concur_list, labels=algoNameList)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.ylabel("Maximum Concurrency", fontweight='bold')
    plt.show()


def plotContainerCSNum(time_series, cold_start_list, color_list, algoNameList):
    plt.boxplot(cold_start_list, labels=algoNameList)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.ylabel("Containers in Cold Start State", fontweight='bold')
    plt.show()


def plotContainerRunNum(time_series, run_list, color_list, algoNameList):
    plt.boxplot(run_list, labels=algoNameList)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.ylabel("Containers in Running State", fontweight='bold')
    plt.show()


def plotContainerIdleNum(time_series, spare_list, color_list, algoNameList):
    plt.boxplot(spare_list, labels=algoNameList)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.ylabel("Containers in Idle State", fontweight='bold')
    plt.show()


def plotContainerDeadNum(time_series, kill_list, color_list, algoNameList):
    plt.boxplot(kill_list, labels=algoNameList)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.ylabel("Containers in Dead State", fontweight='bold')
    plt.show()


def plotPm(time_series, activePm_list, color_list, algoNameList):
    plt.boxplot(activePm_list, labels=algoNameList)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.ylabel("Active PMs", fontweight='bold')
    plt.show()



if __name__ == "__main__":
    # select the Comparison algorithms
    resolveNameList = [ReqAllocAlgo.EARLIEST_KILLED, ReqAllocAlgo.RANDOM, ReqAllocAlgo.LATEST_KILLED]

    time_series = []
    energy_list = []
    latency_list = []
    rej_list = []
    cold_start_times_list = []
    u_cpu_list = []
    u_mem_list = []
    max_concur_list = []
    cold_start_list = []
    run_list = []
    spare_list = []
    kill_list = []
    activePm_list = []
    migration_list = []
    color_list = ['b', 'g', 'y', 'c', 'r', 'm', 'k']
    algoNameList = []
    for resolveName in resolveNameList:
        with open(str(resolveName) + '.json', mode='r') as file:
            time_series_data = json.load(file)
        algoNameList.append(str(resolveName).split('.')[1])
        time_series = time_series_data['time_series']
        energy_list.append(time_series_data['energy_list'])
        latency_list.append(time_series_data['latency_list'])
        rej_list.append(time_series_data['rej_list'])
        cold_start_times_list.append(time_series_data['cold_start_times_list'])
        u_cpu_list.append(time_series_data['u_cpu_list'])
        u_mem_list.append(time_series_data['u_mem_list'])
        max_concur_list.append(time_series_data['max_concur_list'])
        cold_start_list.append(time_series_data['cold_start_list'])
        run_list.append(time_series_data['run_list'])
        spare_list.append(time_series_data['spare_list'])
        kill_list.append(time_series_data['kill_list'])
        activePm_list.append(time_series_data['activePm_list'])
        migration_list.append(time_series_data['migration_list'])
    plt.rcParams.update({'font.size': 12})
    plt.rcParams['font.weight'] = 'bold'

    plotCpu(time_series, u_cpu_list, color_list, algoNameList)
    plotMem(time_series, u_mem_list, color_list, algoNameList)
    plotMaxCurr(time_series, max_concur_list, color_list, algoNameList)
    plotContainerCSNum(time_series, cold_start_list, color_list, algoNameList)
    plotContainerIdleNum(time_series, spare_list, color_list, algoNameList)
    plotContainerDeadNum(time_series, kill_list, color_list, algoNameList)
    plotPm(time_series, activePm_list, color_list, algoNameList)
