import csv
import matplotlib.pyplot as plt
import numpy as np

IL, IIL, IIIL, IIIIL, IIIIIL = [], [], [], [], []
registration, district_wise, principal, groupwise = {}, {}, {}, {}
zip_code = {}


def zipsetter():
    """ Trick is to read zip.csv file.
        Store it into dictonary like `zip:district` format.
        It will reduce the time-complexity of searching.
    """
    with open('zip.csv', encoding='cp1252') as zip:
        code = csv.reader(zip)
        for i in code:
            if(i[0].isdigit()):
                zip_code[i[0]] = i[1]


def main():
    """
    This function is for structurizing our data.
    """
    with open('Maharashtra.csv', encoding='cp1252') as f:
        fo = csv.DictReader(f)
        for i in fo:
            """
             - this if function will check all entities and filter out
               companies into their respective "AUTHORIZED_CAP" Group.
            """
            if(i['AUTHORIZED_CAP'].isdigit()):
                if(int(i['AUTHORIZED_CAP']) <= 10 ** 5):
                    IL.append(int(i['AUTHORIZED_CAP']))
                elif(10 ** 5 < int(i['AUTHORIZED_CAP']) <= 10 ** 6):
                    IIL.append(int(i['AUTHORIZED_CAP']))
                elif(10 ** 6 < int(i['AUTHORIZED_CAP']) <= 10 ** 7):
                    IIIL.append(int(i['AUTHORIZED_CAP']))
                elif(10**7 < int(i['AUTHORIZED_CAP']) <= 10 ** 8):
                    IIIIL.append(int(i['AUTHORIZED_CAP']))
                elif(10**8 < int(i['AUTHORIZED_CAP'])):
                    IIIIIL.append(int(i['AUTHORIZED_CAP']))
            """
             - this trick will split year of registration
               from 'DATE_OF_REGISTRATION'.
            """
            if(i['DATE_OF_REGISTRATION'] != 'NA'):
                year = i['DATE_OF_REGISTRATION'].split("-")

                """
                 - This if loop will only allows entities
                   from year 2015 to 2020 Registration Year
                 - Count the "PRINCIPAL_BUSINESS_ACTIVITY"
                   for each year respectevely.
                 - store it in a dict i.e. `principle:{year:{activity:count}}`
                 - this trick will make code more dynamic
                   and reduce the time complexity.
                """
                if(15 <= int(year[2]) < 20):
                    key_year = 2000 + int(year[2])
                    activity = i['PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN']
                    if(principal.get(key_year) == None):
                        principal[key_year] = {activity: 1}
                    else:
                        if(principal[key_year].get(activity) == None):
                            principal[key_year][activity] = 1
                        else:
                            principal[key_year][activity] += 1

                """
                 - Only allows the entities of registration year 2015.
                 - For extraction of zip code from address and search
                   it into `zip_code` dictionary.
                 - Count district-wise number of companies
                   register in year 2015
                """
                if(int(year[2]) == 15):
                    z = i["Registered_Office_Address"]
                    zips = z[-6:len(z)]
                    if(zips.isdigit()):
                        if(zip_code.get(zips) != None):
                            if(district_wise.get(zip_code[zips]) == None):
                                district_wise[zip_code[zips]] = 0
                            else:
                                district_wise[zip_code[zips]] += 1
                """
                 - Count Companies register by thier respective years
                   from year 2000 to 2020.
                """
                if(0 <= int(year[2]) < 21):
                    year = 2000 + int(year[2])
                    if(registration.get(year) == None):
                        registration[year] = 1
                    else:
                        registration[year] += 1
        sorted(registration)


def setupgroupwise():
    """
     - Trick is to  Filter out 4 common principal from all
       the years from 2015 to 2019.
     - key_arr is a list of all principle dictonary keys
       it's the array of years from 2015 to 2019
     - year_key is a list of all the "priciple business activities"
       in year 2019
     - Iterate over all the years 2015-2019 and find 4 unique principle
       same in all years.
     - Searching Complexity for one  possible search is `O(1)`
    """
    key_arr = list(principal.keys())
    print(key_arr)
    year_key = list(principal[key_arr[0]].keys())
    count = 0
    for i in year_key:
        if(count > 3):
            break
        for j in key_arr:
            if(principal[j].get(i) == None):
                break
        else:
            print(principal[key_arr[-1]][i])
            groupwise[i] = [principal[key_arr[-1]][i],
                            principal[key_arr[-2]][i],
                            principal[key_arr[-3]][i],
                            principal[key_arr[-4]][i],
                            principal[key_arr[-5]][i]]
            print(groupwise)
            count += 1


def plotting():
    labels = [2015, 2016, 2017, 2018, 2019]
    keys = ['texttiles', 'chemical', 'metal', 'transport']
    values = list(groupwise.values())
    x = np.arange(len(labels))  # the label locations
    width = 0.2

    # this Section is for plotting histogram
    plt.subplot(2, 2, 1)
    plt.hist([IL, IIL, IIIL, IIIIL, IIIIIL], rwidth=0.4,
             bins=4,
             label=["<1L", "1L<=10L", "10L<=1C", "1C<=10C", "10C<"])
    plt.title("Histogram of Authorized Cap")
    plt.xlabel("Authorized Caps")
    plt.legend()
    plt.ylabel("No. Of Companies")

    # plotting Bar Graph of companies register Vs year
    plt.subplot(2, 2, 2)
    plt.bar(registration.keys(), registration.values())
    plt.title("Bar Graph of companies register Vs year")
    plt.xlabel("Years")
    plt.ylabel("No. Of Companies")

    # Plotting Bar Graph of companies register Vs District in year 2015
    plt.subplot(2, 2, 3)
    plt.bar(district_wise.keys(), district_wise.values())
    plt.title("Bar Graph of companies register Vs District in year 2015")
    plt.xlabel("Discticts")
    plt.ylabel("No. Of Companies")
    plt.xticks(rotation="vertical")

    # Plotting grouped-bar graph for
    # Year of registration
    # and Principal Business Activities.
    plt.subplot(2, 2, 4)
    for i in range(len(values)):
        plt.bar(x+(width)*i, values[i], width=width, label=keys[i])
    plt.title(" Count Principal Business Activities of Year of registration")
    plt.xlabel("Years")
    plt.ylabel("No. of Principal Business Activities")
    plt.xticks(x, labels, rotation="vertical")
    plt.legend(loc='upper left', ncol=2)

    plt.tight_layout()
    plt.show()


zipsetter()
main()
setupgroupwise()
print(groupwise)
plotting()
