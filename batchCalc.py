system = olca.getSystem("rice")



reference = system.getReferenceProcess()
location = reference.getLocation()
category = olca.getCategory("Agriculture, forestry and fishing")
subcat = category.getChildCategories().elementAt(2).name # log.info(elem.name) == Growing of rice

idX=[]

def checkCat(p):
  if p.getCategory().name == subcat:
    idX.append(p.getName())
    return idX
  else:
    return idX

#olca.inspect(olca)
# Get list of target process ids
olca.eachProcess(checkCat)



for name in idX:
  log.info(name)
