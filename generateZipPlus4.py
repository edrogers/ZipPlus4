#!/usr/bin/python
                 
import requests  
import time      
import re        
import os        
import config

#Grab the first 2 items in each line of the CSV
parcelNumAndAddressRegEx=re.compile("[0-9]{12},[^,]+,")
parcelNumAndAddressObjects = [parcelNumAndAddressRegEx.match(line) for line in open('Assessor_Property_Information.csv')]
for parcelNumAndAddressObject in parcelNumAndAddressObjects:
    # reset the defaults to blank for each parcel
    parcel=""
    address1=""
    address2=""
    city="Madison"
    state="WI"
    zip5=""
    zip4=""
    if parcelNumAndAddressObject != None:
        # Match the parcel num with a regex
        parcelRegEx=re.compile("[0-9]{12}")
        parcelObject=parcelRegEx.match(parcelNumAndAddressObject.group(0))
        if parcelObject != None:
            parcel=parcelObject.group(0)

        # Match the address as anything between the other 2 commas
        address1RegEx=re.compile(",[^,]+,")
        address1Object=address1RegEx.search(parcelNumAndAddressObject.group(0))
        if address1Object != None:
            address1 = address1Object.group(0).strip(",")

            # Send a request for address verification to USPS API
            httpRequestURL="http://production.shippingapis.com/ShippingAPITest.dll?API=Verify&XML=<AddressValidateRequest USERID=\"{}\"><Address ID=\"0\"><Address1>{}</Address1><Address2>{}</Address2><City>{}</City><State>{}</State><Zip5></Zip5><Zip4></Zip4></Address></AddressValidateRequest>".format(config.USPS_UserID,address1,address2,city,state)

            resp = requests.get(httpRequestURL)
            # Pause for 5 seconds as a courtesy to USPS
            time.sleep(5)

            # Match the Zip 5 and Zip 4 in the response
            zip5RegEx=re.compile("<Zip5>[0-9]{5}</Zip5>")
            zip5Object = zip5RegEx.search(resp.text)
            if zip5Object != None:
                zip5 = zip5Object.group(0).replace("<Zip5>","").replace("</Zip5>","")

            zip4RegEx=re.compile("<Zip4>[0-9]{4}</Zip4>")
            zip4Object = zip4RegEx.search(resp.text)
            if zip4Object != None:
                zip4 = zip4Object.group(0).replace("<Zip4>","").replace("</Zip4>","")

        # Write out the results to a CSV
        csvOut = open("ParcelAddressZipPlus4.csv",'a')
        csvOut.write("{},{},{},{},{},{}\n".format(parcel,address1,city,state,zip5,zip4))        
        csvOut.close()                                                    

        # And print them to screen                        
        print parcel
        print address1
        # print address2
        print city
        print state
        print zip5
        print zip4
        print ""

quit()
