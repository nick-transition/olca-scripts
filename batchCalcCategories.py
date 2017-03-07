import org.openlca.core.matrix.ProductSystemBuilder as ProductSystemBuilder
import org.openlca.app.db.Cache as Cache
import org.openlca.core.model.ProcessType as ProcessType
import org.openlca.app.db.Database as Database
import org.openlca.core.matrix.LongPair as LongPair
import csv

def runBatch(fname,subcat,category)
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
        log.info(str(id))
        replacement = olca.getProcess(id)
        rName = replacement.name
        rLoc  = replacement.location.name
        rRef = replacement.quantitativeReference
        rFlow = rRef.flow
        rUnit = rRef.unit
        rProp = rRef.getFlowPropertyFactor()

        sys = ProductSystem()
        sys.name = "temp"
        #product
        sys.referenceExchange = rRef
        #process
        sys.referenceProcess = replacement
        #amount -> 1
        sys.targetAmount = 1
        #unit kg, ha, etc
        sys.targetUnit = rUnit
        #mass land area etc.
        sys.targetFlowPropertyFactor = rProp


        preferSystems = True
        builder = ProductSystemBuilder(Cache.getMatrixCache(), preferSystems);
        for prc in sys.getProcesses():
          longPair = LongPair(prc.id,prc.getQuantitativeReference())
          sysBuild = builder.autoComplete(sys,rRef)

        olca.insertSystem(sys)
        Database.get().notifyUpdate(sys)
        system = olca.getSystem("temp")

        system.setReferenceProcess(replacement)
        system.setReferenceExchange(rRef)
        system.setTargetUnit(rUnit)
        system.setTargetFlowPropertyFactor(rProp)
        system.getProcesses().add(id)

        #log.info(system.referenceProcess.name)
        #log.info("Amount:{}, Units:{}, Process:{}, Property:{}",
        #         system.targetAmount,system.targetUnit,
        #         system.referenceExchange,system.getTargetFlowPropertyFactor().getFlowProperty().name)

        # Run calculation on the system
        result = olca.analyze(system,olca.getMethod("TRACI"))
        impacts = result.getImpactDescriptors()
        processes = result.getProcessDescriptors()
        for process in processes:
            rowValue=[]
            for impact in impacts:
                iName = impact.name+" ("+impact.getReferenceUnit()+")"
                if i==0:
                    header.append(iName) if iName not in header else None
                processContributions = result.getProcessContributions(impact)
                #rowValue.append(str(process.quantitativeReference.unit))
                rowValue.append(str(processContributions.getContribution(process).amount))
            rowId = rName+"-"+rLoc+"-"+process.name
            rows[rowId] = rowValue
        i+=1
        olca.deleteSystem(system)


    f = open('C:/Users/nstoddar/Data/results_'+fname+'.csv','wb')
    writer = csv.writer(f)

    writer.writerow(header)

    for key in rows.keys():
        rowContents = [str(key)]
        for value in rows[key]:
            rowContents.append(value)
        #log.info(rowContents)
        writer.writerow(rowContents)

    f.close()
    return

# Find category folder
batches = ["Establishing a crop","Fertilizer application","Harvesting",
"Operation of agricultural irrigation equipment","Pest control",
"Provision of agricultural machinery","Soil amendment"]

for batch in batches:
    fname = batch.replace(" ","")
    log.info(fname)
