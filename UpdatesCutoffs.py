category = olca.getCategory("Agriculture, forestry and fishing")

subcat = category.getChildCategories().elementAt(0).name

# Find category folder
category = olca.getCategory("Agriculture, forestry and fishing")
subcat = category.getChildCategories().elementAt(0).name # log.info(elem.name) == Growing of rice
keyword = "work"

idX=[]

def checkCat(p):
  if p.getCategory().name == subcat and p.name.find(keyword)==0:
    idX.append(p.getId())
    return idX
  else:
    return idX

# Get list of target process ids
olca.eachProcess(checkCat)

for id in idX:
  pro = olca.getProcess(id)
  exs = pro.getExchanges()
  for ex in exs:
    if ex.flow.name.find("diesel")>=0 and ex.flow.name.find("CUTOFF")>=0:
      log.info("Process:{} Flow:{}",pro.name,ex.flow.name)
