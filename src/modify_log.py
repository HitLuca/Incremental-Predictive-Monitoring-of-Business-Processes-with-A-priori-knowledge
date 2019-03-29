import csv
import time
from datetime import datetime, timedelta
from random import *

class ModifyLog:

    log_name = '50x5_3W'
    difflist = []
    timestamps_list = []

    csvfile = open('../data/final_experiments/%s.csv' % log_name, 'r')
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(spamreader, None)  # skip the headers

    for row in spamreader:
        # x = randint(1, 3)
        # #print(x)
        if row[1] == '0':
            tdiff = 0
        #if row[1] == '1':
           #tdiff = 5 * 3
        # if row[1] == '2':
        #     tdiff = 10 * x
        # if row[1] == '3':
        #     tdiff = 25 * x
        # if row[1] == '4':
        #     tdiff = 12 * x
        # if row[1] == '5':
        #     tdiff = 8 * x
        # if row[1] == '6':
        #     tdiff = 30 * x
        # if row[1] == '7':
        #     tdiff = 40 * x
        # if row[1] == '8':
        #     tdiff = 20 * x
        # if row[1] == '9':
        #     tdiff = 3 * x

        # if row[1] == '1' and row[3] == '0':
        #     tdiff = 25
        # if row[1] == '1' and row[3] == '1':
        #     tdiff = randint(40,60)
        # if row[1] == '1' and row[3] == '2':
        #     tdiff = randint(50,70)
        # if row[1] == '1' and row[3] == '3':
        #     tdiff = randint(10,20)
        # if row[1] == '1' and row[3] == '4':
        #     tdiff = 15
        # if row[1] == '2' and row[3] == '0':
        #     tdiff = 75
        # if row[1] == '2' and row[3] == '1':
        #     tdiff = randint(30,40)
        # if row[1] == '2' and row[3] == '2':
        #     tdiff = randint(50,70)
        # if row[1] == '2' and row[3] == '3':
        #     tdiff = randint(100,115)
        # if row[1] == '2' and row[3] == '4':
        #     tdiff = 45
        # if row[1] == '3' and row[3] == '2' and int(row[5])<=9492:
        #     tdiff = 70
        # if row[1] == '3' and row[3] == '2' and int(row[5])>9492:
        #     tdiff = 140
        # if row[1] == '3' and row[3] == '1':
        #     tdiff = randint(120,150)
        # if row[1] == '3' and row[3] == '0':
        #     tdiff = randint(100,110)
        # if row[1] == '3' and row[3] == '3':
        #     tdiff = randint(80,95)
        # if row[1] == '3' and row[3] == '4':
        #     tdiff = 90
        # if row[1] == '4' and row[3] == '0':
        #     tdiff = randint(5,15)
        # if row[1] == '4' and row[3] == '1' and int(row[5])<=9492:
        #     tdiff = 50
        # if row[1] == '4' and row[3] == '1' and int(row[5])>9492:
        #     tdiff = 10
        # if row[1] == '4' and row[3] == '2':
        #     tdiff = 25
        # if row[1] == '4' and row[3] == '3':
        #     tdiff = randint(10,20)
        # if row[1] == '4' and row[3] == '4':
        #     tdiff = randint(20,30)
        # if row[1] == '5' and row[3] == '0':
        #     tdiff = 70
        # if row[1] == '5' and row[3] == '1':
        #     tdiff = randint(35,55)
        # if row[1] == '5' and row[3] == '2':
        #     tdiff = randint(80,95)
        # if row[1] == '5' and row[3] == '3':
        #     tdiff = randint(100,130)
        # if row[1] == '5' and row[3] == '4':
        #     tdiff = 80

        if row[3] == '0':
            if row[1] == '1' or row[1] == '6' or row[1] == '11' or row[1] == '17' or row[1] == '23' or row[1] == '29' or row[1] == '35' or row[1] == '41' or row[1] == '47':
                tdiff = 90
        if row[3] == '1':
            if row[1] == '1' or row[1] == '6' or row[1] == '11' or row[1] == '17' or row[1] == '23' or row[1] == '29' or row[1] == '35' or row[1] == '41' or row[1] == '47':
                tdiff = 80
        if row[3] == '2':
            if row[1] == '1' or row[1] == '6' or row[1] == '11' or row[1] == '17' or row[1] == '23' or row[1] == '29' or row[1] == '35' or row[1] == '41' or row[1] == '47':
                tdiff = 60
        if row[3] == '3':
            if row[1] == '1' or row[1] == '6' or row[1] == '11' or row[1] == '17' or row[1] == '23' or row[1] == '29' or row[1] == '35' or row[1] == '41' or row[1] == '47':
                tdiff = 80
        if row[3] == '4':
            if row[1] == '1' or row[1] == '6' or row[1] == '11' or row[1] == '17' or row[1] == '23' or row[1] == '29' or row[1] == '35' or row[1] == '41' or row[1] == '47':
                tdiff = 40
        if row[3] == '0':
            if row[1] == '2' or row[1] == '7' or row[1] == '12' or row[1] == '18' or row[1] == '24' or row[1] == '30' or row[1] == '36' or row[1] == '42' or row[1] == '48':
                tdiff = 30
        if row[3] == '1':
            if row[1] == '2' or row[1] == '7' or row[1] == '12' or row[1] == '18' or row[1] == '24' or row[1] == '30' or row[1] == '36' or row[1] == '42' or row[1] == '48':
                tdiff = randint(20,30)
        if row[3] == '2':
            if row[1] == '2' or row[1] == '7' or row[1] == '12' or row[1] == '18' or row[1] == '24' or row[1] == '30' or row[1] == '36' or row[1] == '42' or row[1] == '48':
                tdiff = 25
        if row[3] == '3':
            if row[1] == '2' or row[1] == '7' or row[1] == '12' or row[1] == '18' or row[1] == '24' or row[1] == '30' or row[1] == '36' or row[1] == '42' or row[1] == '48':
                tdiff = 30
        if row[3] == '4':
            if row[1] == '2' or row[1] == '12' or row[1] == '18' or row[1] == '24' or row[1] == '30' or row[1] == '36' or row[1] == '42' or row[1] == '48':
                tdiff = 45
        if row[3] == '0':
            if row[1] == '3' or row[1] == '8' or row[1] == '13' or row[1] == '19' or row[1] == '25' or row[1] == '31' or row[1] == '37' or row[1] == '43' or row[1] == '49':
                tdiff = 120
        if row[3] == '1':
            if row[1] == '3' or row[1] == '8' or row[1] == '13' or row[1] == '19' or row[1] == '25' or row[1] == '31' or row[1] == '37' or row[1] == '43' or row[1] == '49':
                tdiff = 110
        if row[3] == '2':
            if row[1] == '3' or row[1] == '8' or row[1] == '13' or row[1] == '19' or row[1] == '25' or row[1] == '31' or row[1] == '37' or row[1] == '43' or row[1] == '49':
                tdiff = 100
        if row[3] == '3':
            if row[1] == '3' or row[1] == '8' or row[1] == '13' or row[1] == '19' or row[1] == '25' or row[1] == '31' or row[1] == '37' or row[1] == '43' or row[1] == '49':
                tdiff = 70
        if row[3] == '4':
            if row[1] == '3' or row[1] == '8' or row[1] == '13' or row[1] == '19' or row[1] == '25' or row[1] == '31' or row[1] == '37' or row[1] == '43' or row[1] == '49':
                tdiff = 85
        if row[3] == '0':
            if row[1] == '4' or row[1] == '9' or row[1] == '14' or row[1] == '20' or row[1] == '26' or row[1] == '32' or row[1] == '38' or row[1] == '44' or row[1] == '50':
                tdiff = 15
        if row[3] == '1':
            if row[1] == '4' or row[1] == '14' or row[1] == '20' or row[1] == '26' or row[1] == '32' or row[1] == '38' or row[1] == '44' or row[1] == '50':
                tdiff = 10
        if row[3] == '2':
            if row[1] == '4' or row[1] == '9' or row[1] == '14' or row[1] == '20' or row[1] == '26' or row[1] == '32' or row[1] == '38' or row[1] == '44' or row[1] == '50':
                tdiff = 25
        if row[3] == '3':
            if row[1] == '4' or row[1] == '9' or row[1] == '14' or row[1] == '20' or row[1] == '26' or row[1] == '32' or row[1] == '38' or row[1] == '44' or row[1] == '50':
                tdiff = 20
        if row[3] == '4':
            if row[1] == '4' or row[1] == '14' or row[1] == '20' or row[1] == '26' or row[1] == '32' or row[1] == '38' or row[1] == '44' or row[1] == '50':
                tdiff = 20
        if row[3] == '0':
            if row[1] == '5' or row[1] == '10' or row[1] == '15' or row[1] == '20' or row[1] == '25' or row[1] == '30' or row[1] == '35' or row[1] == '40' or row[1] == '45':
                tdiff = 70
        if row[3] == '1':
            if row[1] == '5' or row[1] == '10' or row[1] == '15' or row[1] == '20' or row[1] == '25' or row[1] == '30' or row[1] == '35' or row[1] == '40' or row[1] == '45':
                tdiff = randint(35,55)
        if row[3] == '2':
            if row[1] == '5' or row[1] == '10' or row[1] == '15' or row[1] == '20' or row[1] == '25' or row[1] == '30' or row[1] == '35' or row[1] == '40' or row[1] == '45':
                tdiff = randint(80,95)
        if row[3] == '3':
            if row[1] == '5' or row[1] == '10' or row[1] == '15' or row[1] == '20' or row[1] == '25' or row[1] == '30' or row[1] == '35' or row[1] == '40' or row[1] == '45':
                tdiff = randint(100,130)
        if row[3] == '4':
            if row[1] == '5' or row[1] == '10' or row[1] == '15' or row[1] == '20' or row[1] == '25' or row[1] == '30' or row[1] == '35' or row[1] == '40' or row[1] == '45':
                tdiff = 80
        if row[1] == '9' and row[3] == '4' and int(row[5])<=13271:
            tdiff = 20
        if row[1] == '9' and row[3] == '4' and int(row[5])>13271:
            tdiff = 60
        if row[1] == '9' and row[3] == '1' and int(row[5])<=13271:
            tdiff = 50
        if row[1] == '9' and row[3] == '1' and int(row[5])>13271:
            tdiff = 10
        if row[1] == '7' and row[3] == '4' and int(row[5])<=13271:
            tdiff = 70
        if row[1] == '7' and row[3] == '4' and int(row[5])>13271:
            tdiff = 140
        #tdiff = row[4]
        difflist.append(tdiff)

    difflist = [int(i) for i in difflist]
    print(difflist)

    csvfile.seek(0)
    header = next(spamreader, None)
    line_index = 0

    csvfile2 = open('../data2/final_experiments/%s.csv' % log_name, 'w')
    spamwriter = csv.writer(csvfile2)
    if header:
        spamwriter.writerow(header)

    for row in spamreader:
        if row[1] == '0':
            t0 = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
            #timestamps_list.append(t0)
            row[4] = str(0)
            spamwriter.writerow(row)
            print(t0)
        if row[1] != '0':
            t = t0 + timedelta(seconds=difflist[line_index])
            row[2] = str(t)
            row[4] = str(difflist[line_index])
            spamwriter.writerow(row)
            #timestamps_list.append(t)
            print(t)
            t0 = t
        line_index += 1