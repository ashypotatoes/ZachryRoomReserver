from selenium import webdriver
# from selenium.webdriver.common.key import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


# asking user if they want to go with their preferences or not
pref = raw_input("Do you want to go with your set room type, time slot, and event name preferences or no? (Y or N)  ")
if(pref == "Y" or pref == "y"):
	# <<< ENTER YOUR PREFERRED RESERVATION ROOM TYPE: 1. "single, 2. "chevron/learning studio", or 3. "lobby/green space" (1, 2, or 3) >>>
	roomType = "1"
	# <<< ENTER YOUR PREFERRED TIME FRAME BELOW. TIME FRAME CANNOT EXCEED 2-HOUR RANGE PER 1 RESERVATION >>>
	startTime = "3:00 PM"
	endTime = "5:00 PM"
	# <<< ENTER YOUR PREFERRED RESERVATION NAME >>>
	eventName = "Event Name"

	# asking for date of reservation
	print('What day do you want the reservation? INPUT FORMAT: "DAY MM/DD/YYYY" ')
	print("'DAY' options: Mon, Tue, Wed, Thu, Fri, Sat, Sun")
	print('EXAMPLE:   "Fri 08/07/2020"')
	desiredDate = raw_input("Desired Date: ")
else:
	print("ROOM TYPE OPTIONS: 1. 'single', 2. 'chevron/learning studio', or 3. 'lobby/green space'")
	roomType = input("What type of room do you want? (1, 2, or 3)   ")

	print("RESERVATION TIME FRAME MUST BE WITHIN TWO HOURS MAX")
	startTime = input("What time do you want to start your reservation?   ")
	endTime = input("What time do you want to end your reservation?   ")

	# asking for date of reservation
	print('What day do you want the reservation? INPUT FORMAT: "DAY MM/DD/YYYY" ')
	print("'DAY' options: Mon, Tue, Wed, Thu, Fri, Sat, Sun")
	print('EXAMPLE:   "Fri 08/07/2020"')
	desiredDate = raw_input("Desired Date:   ")

	# asking for event name
	eventName = raw_input("Event Name:   ")


PATH = "/Library/Developer/CommandLineTools/usr/bin/chromedriver"	# <<< ENTER THE PATH OF YOUR CHROMEDRIVER FILE, EX: "/Library/Developer/CommandLineTools/usr/bin/chromedriver" >>>
driver = webdriver.Chrome(PATH)



driver.get("https://coe-ems-web01.engr.tamu.edu/")
loginUsername = driver.find_element_by_id("username")
loginPassword = driver.find_element_by_id("password")

# <<< ENTER YOUR LOGIN INFORMATION BELOW >>>
usernameInput = "johndoe@tamu.edu"
passwordInput = "password123"

# entering information into form and selecting submit
loginUsername.send_keys(usernameInput)
loginPassword.send_keys(passwordInput)
driver.find_element_by_xpath('//*[@id="fm1"]/button').click()

driver.switch_to_frame("duo_iframe")

# <<< ENTER YOUR PREFERRED AUTHENTICATION METHOD BELOW ("DUO push", "phone call", or "DUO code") >>>
authen = "DUO push"
if(authen == "DUO push"):
	driver.find_element_by_xpath('//*[@id="auth_methods"]/fieldset/div[1]/button').click()
elif(authen == "phone call"):
	driver.find_element_by_xpath('//*[@id="auth_methods"]/fieldset/div[2]/button').click()
elif(authen == "DUO code"):
	driver.find_element_by_xpath('//*[@id="auth_methods"]/fieldset/div[3]/button').click()

# letting browser wait until the "CREATE A RESERVATION" option is found
WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.ID, "sidebar-wrapper")))

# switching to reservation window
driver.find_element_by_xpath('//*[@id="sidebar-wrapper"]/ul/li[2]/a').click()

# letting browser wait until the "book now" option is found
WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[6]/div[2]/div/div[3]/div[2]/div/div/div[2]/div/div[1]/div[2]/button[1]')))

# selecting room type
if(roomType == "1"):
	driver.find_element_by_xpath('/html/body/form/div[6]/div[2]/div/div[3]/div[2]/div/div/div[2]/div/div[1]/div[2]/button[1]').click()
elif(roomType == "2"):
	driver.find_element_by_xpath('/html/body/form/div[6]/div[2]/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/button[1]').click()
elif(roomType == "3"):
	driver.find_element_by_xpath('/html/body/form/div[6]/div[2]/div/div[3]/div[2]/div/div/div[2]/div/div[3]/div[2]/button[1]').click()

# wait until "Date & Time" inputs are found on the page
WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.ID, "booking-date-input")))

# setting date of reservation based on user input
driver.find_element_by_xpath('//*[@id="booking-date-input"]').clear()
driver.find_element_by_xpath('//*[@id="booking-date-input"]').send_keys(desiredDate)

# setting time of reservation
driver.find_element_by_xpath('//*[@id="booking-start"]/input').clear()
driver.find_element_by_xpath('//*[@id="booking-start"]/input').send_keys(startTime)
driver.find_element_by_xpath('//*[@id="booking-end"]/input').clear()
driver.find_element_by_xpath('//*[@id="booking-end"]/input').send_keys(endTime)

# searching with desired booking information
driver.find_element_by_xpath('//*[@id="location-filter-container"]/div[2]/button').click()

# wait until the user is on the "Reservation Details" page
WebDriverWait(driver, 500).until(EC.visibility_of_element_located((By.ID, "event-name")))

# fill in event name
driver.find_element_by_xpath('//*[@id="event-name"]').send_keys(eventName)

# select option for drop down agreement
select = Select(driver.find_element_by_xpath('//*[@id="26"]'))
select.select_by_value("33")	# This is the option: "No more than one person will be in the room."

# click agree with terms
driver.find_element_by_xpath('//*[@id="terms-and-conditions"]').click()

# create the reservation
driver.find_element_by_xpath('//*[@id="details"]/div[3]/div/span[2]/button').click()

driver.close()









