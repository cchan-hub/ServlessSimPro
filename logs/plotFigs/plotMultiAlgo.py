from matplotlib import pyplot as plt
import json
from enumClass.enumClass import ReqAllocAlgo, ConPlaceAlgo, ConConsAlgo, PopQueueAlgo


# plot metrics over time figures for multi algorithm

def plotConsumeEnergy(time_series, energy_list, color_list, algoNameList):
    for i in range(len(energy_list)):
        plt.plot(time_series, energy_list[i], c='k', ls='-.', marker='.', mfc='b', mec=color_list[i], mew=1,
                 label=algoNameList[i])
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s", fontweight='bold')
    plt.ylabel("Energy Consumption/J", fontweight='bold')
    plt.legend()
    plt.show()


def plotLatency(time_series, latency_list, color_list, algoNameList):
    for i in range(len(latency_list)):
        plt.plot(time_series, latency_list[i], c='k', ls='-.', marker='.', mfc='b', mec=color_list[i], mew=1,
                 label=algoNameList[i])
    plt.ticklabel_format(style='sci', axis='both', scilimits=(0, 0))
    plt.xlim(140000, 150000)
    plt.ylim(8.3e5, 9.2e5)
    plt.xlabel("t/s", fontweight='bold')
    plt.ylabel("Latency/s", fontweight='bold')
    plt.legend()
    plt.show()


def plotRej(time_series, rej_list, color_list, algoNameList):
    for i in range(len(rej_list)):
        plt.plot(time_series, rej_list[i], c='k', ls='-.', marker='.', mfc='b', mec=color_list[i], mew=1,
                 label=algoNameList[i])
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s", fontweight='bold')
    plt.ylabel("Rejections", fontweight='bold')
    plt.legend()
    plt.show()


def plotCpu(time_series, u_cpu_list, color_list, algoNameList):
    for i in range(len(u_cpu_list)):
        plt.plot(time_series, u_cpu_list[i], c='k', ls='-.', marker='.', mfc='b', mec=color_list[i], mew=1,
                 label=algoNameList[i])
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s", fontweight='bold')
    plt.ylabel("CPU Usage Rate", fontweight='bold')
    plt.legend()
    plt.show()


def plotMem(time_series, u_mem_list, color_list, algoNameList):
    for i in range(len(u_mem_list)):
        plt.plot(time_series, u_mem_list[i], c='k', ls='--', marker='.', mfc='b', mec=color_list[i], mew=1,
                 label=algoNameList[i])
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s", fontweight='bold')
    plt.ylabel("Memory Usage Rate", fontweight='bold')
    plt.legend()
    plt.show()


def plotMaxCurr(time_series, max_concur_list, color_list, algoNameList):
    for i in range(len(max_concur_list)):
        plt.plot(time_series, max_concur_list[i], c='k', ls='-.', marker='.', mfc='b', mec=color_list[i], mew=1,
                 label=algoNameList[i])
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s", fontweight='bold')
    plt.ylabel("Maximum Concurrency", fontweight='bold')
    plt.legend()
    plt.show()


def plotContainerCSNum(time_series, cold_start_list, color_list, algoNameList):
    for i in range(len(cold_start_list)):
        plt.plot(time_series, cold_start_list[i], c='k', ls='-.', marker='.', mfc='b', mec=color_list[i], mew=1,
                 label=algoNameList[i])
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s", fontweight='bold')
    plt.ylabel("Containers in Cold Start State", fontweight='bold')
    plt.legend()
    plt.show()


def plotContainerRunNum(time_series, run_list, color_list, algoNameList):
    for i in range(len(run_list)):
        plt.plot(time_series, run_list[i], c='k', ls='--', marker='.', mfc='b', mec=color_list[i], mew=1,
                 label=algoNameList[i])
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s", fontweight='bold')
    plt.ylabel("Containers in Running State", fontweight='bold')
    plt.legend()
    plt.show()


def plotContainerIdleNum(time_series, spare_list, color_list, algoNameList):
    for i in range(len(spare_list)):
        plt.plot(time_series, spare_list[i], c='k', ls='-.', marker='.', mfc='b', mec=color_list[i], mew=1,
                 label=algoNameList[i])
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s", fontweight='bold')
    plt.ylabel("Containers in Idle State", fontweight='bold')
    plt.legend()
    plt.show()


def plotContainerDeadNum(time_series, kill_list, color_list, algoNameList):
    for i in range(len(kill_list)):
        plt.plot(time_series, kill_list[i], c='k', ls='--', marker='.', mfc='b', mec=color_list[i], mew=1,
                 label=algoNameList[i])
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s", fontweight='bold')
    plt.ylabel("Containers in Dead State", fontweight='bold')
    plt.legend()
    plt.show()


def plotPm(time_series, activePm_list, color_list, algoNameList):
    for i in range(len(activePm_list)):
        plt.plot(time_series, activePm_list[i], c='k', ls='-.', marker='.', mfc='b', mec=color_list[i], mew=1,
                 label=algoNameList[i])
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s", fontweight='bold')
    plt.ylabel("Active PMs", fontweight='bold')
    plt.legend()
    plt.show()


def plotColdStarts(time_series, cold_start_times_list, color_list, algoNameList):
    for i in range(len(cold_start_times_list)):
        plt.plot(time_series, cold_start_times_list[i], c='k', ls='-.', marker='.', mfc='b', mec=color_list[i], mew=1,
                 label=algoNameList[i])
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s", fontweight='bold')
    plt.ylabel("Cold Starts", fontweight='bold')
    plt.legend()
    plt.show()


def plotMigration(time_series, migration_list, color_list, algoNameList):
    for i in range(len(migration_list)):
        plt.plot(time_series, migration_list[i], c='k', ls='-.', marker='.', mfc='b', mec=color_list[i], mew=1,
                 label=algoNameList[i])
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s", fontweight='bold')
    plt.ylabel("Migrations", fontweight='bold')
    plt.legend()
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

    plotConsumeEnergy(time_series, energy_list, color_list, algoNameList)
    plotLatency(time_series, latency_list, color_list, algoNameList)
    plotRej(time_series, rej_list, color_list, algoNameList)
    plotColdStarts(time_series, cold_start_times_list, color_list, algoNameList)
    plotMigration(time_series, migration_list, color_list, algoNameList)
    plotCpu(time_series, u_cpu_list, color_list, algoNameList)
    plotMem(time_series, u_mem_list, color_list, algoNameList)
    plotMaxCurr(time_series, max_concur_list, color_list, algoNameList)
    plotContainerCSNum(time_series, cold_start_list, color_list, algoNameList)
    plotContainerIdleNum(time_series, spare_list, color_list, algoNameList)
    plotContainerDeadNum(time_series, kill_list, color_list, algoNameList)
    plotPm(time_series, activePm_list, color_list, algoNameList)
