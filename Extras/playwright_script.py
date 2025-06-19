# Justin Maxwell - 3.21.25 
# DESCRIPTION: The python code to automate uploading disclosures into FirstIgnite, generating the report
# Then taking the summary and formatting it in a google doc and exporting as a PDF


# Clean up, turn into better functions
# remove the sections that add the section name (do that in the template)
# 



# Import the necessary module from Playwright and others
from playwright.sync_api import *
import re
from time import sleep
from formatting_functions import * # the other functions that gets the file name and just returns the number values (2022-004)
from create_pdf import * # the other function I made that makes the pdf
import glob # to loop through the files in the folder
import os
from datetime import datetime
from contactLink import *
from tagFinder import *



# Folder containing the disclosures
disclosures_folder = r"C:\Users\justi\Desktop\Desktop\Justin\Coding Projects\Automation\Disclosures"

# Get all PDF files
pdfFiles = glob.glob(os.path.join(disclosures_folder, "*.pdf"))

# Function that opens the Chrome browser, goes to FirstIgnite, uploads the disclosure (in a for loop), and calls the function to create the sell sheet pdf
def run(playwright: Playwright) -> None:
    bContinue = True
    while bContinue == True :

        # Opens the browser     
        browser = p.chromium.launch_persistent_context(
            user_data_dir=chrome_user_data_path,  # Use your existing Chrome profile
            headless=False,  # Set to False so you can see the browser window
            args=["--disable-blink-features=AutomationControlled"]  # Helps bypass bot detection
        )

        # for loop that goes through each disclosure pdf in the folder
        for filePath in pdfFiles :
        
            try : 
                sFileName = os.path.basename(filePath)
                
                # Open a new page (tab) in the browser
                page = browser.new_page()

                # Navigate to the website you want to automate
                page.goto("https://app.firstignite.com/autopilot")

                page.locator("div").filter(has_text=re.compile(r"^TextFile$")).locator("label span").click()
                sleep(3)
                # page.locator("section").filter(has_text="Drop your file here or click").click()
                page.get_by_role("textbox", name="󰕒 Drop your file here or").set_input_files(filePath) # uploads the file being used in the for loop
                page.get_by_text("Launch 🚀").click() # launches
                sleep(60) # waits for it to load
                page.locator("#Summary-label").click(timeout=300*1000) # locates where all the text is
                
                # locates where the text is then gets it
                summaryText = page.locator(".editor__content").text_content()

                # tuple that separates each section into parts
                formattedOut = re.findall("Title:(.+)Category:.+Executive Statement:(.+)Description:(.+)Key Advantages:(.+)Problems Solved:(.+)Market Applications:(.+)",summaryText)[0]

                # creates the Cleaned ID --> goes from "2023-004redacted" to "2023-004"
                sCleanID = output_name(sFileName)

                # assigns the tuple value to these variables
                sTitle = formattedOut[0]
                sExecutiveStatement = formattedOut[1]
                sDescription = formattedOut[2]
                sAdvantages = formattedOut[3]
                sProblemsSolved = formattedOut[4]
                sMarketApplications = formattedOut[5]

                # splits the tuple by each period to add to each list to be made into buller points in create_pdf()
                lstAdvantages = [
                    item.strip() 
                    for item in re.sub(r"([a-z])([A-Z])", r"\1. \2", sAdvantages).split(".") 
                    if item.strip()
                ]

                lstProblemsSolved = [
                    item.strip() 
                    for item in re.sub(r"([a-z])([A-Z])", r"\1. \2", sProblemsSolved).split(".") 
                    if item.strip()
                ]

                lstMarketApplications = [
                    item.strip() 
                    for item in re.sub(r"([a-z])([A-Z])", r"\1. \2", sMarketApplications).split(".") 
                    if item.strip()
                ]


                # calls the create_pdf function
                create_pdf(sTitle, sCleanID, sExecutiveStatement, sDescription, lstAdvantages, lstProblemsSolved, lstMarketApplications)
                page.close() # closes the page/tab after it runs the whole thing

            except :
                print("PDF not created")

            # The code that puts this information into Brightspot now.
            # Opens brightspot
        
            page1 = browser.new_page()
            page1.goto("https://brightspot.byu.edu/cms/logIn.jsp?returnPath=%2Fcms%2Findex.jsp")


            # My username and password
            # REMOVE WHEN PUT ON GITHUB!!!
            userUsername = "justmax"
            userPassword = "newJustinpW10854$"

            try: # Logs into the Brightspot
                page1.get_by_role("link", name="Log in to BYU", exact=True).click()
                page1.get_by_role("textbox", name="Net ID").click()
                page1.get_by_role("textbox", name="Net ID").fill(userUsername)
                page1.get_by_role("textbox", name="Password").click()
                page1.get_by_role("textbox", name="Password").fill(userPassword)
                page1.get_by_role("button", name="Sign In").click()

                sleep(5)
            except:
                pass

            # Opens the template
            page1.get_by_role("link", name="Technology Page Template").click()
            sleep(5)

            # Display Name and Internal Name
            try: 
                page1.get_by_role("textbox", name="Display Name").click()
                page1.get_by_role("textbox", name="Display Name").press("ControlOrMeta+a")
                page1.get_by_role("textbox", name="Display Name").fill(f'{sTitle}')
                page1.get_by_role("textbox", name="Internal Name").click()
                page1.get_by_role("textbox", name="Internal Name").press("ControlOrMeta+a")
                page1.get_by_role("textbox", name="Internal Name").fill(f"{sTitle} ID: {sCleanID}")
            except :
                lstNotMade.append(f"{sCleanID}'s Title or display name was not made.")
                
            # First Rich Text Box with the tech name and ID and executive statement
            try :
                page1.locator(".repeatableLabel").first.click()
                page1.get_by_role("list").filter(has_text="Rich Text: (RichText)").locator("bsp-line").click()
                page1.locator("div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").fill(f"{sTitle} ID: {sCleanID}")
                page1.locator("div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").press("ControlOrMeta+Shift+ArrowUp")
                page1.get_by_role("link", name="H2").nth(1).click()
                
                page1.locator(".is-collapsed > .repeatableLabel").first.click()
                
                page1.locator("bsp-line").nth(2).click()
                page1.locator("li:nth-child(2) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").fill(f"{sExecutiveStatement}")
                page1.locator("li:nth-child(2) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").press("ControlOrMeta+Shift+ArrowUp")
                page1.get_by_role("link", name="H4").nth(2).click()
                page1.locator("li:nth-child(4) > .repeatableLabel").click()
            except :
                lstNotMade.append(f"{sCleanID}'s Title or executive statement was not made")

            
            # Technology Overview
            try :
                page1.locator("bsp-line").nth(3).click()
                page1.locator("li:nth-child(4) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").fill("Technology Overview")
                page1.locator("li:nth-child(4) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").press("ControlOrMeta+Shift+ArrowUp")
                page1.get_by_role("link", name="H4").nth(3).click()
                page1.locator("li:nth-child(5) > .repeatableLabel").click()
                page1.locator("bsp-line").nth(4).click()
                page1.locator("li:nth-child(5) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").fill(f"{sDescription}")
            except :
                lstNotMade.append(f"{sCleanID}'s description wasn't made")
                
            # Key Advantages Label
            try :
                page1.locator("li:nth-child(7) > .repeatableLabel").click()

                page1.get_by_role("list").filter(has_text="Rich Text: (RichText)").locator("bsp-line").nth(4).click()
                
                page1.locator("li:nth-child(7) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").fill("Key Advantages")
                page1.locator("li:nth-child(7) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").press("ControlOrMeta+Shift+ArrowUp")
                page1.locator("li:nth-child(7) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirrorToolbar > ul > li:nth-child(31) > .rte2-toolbar-custom").click()
                
            except TimeoutError: 
                pass

            try: 
                page1.locator("li:nth-child(8) > .repeatableLabel").click()
                page1.locator("li:nth-child(8) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror > bsp-line").click()
                page1.locator("li:nth-child(8) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirrorToolbar > ul > li:nth-child(7) > .rte2-toolbar-ul").click()

                # Bullet point Key Advantages
                if len(lstAdvantages) == 2 :
                    page1.locator("li:nth-child(8) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").fill(f"{lstAdvantages[0]}\n{lstAdvantages[1]}")
                elif len(lstAdvantages) == 3 :
                    page1.locator("li:nth-child(8) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").fill(f"{lstAdvantages[0]}\n{lstAdvantages[1]}\n{lstAdvantages[2]}")
                else :
                    page1.locator("li:nth-child(8) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").fill(f"{lstAdvantages[0]}\n{lstAdvantages[1]}\n{lstAdvantages[2]}\n{lstAdvantages[3]}")
            except TimeoutError:
                lstNotMade.append(f"{sCleanID}'s list of advantages wasn't made")


            # Problems Addressed Label
            try :
                page1.locator("li:nth-child(9) > .repeatableLabel").click()
                page1.locator("li:nth-child(9) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror > bsp-line").click()
                page1.locator("li:nth-child(9) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").fill("Problems Addressed")
                page1.locator("li:nth-child(9) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").press("ControlOrMeta+Shift+ArrowUp")
                page1.locator("li:nth-child(9) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirrorToolbar > ul > li:nth-child(31) > .rte2-toolbar-custom").click()
            except TimeoutError: 
                pass

            try :  
                page1.locator("li:nth-child(10) > .repeatableLabel").click()
                page1.locator("li:nth-child(10) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror > bsp-line").click()
                page1.locator("li:nth-child(10) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirrorToolbar > ul > li:nth-child(7) > .rte2-toolbar-ul").click()
                
                # Bullet points for Problems Addressed
                if len(lstProblemsSolved) == 2 :
                    page1.locator("li:nth-child(10) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").fill(f"{lstProblemsSolved[0]}\n{lstProblemsSolved[1]}")
                elif len(lstProblemsSolved) == 3 :
                    page1.locator("li:nth-child(10) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").fill(f"{lstProblemsSolved[0]}\n{lstProblemsSolved[1]}\n{lstProblemsSolved[2]}")
                else :
                    page1.locator("li:nth-child(10) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").fill(f"{lstProblemsSolved[0]}\n{lstProblemsSolved[1]}\n{lstProblemsSolved[2]}\n{lstProblemsSolved[3]}")
            except :
                lstNotMade.append(f"{sCleanID}'s list of problems solved wasn't made")               
                
            # Market Applications Label
            try :
                page1.get_by_text("Rich Text: (RichText) Untitled").nth(1).click()
                
                page1.locator("li:nth-child(12) > .repeatableLabel").click()
                page1.locator("li:nth-child(12) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror > bsp-line").click()
                page1.locator("li:nth-child(12) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").fill("Market Applications")
                page1.locator("li:nth-child(12) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").press("ControlOrMeta+Shift+ArrowUp")
                page1.locator("li:nth-child(12) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirrorToolbar > ul > li:nth-child(31) > .rte2-toolbar-custom").click()

            except TimeoutError:
                pass

            try : 
                page1.locator("li:nth-child(13) > .repeatableLabel").click()
                page1.locator("li:nth-child(13) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror > bsp-line").click()
                page1.locator("li:nth-child(13) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirrorToolbar > ul > li:nth-child(7) > .rte2-toolbar-ul").click()
                
                # Bullet points for market applications
                if len(lstMarketApplications) == 2 :
                    page1.locator("li:nth-child(13) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").fill(f"{lstMarketApplications[0]}\n{lstMarketApplications[1]}")
                    
                elif len(lstMarketApplications) == 3 :
                    page1.locator("li:nth-child(13) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").fill(f"{lstMarketApplications[0]}\n{lstMarketApplications[1]}\n{lstMarketApplications[2]}")
                else : 
                    page1.locator("li:nth-child(13) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").fill(f"{lstMarketApplications[0]}\n{lstMarketApplications[1]}\n{lstMarketApplications[2]}\n{lstMarketApplications[3]}")
            except :
                lstNotMade.append(f"{sCleanID}'s list of market applications wasn't made")      

            # Additional Information Label
            try :         
                page1.locator("li:nth-child(15) > .repeatableLabel").click()
                page1.locator("li:nth-child(15) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror > bsp-line").click()
                page1.locator("li:nth-child(15) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").fill("Additional Information")
                page1.locator("li:nth-child(15) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").press("ControlOrMeta+Shift+ArrowUp")
                page1.locator("li:nth-child(15) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirrorToolbar > ul > li:nth-child(31) > .rte2-toolbar-custom").click()
                page1.get_by_text("Rich Text: (RichText) Untitled").nth(1).click()
            except TimeoutError :
                pass
                
            try :
                page1.locator("li:nth-child(16) > .repeatableLabel").click()
                page1.locator("li:nth-child(16) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror > bsp-line").click()
                
                date_published = datetime.now().strftime("%d %B, %Y")  # Example: "21 April, 2025"
                
                page1.locator("li:nth-child(16) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirror").fill(f"Technology ID: {sCleanID}\nSell Sheet: Download the Sell Sheet here\nMarket Analysis: Contact us for a more in-depth market report\nDate Published: {date_published}")
            except :
                lstNotMade.append(f"{sCleanID}'s additional information section wasn't made")

            # Highlights the text to then upload and link the sell sheet
            try : 
                for iCount in range(0, 93) : # moves the cursor
                    page1.get_by_text(f"Technology ID: {sCleanID}Sell").press("ArrowLeft")
                
                for iCount in range (0, 28) : # highlights the text
                    page1.get_by_text(f"Technology ID: {sCleanID}Sell").press("Shift+ArrowLeft")

                # Uploads the PDF just made and links it
                page1.locator("li:nth-child(16) > .objectInputs > div:nth-child(3) > div:nth-child(2) > .ProseMirrorContainer > .ProseMirrorToolbar > ul > li:nth-child(24) > .brightspot-core-link-LinkRichTextElement").click()
                page1.get_by_role("link", name="(Required) search").click()
                page1.locator("div").filter(has_text=re.compile(r"^Article$")).nth(2).click()
                page1.get_by_role("textbox", name="Search", exact=True).press("ArrowDown")
                page1.get_by_role("textbox", name="Search", exact=True).press("Enter")
                page1.get_by_role("button", name="New").click()
                pdf_path = os.path.join(r"C:\Users\justi\Desktop\Desktop\Justin\Coding Projects\Automation\Exported Sell Sheets", f"{sCleanID} Sell Sheet.pdf")
                page1.get_by_role("textbox", name="Choose").set_input_files(pdf_path)
                sleep(5)
                page1.locator("form").filter(has_text=f"New Attachment: {sCleanID}-sell").locator("button[name=\"action-publish\"]").click()
                sleep(5)
                page1.get_by_text("Back", exact=True).click()
                sleep(3)
                firstNum, lastNum = sCleanID.split('-') # splits the sCleanID so I can get the last digits to be able to link it
                page1.get_by_role("link", name=f"-{lastNum}-sell-sheet.pdf").first.click()
                page1.get_by_role("button", name="Save & Close").click()

            except :
                print(f"{sCleanID}'s sell sheet wasn't linked.")

            # Chooses the correct year tag
            try : 
                # Depending on the year of the tech, chooses that Tag
                years = ["2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]
                yearTag = next((year for year in years if year in sCleanID), None)

                # Chooses the tags
                page1.get_by_role("link", name="search Tech 2024: Tag").click(timeout=300*10000)
                page1.get_by_role("link", name="chevron_right").click(timeout=300*10000)
                page1.get_by_role("link", name=f"Tech {yearTag}: Tag").click(timeout=300*10000)
                sleep(10)
            except :
                lstNotMade.append(f"{sCleanID}'s year tag wasn't added.")


            # changes the type of the tag after finding which tag was on the original tech page
            try :
                # tagTypes = [""]
                tagName = findTag(page, sCleanID)
                page1.get_by_role("link", name="search Engineering").click()
                page1.get_by_role("link", name=tagName).click()
                page1.get_by_title("Close", exact=True).click()

            except :
                pass

            
            # creates and inserts the link that pulls the tech name to the contact form
            try : 
                halfLink = page1.get_by_role("textbox", name="Internal Name").input_value()
                fullLink = f"https://techtransfer.byu.edu/contact?technology-id={halfLink}"
                insertNewLink(page, fullLink)
            except :
                pass

            try :
                # Goes to the Overrides tab and changes the techID
                page1.get_by_role("link", name="Overrides").first.click()
                page1.get_by_role("heading", name="Promo Module Overrides (").locator("div").click()
                page1.locator("div").filter(has_text=re.compile(r"^ID: 0000-000$")).fill(f"ID: {sCleanID}")
            except :
                lstNotMade.append(f"{sCleanID} override description not changed. ")

            # Publishes it
            try :
                page1.get_by_role("button", name="Publish").click()
                sleep(10)
                # browser.close()
                page1.close()

            except :
                print(f"{sCleanID} not published")

# makes the list that will get the list of ID's that did not work
lstNotMade = []
notMade = False

# Define the path to your Chrome user data directory.
# Replace "YourUsername" with your actual Windows username.
chrome_user_data_path = r"C:\Users\justi\AppData\Local\Google\Chrome\User Data\Profile 2"

# # # Start Playwright
# with sync_playwright() as p:
#     run(p)
