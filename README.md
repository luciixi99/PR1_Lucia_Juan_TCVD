# PR1_Lucia_Juan_TCVD




## Descripción del repositorio

En este código hemos querido realizar una pequeña demo de webscrapping usando python y selenium
de la página web de alquileres turísticos Airbnb.

## Ejecución del código

Ejecutar el código es tan sencillo como ejecutar el archivo main.py desde un terminal que tenga
python instalado:

```
python  main.py
```

El código hace el scrapping únicamente de los alojamientos de Barcelona, pero este código es
altamente modificable así que si se quiere scrappear cualquier otra ciudad, sólo habría que o
modificar la url.


## Output

Este código nos devuelve dos ficheros csv:  output.csv y aparments_data13.csv

- *output.csv* es un fichero con los datos de manera exhaustiva. Aunque está escrito en csv 
es un fichero también interesante de entender en formato json por el formato que tienen 
algunas de sus columnas

Este fichero se ve de esta manera:

| title | price | rating | amenities | numero_registro | reviews | Bedroom | Dormitorio 1 | Dormitorio 2 |
|-------|-------|--------|-----------|-----------------| ------- | ------- | ------------ | ------------ |
| ..... | ..... | ...... | ......... | ............... | ....... | ....... | ............ | ............ |


- título es el título del alojamiento en airbnb
- price: precio del alojamiento en euros por noche
- rating: puntuación con el número de reviews
- amenties: lista con todas las distintas utilidades que ofrece el alojamiento
- numero_registro: numero de registro del alojamiento. A veces lo hay y hay veces que este está vacío.
- reviews: es un diccionario donde cada entrada es una review con la valoración numérica, la fecha y el comentario que dejó la persona.
Si no hay valoraciones se deja en vacío.
- Bedroom: dormitorios que tiene el alojamiento si lo indica
- Dormitorio 1: como es el dormitorio 1
- Dormitorio 2: como es el dormitorio 2

- apartments_data13.csv: es un dataset mucho más reducido donde sólo incluímos la información importante como el tipo
de alojamiento, la url, el precio y la valoración.

| title | price | linkg | rating | 
|-------|-------|-------|--------|
| ..... | ..... | ..... | ...... | 

Ambos archivos contienen el mismo número de filas pues contienen la información de los mismos alojamientos.

## Librerías usadas en el código
- selenium
- webdriver_manager.chrome
- pandas
- bs4
- time
- csv

## Entendimiento del código:

1. LLamamos a una funcióin setup que nos ayuda a elegir si queremos un agente en concreto y  nos levanta tanto el servicio 
como el driver:

```
def setup_driver(user_agent = None):
    opts = Options()

    # opts.add_argument("--headless")
    # Para poder configurar el user-agent añadimos esto:
    if user_agent:
        opts.add_argument(f"user-agent={user_agent}")

    #Dejamos aquí un ejemplo de user agnet por si quiere usarse:
    # opts.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    # Configuración de Selenium
    return driver
```

2. Llamamos a la url (esto se puede customizar), aceptamos las cookies del sitio y extraemos los datos básicos de los
alojamientos de todas las páginas. Veamos más detalladamente:

```
# Abre la página de búsqueda de Airbnb
driver.get('https://www.airbnb.es/s/Barcelona--Espa%C3%B1a/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-11-01&monthly_length=3&monthly_end_date=2025-02-01&price_filter_input_type=0&channel=EXPLORE&query=Barcelona%2C%20Espa%C3%B1a&place_id=ChIJZb1_yQvmpBIRsMmjIeD6AAM&location_bb=QilKtkAxw%2FFCJMVfP64hfA%3D%3D&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click')


# Espera que la página cargue completamente
time.sleep(5)


try:
    accept_cookies = driver.find_element(By.XPATH, '//button[contains(@class, "l1ovpqvx ")]')
    accept_cookies.click()
except NoSuchElementException:
    print("No 'Accept cookies' found.")

```

Tenemos una función que en cada página encuentra los datos de todos los elementos:

