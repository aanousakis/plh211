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
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.CRITICAL)

msg = "Give your preference: (1: read new input file, 2: print statistics for a specific product, 3: print statistics for a specific AFM, 4: exit the program) "
productDict = { }
afmDict     = { }

epsilon= np.finfo(float).eps

# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')

def searchForReceiptStart(inputFile):
    for line in inputFile:
        pattern = '^-+$'
        result = re.match(pattern, line)


        if result:  # an brike tin arxi tis apodeixis termatizei
            logging.debug('Receipt beginning found')
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

    if  not afm in afmDict.keys():
        afmDict[afm] = {}

    for product_name, product_total in productList.items() :
        if not product_name in productDict.keys():    #an den uparxei auto to proion sto lexiko
            productDict[product_name] = {}
            productDict[product_name][afm] = product_total
        else:
            #an den uparxei to afm    tote i get epistrefei  0
            productDict[product_name][afm] = productDict.get(product_name).get(afm, 0) + product_total

        afmDict[afm][product_name] = afmDict.get(afm).get(product_name, 0) + product_total




def insertData(product_name, afm, total):
    pass


# anoigoume to arxeio kai kaloume ti sunartisi readReceipt gia na diabasei mia mia tis apodeixeis
def readInputFile():
    logging.debug('Read new input file')

    receiptsNum =0
    error = 0

    #diabazoume to onoma tou arxeiou kai elegxoume an einai keno
    try:
        file_name = input("Enter filename : ")

        start_time = timeit.default_timer()

        with open(file_name,'r',encoding='utf8') as inputFile:
            logging.debug('File Size is %s MB', os.stat(file_name).st_size / (1024 * 1024))
            
            #psaxnoume na broume tin arxi tis protis apodeixis
            searchForReceiptStart(inputFile)     

            while True:
                try:
                    afm, productList, total = readReceipt(inputFile)
                except PARSEError as e:
                    logging.debug("Invalid receipt")
                    error +=1
                else:# an i apodeixi einai sosti apothikeuoyme ta dedomena tis
                    receiptsNum += 1
                    logging.debug("Valid receipt")
                    saveData(afm, productList, total)
                finally:
                    pass
    except EOFError:  # an uparxei kapoio problima me to onoma tou arxeiou (an einai keno)
        logging.warning('EOFError while reading filename')
    except IOError as e:  # an uparxei kapoio problima me to anoigma tou arxeiou
        logging.warning('%s while reading input file', type(e))
    except EOF as e:  # an ftasouse sto telos tou arxeiou   termatizei to loop
        logging.debug("%s", e)
        logging.info("Parsed %d correct and %d incorrect receipts", receiptsNum, error)
        logging.info("Executed in %s seconds.", timeit.default_timer() - start_time)

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
    productList = {}  
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

            if isEqual(total, quantity * price) and (quantity > 0) and (total > 0) :# an to proion einai sosto
                productsNum += 1
                products_total += total

                if product_name in productList.keys(): # an uparxei to proion, enimerose tin timi tou
                    productList[product_name] += total
                else:# an den uparxei prosthese to proion sto lexiko
                    productList[product_name] = total
            else:
                logging.debug('Product numerical error. total != quantity * price in line %s', line)
                raise PARSEError('Product numerical error. total != quantity * price in line %s', line)
    
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

                if (productsNum > 0) and (total > 0) and isEqual(products_total, total): # an exei toulaxiston ena proion kai to sunolo einai sosto
                    logging.info("Parsed %d correct products, products total %f", productsNum, products_total)  
                    return productList, total # an ftasei edo tote i apodeixi einai sosti kai i sunartisi epistrefei
                else:
                    raise PARSEError("Numerical error or zero products in line : " + line)
            
            #elegxos an eftase sto telos tis apodeixis "---"
            pattern = '^-+$'
            result = re.match(pattern, line)
            
            if result:  # an ftasei edo tote yparxei kapoio sfalma, leipei to sunolo
                raise PARSEError("Error Total is missing in line : " + line)
                
            #an ftasei edo, tote einai lanthasmeno proion
            raise PARSEError("Product parsing error in line : " + line)

        line = inputFile.readline().upper()
    #while end

# sugkrinei duo float arithmous gia isotita
def isEqual(x, y):
    #if abs(x - y) > max(abs(x), abs(y))* epsilon:
    error = 0.00001 

    if abs(x - y) > max(abs(x), abs(y)) * error:
        logging.info("x = %f y = %f", x, y)
        return False
    else:
        return True

def parseDelimiter(inputFile):
    line = inputFile.readline().upper()

    pattern = '^-+$'
    result = re.match(pattern, line)

    if result: 
        pass
    else:
        raise PARSEError("Error. Expected delimiter in line : " + line)
#@profile
def productStats():
    logging.debug("Printing product Statistics")

    try:
        productName = input("Enter product name : ").upper()
    except EOFError:
        logging.debug("Empty product name")
    else:
        if productName in productDict:# an to proion uparxei sto lexiko
            for element in sorted(productDict[productName].items()):#taxinomoume ta kleidia tou lexikou kai emfanizoume tis times tous
                 #print(element[0], element[1] )

                 print("{:010d}".format(element[0]), "{:.2f}".format(element[1]))

def salesStats():
    logging.debug("Printing sales Statistics")

    try:
        afm = int(input("Enter afm : "))
    except EOFError:
        logging.debug("Empty product name")
    except ValueError:
        logging.debug("Value error")
    else:
        if afm in afmDict.keys():
            for element in sorted(afmDict[afm].items()):
                print(element[0], "{:.2f}".format(element[1]))


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
                salesStats()
            else:
                logging.debug('Exiting')
                break

    kilobytes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss # peak memory usage (bytes on OS X, kilobytes on Linux)
    megabytes = kilobytes / 1024

    logging.info("Max memory usage : %s MB", megabytes)