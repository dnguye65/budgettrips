from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

## Definition to navigate and search American Airlines website based on search parameters
## Not quite finished    
def aa_search(tripType, start, end, budget, passengers, depart, returnD):
    
    budget = budget * num
    
    ## Radio buttons are unable to be targeted at the moment. The webpage may
    ## not have time to load before the script begins searching for the Xpath.
    """if tripType == "One":
        WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="flightSearchForm.tripType.oneWay"]')))
        radio = driver.find_element_by_xpath('//*[@id="flightSearchForm.tripType.oneWay"]')
        radio.click()
    else:
        WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="flightSearchForm.tripType.roundTrip"]')))
        radio = driver.find_element_by_xpath('//*[@id="flightSearchForm.tripType.roundTrip"]')
        radio.click()
    driver.save_screenshot('radio.png')"""
    
    ## Makes sure the fields being targeted are clear before entering data
    ## Takes the parameters submitted and uses them to fill the Departure
    ## and arrival destination. Creates a screenshot in the working directory
    ## to make sure the input is valid
    driver.find_element_by_name("originAirport").clear()
    start = driver.find_element_by_name("originAirport")
    start.send_keys(startLoc)
    end = driver.find_element_by_name("destinationAirport")
    end.send_keys(endLoc)
    driver.save_screenshot("End Location.png")
    
    ## Targets the number of passengers text box and enters valid data
    ## sleep definition is so automation is not completed too quickly
    passengers = driver.find_element_by_name("adultOrSeniorPassengerCount")
    passengers.send_keys(num)
    time.sleep(2)
    
    ## Date user intends to leave on. As a note, need to make sure to format date
    ## strings for websites
    depart = driver.find_element_by_name("departDate")
    depart.send_keys(leaveDate)
    time.sleep(2)
    
    ## Date user intends to return by if a round trip is chosen.
    ## This will eventually be contained in an if block to determine
    ## if a round trip is desired once radio button functionality is ensured
    returnD = driver.find_element_by_name("returnDate")
    returnD.send_keys(returnDate)
    time.sleep(2)
        
    ## Again, creates an image of the completely filled form to ensure the data is
    ## valid
    driver.save_screenshot("fill.png")
    
    ## Xpath for the submit button
    submit = driver.find_element_by_xpath('//*[@id="flightSearchForm.button.reSubmit"]')
    submit.click()
    
    ## Ensures the next page loads before anymore manipulation is done. Can possibly
    ## be lowered a couple seconds.
    time.sleep(15)
    driver.save_screenshot("submit.png")
    try:
        showMore = driver.find_element_by_xpath('//*[@id="showMoreLink"]')
    except:
        log_error("Search Query Unavailable")
        return []
    
    i = 0
    while i < 10:
        try:
            showMore.click()
        except:
            break
    
    flightTable = driver.find_element_by_xpath('/html/body/main/div/section[2]/div[4]/ul')
    flightList = flightTable.find_elements_by_tag_name('li')
    flightSlice = []
    
    i = 1
    while i < (len(flightList) - 1):
        index = str(i)
        if int(driver.find_element_by_xpath('/html/body/main/div/section[2]/div[4]/ul/li['+index+']/div/div[2]/div/div[1]/button/span[1]/span[2]/span').text) <= budget:
            try:
                flightSlice.append({'Airline': 'American Airlines',
                                    'Price': '$'+driver.find_element_by_xpath('/html/body/main/div/section[2]/div[4]/ul/li['+index+']/div/div[2]/div/div[1]/button/span[1]/span[2]/span').text,
                                    'Departure Time': driver.find_element_by_xpath('/html/body/main/div/section[2]/div[4]/ul/li['+index+']/div/div[1]/div/div[2]/div[1]/span').text,
                                    'Arrival Time': driver.find_element_by_xpath('/html/body/main/div/section[2]/div[4]/ul/li['+index+']/div/div[1]/div/div[2]/div[3]/span').text})
            except:
                None
        i = i + 1
    
    ## closes the browser. May need to be moved outside of definitions based on how it interacts with
    ## the website
    return flightSlice
