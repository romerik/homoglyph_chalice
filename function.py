from unittest import result
import dnstwist
import os
import homoglyphs as hg
import json
import dask
import sys

original_stdout = sys.stdout

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

    result = all_result.compute()

    to_write = {f"{domain}_homoglyphs": result}
    with open(f"{domain}_homoglyphs.txt", "a+") as file:
        sys.stdout = file
        for i in result:
            print(i)
        sys.stdout = original_stdout

    return result
