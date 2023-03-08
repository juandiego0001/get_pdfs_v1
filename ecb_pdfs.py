"""save pdf files in local folder"""
import datetime
from urllib.request import Request, urlopen
import os
import requests
from bs4 import BeautifulSoup

#now datetime
now = datetime.datetime.now()
#Collect the different categories
urls = []
cat_1 = []
cat_2 = []
cat_3 = []

#functions
def get_mime(file):
    """returns the file extension"""
    check_pdf_extension = file.find(".pdf")
    if check_pdf_extension is -1:
        mimetype = "0"
    else:
        mimetype = "1"
    return mimetype

def get_mime_open_file(file):
    """returns the file extension to the opened file"""
    hdr_save  = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(file,headers=hdr_save,timeout=30)
    check_file = '%PDF-' in str(response.content)
    return check_file

def save_file(folder_name, file,name):
    """save the file"""
    name = name[0:250]
    hdr_save  = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(file,headers=hdr_save,timeout=30)
    try:
        with open(folder_name + "/" + name + '.pdf', 'wb') as file_opened:
            file_opened.write(response.content)
    except TypeError:
        #print(name)
        now_uno = datetime.datetime.now()
        name = now_uno.strftime("%Y%m%d_%H%M%S")
        with open(folder_name + "/" + name + '.pdf', 'wb') as file_opened:
            file_opened.write(response.content)
        #print("Copied changed name: " + name)

def browse_and_save(urls_check,position,div_id):
    """browse the categories"""
    count_0 = 0
    for courrent_url in urls_check:
        if count_0 == 1:
            #EXEC_LOGS = EXEC_LOGS + "\n" + a
            if position == 1:
                cat_2.clear()
            if position == 2:
                cat_3.clear()

            #Connect to page
            now_dos = datetime.datetime.now()
            courrent_hdr  = {'User-Agent': 'Mozilla/5.0'}
            courrent_req  = Request(courrent_url,headers=courrent_hdr)
            with urlopen(courrent_req) as courrent_page:
                courrent_soup = BeautifulSoup(courrent_page,'html.parser')
            panecontent1 = courrent_soup.find(class_=div_id)
            if panecontent1.lenght is not None:
                print("not none")
            for courrent_link in panecontent1.find_all('a', href=True):
                file = courrent_link['href']
                try:
                    if len(courrent_link.contents) > 0:
                        temp_name = courrent_link.contents[0]
                        temp_name = clearname(temp_name)
                    else:
                        temp_name = now_dos.strftime("%Y%m%d_%H%M%S")
                except TypeError:
                    temp_name = now_dos.strftime("%Y%m%d_%H%M%S")

                validate_url = 'https' in file
                if validate_url is not True:
                    file = BASE_SITE + file
                    #print("Changed to BASE_SITE 1:" + BASE_SITE + " file:" + file)

                file = file.replace("//", "/")
                file = file.replace("https:/", "https://")
                save_file_bridge(file,cat_1[count_0],temp_name,position)
        count_0 = count_0 + 1

    #print("end of exe-->"+str(position) + "-->")
    #print(cat_2)
    if position == 1:
        browse_and_save(cat_2,2,'right-main-area')
    if position == 2:
        browse_and_save(cat_3,3,'right-main-area')
    if position == 3:
        save_log(EXEC_LOGS)

def save_file_bridge(file,cat,temp_name,position):
    """Save the file"""
    if get_mime(file) == "1":
        print("Saving->" + file)
        #EXEC_LOGS = EXEC_LOGS + "Saving file:" + file
        save_file(BASE_FOLDER + "/" + cat, file, str(temp_name))
    else:
        check_anchor = 'https://www.eba.europa.eu/#' in file
        if check_anchor is False:
            if file != 'https://www.eba.europa.eu/':
                if get_mime_open_file(file) is True:
                    #EXEC_LOGS = EXEC_LOGS + "Saving file:" + file
                    save_file(BASE_FOLDER + "/" + cat, file, str(temp_name))
                else:
                    check_file = 'https://www.eba.europa.eu/' in file
                    if position == 1 and check_file is True:
                        cat_2.append(file)
                    if position == 2 and check_file is True:
                        cat_3.append(file)
    #print(file,cat,temp_name,position)

def clearname(name: str) -> str:
    """Clears invalid characters from a string and replaces them with hyphens.

    Args:
        name: A string representing the name to be cleaned.

    Returns:
        A string with all invalid characters replaced with hyphens.

    Raises:
        None.
    """
    name = name.lower()
    invalid_chars = [' ', '(', ')', '%20', '/', '"', '?', '\n', "'", "|", "!", "#",
    "$", "%", "&", "=", "+", "*", "}", "{", "[", "]", ";", ":", "á", "é", "í", "ó", "ú"]
    for char in invalid_chars:
        name = name.replace(char, "-")
    while "--" in name:
        name = name.replace("--", "-")
    return name

def save_log(log):
    """Save log"""
    log = log + "\nEnd of execution"
    with open("logs/" + FOLDER_NAME + '.log', 'wb') as log_file:
        log_file.write(log.encode())

#End of functions

#Define urls to execution
BASE_SITE = "https://www.eba.europa.eu/"
SITE = "https://www.eba.europa.eu/regulation-and-policy"
FOLDER = "pdfs/"

date_time = now.strftime("%Y-%m-%d %H:%M:%S")
#log var
EXEC_LOGS = "Start execution on: "
EXEC_LOGS = EXEC_LOGS + date_time

date_folder = now.strftime("%Y%m%d")
date_folder_copy = now.strftime("%Y%m%d_%H%M%S")
FOLDER_NAME = date_folder
BASE_FOLDER = FOLDER+date_folder
if os.path.exists(BASE_FOLDER) is False:
    os.mkdir(BASE_FOLDER)
else:
    BASE_FOLDER = FOLDER+date_folder_copy
    FOLDER_NAME = date_folder_copy
    os.mkdir(BASE_FOLDER)

#Connect to main page
hdr  = {'User-Agent': 'Mozilla/5.0'}
req  = Request(SITE,headers=hdr)
with urlopen(req) as page:
    soup = BeautifulSoup(page)
panecontent = soup.find(class_='view-content')
for url_link in panecontent.find_all('a', href=True):
    link_href = url_link['href']
    urls.append(BASE_SITE + link_href)
    folder_name_1 = link_href.replace("regulation-and-policy", "")
    folder_name_1 = folder_name_1.replace("/", "")
    os.mkdir(BASE_FOLDER + "/" + folder_name_1)
    cat_1.append(folder_name_1)
#Browse the categories found
browse_and_save(urls,1,'right')
