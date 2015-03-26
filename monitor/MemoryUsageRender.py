import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import MapMemoryLogParser as mapParser
import ReduceMemoryLogParser as reduceParser


def initFigure():
    rc('mathtext', default='regular')

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.grid()
    ax.set_xlabel("Record")
    ax.set_ylabel(r"Memory Usage (KB)")
    #ax2 = ax.twinx()
    #ax2.set_ylabel(r"GC count")

    return ax

def plotPreRecords(ax, preRecordUsageList):
    records = []
    totals = []
    preUseds = []

    for t in preRecordUsageList:
        records.append(t[0])
        totals.append(t[1])
        preUseds.append(t[2])

    ax.plot(records, preUseds, "-bo", label=r'preRecords')


def plotIngRecords(ax, ingRecordUsageList):
    records = []
    totals = []
    ingUseds = []
    gcCounts = []

    for t in ingRecordUsageList:
        records.append(t[0])
        totals.append(t[1])
        ingUseds.append(t[2])
        gcCounts.append(t[3])


    ax.plot(records, ingUseds, "-ro", label=r'ingRecords')
    # ax.plot(records, totals, "-go", label=r'total')
    # ax2.plot(records, gcCounts, '-', label='gcCount', color='cyan')

def show(ax):
    ax.legend(loc=0)
    # axs[1].legend(loc=1)
    plt.grid(False)
    plt.show()

def plotFirstRecordInEachGroup(ax, firstRecords):
    for r in firstRecords:
        plt.axvline(x=r, color='lightgray')


def plotGroupList(axs, groupList):
    preRecords = []
    ingRecords = []

    firstRecords = []

    recordsInPreGroup = 0L

    for group in groupList:
        for pr in group.preRecordsUsageList:
            preRecords.append((pr[0] + recordsInPreGroup, pr[1], pr[2]))
        firstRecords.append(group.preRecordsUsageList[0][0] + recordsInPreGroup)

        for ir in group.ingRecordsUsageList:
            ingRecords.append((ir[0] + recordsInPreGroup, ir[1], ir[2], ir[3]))
        recordsInPreGroup += group.totalRecords

    plotPreRecords(ax, preRecords)
    #print(preRecords)
    plotIngRecords(ax, ingRecords)
    #print(ingRecords)
    plotFirstRecordInEachGroup(ax, firstRecords)


filename = '/Users/xulijie/Documents/Research/MemoryEstimator/logs/InMemWordCount/mapmemUsage.txt'
isMapLog = True


#filename = '/Users/xulijie/Documents/Research/MemoryEstimator/logs/ReduceJoin/memoryusage3.txt'
#isMapLog = False

ax = initFigure()

if(isMapLog):
    parser = mapParser.MapMemoryLogParser()
    mapRecordList = parser.parseLog(filename)

    plotPreRecords(ax, mapRecordList.preRecordUsageList)
    plotIngRecords(ax, mapRecordList.ingRecordUsageList)

else:
    parser = reduceParser.ReduceMemoryLogParser()
    groupList = parser.parseLog(filename)
    plotGroupList(ax, groupList)
    
show(ax)


#ax2.set_ylim(0, 35)
#ax.set_ylim(-20,100)
