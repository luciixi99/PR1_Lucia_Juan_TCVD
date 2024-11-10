from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException,TimeoutException
import csv
from selenium.webdriver.common.action_chains import ActionChains


def setup_driver(user_agent = None):
    opts = Options()
    # Uncomment the next line to run the browser in headless mode
    # opts.add_argument("--headless")

    # Setting up user-agent if provided
    if user_agent:
        opts.add_argument(f"user-agent={user_agent}")

    # Example user-agent string for reference:
    # opts.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    return driver


# Initialize the Selenium driver
driver = setup_driver()

# Open Airbnb search page for Barcelona
driver.get('https://www.airbnb.es/s/Barcelona--Espa%C3%B1a/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-11-01&monthly_length=3&monthly_end_date=2025-02-01&price_filter_input_type=0&channel=EXPLORE&query=Barcelona%2C%20Espa%C3%B1a&place_id=ChIJZb1_yQvmpBIRsMmjIeD6AAM&location_bb=QilKtkAxw%2FFCJMVfP64hfA%3D%3D&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click')

# Wait for the page to load completely
time.sleep(5)

# Attempt to accept cookies, if the button is available
try:
    accept_cookies = driver.find_element(By.XPATH, '//button[contains(@class, "l1ovpqvx atm_1he2i46_1k8pnbi_10saat9 atm_yxpdqi_1pv6nv4_10saat9 atm_1a0hdzc_w1h1e8_10saat9 atm_2bu6ew_929bqk_10saat9 atm_12oyo1u_73u7pn_10saat9 atm_fiaz40_1etamxe_10saat9 bmx2gr4 atm_9j_tlke0l atm_9s_1o8liyq atm_gi_idpfg4 atm_mk_h2mmj6 atm_r3_1h6ojuz atm_rd_glywfm atm_70_5j5alw atm_tl_1gw4zv3 atm_9j_13gfvf7_1o5j5ji c1ih3c6 atm_bx_48h72j atm_cs_10d11i2 atm_5j_t09oo2 atm_kd_glywfm atm_uc_1lizyuv atm_r2_1j28jx2 atm_jb_1fkumsa atm_3f_glywfm atm_26_18sdevw atm_7l_1v2u014 atm_8w_1t7jgwy atm_uc_glywfm__1rrf6b5 atm_kd_glywfm_1w3cfyq atm_uc_aaiy6o_1w3cfyq atm_70_1b8lkes_1w3cfyq atm_3f_glywfm_e4a3ld atm_l8_idpfg4_e4a3ld atm_gi_idpfg4_e4a3ld atm_3f_glywfm_1r4qscq atm_kd_glywfm_6y7yyg atm_uc_glywfm_1w3cfyq_1rrf6b5 atm_kd_glywfm_pfnrn2_1oszvuo atm_uc_aaiy6o_pfnrn2_1oszvuo atm_70_1b8lkes_pfnrn2_1oszvuo atm_3f_glywfm_1icshfk_1oszvuo atm_l8_idpfg4_1icshfk_1oszvuo atm_gi_idpfg4_1icshfk_1oszvuo atm_3f_glywfm_b5gff8_1oszvuo atm_kd_glywfm_2by9w9_1oszvuo atm_uc_glywfm_pfnrn2_1o31aam atm_tr_18md41p_csw3t1 atm_k4_kb7nvz_1o5j5ji atm_3f_glywfm_1nos8r_uv4tnr atm_26_wcf0q_1nos8r_uv4tnr atm_7l_1v2u014_1nos8r_uv4tnr atm_3f_glywfm_4fughm_uv4tnr atm_26_4ccpr2_4fughm_uv4tnr atm_7l_1v2u014_4fughm_uv4tnr atm_3f_glywfm_csw3t1 atm_26_wcf0q_csw3t1 atm_7l_1v2u014_csw3t1 atm_7l_1v2u014_pfnrn2 atm_3f_glywfm_1o5j5ji atm_26_4ccpr2_1o5j5ji atm_7l_1v2u014_1o5j5ji f1hzc007 atm_vy_1osqo2v b1sbs18w atm_c8_km0zk7 atm_g3_18khvle atm_fr_1m9t47k atm_l8_182pks8 dir dir-ltr")]')
    accept_cookies.click()
except NoSuchElementException:
    print("No 'Accept cookies' found.")

data = [] # Stores data for the main listings
data2 = [] # Stores detailed data for each listing

