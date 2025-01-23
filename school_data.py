from playwright.sync_api import sync_playwright
import re
import tabula
import tempfile

def get_school_data():
   with sync_playwright() as p:
       browser = p.chromium.launch()
       page = browser.new_page()
       base_url = 'https://dhs.gov'
       page.goto(base_url + '/hsi/sevp/sevis-by-the-numbers')

       years = {}
       links = page.locator('a').all()
       for link in links:
           text = link.inner_text().lower()
           if 'school data for' in text:
               match = re.search(r'(\d{4})', text)
               if match:
                   years[int(match.group(1))] = link

       latest_link = years[max(years.keys())]
       page.goto(base_url + latest_link.get_attribute('href'))

       pdf_link = page.locator('a:text-matches(".*top 500 f-1 higher education.*", "i")').first
       with tempfile.NamedTemporaryFile(suffix='.pdf') as tf:
           with page.expect_download() as download_info:
               pdf_link.click()
           download = download_info.value
           download.save_as(tf.name)
           
           tables = tabula.read_pdf(tf.name, pages=1)
           if tables:
               print(tables[0].head(10))

       browser.close()

get_school_data()