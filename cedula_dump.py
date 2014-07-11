import requests
import re
from bs4 import BeautifulSoup,SoupStrainer

original_data = {
    '__LASTFOCUS':'' ,
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    'txtCedula':'', 
    'Button1':'Consultar'
}

def increment_cedula(cedula):
    cedula_digits = cedula.split('-')
    cedula_digits[-1] = str(int(cedula_digits[-1]) + 1)
    return '-'.join(cedula_digits)

def set_viewstate(data,viewstate):
    data = dict(data)
    data['__VIEWSTATE'] = viewstate
    return data

def set_eventvalidation(data,eventvalidation):
    data = dict(data)
    data['__EVENTVALIDATION'] = eventvalidation
    return data

def update_data_for_form(cedula):
    data = original_data.copy()
    r = requests.get('http://verificate.pa/cinteext/Verificate.aspx')
    viewstate = re.search("__viewstate[^>]+value=\"(?P<Value>[^\"]*)", r.text, re.IGNORECASE).group(1)
    eventvalidation = re.search("__eventvalidation[^>]+value=\"(?P<Value>[^\"]*)", r.text, re.IGNORECASE).group(1)
    data = set_eventvalidation(set_viewstate(data,viewstate),eventvalidation)
    data['txtCedula'] = cedula
    return data

def query_cedula(cedula):
    data = update_data_for_form(cedula)
    r = requests.post('http://verificate.pa/cinteext/Verificate.aspx', data=data)
    soup = BeautifulSoup(r.text,'lxml')
    return parse_cedula(soup,cedula)

def extract_apellidos(soup):
    return [cell.string.strip() if cell.string is not None else '' for cell in soup.find(text='Apellido Paterno').parent.parent.parent.parent.find_next_sibling('tr').find_all('font')]

def extract_nombres(soup):
    return [cell.string.strip() if cell.string is not None else '' for cell in soup.find(text='Primer Nombre').parent.parent.parent.parent.find_next_sibling('tr').find_all('font')]

def extract_pais(soup):
    return [cell.string.strip() if cell.string is not None else '' for cell in soup.find(text='País').parent.parent.parent.find_next_sibling('td').find_all('font')][0]

def extract_provincia(soup):
    return [cell.string.strip() if cell.string is not None else '' for cell in soup.find(text='Provincia').parent.parent.parent.find_next_sibling('td').find_all('font')][0]

def parse_cedula(soup, cedula):
    try:
        apellidos = extract_apellidos(soup)
        nombres = extract_nombres(soup)
        pais = extract_pais(soup)
        provincia = extract_provincia(soup)
    except:
        return None
    return {'numero':cedula, 'primer_nombre':nombres[0], 'segundo_nombre':nombres[1], 'primer_apellido':apellidos[0], 'segundo_apellido':apellidos[1], 'pais':pais, 'provincia':provincia}

def query_cedulas(cedulas):
    from multiprocessing import Pool
    pool = Pool(processes=5)
    r = pool.map(query_cedula,cedulas)
    print(r)

def brute_force(n=100,cedula='8-832-1000'):
    for i in range(n):
        print(query_cedula(cedula))
        cedula = increment_cedula(cedula)

if __name__ == "__main__":
    #brute_force()
    cedulas = ['8-832-1700']
    for i in range(1000):
        c = cedulas[-1]
        cedulas.append(increment_cedula(c))
    query_cedulas(cedulas)
