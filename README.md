# web_dev_automation
Python automation script for BYU TTO

INSTRUCTIONS:

Download VS CODE: https://code.visualstudio.com/download
Download repository 
Place repository folder where you want it (and where you will never move it)

Download noto sans from google fonts:
https://fonts.google.com/noto/specimen/Noto+Sans?query=noto+sans
- and place in the fonts folder

FROM TERMINAL in VS CODE:
- pip install playwright
- playwright install
- pip install fpdf

CHANGE PYTHON INTERPRETER:
- ctrl + shift + p (windows) and choose python 3.11 (3.11.5 if it needs to be super specific)

In the CONFIG.PY FILE - update the following:
- disclosures_folder
- images_folder
- noto_sans_r
- noto_sans_b
- banner_path
- footer_banner_path
- export_folder

PREPARE TO RUN THE PROGRAM:
- put the disclosures (make sure they're OCR'd) into the disclosures folder

RUNNING THE CODE FOR THE FIRST TIME:
- the first time launching this, you will need to sign in to the FirstIgnite account manually
- for BRIGHTSPOT, it may have you do duo/confirm text message. You should only have to do that once each time you run the code



EXTRA TIPS TO MAKE SURE: 
- make sure that you installed the repository with correct version of python
- use "python -m venv .venv"
- then "source .venv/bin/activate"
- install playwright again using "pip install playwright" then "playwright install"
- then install fpdf with "pip install fpdf"


FOR TESTING:
- You can use the code below to test the brightspot functions without having to run the first ignite function every time
- It gives you all the variables you need to be able to run the brightspot functions
- you'll need to comment out the firstignite functions (lines 37-58)

# sCleanID = "2025-001"
# sTitle = 'Constitutively Active Death Receptor (CADRE)'
# sExecutiveStatement = 'A revolutionary anticancer therapeutic designed to specifically induce apoptosis in cancer cells.'
# sDescription = 'The Constitutively Active Death Receptor (CADRE) represents a novel approach to cancer therapy, utilizing ag modified death receptor that triggers apoptosis directly within cancer cells, bypassing common resistance mechanisms. This technology leverages a unique amino acid sequence and delivery system to target cancer cells selectively, minimizing harm to normal cells.'
# lstAdvantages = ['High specificity to cancer cells, reducing potential side effects', 'Overcomes resistance mechanisms present in traditional therapies', 'Applicability across a broad range of cancer types', 'Potential to complement existing treatments like chemotherapy and radiotherapy', 'Innovative delivery methods using bacterial vesicles and p', 'H-sensitive peptides enhance targeting capabilities']
# lstProblemsSolved = ['Resistance to traditional cancer therapies such as chemotherapy and radiotherapy', 'Non-specific targeting of cancer cells, leading to damage of healthy cells and tissues', 'Limited efficacy of current treatments across diverse cancer types']
# lstMarketApplications = ['Novel anticancer therapeutics', 'Complementary treatment to enhance efficacy of existing cancer therapies', 'Targeted cancer therapy research and development', 'Potential for personalized cancer treatment strategies']
# exportFolder = r"/Users/willy/Desktop/TTO/web_dev_automation-main/Exported Sell Sheets"
# sTypeTag = "Engineered Structures & Materials"


- If you want to go back and change previous pages:


Uncomment out line 70 ->

(try_function(bs_search_technology, page, sCleanID=sCleanID, func_name="bs_search_technology")) 

and comment out line 74 ->

(try_function(bs_template_click, page, sCleanID=sCleanID, func_name="bs_template_click"))

so that it searches for a technology rather than opening up a new template. 

Then comment out the first ignite stuff (lines 37-58) (so that it doesn't run the firstingite stuff)
Then comment out any of the brightspot functions you don't want to change 
    -> so if you only want to change the images, then make sure that is the only one uncommented so that it runs

Then put the disclosures of the pages you want to change in the disclosures folder (so if you need to change all the 2015 pages, put all the 2015 disclosures in the folder)
