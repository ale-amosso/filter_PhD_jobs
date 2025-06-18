from bs4 import BeautifulSoup
from datetime import datetime
import requests
import webbrowser
import os
from dateutil import parser
import time

# KEYWORDS FOR THE FILTER
keywords = ["dark matter", "cosmology", "astroparticles", "theory"]

# URL of RSS (xml) from AcademicJobsOnline
url_xml = "https://academicjobsonline.org/ajo?joblist-0-0-0-0----rss--"

# PATHS
this_folder_path= os.path.dirname(__file__) 
output_path = os.path.join(this_folder_path, "output.html")

def main():
    
    items= download_xml_content(url_xml)

    html_content= build_html(items)

    print_output_file(html_content)

    open_output_file()



def download_xml_content(url_xml):

    response = requests.get(url_xml)
    if response.status_code != 200:
        raise Exception(f"Error during the download: {response.status_code}")
    
    # Use XML content as string text
    raw_xml = response.text

    soup = BeautifulSoup(raw_xml, "xml") # Library used for avoiding errors due to the "&" characters containted in the description field
    items = soup.find_all("item")
    print(f"{len(items)} items found in total.")

    return items



def build_html(items):

    html_blocks = []

    for item in items:
        title = item.title.get_text(strip=True)
        link = item.link.get_text(strip=True)
        description = item.description.get_text(" ", strip=True).lower()

        tag_elem = item.find("ads:Tag")
        tag = tag_elem.get_text(strip=True).lower() if tag_elem else ""
        if "phd" not in tag:
            continue

        if not any(k in description for k in keywords):
            continue

        country_elem= item.find("ads:Country")
        country_str= country_elem.text.strip() if country_elem else "N/A"

        university_elem= item.find("ads:Univ")
        university_str= university_elem.text.strip() if university_elem else "N/A"

        dep_elem= item.find("ads:Dept")
        dep_str= dep_elem.text.strip() if dep_elem else "N/A"  

        deadline_elem = item.find("ads:Deadline")
        deadline_str= convert_deadline_format(deadline_elem)

        html_block = f"""
        <h2>🎓 {title}</h2>
        <p style="margin-bottom: 6px;"><strong>University:</strong> {university_str} - {dep_str} ({country_str})</p>
        <p style="margin-bottom: 6px;"><strong>Deadline:</strong> {deadline_str}</p>
        <p><strong>Link:</strong> <a href="{link}" target="_blank">{link}</a></p>
        <hr>
        """


        html_blocks.append(html_block)

    # HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>PhD Job List - Dark Matter</title>
    </head>
    <body style="font-family:sans-serif; padding:20px; max-width:800px; margin:auto;">
        <h1>🔭 PhDs for Dark Matter and Cosmology</h1>
        {''.join(html_blocks)}
    </body>
    </html>
    """
    return html_content

def print_output_file(html_content):
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def open_output_file():
    timestamp = int(time.time())
    webbrowser.open(f"file://{output_path}?t={timestamp}") # Added timestamp to avoid caching issues

    print(f"File HTML has been generated: {output_path}")

def convert_deadline_format(deadline_elem):
    if deadline_elem:
        raw_date = deadline_elem.text.strip()
        try:
            dt = parser.parse(raw_date)
            deadline_str = dt.strftime("%d %b %Y")
        except Exception:
            deadline_str = raw_date
    else:
        deadline_str = "N/A"
    return deadline_str


if __name__ == "__main__":
    main()