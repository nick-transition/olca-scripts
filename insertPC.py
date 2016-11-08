import org.openlca.app.db.Cache as Cache
import org.openlca.core.model.ProcessType as ProcessType
import org.openlca.app.db.Database as Database
import org.openlca.core.matrix.LongPair as LongPair
import org.openlca.core.matrix.ProductSystemBuilder as ProductSystemBuilder
import csv

# Find category folder
category = olca.getCategory("Agriculture, forestry and fishing")
#subcat = category.getChildCategories().elementAt(0).name # log.info(elem.name) == Growing of rice
subcat = category.getChildCategories().elementAt(0).getChildCategories().elementAt(4).name
keyword = subcat
idX=[]

def checkCat(p):
  if p.getCategory().name == subcat:
    idX.append(p.getId())
    return idX
  else:
    return idX

# Get list of target process ids
olca.eachProcess(checkCat)

header =['ParentProcess-Location-ChildProcess']

rows = {}
i=0
for id in idX:
# update rice product system with a process
    proc = olca.getProcess(id)
    rName = proc.name
    rLoc  = proc.location.name
    rRef = proc.quantitativeReference
    rFlow = rRef.flow
    rUnit = rRef.unit
    rProp = rRef.getFlowPropertyFactor()
    log.info(rName)
    log.info(rLoc)

    sys = ProductSystem()
    sys.name = "temp"
    #product
    sys.referenceExchange = rRef
    #process
    sys.referenceProcess = proc
    #amount -> 1
    sys.targetAmount = 1
    #unit kg, ha, etc
    sys.targetUnit = rUnit
    #mass land area etc.
    sys.targetFlowPropertyFactor = rProp
    olca.insertSystem(sys)

    preferSystems = True
    builder = ProductSystemBuilder(Cache.getMatrixCache(), preferSystems)

    # Long1-proc id long2- rRef.id
    lp = LongPair(proc.id,rRef.id)
    sys = builder.autoComplete(sys,lp)
    sys = olca.updateSystem(sys)
    result = olca.analyze(sys,olca.getMethod("TRACI"))
    impacts = result.getImpactDescriptors()
    processes = result.getProcessDescriptors()
    for process in processes:
    	rowValue=[]
        for impact in impacts:
            iName = impact.name+" ("+impact.getReferenceUnit()+")"
            if i==0:
                header.append(iName) if iName not in header else None
            processContributions = result.getProcessContributions(impact)
            rowValue.append(str(processContributions.getContribution(process).amount))
    	rowId = rName+"-"+rLoc+"-"+process.name
    	rows[rowId] = rowValue
    i+=1
    olca.deleteSystem(sys)


f = open('C:/Users/nstoddar/Data/results_'+keyword+'.csv','wb')
writer = csv.writer(f)

writer.writerow(header)

for key in rows.keys():
    rowContents = [str(key)]
    for value in rows[key]:
        rowContents.append(value)
    #log.info(rowContents)
    writer.writerow(rowContents)

f.close()
