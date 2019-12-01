import logging
import re
###################################

import resource
import os
import sys
import time
import timeit

import numpy as np





#####################################

#an uparxei kapoio sfalma sta dedomena tou arxeiou
class PARSEError(Exception):
   pass

#otan ftasei sto telos tou arxeiou
class EOF(Exception):
   pass

class list_item:
    def __init__(self, productName, total):
        self.productName = productName
        self.total   = total

#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

msg = "Give your preference: (1: read new input file, 2: print statistics for a specific product, 3: print statistics for a specific AFM, 4: exit the program) "
Dict = { }

epsilon= np.finfo(float).eps

# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')

def searchForReceiptStart(inputFile):
    for line in inputFile:
        #pattern = '^-+\s*$'
        #result = re.match(pattern, line)


        if line == ('-' * (len(line) -1 ) + '\n'):  # an brike tin arxi tis apodeixis termatizei
            #logging.debug('Receipt beginning found')
            return
        else: # an oxi, diabazei tin epomeni grammi mexri na ti brei
            logging.debug('Ignoring line : %s', line)
            continue
    logging.debug("Receipt beginning not found") 
    raise EOF("Reached end of file")

# gia kathe proion prosthetei sto lexiko to afm kai to sunolo tou proiontos
# an to proion uparxei idi kai uparxei to idio afm tote auxanei to sunolo tou
def saveData(afm, productList, total):
    logging.debug("Saving data")

    for product in productList:

        #an den uparxei to proion tote i get epistrefei -1
        #an den uparxei to afm    tote i get epistrefei  0
        if not product.productName in Dict:    #an den uparxei auto to proion sto lexiko
            Dict[product.productName] = {}
            Dict[product.productName][afm] = product.total
        else:
            Dict[product.productName][afm] = Dict.get(product.productName).get(afm, 0) + product.total


    


# anoigoume to arxeio kai kaloume ti sunartisi readReceipt gia na diabasei mia mia tis apodeixeis
def readInputFile():
    logging.debug('Read new input file')

    #diabazoume to onoma tou arxeiou kai elegxoume an einai keno
    try:
        file_name = input("Enter filename : ")

        with open(file_name,'r',encoding='utf8') as inputFile:
            logging.debug('File Size is %s MB', os.stat(file_name).st_size / (1024 * 1024))
            
            #psaxnoume na broume tin arxi tis protis apodeixis
            searchForReceiptStart(inputFile)     

            while True:
                try:
                    afm, productList, total = readReceipt(inputFile)
                except PARSEError as e:
                    logging.debug("Invalid receipt")
                else:# an i apodeixi einai sosti apothikeuoyme ta dedomena tis
                    logging.debug("Valid receipt")
                    saveData(afm, productList, total)
                finally:
                    pass
    except EOFError:  # an uparxei kapoio problima me to onoma tou arxeiou (an einai keno)
        logging.warning('EOFError while reading filename')
    except IOError as e:  # an uparxei kapoio problima me to anoigma tou arxeiou
        logging.warning('%s while reading input file', type(e))
    except EOF as e:  # an ftasouse sto telos tou arxeiou kai den broume auto pou psaxnoume
        logging.debug("%s", e)

# diabazei grammi grammi kai elegxei an exei ti sosti domi i apodeixi    
def readReceipt(inputFile):

    logging.debug('Receipt parsing started')

    try:
        #parse AFM
        afm = parseAfm(inputFile)

        #parse product kai to sunolo
        productList, total = parseProduct(inputFile)

        #parse delimiter "------"
        parseDelimiter(inputFile)

    except PARSEError as e:
        logging.debug("%s", e)

        searchForReceiptStart(inputFile) #otan broume ena sfalma, diabazoume mexri na broume tin arxi tis epomenis apodeixis
        raise PARSEError("Receipt parsing failed")
        
    else: #an den uparxei kapoio sfalma
        logging.debug('Receipt parsing finished')
        return afm, productList, total

def parseAfm(inputFile):
    line = inputFile.readline().upper()

    if not line:     
        raise EOF("Reached end of file")

    pattern = '^ΑΦΜ:\s*(\d{10})\s*$'
    result = re.match(pattern, line)

    if result: #elegxos an to afm exei ti sosti morfi
        try:
            afm = int(result.group(1))
        except ValueError:
            raise PARSEError("Error in AFM declaration in line : " + line)
        else:
            logging.debug("AFM =[%s]", str(afm))
        return afm
    else:
        raise PARSEError("Error in AFM declaration in line : " + line)

