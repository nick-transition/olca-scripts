import csv


filePath = 'C:/Users/nstoddar/Data/template.csv'


def findId(folder, process, location):
  id = []
  def checkProc(p):
    if p.getCategory().name == folder and p.name == process and p.location.name==location:
      id.append(p.id)
      return id
  olca.eachProcess(checkProc)
  if len(id)==1:
    return id[0]
  elif len(id)>1:
    log.error("Whoops I found more than one {}{} to update in {}", process, location, folder)
    return
  else:
    log.error("Uh oh! I couldn't find {}{} anywhere in {}. Check your spelling and try again!",process,location,folder)
    return

def updateProcess(id,flow,amount):
  pro = olca.getProcess(id)
  exs = olce.getExchanges()

  for ex in exchanges:
    if ex.flow.name == flow:
      log.info("I am working :)")
      ex.amountValue = amount
  olca.updateProcess(pro)
  return


with open(filePath, 'rb') as csvfile:
    linereader = csv.reader(csvfile, delimiter=',',quotechar='"')
    next(linereader)
    for row in linereader:
        id = findId(row[0],row[1],row[4])
        log.info(str(id))
        updateProcess(id,row[2],row[3])
