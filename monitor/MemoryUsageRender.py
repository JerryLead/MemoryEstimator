import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import MonitorLogParser


def initFigure():
    rc('mathtext', default='regular')

    fig = plt.figure()
    ax = fig.add_subplot(111)


    ax.grid()
    ax.set_xlabel("Record")
    ax.set_ylabel(r"Memory Usage (KB)")
    ax2 = ax.twinx()
    ax2.set_ylabel(r"GC count")


    return (ax, ax2)

def plotPreRecords(ax):
    records = []
    totals = []
    preUseds = []

    for t in mapPreRecordUsageList:
        records.append(t[0])
        totals.append(t[1])
        preUseds.append(t[2])

    ax.plot(records, preUseds, "-bo", label=r'preRecords')


def plotIngRecords(ax, ax2):
    records = []
    totals = []
    ingUseds = []
    gcCounts = []

    for t in mapIngRecordUsageList:
        records.append(t[0])
        totals.append(t[1])
        ingUseds.append(t[2])
        gcCounts.append(t[3])


    ax.plot(records, ingUseds, "-ro", label=r'ingRecords')
    # ax.plot(records, totals, "-go", label=r'total')

    ax2.plot(records, gcCounts, '-r', label='gcCount', color='cyan')

def show(axs):
    axs[0].legend(loc=0)
    axs[1].legend(loc=1)
    plt.show()



filename = '/Users/xulijie/Documents/Research/MemoryEstimator/logs/InMemWordCount/mapmemUsage.txt'
parser = MonitorLogParser.MonitorLogParser()
recordLists = parser.readLog(filename)


# (record, total, preUsed)
mapPreRecordUsageList = recordLists[0]
# (record, total, ingUsed, gcCount)
mapIngRecordUsageList = recordLists[1]


axs = initFigure()
plotPreRecords(axs[0])
plotIngRecords(axs[0], axs[1])
show(axs)
#ax2.set_ylim(0, 35)
#ax.set_ylim(-20,100)
