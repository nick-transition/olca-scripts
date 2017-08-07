import csv
from org.openlca.core.database import ProcessDao

processDao = ProcessDao(db)

# Match process on UUID for unique result
filePath = 'C:/Users/nstoddar/Data/proUpdate.csv'

def readRow(row):
    parentCat= row[0].replace("\"","").strip()
    proKey = row[1].replace("\"","").strip()
    newProName = row[2].replace("\"","").strip()
    newProDescription = row[3].replace("\"","").strip()

    rowObj = {
        'pCat': parentCat,
        'pKey':proKey,
        'newPName':newProName,
        'newPDesc':newProDescription
    }

    return rowObj


def getProcesses(parentCat,proKey):

    proList = []

    def checkCat(p):
      if p.getCategory().name == parentCat and p.name.find(proKey) >= 0:
        proList.append(p.getId())
        return proList
      else:
        return proList

    # Get list of target process ids
    olca.eachProcess(checkCat)

    return proList

# Read input csv
def main():
    with open(filePath, 'rb') as csvfile:
        linereader = csv.reader(csvfile, delimiter=',',quotechar='"')
        next(linereader)
        for row in linereader:
            rowObj = readRow(row)
            processIds = getProcesses(rowObj['pCat'],rowObj['pKey'])
            for id in processIds:
                pro = processDao.getProcess(id)
                pro.name = rowObj['newPName']
                pro.description = rowObj['newPDesc']
                olca.updateProcess(pro)
main()
