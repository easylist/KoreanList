
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd 
import os.path
#import msvcrt

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
EXCELFILE_NAME = r'Korean website filters.xlsx'
SHEET_NAME = r'February'
FILE_PREFIX = "koreanlist_"

# check whether this filter already exists.
def VerifingDuplicatedFilter(pendingFilter):
    if os.path.isfile(TOTAL_WRITTEN_TXT):
        with open(TOTAL_WRITTEN_TXT) as f:
            lines = f.readlines()
            for l in lines:
                l = l.replace('\n', '')
                if pendingFilter == l:
                    return False
    return True

def AppendToTextFile(filename, filterToAppend):
    FILE_PREFIX = "koreanlist_"
    with open(FILE_PREFIX+filename, "a") as currFile:
        currFile.write(filterToAppend + "\r\n")
    with open(TOTAL_WRITTEN_TXT, "a") as currFile:
        currFile.write(filterToAppend + "\r\n")
    print("This filter is saved to: " + filename)


df = pd.read_excel(EXCELFILE_NAME , SHEET_NAME)
for idx, x in enumerate(df['Suggested filter (to be reviewed)']):
    # Verified : if the background cell color of filter is Green or the "New filter" column is filled.
    isVerified= df['Verified'][idx]
    if isVerified == 'x':
        print("Passing not verified filter.")
        continue
    
    if VerifingDuplicatedFilter(x) == False:
        print("This filter is already in the list.")
        continue

    # If there is a new filter, using "New filter" column instead of "Suggested filter".
    IsNewFilter = False
    targetFilter = ''
    if df['New filter (If necessary)'][idx] is pd.np.nan:
        targetFilter = x
    else:
        targetFilter = df['New filter (If necessary)'][idx]
        IsNewFilter = True

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
    print("Is this domain is a... 1.adserver  2.sub-adserver  3.non-adserver.")
    answer= input()

    if answer.strip() == '':
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