def parseProduct(inputFile):

    line = inputFile.readline().upper()
    productsNum = 0
    productList = []
    products_total = 0

    if not line:
        raise PARSEError("Product parsing error in line : " + line)

    while line:
        pattern = '(^.*):\s*(\d+)\s+(\d+|\d+\.\d+)\s+(\d+|\d+\.\d+)\s+$'
        result = re.match(pattern, line)

        if result: # elegxos an to proion exei ti  sosti morfi

            try :
                product_name  = result.group(1)
                quantity      = int(result.group(2))
                price         = float(result.group(3))
                total         = float(result.group(4))
            except ValueError:# an uparxei kapoio sfalma stin metatropi apo string se aritmous
                raise PARSEError("Product parsing error in line : " + line) 

            logging.debug('Product:%s Quantity:%s Price:%s Final:%s', product_name, quantity, price, total)

            if total == quantity * price: # an to proion einai sosto
                productsNum += 1
                products_total += total

                #prosthiki sti lista
                new_product = list_item(product_name, total)
                productList.append(new_product)
            else:
                logging.debug('Product numerical error. total != quantity * price in line %s', line)
    
        else:   # an den einai sosto proion
            #elegxos an eftase sto SUNOLO
            pattern = '^ΣΥΝΟΛΟ:\s*(\d+|\d+\.\d+)\s*$'
            result = re.match(pattern, line)
            

            if result:  #an eftase sto sunolo
                try:
                    total = float(result.group(1))
                except ValueError:
                    raise PARSEError("Total parsing error in line : " + line)
                
                logging.debug('Total : [%s]', total)

                if (productsNum > 0) and isEqual(products_total, total): # an exei toulaxiston ena proion kai to sunolo einai sosto
                    logging.info("Parsed %d correct products, products total %f", productsNum, products_total)  
                    return productList, total # an ftasei edo tote i apodeixi einai sosti kai i sunartisi epistrefei
                else:
                    raise PARSEError("Total numerical error in line : " + line)
            
            #elegxos an eftase sto telos tis apodeixis "---"
            #pattern = '^-+\s*$'
            #result = re.match(pattern, line)
            
            if line == ('-' * (len(line) -1 ) + '\n'):  # an ftasei edo tote yparxei kapoio sfalma, leipei to sunolo
                raise PARSEError("Error Total is missing in line : " + line)
                
            #an ftasei edo, tote einai lanthasmeno proion
            raise PARSEError("Product parsing error in line : " + line)

        line = inputFile.readline().upper()
    #while end

def isEqual(x, y):
    if abs(x - y) > max(abs(x), abs(y))* epsilon:
        return False
    else:
        return True

def parseDelimiter(inputFile):
    line = inputFile.readline().upper()

    pattern = '^-+\s*$'
    result = re.match(pattern, line)

    if result: 
        pass
    else:
        raise PARSEError("Error. Expected delimiter in line : " + line)
#@profile
def productStats():
    logging.debug("Printing product Statistics")

    try:
        productName = input("Enter product name : ")
    except EOFError:
        logging.debug("Empty product name")
    else:
        print(Dict[productName])
    


#main
#****************************************************************************
if __name__ == '__main__':

    while True:
        
        # diabazoume tin epilogi tou xristi kai elegxoume oti exei sosti timi
        try:
            choice = int( input(msg))
            if (choice < 0) or (choice > 4):
                raise ValueError

        except EOFError as e: #an o xristis den epilexei tpt
            logging.warning('EOFError exception')
            continue
        except ValueError as e: #an o xristis den epilexei akaireo
            logging.warning('ValueError exception')
            continue
        else:
            logging.debug('Input = %s', choice)

            if choice == 1:
                readInputFile()
            elif choice ==2:
                productStats()
            elif choice ==3:
                pass
            else:
                logging.debug('Exiting')
                break
        
        """ 
        start_time = timeit.default_timer()
        logging.info("Executed in %s seconds.", timeit.default_timer() - start_time) """

    kilobytes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss # peak memory usage (bytes on OS X, kilobytes on Linux)
    megabytes = kilobytes / 1024

    logging.info("Max memory usage : %s MB", megabytes)