# Function to extract titles, prices, links, and ratings from the page
def extract_data():
    try:
        # Locate elements for titles, prices, and ratings
        titulos = driver.find_elements(By.XPATH, '//div[@data-testid="listing-card-title"]')
        precios = driver.find_elements(By.XPATH, '//div[@data-testid="price-availability-row"]//span[contains(@class, "_11jcbg2")]')
        ratings = driver.find_elements(By.CSS_SELECTOR, 'span.r4a59j5.atm_h_1h6ojuz.atm_9s_1txwivl.atm_7l_jt7fhx.atm_84_evh4rp.atm_mk_h2mmj6.atm_mj_glywfm.dir.dir-ltr > span[aria-hidden="true"]')
        allApartments = driver.find_elements(By.XPATH, "//meta[@itemprop='url']")
        
        # Print total number of apartments found
        totalNumbreOfApartments = len(allApartments)
        print("There are total ", totalNumbreOfApartments, "found on this page")
        
        apartmentLinks = []
        for apartment in allApartments:
            apartmentUrl = apartment.get_attribute('content')

            apartmentUrl = "https://" + apartmentUrl
            print(apartmentUrl)
            apartmentLinks.append(apartmentUrl)
            apartmentUrl = ""

        # Print and store each listing's title, price, link, and rating
        for titulo, precio, url, rating in zip(titulos, precios,apartmentLinks, ratings):
            print("Title:", titulo.text)
            print("Price:", precio.text)
            print("Price:", rating.text)
            print("Link:", url)
            # print("Fecha:", fecha.text)

            data.append([titulo.text, precio.text, url, rating.text])
    except StaleElementReferenceException:
        print("Los elementos ya no son válidos en el DOM actual. Reintentando...")

# Pagination settings
pagina_count = 0
max_paginas = 4  # Limit the number of pages to scrape

# Loop to extract data from multiple pages
while pagina_count < max_paginas:
    # Extrae y muestra datos de la página actual
    print(f"\nDatos de la página {pagina_count + 1}:")
    extract_data()

    # Attempt to navigate to the next page
    try:
        siguiente = driver.find_element(By.XPATH, '//a[@aria-label="Siguiente"]')
        siguiente.click() 
        time.sleep(3)  # Wait for the next page to load
        pagina_count += 1
    except NoSuchElementException:
        print("No hay más páginas.")
        break


# Save extracted data to a CSV file
with open('apartments_data13.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Escribe la cabecera
    writer.writerow(["Title", "Price", "Link", "Rating"])
    # Escribe los datos
    writer.writerows(data)

# Visit each listing page and extract detailed data
for _,price,url,rating in data:
    try:
        driver.get(url)
        print('Busqueda en nuevo alojamiento')

        # Handle any pop-up that appears
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[1]/button'))).click()
        except Exception as e:
            print("No pop-up found or couldn't close it:", e)

        # Extract registration number or other details as text
        try:
            # Wait for the div to be present and retrieve its text
            div_text_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="c2a9hgn atm_9s_1txwivl atm_ar_1bp4okc atm_cx_1fwxnve dir dir-ltr"]'))
            )
            div_text = div_text_element.text
            registry = [item.strip() for item in div_text.split('\n')]
            print(registry)
        except Exception as e:
            print("Error:", e)
            registry = 'No information'

        # Access the Amenities section
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-section-id="AMENITIES_DEFAULT"] button'))).click()
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        d = {
            'title': soup.h1.text,
            'price':price,
            'rating':rating,
            'amenities': [i.text.split('\n')[0] for i in WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="modal-container"] [id$="-row-title"]')))],
            'numero_registro': registry
        }
        if soup.select_one('[data-section-id="SLEEPING_ARRANGEMENT_DEFAULT"] div+div'):
            sleep_areas = list(soup.select_one('[data-section-id="SLEEPING_ARRANGEMENT_DEFAULT"] div+div').stripped_strings)
            d.update(dict(zip(sleep_areas[0::2], sleep_areas[1::2])))
        else:
            d.update({'Bedroom': None})

        # Close the amenities modal
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.c11vnb9k.atm_mk_stnw88.atm_9s_1txwivl.atm_tk_exct8b.atm_fq_1tcgj5g.atm_wq_kb7nvz.atm_1wn1q82_xond3e.atm_tk_1tcgj5g__oggzyc.dir.dir-ltr button'))).click()
        print('Se han cerrado las amenities')

        # Extract reviews if available
        try:
            reviews_section = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@data-section-id, "REVIEWS_DEFAULT")]'))
            )
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            reviews = []
            for review in soup.select('[data-section-id="REVIEWS_DEFAULT"] [role="listitem"]'):
                rating = review.select_one('.c5dn5hn span')
                date = review.select_one('.s78n3tv ')
                text = review.select_one('.r1bctolv > div > span > span')

                review_data = {
                    'rating': rating.text if rating else None,
                    'date': date.text if date else None,
                    'review': text.text if text else None
                }
                reviews.append(review_data)

            d['reviews'] = reviews
        except Exception as e:
            print("Error retrieving reviews:", e)
            d['reviews'] = []

        data2.append(d)
    except Exception as e:
        print(e)

# Save the detailed data to a CSV
df = pd.DataFrame(data2)
print(df)
df.to_csv('output.csv', index=False)

# Close the driver
driver.quit()


##### If we wanted to navigate through all the pages:
# while True:
#     # Extract data from the current page
#     print("Extracting data from the current page...")
#     extract_data()

#     # Attempt to locate and click the "Next" button to navigate to the next page
#     try:
#         next_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="Siguiente"]'))
#         )
#         next_button.click()  # Proceed to the next page
#         time.sleep(3)  # Allow time for the new page to load fully
#     except (NoSuchElementException, TimeoutException):
#         print("Reached the last page.")
#         break  # Terminate the loop if "Next" button is absent or unreachable
