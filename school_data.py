# from playwright.sync_api import sync_playwright 
# import re 
# import tabula 
# import tempfile 
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import os

# def get_school_data():
#     with sync_playwright() as p:
#         browser = p.chromium.launch()
#         page = browser.new_page()
#         base_url = 'https://dhs.gov'
#         page.goto(base_url + '/hsi/sevp/sevis-by-the-numbers')

#         years = {}
#         links = page.locator('a').all()
#         for link in links:
#             text = link.inner_text().lower()
#             if 'school data for' in text:
#                 match = re.search(r'(\d{4})', text)
#                 if match:
#                     years[int(match.group(1))] = link

#         latest_link = years[max(years.keys())]
#         page.goto(base_url + latest_link.get_attribute('href'))

#         pdf_link = page.locator('a:text-matches(".*top 500 f-1 higher education.*", "i")').first
#         with tempfile.NamedTemporaryFile(suffix='.pdf') as tf:
#             with page.expect_download() as download_info:
#                 pdf_link.click()
#             download = download_info.value
#             download.save_as(tf.name)
           
#             tables = tabula.read_pdf(tf.name, pages=1)
#             if tables:
#                 print(tables[0].head(10))

#         browser.close()

def test_write():
   conn = snowflake.connector.connect(
       user=os.environ.get('SNOWFLAKE_USER'),
       password=os.environ.get('SNOWFLAKE_PASSWORD'),
       account=os.environ.get('SNOWFLAKE_ACCOUNT'),
       region=os.environ.get('SNOWFLAKE_REGION'),
       warehouse=os.environ.get('SNOWFLAKE_WAREHOUSE'),
       database=os.environ.get('SNOWFLAKE_DATABASE'),
       schema=os.environ.get('SNOWFLAKE_SCHEMA'),
       role=os.environ.get('SNOWFLAKE_ROLE')
   )

   df = pd.DataFrame({
       'year': [2023, 2023, 2023],
       'campus_id': [1, 2, 3],
       'total_sevis': [5840, 4950, 4320]
   })

   write_pandas(conn, df, os.environ.get('SNOWFLAKE_TOP_CAMPUSES_TABLE'))
   conn.close()

test_write()