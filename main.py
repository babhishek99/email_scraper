from userInput import userInput
from scraperUtils import *
from excelOutput import excelOutput
import getpass

#Initializing User Input Object
user_obj = userInput()

#Asking for company list input (comma-seperated)
company_input = input("Enter companies as comma-seperated list:")
user_obj.set_companies(company_input)

#Asking for location list input (comma-seperated and Linkedin validated)
location_input = input("Enter locations as comma-seperated list:")
user_obj.set_locations(location_input)

#Asking for titles list input (comma-seperated)
title_input = input("Enter titles as comma-seperated list:")
user_obj.set_titles(title_input)

#Asking for Linkedin Authentication
username_input = input("Enter Linkedin username:")
password_input = getpass.getpass("Enter Linkedin password:")
user_obj.set_username(username_input)
user_obj.set_password(password_input)

#---------------------------------------------------------------------------------------------------#

excel_file = excelOutput("test.xlsx")

execute(excel_file, user_obj)


