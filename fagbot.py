from pyfiglet import Figlet
import urllib3,io
from os import system as System
from os import rename as Move_file
from os import makedirs as MakeDir
from os import path as Path
from datetime import datetime
from datetime import date, timedelta
import zipfile
class bcolors:
    BLACK='\033[30m'
    GREY='\033[90m'
    CYAN='\033[96m'
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    BGREEN = '\033[32m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RRED = '\033[101m'
    BRED = '\033[31m'
    RGREEN = '\033[42m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ------| command line parameters |------
import argparse # command line parser
parser = argparse.ArgumentParser(description='Fear and greed Bot')
# parser = argparse.ArgumentParser(prog=(parser.prog).split(".")[0].capitalize())
# //parser = argparse.ArgumentParser(epilog='Have fun.')
# parser.add_argument('-p','--profile', action='store',help='set alternate profile file',dest="profile")
# parser.add_argument('-t','--tweet', action='store',help='send a tweet',dest="tweet")
# parser.add_argument('-r','--retweet', action='store',help='retweet',dest="retweet")
# parser.add_argument('-q','--quote', action='store',help='quote a tweet',dest="quote")
# parser.add_argument('-l','--like  ', action='store',help='Like tweet',dest="like")
# parser.add_argument('-u','--unlike  ', action='store',help='Unike tweet',dest="unlike")
parser.add_argument("-s","--silent", action='store_false',help='Hide messages')
parser.add_argument('-n',"--no-banner", action='store_false',dest="nobanner")
parser.add_argument('-v','--version', action='version', version=f'%(prog)s 1.0')
args = parser.parse_args()
# for i in range(0,500):
#     print(f'{i} \033[{i}m'+"hola"+bcolors.ENDC)
# exit()
# def stringBetween(text,start,end):
# def find_between( s, first, last ):
#     try:
#         start = s.index( first ) + len( first )
#         end = s.index( last, start )
#         return s[start:end]
#     except ValueError:
#         return ""

# def find_between_r( s, first, last ):
#     try:
#         start = s.rindex( first ) + len( first )
#         end = s.rindex( last, start )
#         return s[start:end]
#     except ValueError:
#         return ""
def string_between(string, start, end):
    # https://stackoverflow.com/questions/3368969/find-string-between-two-substrings
    return (string.split(start))[1].split(end)[0]


# date,level,description = find_between( s, "[\n", "\n\t]" ).split("\n")[1].split(",")
# ▄
# █
# █
# region get values from web
def getWebValues(limit=31):
    http = urllib3.PoolManager()
    r = http.request('GET', f'https://api.alternative.me/fng/?limit={limit}&format=csv')
    values=(string_between(str(r.data).replace("\\n\\t",""),"[","]")).split("\\n")[2:]
    return values
# endregion
# Function : file_compress

def getPercent(new,old):
    new=int(new)
    old=int(old)
    if old >0 :
        totalpercent = round(((new - old)/old)*100,2)
    else:
        totalpercent=100

    if totalpercent >=0:
        totalpercent=bcolors.GREEN + str(totalpercent) + "%" + bcolors.ENDC
    else:
        totalpercent = bcolors.RED + str(abs(totalpercent)) + "%" + bcolors.ENDC
    return totalpercent

def getfear(value):
    value=int(value)
    if value < 26:
        # print("extreme Fear")
        return bcolors.BRED+bcolors.UNDERLINE +"Extreme Fear"+bcolors.ENDC
    elif value < 47:
        # print("Fear")
        return bcolors.RED+"Fear"+bcolors.ENDC
    elif value < 55:
        # print("Fear")
        return "Neutral"+bcolors.ENDC
    elif value < 76:
        # print("greed")
        return bcolors.GREEN +"Greed"+bcolors.ENDC
    elif value < 100:
        return bcolors.BGREEN+bcolors.UNDERLINE +"Extreme greed"+bcolors.ENDC
    else:
        print("Invalid Value")
def mediumfag(values,count):
        returncount=0
        for i in range(0,count):
            returncount += int(values[i].split(",")[1])
        return round(returncount/count)

def getfag(values,returnvalue=""): # get the results
    count=0
    returnvalue=returnvalue.lower()
    if returnvalue == "" or returnvalue == "last":
        return values[0].split(",")[1]
    elif returnvalue == "y" or returnvalue == "yesterday":
        return values[1].split(",")[1]
    elif returnvalue == "week":
        return mediumfag(values,7)
    elif returnvalue == "month":
        return mediumfag(values,31)
    elif returnvalue == "fortnight":
        return mediumfag(values,15)
    else:
        try:
          returnvalue=int(returnvalue) 
          return mediumfag(values,returnvalue)
        except:
            return values[0].split(",")[1]

# Region print banner
def getBanner(text,font='graffiti'):
    custom_fig = Figlet(font)
    print(bcolors.GREEN+custom_fig.renderText(text)+" "*32+"by dr_D00m4n"+bcolors.ENDC)
# endregion
def getFagPercent(values,days=1): # get % of the fear variation
    # // todo get variation of diferent days
    returnValue=0
    newValue=int(values[0].split(",")[1])
    oldValue=int(values[days].split(",")[1])
    return getPercent(newValue,oldValue)
    # for i in range(0,days+1):
    #     returnValue += int(values[i].split(",")[1])
    # return round(returnValue/(days+1))
def _loadFile(file, format="none"):
    try:
        text_file = open(file, "r", encoding="utf-8")
        if format == "raw":
            lines = text_file.read()
        else:
            lines = text_file.read().splitlines()
    except Exception as errorEx:
        print(errorEx)
        return False

    return lines

def _saveFile(file, text, raw=False):
    with io.open(file, 'w', encoding='utf8') as txt_file:
        if raw:
            txt_file.write(str(text))
        else:
            for line in text:
                # works with any number of elements in a line
                txt_file.write(str(line) + "\n")



def showfear(when="today"):
    todayFile=datetime.today().strftime('%y%m%d')
    yesterdayFile=(datetime.today() - timedelta(days=1)).strftime('%y%m%d')
    if not Path.isfile(todayFile): # view if today file is still generated
        if not args.silent:
            print(f'{bcolors.CYAN}Saving today file...{bcolors.ENDC}')

        if Path.isfile(yesterdayFile): # check if there are previus version
            MakeDir("history", exist_ok=True)
            if not args.silent:
              print(f'{bcolors.CYAN}Backing up old file...{bcolors.ENDC}')
            # print("Backing up old file")
            Move_file(yesterdayFile,"history/"+yesterdayFile)
            
        # Download values from web
        webValues=getWebValues() # dowload weg values
        fear=getfag(webValues)
        yesterday=getfag(webValues,"yesterday")
        week=getfag(webValues,"week")
        fortnight=getfag(webValues,"fortnight")
        month=getfag(webValues,"month")
        percent=getFagPercent(webValues)
        yesterdayPercent=getPercent(yesterday,fear)
        weekPercent=getPercent(week,fear)
        fortnightPercent=getPercent(fortnight,fear)
        monthPercent=getPercent(month,fear)
        _saveFile(todayFile,(fear,yesterday,week,fortnight,month))
    else:
        if not args.silent:
            print(f'{bcolors.CYAN}Loading saved data...{bcolors.ENDC}')
        # ("Loading saved data")
        # loadedFile=_loadFile(todayFile)
        fear,yesterday,week,fortnight,month = _loadFile(todayFile)
        percent=getPercent(fear,yesterday)
        yesterdayPercent=getPercent(yesterday,fear)
        weekPercent=getPercent(week,fear)
        fortnightPercent=getPercent(fortnight,fear)
        monthPercent=getPercent(month,fear)

    if when=="today":
        print(f'Today      : {fear} ({percent}) {getfear(fear)}' )
    print(f'Yesterday  : {yesterday} ({yesterdayPercent}) {getfear(yesterday)}' )
    print(f'Week       : {week} ({weekPercent}) {getfear(week)}' )
    print(f'Fortnight  : {fortnight} ({fortnightPercent}) {getfear(fortnight)}' )
    print(f'Month      : {month} ({monthPercent}) {getfear(month)}' )


def main():
    if args.nobanner:
        System("clear")
        getBanner((parser.prog).split(".")[0].capitalize())
        print("\n")
    if args.silent:
        print(f'{bcolors.CYAN}Downloading data...{bcolors.ENDC}')
    showfear()

    
if __name__ == '__main__':
    main()
# print("import")
# exit()


# print( find_between_r( s, "[", "]" ))



# for value in values:
#     print(value)
# # print(str(data).split("[")[1])
# # print(getfag(values))
# exit()
# value=getfag(values,28)

# # exit()
# old_value=(values[1].split(",")[1])
# new_value=(values[0].split(",")[1])
# print(f'- Today: {bcolors.BOLD+bcolors.RED+new_value+bcolors.ENDC} ({getPercent(new_value,old_value)}) {getfear(new_value)}' )
# print(f'- Today: {bcolors.BOLD+bcolors.RED+new_value+bcolors.ENDC} ({getPercent(new_value,old_value)}) {getfear(30)}' )
# print(f'- Today: {bcolors.BOLD+bcolors.RED+new_value+bcolors.ENDC} ({getPercent(new_value,old_value)}) {getfear(49)}' )
# print(f'- Today: {bcolors.BOLD+bcolors.RED+new_value+bcolors.ENDC} ({getPercent(new_value,old_value)}) {getfear(55)}' )
# print(f'- Today: {bcolors.BOLD+bcolors.RED+new_value+bcolors.ENDC} ({getPercent(new_value,old_value)}) {getfear(85)}' )
# print("· 0 - 25   "+f'{getfear(0)}')
# print("· 26 - 46  "+f'{getfear(26)}')
# print("· 47 - 54  "+f'{getfear(47)}')
# print("· 55 - 75  "+f'{getfear(55)}')
# print("· 76 - 100 "+f'{getfear(76)}')


