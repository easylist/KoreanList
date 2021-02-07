# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals # CLI-UIs
from PyInquirer import prompt, print_json # CLI-UIs

import sys
import numpy as np 
import math
import os.path
import webbrowser
from pathlib import Path
import tldextract # pip install tldextract


if __name__ == "__main__":
    pass

print("Python version: ", sys.version)
#print("openpyxl version: ", openpyxl.__version__)

# print("execute script from : " +sys.argv[0])
# print("running target file : " +sys.argv[1] + "\n")


path = ""
if len(sys.argv) == 1:
    path = 'Korean website filters.xlsx'
    print("use a default path : " + path)
else:
    path = sys.argv[1]

if path == "":
    print("path null error.")
    sys.exit()

def OpenChrome(url):
    # MacOS
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    # Windows
    #chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    # Linux
    # chrome_path = '/usr/bin/google-chrome %s'
    webbrowser.get(chrome_path).open(url) 

#https://mxtoolbox.com/SuperTool.aspx?action=whois%3anaver.com&run=networktools
#https://mxtoolbox.com/SuperTool.aspx?action=whois%3a.tpmn.co.kr&run=networktools
def CallALookup(filter):
    filter= filter[:filter.find('$')]
    filter= filter.replace('#', '').replace('|', '').replace('^', '')
    ext = tldextract.extract(filter)
    DNSLookupURL= "https://mxtoolbox.com/SuperTool.aspx?action=whois%3a"
    param = "&run=networktools" 

    print("subdomain: " + ext.subdomain)
    print("domain: " + ext.domain)
    print("suffix: " + ext.suffix)
    
    OpenChrome(DNSLookupURL + ext.domain + '.' + ext.suffix + param)

def IsPopup(filter):
    if "$popup" in filter:
        return True;
    else:
        return False;

def IsHidingFilter(filter):
    if "##" in filter:
        return True;
    else:
        return False;

def IsGeneralFilter(filter):
    return filter.startswith('.') or filter.startswith('&') or filter.startswith('-') or filter.startswith('_') or filter.startswith('##')

def IsWhitelistFilter(filter):
    return filter.startswith('@@||')

def IsGeneralWhitelistFilter(filter):
    return filter.startswith('#@#')

def IsDeminsionalWhitelistFilter(filter):
    return False



TOTAL_WRITTEN_TXT = "total_written.txt"
#EXCELFILE_NAME = r'Korean website filters.xlsx'
#PRESET_SHEET_NAME = r'2019.Feb'
SUB_FOLDER = Path("KoreanList")
FILE_PREFIX = "koreanlist_"

# check whether this filter already exists.
def VerifingDuplicatedFilter(pendingFilter):
    if os.path.isfile(TOTAL_WRITTEN_TXT):
        with open(TOTAL_WRITTEN_TXT) as f:
            lines = f.readlines()
            for l in lines:
                check1 = str(l).replace('\n', '')
                check2 = str(pendingFilter).replace('\n', '')
                if check1 == '' or check2 == '':
                    continue
                if check1 == check2:
                    return False
    return True

def AppendToTextFile(filename, filterToAppend):
    with open(SUB_FOLDER / (FILE_PREFIX+filename), "a") as currFile:
        currFile.write(filterToAppend + "\n")
    with open(TOTAL_WRITTEN_TXT, "a") as currFile:
        currFile.write(filterToAppend + "\n")
    print("This filter is saved to: " + filename)

def checkVerified():
    return

while(True):
    # If there is a new filter, using "New filter" column instead of "Suggested filter".
    print("Please input a filter: (Press 'q' to quit)")

    lines = []
    while(True):
        line = input()
        if line:
            lines.append(line)
        elif(line == 'q'):
            break
        else:
            break

    print(lines)
    for x in lines:
	    targetFilter = x

	    if targetFilter is None:# or np.isnan(targetFilter):
	        print("Please input a valid filter.")
	        continue

	    if VerifingDuplicatedFilter(targetFilter) == False:
	        print("This filter is already in the list.")
	        continue

	    targetFilter=str(targetFilter)
	    # Set boolean variables
	    isPopup = IsPopup(targetFilter)
	    isHidingFilter = IsHidingFilter(targetFilter)
	    isGeneralFilter = IsGeneralFilter(targetFilter)
	    isWhitelistFilter = IsWhitelistFilter(targetFilter)
	    isGeneralWhitelistFilter = IsGeneralWhitelistFilter(targetFilter)
	    isDeminsionalWhitelistFilter = IsDeminsionalWhitelistFilter(targetFilter)

	    if(isWhitelistFilter):
	        if(isPopup):
	            AppendToTextFile("whitelist_popup.txt", targetFilter)
	            continue
	        if(isDeminsionalWhitelistFilter):
	            AppendToTextFile("whitelist_dimensions.txt", targetFilter)
	            continue
	        else:
	            AppendToTextFile("whitelist.txt", targetFilter)
	            continue

	    if(isGeneralWhitelistFilter):
	        AppendToTextFile("whitelist_general_hide.txt", targetFilter)
	        continue

	    
	    
	    print("\n"+targetFilter) #+ " --> (Verified : " + str(isVerified) +", New suggestion : " + str(IsNewFilter) + ")")
	    print("This domain is a... (1)adserver  (2)sub-adserver  (3)non-adserver. (w)whois searching. (u)undo. (p)pass. (q)exit")
	    answer= input()

	    if answer.strip() == 'p' or answer.strip() == 'n':
	        print ("next.")
	        continue
		
	    if answer.strip() == 'w' or answer.strip() == 'l':
	        print("Calling a WHOIS lookup.")
	        CallALookup(targetFilter)
	        answer= input()
	        pass

	    if answer.strip() == '' or answer.strip() == 'q':
	        print("Shutdown the program.")
	        sys.exit()

	    if int(answer) == 1: # Ad-server
	        if isPopup == True:
	            AppendToTextFile("adservers_popup.txt", targetFilter)
	        else:
	            AppendToTextFile("adservers.txt", targetFilter)
	    if int(answer) == 2: # Non-ad-server
	        if isPopup == True:
	            AppendToTextFile("thirdparty_popup.txt", targetFilter)
	        else:
	            AppendToTextFile("thirdparty.txt", targetFilter)

	    if int(answer) == 3: # Non-ad-server
	        if isGeneralFilter == True:
	            if isHidingFilter == True:
	                AppendToTextFile("general_hide.txt", targetFilter)
	            else:
	                if isPopup == True:
	                    AppendToTextFile("general_block_popup.txt", targetFilter)
	                else:
	                    AppendToTextFile("general_block.txt", targetFilter)
	        else:
	            if isHidingFilter is True:
	                AppendToTextFile("specific_hide.txt", targetFilter)
	            else:
	                if isPopup is True:
	                    AppendToTextFile("specific_block_popup.txt", targetFilter)
	                else:
	                    AppendToTextFile("specific_block.txt", targetFilter)
