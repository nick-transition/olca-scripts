import org.openlca.core.results.ContributionResultProvider as rp
import org.openlca.core.results.Contributions as contributions
import csv

# Find category folder
category = olca.getCategory("Agriculture, forestry and fishing")
subcat = category.getChildCategories().elementAt(0).name # log.info(elem.name) == Growing of rice
keyword = "operation of Bed-Paratill"
sysName = "Operation"
idX=[]

def checkCat(p):
  if p.getCategory().name == subcat and p.name.find(keyword)==0:
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
    replacement = olca.getProcess(id)
    rName = replacement.name
    rLoc = replacement.location.name
    olca.getSystem(sysName).setReferenceProcess(replacement)

    # Run calculation on the system
    result = olca.analyze(olca.getSystem(sysName),olca.getMethod("TRACI"))
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


f = open('C:/Users/nstoddar/Desktop/results_'+keyword+'.csv','wb')
writer = csv.writer(f)

writer.writerow(header)

for key in rows.keys():
    rowContents = [str(key)]
    for value in rows[key]:
        rowContents.append(value)
    #log.info(rowContents)
    writer.writerow(rowContents)

f.close()
