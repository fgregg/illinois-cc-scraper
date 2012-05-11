import mechanize
import cookielib
import re
import csv
import StringIO

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

contributions_url_base = 'http://www.elections.il.gov/CampaignDisclosure/DownloadList.aspx?DownloadListType=Receipts&ContributionSearchType=Committees&LastOnlyNameSearchType=Starts+with&LastOnlyName=&FirstNameSearchType=Starts+with&FirstName=&AddressSearchType=Starts+with&Address=&CitySearchType=Starts+with&City=&State=&Zip=&ZipThru=&VendorLastOnlyNameSearchType=Starts+with&VendorLastOnlyName=&VendorFirstNameSearchType=Starts+with&VendorFirstName=&VendorAddressSearchType=Starts+with&VendorAddress=&VendorCitySearchType=Starts+with&VendorCity=&VendorState=&VendorZip=&VendorZipThru=&PurposeState=Starts+with&Purpose=&ContributionType=All+Types&OccupationSearchType=Starts+with&Occupation=&EmployerSearchType=Starts+with&Employer=&Amount=&AmountThru=&RcvDate=&RcvDateThru=&CmteNameSearchType=Contains&CmteName=&CmteID=%s&CmteLocalID=&CmteStateID=&Archived=false&QueryType=ContribCommittee&LinkedQuery=true&OrderBy=Date+Received+-+most+recent+first'

alderman_committees = {'hairston, leslie' : (14216,),
                       'arena, john' : (22749,),
                       'austin, carrie': (1184, 1185),
                       'balcer, james' : (17491,),
                       'beale, anthony' : (14556,),
                       'brookins, jr., howard' : (522, 14525, 17003, 20626, 2516),
                       'burke, edward' : (9936, 4410, 4326, 11297, 3031),
                       'burnett, jr., walter': (10591,),
                       'burns, william' : (20749,),
                       'cappleman, james' : (19747,),
                       'cardenas, george' : (7271,),
                       'chandler, michael' : (23005, 14947, 10930),
                       'cochran, willie' : (19880,),
                       'colon, rey' : (14238, 17037, 18010),
                       'cullerton, tim' : (23111,),
                       'dowell, pat' : (16892,),
                       'ervin, jason' : (16671, 23112),
                       'fiorreti, bob' : (19819, 21102),
                       'foulkes, toni' : (20107,),
                       'graham, deborah' : (16505,),
                       'harris, michelle' : (20016,),
                       'jackson, sandi' : (20052,),
                       'lane, lona' : (20015,),
                       'laurino, margaret' : (1400, 9808),
                       'oconnor, mary' : (20673,),
                       'maldonado, robert' : (14611, 9533, 12249),
                       'mell, richard' : (4317, ),
                       'mitts, emma' : (15622,),
                       'moore, joe' : (6380, ),
                       'moreno, joe' : (20809,),
                       'munoz, ricardo' : (9487, 13134),
                       'oshea, matthew' : (22919,),
                       'osterman, harry' : (14971, 22976),
                       'oconnor, patrick' : (4353, 5119),
                       'pawar, ameya' : (23607, 22524),
                       'pope, john' : (19733, 14501),
                       'quinn, marty' : (23282,),
                       'reboyras, ariel' : (17163,),
                       'reilly, brendan' : (19263, ),
                       'sawyer, roderick' : (11715,),
                       'silverstein, debra' : (22982,),
                       'smith, michelle' : (19682,),
                       'solis, danny' : (12260,),
                       'sposato, nicholas' : (19830,),
                       'suarez, regner' : (6555, 14968),
                       'thomas, latasha' : (15729, ),
                       'thompson, joann' : (16425,),
                       'tunney, thomas' : (17150,),
                       'waguespack, scott' : (19898,),
                       'zalewski, mike' : (14156,)
                       }
                       

f = open('/home/fgregg/academic/politics/aldermanic_contributions.csv', 'w')
f.write("CommitteeID,LastOnlyName,FirstName,RcvDate,Amount,LoanAmount,Occupation,Employer,Address1,Address2,City,State,Zip,RctType,Description,VendorLastOnlyName,VendorFirstName,VendorAddress1,VendorAddress2,VendorCity,VendorState,VendorZip,RptType,ElectionType,ElectionYear,RptPdBegDate,RptPdEndDate,RptRcvdDate,CmteReferName,CmteName,StateCmte,StateID,LocalCmte,LocalID\n")
f.close
                      

for alderman in alderman_committees.keys() :
    for committee_id in alderman_committees[alderman] :
        print committee_id
        contributions_url = contributions_url_base % (committee_id,)

        br.open(contributions_url)
        br.select_form(nr=0)
        br.form.set_all_readonly(False)
        br.form['__EVENTTARGET']='ctl00$ContentPlaceHolder1$btnText'
        for field in br.form.controls :
            if field.id == 'ctl00_btnSearch' :
                br.form.controls.remove(field)



        contributions = br.submit().read()
        # Strip first header, which is the first line
        contributions = re.sub(r"^.*\n", "", contributions, count=1)
        contributions = StringIO.StringIO(contributions)
        tabin = csv.reader(contributions, dialect=csv.excel_tab)

        f = open('/home/fgregg/academic/politics/aldermanic_contributions.csv', 'a')
        writer = csv.writer(f, dialect=csv.excel)
        for row in tabin :
            writer.writerow(row)

        f.close()



