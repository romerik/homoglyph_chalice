import dnstwist
import os
import homoglyphs as hg
import json
import dask


def genTldsDnstwist(domain):
    """Generate a file and upload to S3 with dnstwist 
        :param domain: list of domain
        :param organisation_name: organisation name
    """
    return dnstwist.run(domain=f"{domain}", registered=True, format='null')

def homoglyphForOneCategory(category, domain):
    homo = hg.Homoglyphs(categories=(category,)).get_combinations(domain)
    list_homoglyphs = []
    for element in homo:
        list_homoglyphs.append(str(element))
    return list_homoglyphs

def getAll(homoList):
    mylist = []
    for i in homoList:
        mylist.extend(i)
    return mylist

def homoglyphGenerator(domain):
    allCategory = ['ARMENIAN', 'BUGINESE', 'CARIAN', 'CHEROKEE', 'CYRILLIC', 'GREEK', 'LATIN']
    #homoglyphs = hg.Homoglyphs(categories=('ARMENIAN', 'BUGINESE', 'CARIAN', 'CHEROKEE', 'CYRILLIC', 'GREEK', 'LATIN')).get_combinations(domain)
    list_homoglyphs = []
    for category in allCategory:
        list_homoglyphs.append(dask.delayed(homoglyphForOneCategory)(category, domain))
    
    all_result = dask.delayed(getAll)(list_homoglyphs)

    return all_result.compute()




