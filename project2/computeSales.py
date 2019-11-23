import logging

logging.basicConfig(level=logging.DEBUG)

msg = "Give your preference: (1: read new input file, 2: print statistics for a specific product, 3: print statistics for a specific AFM, 4: exit the program)"


# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')




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
        pass
    elif choice ==2:
        pass
    elif choice ==3:
        pass
    else:
        logging.debug('Exiting')
        break