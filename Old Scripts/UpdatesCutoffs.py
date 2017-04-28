import org.openlca.core.model.Exchange;
import csv

# Path to csv template containing inventory information
filePath = 'C:/Users/nstoddar/Data/replacmentdata.csv'

def updateCutoff(folder,proKey,flowKey,flowConversion,targetRefId):
    # Initial Conditions
    idX=[]
    flowId = []

    def checkCat(p):
      if p.getCategory().name == folder and p.name.find(proKey)>=0:
        idX.append(p.getId())
        return idX
      else:
        return idX

    def checkFlowRef(f):
        if f.refId == targetRefId:
            flowId.append(f.id)
            return flowId
        else:
            return flowId

    # Get list of target process ids
    olca.eachProcess(checkCat)
    olca.eachFlow(checkFlowRef)

    if len(flowId)==0 or len(flowId)>1:
        log.error("Replacement flow could not be found. Please check flow UUID: {}",targetRefId)

    if len(idX)<1:
      log.error("No replacement processes found for {}",proKey)

    newFlow = olca.getFlow(flowId[0])
    unit = newFlow.getReferenceFactor().getFlowProperty().getUnitGroup().getReferenceUnit()
    numUpdates = 0

    for id in idX:
      pro = olca.getProcess(id)
      exs = pro.getExchanges()
      oldFlow = None
      e = None
      flowFound = False

      for ex in exs:
        if ex.flow.name.find(flowKey)>=0:
          flowFound = True
          numUpdates += 1
          log.info("Updating Process:{} Flow:{}",pro.name,ex.flow.name)
          e = Exchange()
          e.setFlow(newFlow)
          e.amountValue = ex.amountValue * float(flowConversion)
          e.unit = unit
          e.baseUncertainty = ex.baseUncertainty
          e.input = ex.input
          oldFlow = ex
      if flowFound == True:
        log.info("Updated process with flow: {}",e.flow.name)
        pro.getExchanges().remove(oldFlow)
        pro.getExchanges().add(e)
        olca.updateProcess(pro)
    if numUpdates == 0:
      log.error("Could not find Flow with key:{} in any target processes.",flowKey)

rowObjs = []
with open(filePath, 'rb') as csvfile:
    linereader = csv.reader(csvfile, delimiter=',',quotechar='"')
    next(linereader)
    for row in linereader:
        folder = row[0].replace("\"","").strip()
        proKey = row[1].replace("\"","").strip()
        flowKey = row[2].replace("\"","").strip()
        conversion = row[3]
        refId = row[4].replace("\"","").strip()
        log.info("Evaluating row contents: {}",str(row))
        obj = {
            'folder':folder,
            'proKey':proKey,
            'flowKey':flowKey,
            'conversion':conversion,
            'refId': refId
        }
        rowObjs.append(obj)

log.info(rowObjs[0])
