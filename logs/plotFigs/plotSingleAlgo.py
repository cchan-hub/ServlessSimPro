from matplotlib import pyplot as plt
import json
from enumClass.enumClass import ReqAllocAlgo, ConPlaceAlgo, ConConsAlgo, PopQueueAlgo


# plot metrics over time figures for one algorithm

def plotConsumeEnergy(time_series, energy_list):
    plt.plot(time_series, energy_list, c='k', ls='-.', marker='.', mfc='b', mec='b', mew=1)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s")
    plt.ylabel("Energy Consumption/J")
    plt.show()


def plotLatency(time_series, latency_list):
    plt.plot(time_series, latency_list, c='k', ls='-.', marker='.', mfc='b', mec='g', mew=1)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s")
    plt.ylabel("Latency/s")
    plt.show()


def plotRej(time_series, rej_list):
    plt.plot(time_series, rej_list, c='k', ls='-.', marker='.', mfc='b', mec='r', mew=1)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s")
    plt.ylabel("Rejections")
    plt.show()


def plotCpuMem(time_series, u_cpu_list, u_mem_list):
    plt.plot(time_series, u_cpu_list, c='k', ls='-.', marker='.', mfc='b', mec='y', mew=1, label='CPU')
    plt.plot(time_series, u_mem_list, c='k', ls='--', marker='.', mfc='b', mec='g', mew=1, label='memory')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s")
    plt.ylabel("Resources Usage Rate")
    plt.legend()
    plt.show()


def plotMaxCurr(time_series, max_concur_list):
    plt.plot(time_series, max_concur_list, c='k', ls='-.', marker='.', mfc='b', mec='c', mew=1)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s")
    plt.ylabel("Maximum Concurrency")
    plt.show()


def plotContainerStateNum(time_series, cold_start_list, run_list, spare_list, kill_list):
    plt.plot(time_series, cold_start_list, c='k', ls='-.', marker='.', mfc='b', mec='y', mew=1, label='cold start')
    plt.plot(time_series, run_list, c='k', ls='--', marker='.', mfc='b', mec='g', mew=1, label='running')
    plt.plot(time_series, spare_list, c='k', ls='-.', marker='.', mfc='b', mec='r', mew=1, label='idle')
    # plt.plot(time_series, kill_list, c='k', ls='--', marker='.', mfc='b', mec='m', mew=1, label='dead')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s")
    plt.ylabel("Containers in Different States")
    plt.legend()
    plt.show()


def plotPm(time_series, activePm_list):
    plt.plot(time_series, activePm_list, c='k', ls='-.', marker='.', mfc='b', mec='m', mew=1)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s")
    plt.ylabel("Active PMs")
    plt.show()


def plotColdStarts(time_series, cold_start_times_list):
    plt.plot(time_series, cold_start_times_list, c='k', ls='-.', marker='.', mfc='b', mec='y', mew=1)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s")
    plt.ylabel("Cold Starts")
    plt.show()


def plotMigration(time_series, migration_list):
    plt.plot(time_series, migration_list, c='k', ls='-.', marker='.', mfc='b', mec='k', mew=1)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel("t/s")
    plt.ylabel("Migrations")
    plt.show()


if __name__ == "__main__":
    resolveName = ConPlaceAlgo.FIRST_FIT
    with open(str(resolveName)+'.json', mode='r') as file:
        time_series_data = json.load(file)
    time_series = time_series_data['time_series']
    energy_list = time_series_data['energy_list']
    latency_list = time_series_data['latency_list']
    rej_list = time_series_data['rej_list']
    cold_start_times_list = time_series_data['cold_start_times_list']
    u_cpu_list = time_series_data['u_cpu_list']
    u_mem_list = time_series_data['u_mem_list']
    max_concur_list = time_series_data['max_concur_list']
    cold_start_list = time_series_data['cold_start_list']
    run_list = time_series_data['run_list']
    spare_list = time_series_data['spare_list']
    kill_list = time_series_data['kill_list']
    activePm_list = time_series_data['activePm_list']
    migration_list = time_series_data['migration_list']

    plt.rcParams.update({'font.size': 12})

    plotConsumeEnergy(time_series, energy_list)
    plotLatency(time_series, latency_list)
    plotRej(time_series, rej_list)
    plotColdStarts(time_series, cold_start_times_list)
    plotMigration(time_series, migration_list)
    plotCpuMem(time_series, u_cpu_list, u_mem_list)
    plotMaxCurr(time_series, max_concur_list)
    plotContainerStateNum(time_series, cold_start_list, run_list, spare_list, kill_list)
    plotPm(time_series, activePm_list)
