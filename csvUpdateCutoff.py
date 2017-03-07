import org.openlca.core.model.Exchange;
import csv

# Path to csv template containing inventory information
filePath = 'C:/Users/nstoddar/Data/template.csv'

def updateCutoff(folder,proKey,flowKey,flowConversion,targetRefId)
    # Initial Conditions
    idX=[]
    flowId = []

    def checkCat(p):
      if p.getCategory().name == folder and p.name.find(proKey)==0:
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

    newFlow = olca.getFlow(flowId[0])
    unit = newFlow.getReferenceFactor().getFlowProperty().getUnitGroup().getReferenceUnit()

    for id in idX:
      pro = olca.getProcess(id)
      exs = pro.getExchanges()

      for ex in exs:
        if ex.flow.name.find(flowKey)>=0:
          log.info("Process:{} Flow:{}",pro.name,ex.flow.name)
          e = Exchange()
          e.setFlow(flow)
          e.amountValue = ex.amountValue * flowConversion
          e.unit = unit
          e.baseUncertainty = ex.baseUncertainty
          e.input = ex.input

      log.info(e.flow.name)
      pro.getExchanges().add(e)
      olca.updateProcess(pro)

with open(filePath, 'rb') as csvfile:
    linereader = csv.reader(csvfile, delimiter=',',quotechar='"')
    next(linereader)
    for row in linereader:
        folder = row[0].replace("\"","").strip()
        proKey = row[1].replace("\"","").strip()
        flowKey = row[2].replace("\"","").strip()
        conversion = row[3].replace("\"","").strip()
        refId = row[4].replace("\"","").strip()
        updateCutoff(folder,proKey,flowKey,conversion,refId)