## Definition to navigate and search Alaskan Airlines based on parameters
## Currently is able to find and list the price of each flight based on the search parameters
## To add: Scrape times and possible overlays
def alaskan_airlines_search(tripType, start, end, budget, passengers, depart, returnD):
    
    ## A large block of this code is almost exactly the same as the aa_search definition.
    ## The only differences are the element names and Xpaths
    driver.save_screenshot("Alaskan_test.png")
    tripType = driver.find_element_by_name("IsOneWay")
    tripType.click()
    
    start = driver.find_element_by_name("DepartureCity1")
    start.send_keys(startLoc)
    end = driver.find_element_by_name("ArrivalCity1")
    end.send_keys(endLoc)
    driver.save_screenshot("End Location_Alaskan.png")

    passengers = driver.find_element_by_name("AdultCount")
    passengers.send_keys(num)
    
    driver.find_element_by_name("DepartureDate1").clear()
    depart = driver.find_element_by_name("DepartureDate1")
    depart.send_keys(leaveDate)

    ## Commented out the return date field manipulation until the
    ## interaction with radio buttons can be ensured
    """driver.find_element_by_name("ReturnDate").clear()
    returnD = driver.find_element_by_name("ReturnDate")
    returnD.send_keys(returnDate)
    time.sleep(2)"""
    
    driver.save_screenshot("fillAlaskan.png")
    
    submit = driver.find_element_by_xpath('//*[@id="findFlights"]')
    submit.click()
    time.sleep(10)
    driver.save_screenshot("submit_Alaskan.png")
    
    ## If there are no flights, simply prints the message and exits the definition.
    ## Might be a good idea to add something more meaniful here once the base of the script is built
    ## and tested with the website.
    try:
        driver.find_element_by_class_name('FlightCell')
    except:
        print("There are no flights")
        return
    
    ## Targets the table which contains a record of all flights found through the search and
    ## populates a list with WebElement objects for each flight found. Used to determine how many
    ## flights there are and how many prices expected to be added to the priceList list object    
    flightTable = driver.find_element_by_id('MatrixTable0')
    flightList = flightTable.find_elements_by_tag_name('tr')
    
    ## Based on the amount of flights found, the script will pull the price of each one and add it to the
    ## priceList list object. Then based on the budget of the user, only those that fall within the desired
    ## value will be considered to be displayed. If the budget is met, it will record the flight leave time,
    ## flight arrival time, and price into another list to be displayed to the user
    i=1
    layover = False
    layover2 = False
    flightSlice = []
    
    while i < (len(flightList) - 1):
        index = str(i)
        
        if int(driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[3]/div/label').text.strip('$')) <= budget:
            
            ## Issues a try; catch block to determine if there is a layover for this flight. If this Xpath is found, then it means this
            ## flight has a lay over and the flightSlice will need to reflect that. Otherwise, the flightSlice will just indicate
            ## a departure and arrival time.
            try:
                driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[1]/ul/li[2]/div/div[7]')
                layover = True
                try:
                    driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[1]/ul/li[3]/div/div[7]')
                    layover2 = True
                except:
                    layover2 = False
            except:
                layover = False
            
            if layover == True and layover2 == False:
                flightSlice.append({"Airline": "Alaska Airlines",
                                    "Price": "$"+driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[3]/div/label').text.strip('$'), 
                                    "Leave Time ": driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[1]/ul/li[1]/div/div[7]').text, 
                                    "Layover Arrival Time": driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[1]/ul/li[1]/div/div[9]').text,
                                    "Layover Airport": driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[1]/ul/li[1]/div/div[8]').text,
                                    "Layover Departure Time": driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[1]/ul/li[2]/div/div[7]').text,
                                    "Destination Arrival Time": driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[1]/ul/li[2]/div/div[9]').text})
            elif layover == True and layover2 == True:
                flightSlice.append({"Airline": "Alaska Airlines",
                                    "Price": driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[3]/div/label').text, 
                                    "Leave Time ": driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[1]/ul/li[1]/div/div[7]').text, 
                                    "First Layover Arrival Time": driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[1]/ul/li[1]/div/div[9]').text,
                                    "First Layover Destination": driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[1]/ul/li[1]/div/div[8]').text,
                                    "First Layover Departure Time": driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[1]/ul/li[2]/div/div[7]').text,
                                    "Second Layover Arrival Time": driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[1]/ul/li[2]/div/div[9]').text,
                                    "Second Layover Destination:": driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[1]/ul/li[2]/div/div[8]').text,
                                    "Second Layover Departure Time": driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[1]/ul/li[3]/div/div[7]').text,
                                    "Destination Arrival Time": driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[1]/ul/li[3]/div/div[9]').text})
            else:
                flightSlice.append({"Airline": "Alaska Airlines",
                                    "Price": driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[3]/div/label').text.strip('$'), 
                                    "Leave Time": driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[1]/ul/li[1]/div/div[7]').text, 
                                    "Arrival Time": driver.find_element_by_xpath('/html/body/div[6]/div[4]/div/form/div[6]/table/tbody/tr['+index+']/td[1]/ul/li[1]/div/div[9]').text})
                
        i = i + 1

    ## This can be used as an example to print a specific value from the hash table
    """i = 0 
    while i < (len(flightSlice)):
        print(flightSlice[i]["Price"])
        i = i + 1"""
    
    return flightSlice



## Intended to log errors during run time. Will need to add more functionality for
## this to be useful
def log_error(e):
    print(e)

## Static variables to test the script with until it is connected to the webpage
## and is able to pull from user entered information. One thing I would like to note, while 
## Looking through flight websites, is that most of them use three letter airport codes when
## searching for departure and arrival destinations. It may be wise to create a function in the web
## site that can either predict or suggest these codes to the user.
RoundOrOne = "One"
startLoc = "CLT"
endLoc = "LAS"
num = 2
budget = 300
leaveDate = "1/21/2020"
returnDate = "1/25/2020"
allFlights = []

## Creates an instance of the browser in the background
options = Options()
options.headless = True

## Will use the geckodriver.exe found within the working directory to open
## an instance of FireFox. This can also be changed to use the Chrome browser
## or IE browser if needed.
driver = webdriver.Firefox(options=options)
driver.set_window_position(0, 0)
driver.set_window_size(1920, 1080)


driver.get("https://www.aa.com/homePage.do")
time.sleep(5)
allFlights.append(aa_search(RoundOrOne, startLoc, endLoc, budget, num, leaveDate, returnDate))

## Gives the website some time to breath when running the script multiple times in a row.
## Opens the homepage of Alaskan Airlines and also creates a screenshot to ensure
## it is actually opening the correct page.
driver.get("https://www.alaskaair.com/")
time.sleep(3)
driver.save_screenshot('homepage.png')

## Executing the Alaskan Airlines search definition with parameters
allFlights.append(alaskan_airlines_search(RoundOrOne, startLoc, endLoc, budget, num, leaveDate, returnDate))


#driver.get("https://www.jetblue.com/flights")
#time.sleep(3)
#driver.save_screenshot("homepage.png")
#allFlights.append(sw_search(RoundOrOne, startLoc, endLoc, budget, num, leaveDate, returnDate))


## Populates a list with a 2 dimensional array of all searched sites
i = 0
while i < len(allFlights):
    print("Flight Search "+str(i+1))
    print("")
    x = 0
    while x < len(allFlights[i]):
        print(allFlights[i][x])
        print("")
        x = x + 1
    i = i + 1
driver.close()