```
def extract_data():
    try:
        # Encuentra los elementos de títulos y precios en la página actual
        titulos = driver.find_elements(By.XPATH, '//div[@data-testid="listing-card-title"]')
        precios = driver.find_elements(By.XPATH, '//div[@data-testid="price-availability-row"]//span[contains(@class, "_11jcbg2")]')
        ratings = driver.find_elements(By.CSS_SELECTOR, 'span.r4a59j5.atm_h_1h6ojuz.atm_9s_1txwivl.atm_7l_jt7fhx.atm_84_evh4rp.atm_mk_h2mmj6.atm_mj_glywfm.dir.dir-ltr > span[aria-hidden="true"]')
        allApartments = driver.find_elements(By.XPATH, "//meta[@itemprop='url']")
        totalNumbreOfApartments = len(allApartments)
        print("There are total ", totalNumbreOfApartments, "found on this page")
        apartmentLinks = []
        for apartment in allApartments:
            apartmentUrl = apartment.get_attribute('content')

            apartmentUrl = "https://" + apartmentUrl
            print(apartmentUrl)
            apartmentLinks.append(apartmentUrl)
            apartmentUrl = ""

        # Itera sobre los títulos y precios y los imprime
        for titulo, precio, url, rating in zip(titulos, precios,apartmentLinks, ratings):
            print("Title:", titulo.text)
            print("Price:", precio.text)
            print("Price:", rating.text)
            print("Link:", url)
            # print("Fecha:", fecha.text)

            data.append([titulo.text, precio.text, url, rating.text])
    except StaleElementReferenceException:
        print("Los elementos ya no son válidos en el DOM actual. Reintentando...")
```

Luego estableciendo el número máximo de páginas que queremos usar aplicamos este código de recopilar la info básica
a cada una de ellas:

```
pagina_count = 0
max_paginas = 4  # Límite de páginas a recorrer

# Bucle para navegar y extraer datos en las dos primeras páginas
while pagina_count < max_paginas:
    # Extrae y muestra datos de la página actual
    print(f"\nDatos de la página {pagina_count + 1}:")
    extract_data()

    # Intenta encontrar y hacer clic en el botón "Siguiente"
    try:
        siguiente = driver.find_element(By.XPATH, '//a[@aria-label="Siguiente"]')
        siguiente.click()  # Haz clic en el botón para ir a la siguiente página

        # Espera un momento para que la siguiente página cargue completamente
        time.sleep(3)  # Ajusta este tiempo si es necesario

        # Incrementa el contador de páginas
        pagina_count += 1
    except NoSuchElementException:
        print("No hay más páginas.")
        break

```

3. Guardamos los datos básicos en el ficheros apartments_data13.csv


```
with open('apartments_data13.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Escribe la cabecera
    writer.writerow(["Title", "Price", "Link", "Rating"])
    # Escribe los datos
    writer.writerows(data)
```


4. Iteramos sobre todos las url que hemos recopilado anteriormente, accedemos a cada sitio y recolectamos información más 
específica:

Cerramos el pop up de la traducción, encontramos los datos del registro del alojamiento, abrimos el apartado de amenities
y recolectamos todos los datos:


```
for _,price,url,rating in data:
    try:
        driver.get(url)
        print('Busqueda en nuevo alojamiento')
        # Manejar el pop-up si aparece
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[1]/button'))).click()
        except Exception as e:
            print("No pop-up found or couldn't close it:", e)

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

        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-section-id="AMENITIES_DEFAULT"] button'))).click()

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        d = {
            'title': soup.h1.text,
            'price':price,
            'rating':rating,
            'amenities': [i.text.split('\n')[0] for i in WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="modal-container"] [id$="-row-title"]')))],
            'numero_registro': registry
        }
```

Recolectamos la información acerca de los dormitorios y cerramos las amenities:

        if soup.select_one('[data-section-id="SLEEPING_ARRANGEMENT_DEFAULT"] div+div'):
            sleep_areas = list(soup.select_one('[data-section-id="SLEEPING_ARRANGEMENT_DEFAULT"] div+div').stripped_strings)
            d.update(dict(zip(sleep_areas[0::2], sleep_areas[1::2])))
        else:
            d.update({'Bedroom': None})

        #Cerrar las amenities
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.c11vnb9k.atm_mk_stnw88.atm_9s_1txwivl.atm_tk_exct8b.atm_fq_1tcgj5g.atm_wq_kb7nvz.atm_1wn1q82_xond3e.atm_tk_1tcgj5g__oggzyc.dir.dir-ltr button'))).click()


        print('Se han cerrado las amenities')


Nos vamos a la parte de review e intentamos extraer todos los datos:

```
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
```

5. Escribimos el output.csv

