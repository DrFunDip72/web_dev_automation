# Justin Maxwell

# The home file to call all the other functions from the other python files

# IMPORTS
from playwright.sync_api import * # necessary playwright import
import os # for file paths and getting file names
from user_input import *
from playwright_launcher import run # 
from first_ignite import *
from formatting_functions import *
from create_pdf import *
from brightspot_functions import *
from config import user_login, pdfFiles, logging, try_function, export_folder, disclosures_folder

image_input = input("Do you want to use images? (y/n): ").strip().lower()
tag_type_input = input("Do you want to use tag types? (y/n): ").strip().lower()

# --- GETS USER INPUT FOR TAG TYPES ---
if tag_type_input == 'y':
    tagTypeSelections = get_user_selections(disclosures_folder)

# --- GETS USER INPUT FOR BRIGHTSPOT LOGIN ---
userUsername, userPassword = user_login() # Gets the username and password for the Brightspot login

# --- PLAYWRIGHT SESSION ---
with sync_playwright() as p:
    browser, page = run(p)

    for filePath in pdfFiles:
        try:
            # # --- GET CLEAN ID ---
            sFileName = os.path.basename(filePath)
            sCleanID = get_clean_id(sFileName)
            sleep(3)

            # # --- FIRST IGNITE
            try:
                page = browser.new_page()
                page.goto("https://app.firstignite.com/autopilot")
                extractedSummaryText = launch_first_ignite(page, filePath) #  comment out when uncommenting the testing comment section below
            except Exception as e:
                logging.warning(f"{sCleanID} - launch_first_ignite failed: {str(e)}")
                continue
            
            # # --- DATA EXTRACTION & PDF CREATION ---
            print("enter")
            try:
                sTitle, sExecutiveStatement, sDescription, lstAdvantages, lstProblemsSolved, lstMarketApplications = format_summary(extractedSummaryText) # comment this one out as well when using the above testing comments
                sleep(3)
                create_pdf(sTitle, sCleanID, sExecutiveStatement, sDescription, lstAdvantages, lstProblemsSolved, lstMarketApplications)
            except TimeoutError as e:
                logging.warning(f"{sCleanID} - format_summary or create_pdf failed: {str(e)}")
                continue  # Skip this file if critical data missing
            except Exception as e:
                logging.warning(f"{sCleanID} - something broke when making pdf: {str(e)}")
                raise e 

            print("exit first ignite")
            # --- BRIGHTSPOT WORKFLOW ---
            try:
                page.goto("https://brightspot.byu.edu/cms/logIn.jsp?returnPath=%2Fcms%2Findex.jsp")
                sleep(3)
                bs_login(page, userUsername, userPassword)
            except Exception as e:
                logging.warning(f"{sCleanID} - bs_login failed: {str(e)}")
                raise e
            print("exit brightspot login")

            # --- SEARCH FOR TECHNOLOGY ---
            # try_function(bs_search_technology, page, sCleanID=sCleanID, func_name="bs_search_technology")

            # --- BRIGHTSPOT FUNCTIONS (INDIVIDUAL TRY) ---
            try_function(bs_template_click, page, sCleanID=sCleanID, func_name="bs_template_click")
            try_function(bs_display_internal_name, page, sTitle, sCleanID, sCleanID=sCleanID, func_name="bs_display_internal_name")
            try_function(bs_title_techID, page, sTitle, sCleanID, sCleanID=sCleanID, func_name="bs_title_techID")
            try_function(bs_executive_statement, page, sExecutiveStatement, sCleanID=sCleanID, func_name="bs_executive_statement")
            if image_input == 'y':
                try_function(bs_image_main_page, page, sCleanID, sCleanID=sCleanID, func_name="bs_image_main_page")
            try_function(bs_technology_overview, page, sDescription, sCleanID=sCleanID, func_name="bs_technology_overview")
            try_function(bs_key_advantages, page, lstAdvantages, sCleanID=sCleanID, func_name="bs_key_advantages")
            try_function(bs_problems_addressed, page, lstProblemsSolved, sCleanID=sCleanID, func_name="bs_problems_addressed")
            try_function(bs_market_applications, page, lstMarketApplications, sCleanID=sCleanID, func_name="bs_market_applications")
            try_function(bs_additional_information, page, sCleanID, sCleanID=sCleanID, func_name="bs_additional_information")
            try_function(bs_upload_pdf, page, sCleanID, export_folder, sCleanID=sCleanID, func_name="bs_upload_pdf")
            try_function(bs_year_tag, page, sCleanID, sCleanID=sCleanID, func_name="bs_year_tag")
            if tag_type_input == 'y':
                try_function(bs_type_tag, page, sCleanID, tagTypeSelections, sCleanID=sCleanID, func_name="bs_type_tag")
            try_function(bs_contact_link, page, sCleanID=sCleanID, func_name="bs_contact_link")
            try_function(bs_override_description, page, sCleanID, sCleanID=sCleanID, func_name="bs_override_description")
            if image_input == 'y':
                try_function(bs_override_image, page, sCleanID, sCleanID=sCleanID, func_name="bs_override_image")
            print("Everything done. Ready to publish.")
            try_function(bs_publish, page, sCleanID=sCleanID, func_name="bs_publish")

            # Closes the page
            page.close()
  
        except Exception as e:
            # Catches if anything fatally wrong happens per disclosure
            logging.warning(f"{sCleanID} - Fatal error in main loop: {str(e)}")
            page.close()
            raise e
