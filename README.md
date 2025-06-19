# web_dev_automation
Python automation script for BYU TTO

INSTRUCTIONS:

Download VS CODE: https://code.visualstudio.com/download
Download repository 
Place folder where you want it (and where you will never move it)

Download noto sans from google fonts:
https://fonts.google.com/noto/specimen/Noto+Sans?query=noto+sans

FROM TERMINAL (go to terminal in the top menu bar of your computer if mac):
- import playwright (copy and paste "pip install playwright" into terminal)
- import FPDF (copy and paste "pip install pfdf" into terminal)

CHANGE FOLDER/FILE DESTINATIONs:
- disclosures_folder (main.py line 34)
- NotoSans font (create_pdf.py lines 46-47)
- banner_path (create_pdf.py line 60)
- footer_banner_path (create_pdf.py line 114)
- export_folder (create_pdf.py line 123)

USERNAME & PASSWORD:
- Option A: Hardcode your username and password and comment out line 52
- Option B: Keep as is so it asks you for your username and password each time

Put disclosures into disclosures folder and run it

LOGGING IN:
- the first time launching this, you will need to sign in to the FirstIgnite account manually
- for BRIGHTSPOT, it may have you do duo/confirm text message. You should only have to do that once.

MAKE SURE:
- make sure that you installed the repository with correct version of python
- use "python -m venv .venv"
- then "source .venv/bin/activate"
- use "which python" to make sure that you have the correct version dowloaded. It should say "(.venv)" at the beginning of the line of code
- install playwright again using "pip install playwright" then "playwright install"
- then install fpdf with "pip install fpdf"
