__author__ = 'xulijie'

class MapRecordList:
    def __init__(self):
        self.preRecordUsageList = []
        self.ingRecordUsageList = []

class MapMemoryLogParser:



    def __init__(self, bufferSize):
        self.mapBufferKB = bufferSize * 1024
        self.mapRecordList = MapRecordList()

    def process(self, line):
        # process map log
        if line.startswith("record"):
            items = line.strip('\n').split(", ")
            record = long(items[0][items[0].find('=') + 2:])
            total = long(items[1][items[1].find('=') + 2:]) - self.mapBufferKB

            # record = 600001, total = 168448, used = 106592
            if len(items) == 3:
                preUsed = long(items[2][items[2].find('=') + 2:]) - self.mapBufferKB
                self.mapRecordList.preRecordUsageList.append((record, total, preUsed))

            # record = 600001, total = 168448, used = 106592, gcCount = 65
            else:
                ingUsed = long(items[2][items[2].find('=') + 2:]) - self.mapBufferKB
                gcCount = int(items[3][items[3].find('=') + 2:])
                self.mapRecordList.ingRecordUsageList.append((record, total, ingUsed, gcCount))

    def parseLog(self, filename):
        f = open(filename, 'r')
        while True:
            line = f.readline()
            if not line:
                break
            self.process(line)
        f.close()

        return self.mapRecordList




