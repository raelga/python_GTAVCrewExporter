#!/usr/bin/python


#### Import modules
from selenium import selenium
from selenium import webdriver
import sys, time, re, string, getopt

#### Constants
default_crew = 'elotrolado'
login_url = 'https://socialclub.rockstargames.com/profile/signin'
base_crew_url = 'http://socialclub.rockstargames.com/crew'
path_online_url = '/games/gtav/career/overview/gtaonline'

#### Global
username = ''
password = ''
crew_name = ''
output_file = ''
verbose_flag = '1'

#### Class definition
class crew_member:
    def __init__(self):
        self.id = ''
        self.psn = ''
        self.url = ''
        self.playtime = ''
        self.language = ''
        self.rank = ''

#### Function definitions

def arg_parser(argv):
    global crew_name
    global username
    global password
    global output_file
    try:
        opts, args = getopt.getopt(argv,"hvu:p:c:o:",["verbose","username","password","crew=","ofile="])
    except getopt.GetoptError:
        print 'gtav_crew_exporter.py -c <crew_name> [-u <username> -p <password>] [-o <output_file>] [-v]'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'gtav_crew_exporter.py -c <crew_name> [-u <username> -p <password>] [-o <output_file>] [-v]'
            sys.exit()
        elif opt in ("-c", "--crew"):
            crew_name = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
        elif opt in ("-v", "--verbose"):
            verbose_flag = 1
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg

    if not crew_name:
        crew_name = default_crew
    print 'Crew: ' + crew_name

    if output_file:
        print 'Output file : ' + output_file

    return 0

def debug(msg):
    global verbose_flag
    if verbose_flag: print 'DBG : ' + msg

def WaitForElement(webdriver, path):
    limit = 10   # waiting limit in seconds
    inc = 1   # in seconds; sleep for 500ms
    c = 0
    while (c < limit):
        try:
            webdriver.find_element_by_xpath(path)
            return 1        # Success
        except:
            time.sleep(inc)
            c = c + inc 
 
    # print sys.exc_info()
    return 0   

####
def LoginSocialClub(driver):

    if not username or not password:
        print 'Without login and password, only username and rank are available:'
        for cm in crew_members:
            print cm.rank + ", " + cm.id + ", " + cm.url

        sys.exit('You need to provide login information to view each member info.')

    driver.get(login_url)
        
    path = '//*[@id="submitBtn"]'
    result = WaitForElement(driver, path)

    if not result:              # interprets returned value
    #        driver.close()
        sys.exit("\nThe page is not loaded yet.")
    else:
        debug('web - page fully loaded!')

    path='//input[@id="login-field"]'
    driver.find_element_by_xpath(path).clear()
    driver.find_element_by_xpath(path).send_keys(username)

    path='//input[@id="password-field"]'
    driver.find_element_by_xpath(path).clear()
    driver.find_element_by_xpath(path).send_keys(password)

    path = '//*[@id="submitBtn"]'
    driver.find_element_by_xpath(path).click()

    return 0
#### 
def GetMembersList(driver):

    crew_url = base_crew_url + '/' + crew_name + '/hierarchy'
    driver.get(crew_url)
        
    path = '//*[@id="muscleList"]'
    result = WaitForElement(driver, path)

    if not result:              # interprets returned value
    #        driver.close()
        sys.exit("\nThe page is not loaded yet.")
    else:
        debug('web - page fully loaded!')
        

    path = '//a[@data-ga="footer_selectlanguage_en"]'
    viewall = driver.find_element_by_xpath(path)

    if not viewall:
        debug("meh.")
    else:
        debug("web - set page in english.")
    #    viewall.click()

    path = '//a[@class="viewAll"]'
    viewall = driver.find_element_by_xpath(path)

    if not viewall:
        debug("web - all users visible.")
    else:
        debug("web - unfold users.")
        viewall.click()

    path = '//div[contains(@id, "crewRank_")]'
    hierarchy = driver.find_elements_by_xpath(path)

    crew_members = list()

    for rank in hierarchy:

    #    print rank.get_attribute('id')
        path = '//div[@id="' + rank.get_attribute('id') + '"]//i[@class="icon-info"]'
        rank_name = rank.find_element_by_xpath(path).get_attribute('data-name')
        
    #    print rank_name

        path = '//div[@id="' + rank.get_attribute('id') + '"]//ul[@id="' + rank_name + 'List"]//div[@class="member"]//img'
        members = rank.find_elements_by_xpath(path)

        for member in members:
            
            cm = crew_member()
            cm.id = member.get_attribute('data-original-title')
            cm.url = member.find_element_by_xpath('..').get_attribute('href')
            cm.rank = rank_name

            crew_members.append(cm)

    return crew_members

#### Function definitions
def GetMemberInfo(driver, profile_url):
    
    # print sys.exc_info()
    return 0   

#### Main function

if __name__ == "__main__":
    arg_parser(sys.argv[1:])

    debug('web - starting browser')
    driver = webdriver.Firefox()

    crew_members = GetMembersList(driver)
    #print 'Loaded :' + len(crew_members) + 'members'
    print len(crew_members)

    LoginSocialClub(driver)
    

#### Log into social club

    sys.exit()


    #    driver.close()

        #elem = driver.find_element_by_id('viewall')  # Find the muscle list
        #elem = driver.find_element_by_name('muslceList')  # Find the muscle list
        #elem.send_keys('seleniumhq' + Keys.RETURN)

    #	driver.quit()



    # Grab URL
    #url = str(sys.argv[1])
    # Check if it's malformed
    #regex = re.compile(
    #        r'^(?:http|ftp)s?://' # http:// or https://
    #        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    #        r'localhost|' #localhost...
    #        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    #        r'(?::\d+)?' # optional port
    #        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    #vurl = regex.match(url)
    #if vurl:
    #	print ("Good url : %s" % url)
    #else:
    #	sys.exit ("Malformed url : %s" % url)