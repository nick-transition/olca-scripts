import csv

# Path to csv template containing inventory information
filePath = 'C:/Users/nstoddar/Data/template.csv'

#Finds process to be updated
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

# updates discovered process
def updateProcess(id,flow,amount,description):
  pro = olca.getProcess(id)
  exs = pro.getExchanges()



  for ex in exs:
    if ex.flow.name == flow and ex.flow.desciption == description:
      ex.amountValue = float(amount)
      olca.updateProcess(pro)
      log.info("{}'s flow — {} — has been updated",pro.name,flow)
    else:
      log.error("{} flow not found in {}.",flow,pro.name)
  return


with open(filePath, 'rb') as csvfile:
    linereader = csv.reader(csvfile, delimiter=',',quotechar='"')
    next(linereader)
    for row in linereader:
        folder = row[0].replace("\"","").strip()
        process = row[1].replace("\"","").strip()
        flow = row[2].replace("\"","").strip()
        amount = row[3].replace("\"","").strip()
        location = row[4].replace("\"","").strip()
        description = row[5].replace("\"","").strip()
        id = findId(folder,process,location)
        updateProcess(id,flow,amount,description)
