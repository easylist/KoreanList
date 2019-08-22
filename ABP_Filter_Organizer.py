
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd 
import os.path
import webbrowser
import tldextract # pip install tldextract
from xlrd import open_workbook
import numpy as np 
import sys
from StyleFrame import StyleFrame, utils

print("Python version: ", sys.version)
print ("Pandas version: ", pd.__version__)
#print("openpyxl version: ", openpyxl.__version__)

print("execute script from : " +sys.argv[0])
print("running target file : " +sys.argv[1] + "\n")

path = ""
if sys.argv[1] == "":
    path = 'Korean website filters.xlsx'
    print("use a default path : " + path)
else:
    path = sys.argv[1]

if path == "":
    print("path null error.")
    sys.exit()

def OpenChrome(url):
    # MacOS
    # chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    # Windows
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
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
SHEET_NAME = r'2019.Feb'
SUB_FOLDER = "KoreanList"
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
    with open(SUB_FOLDER + "\\" + FILE_PREFIX+filename, "a") as currFile:
        currFile.write(filterToAppend + "\r\n")
    with open(TOTAL_WRITTEN_TXT, "a") as currFile:
        currFile.write(filterToAppend + "\r\n")
    print("This filter is saved to: " + filename)



def only_cells_with_green_background(cell):
    #print(cell.value, cell.style.bg_color)
    return cell if cell.style.bg_color in {utils.colors.green, 'FF93C47D'} else np.nan


sf = StyleFrame.read_excel(path, sheet_name=SHEET_NAME, read_style=True, use_openpyxl_styles=False)
sf_3 = StyleFrame(sf.applymap(only_cells_with_green_background).dropna(axis=(0, 1), how='all'))
print(sf_3)

sys.exit()

df = pd.read_excel(path , SHEET_NAME)
for idx, x in enumerate(df['Suggested filter (to be reviewed)']):
    # Verified : if the background cell color of filter is Green or the "New filter" column is filled.
    isVerified= df['Verified'][idx]
    if isVerified == 'x':
        print(str(idx)+ ". Passed unverified filter.")
        continue

    # If there is a new filter, using "New filter" column instead of "Suggested filter".
    IsNewFilter = False
    targetFilter = ''
    if df['New filter (If necessary)'][idx] is pd.np.nan:
        targetFilter = x
    else:
        targetFilter = df['New filter (If necessary)'][idx]
        IsNewFilter = True

    if targetFilter is pd.np.nan:
        print(str(idx)+ ". No filters can be found in this row.")
        continue

    if VerifingDuplicatedFilter(targetFilter) == False:
        print(str(idx)+ ". This filter is already in the list.")
        continue
    
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

    
    
    print("\n"+targetFilter+ "(" + isVerified +"," + str(IsNewFilter) + ")")
    print("Is this domain is a... (1)adserver  (2)sub-adserver  (3)non-adserver. (w)whois searching. (u)undo. (x)exit")
    answer= input()
	
    if answer.strip() == 'w' or answer.strip() == 'l':
        print("Calling a WHOIS lookup.")
        CallALookup(targetFilter)
        answer= input()
        pass

    if answer.strip() == '' or answer.strip() == 'x':
        print("Shutdown the program.")
        break

    if int(answer) is 1: # Ad-server
        if isPopup == True:
            AppendToTextFile("adservers_popup.txt", targetFilter)
        else:
            AppendToTextFile("adservers.txt", targetFilter)
    if int(answer) is 2: # Non-ad-server
        if isPopup == True:
            AppendToTextFile("thirdparty_popup.txt", targetFilter)
        else:
            AppendToTextFile("thirdparty.txt", targetFilter)

    if int(answer) is 3: # Non-ad-server
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
                    AppendToTextFile("specific_block.txt ", targetFilter)
