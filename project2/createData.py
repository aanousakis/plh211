import random

random_products = 20
random_afm_cnt = 1000
receipt_cnt = 1000000

product = ['ΤΖΑΤΖΙΚΙ', 'ΜΠΡΙΖΟΛΑ ΜΟΣΧΑΡΙΣΙΑ', 'AMSTEL', 'ΠΟΙΚΙΛΙΑ']

randomAfmList = [random.randrange(random_afm_cnt) for i in range(random_afm_cnt)] 

for i in range(receipt_cnt):
    print("---------------------")
    print('ΑΦΜ:  ' + '{0:010d}'.format(randomAfmList[random.randrange(random_afm_cnt)]))

    # make random_products
    for j in range(random.randrange(random_products)):

        quantity = random.randrange(10)
        value    = random.randrange(10)
        total    = quantity * value

        print(product[random.randrange(len(product))] + ":  " + str(quantity) + "  " + str(value) + "  " + str(total))

        print("ΣΥΝΟΛΟ:   888")


print("---------------------")