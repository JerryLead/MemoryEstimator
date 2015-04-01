__author__ = 'xulijie'

class Group:

    def __init__(self, gid):
        self.gid = gid
        self.totalRecords = 0L
        self.preRecordsUsageList = []
        self.ingRecordsUsageList = []


    def addPreRecordUsage(self, record, total, used):
        self.preRecordsUsageList.append((record, total, used))

    def addIngRecordUsage(self, record, total, used, gcCount):
        self.ingRecordsUsageList.append((record, total, used, gcCount))

    def setTotalRecords(self):
        if(len(self.preRecordsUsageList) > 0):
            self.totalRecords = self.preRecordsUsageList[-1][0]

class ReduceMemoryLogParser:

    def __init__(self):
        self.groupList = []
        self.currentGroup = Group(0)

    def process(self, line):

        if line.startswith("group"):
            items = line.strip('\n').split(", ")
            group = long(items[0][items[0].find('=') + 2:])
            record = long(items[1][items[1].find('=') + 2:])
            total = long(items[2][items[2].find('=') + 2:])

            # group = 1, record = 1, total = 125952, used = 2310
            if len(items) == 4:
                preUsed = long(items[3][items[3].find('=') + 2:])

                if(group == self.currentGroup.gid):
                    self.currentGroup.addPreRecordUsage(record, total, preUsed)
                else:
                    self.currentGroup.setTotalRecords()
                    self.currentGroup = Group(group)
                    self.currentGroup.addPreRecordUsage(record, total, preUsed)
                    self.groupList.append(self.currentGroup)


            # group = 1, record = 1, total = 125952, used = 44622, gcCount = 1
            else:
                ingUsed = long(items[3][items[3].find('=') + 2:])
                gcCount = int(items[4][items[4].find('=') + 2:])

                assert(self.currentGroup.gid >= group)

                for g in reversed(self.groupList):
                    if(g.gid == group):
                        g.addIngRecordUsage(record, total, ingUsed, gcCount)
                        break


    def parseLog(self, filename):
        f = open(filename, 'r')
        while True:
            line = f.readline()
            if not line:
                break
            self.process(line)
        f.close()
        return self.groupList











