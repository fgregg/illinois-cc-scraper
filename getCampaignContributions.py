import mechanize
import cookielib

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
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

contributions_url = 'http://www.elections.il.gov/CampaignDisclosure/DownloadList.aspx?DownloadListType=Receipts&ContributionSearchType=Committees&LastOnlyNameSearchType=Starts+with&LastOnlyName=&FirstNameSearchType=Starts+with&FirstName=&AddressSearchType=Starts+with&Address=&CitySearchType=Starts+with&City=&State=&Zip=&ZipThru=&VendorLastOnlyNameSearchType=Starts+with&VendorLastOnlyName=&VendorFirstNameSearchType=Starts+with&VendorFirstName=&VendorAddressSearchType=Starts+with&VendorAddress=&VendorCitySearchType=Starts+with&VendorCity=&VendorState=&VendorZip=&VendorZipThru=&PurposeState=Starts+with&Purpose=&ContributionType=All+Types&OccupationSearchType=Starts+with&Occupation=&EmployerSearchType=Starts+with&Employer=&Amount=&AmountThru=&RcvDate=&RcvDateThru=&CmteNameSearchType=Contains&CmteName=&CmteID=%s&CmteLocalID=&CmteStateID=&Archived=false&QueryType=ContribCommittee&LinkedQuery=true&OrderBy=Last+or+Only+Name+-+A+to+Z'

contributions_url = contributions_url % ('14216',)

br.open(contributions_url)
br.select_form(nr=0)
br.form.set_all_readonly(False)
br.form['__EVENTTARGET']='ctl00$ContentPlaceHolder1$btnText'
for field in br.form.controls :
    if field.id == 'ctl00_btnSearch' :
        br.form.controls.remove(field)

f = open('/home/fgregg/academic/politics/hairston.tdf', 'w')
f.write(br.submit().read())
f.close()


