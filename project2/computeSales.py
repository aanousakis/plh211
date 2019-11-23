import logging
import re
###################################

import resource
import os




#####################################

class PARSEError(Exception):
   pass

logging.basicConfig(level=logging.DEBUG)

msg = "Give your preference: (1: read new input file, 2: print statistics for a specific product, 3: print statistics for a specific AFM, 4: exit the program) "


# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')

# anoigoume to arxeio kai kaloume ti sunartisi readReceipt gia na diabasei mia mia tis apodeixeis
def readInputFile():
    logging.debug('Read new input file')

    #diabazoume to onoma tou arxeiou kai elegxoume an einai keno
    try:
        file_name = input("Enter filename : ")

        logging.debug('File Size is %s MB', os.stat(file_name).st_size / (1024 * 1024))

        with open(file_name,'r',encoding='utf8') as inputFile:
            for line in inputFile:
                # process the line

                pattern = '(^--*-$)'
                result = re.match(pattern, line)
                print(result)

                if result:  # an brike tin arxi mias apodeixis kalei ti readReceipt()
                    logging.debug('Receipt beginning found')
                    readReceipt(inputFile)
                else:       # an oxi, diabazei tin epomeni grammi mexri na ti brei
                    continue        



                print("zzz" + line)


    except EOFError:  # an uparxei kapoio problima me to onoma tou arxeiou
        logging.warning('EOFError while reading filename')
    except IOError as e:  # an uparxei kapoio problima me to anoigma tou arxeiou
        logging.warning('%s while reading input file', type(e))

# diabazei grammi grammi kai elegxei an exei ti sosti domi i apodeixi    
def readReceipt(inputFile):

    logging.debug('Parsing receipt')

    try:
        #parse AFM
        parseAfm(inputFile)

        #parse product
        parseProduct(inputFile)
    except PARSEError as e:
        logging.debug("%s", e)


    logging.debug('Receipt parsing finished')

def parseAfm(inputFile):
    line = inputFile.readline().upper()

    pattern = '^ΑΦΜ:\s*(\d{10})\s*$'
    result = re.match(pattern, line)

    if result: #elegxos an to afm exei ti sosti morfi
        afm = int(result.group(1))
        print ("AFM =[" + str(afm) + "]")
    else:
        raise PARSEError("Error in AFM declaration in line : " + line)

def parseProduct(inputFile):
    line = inputFile.readline().upper()

    while line:

        pattern = '(^.*):\s*(\d+)\s+(\d+|\d+\.\d+)\s+(\d+|\d+\.\d+)\s+$'
        result = re.match(pattern, line)

        if result: # elegxos an to proion exei ti  sosti morfi
            product  = result.group(1)
            quantity = int(result.group(2))
            price    = float(result.group(3))
            final    = float(result.group(4))

            print(result)
            logging.debug('Product:%s Quantity:%s Price:%s Final:%s', product, quantity, price, final)

            if final == quantity * price:
                pass
            else:
                logging.debug('Product numerical error. final != quantity * price in line %s', line)
    
        else:
            #elegxos an eftase to telos tis apodeixis
            pattern = '^ΣΥΝΟΛΟ\s*(\d+|\d+\.\d+)\s+$'
            result = re.match(pattern, line)

            if result:
                pass
            else:
                logging.debug('Product parsing error in line %s', line)

        line = inputFile.readline().upper()
    #while end





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


    logging.debug('Input = %s', choice)

    if choice == 1:
        readInputFile()
    elif choice ==2:
        pass
    elif choice ==3:
        pass
    else:
        logging.debug('Exiting')
        break





    print('Peak Memory Usage =', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print('User Mode Time =', resource.getrusage(resource.RUSAGE_SELF).ru_utime)
    print('System Mode Time =', resource.getrusage(resource.RUSAGE_SELF).ru_stime)