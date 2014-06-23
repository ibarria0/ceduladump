import requests
import re
from bs4 import BeautifulSoup,SoupStrainer

data = {
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

def update_data_for_form(data,cedula):
    data = dict(data)
    r = requests.get('http://ve.tribunal-electoral.gob.pa/cinteext/Verificate.aspx')
    viewstate = re.search("__viewstate[^>]+value=\"(?P<Value>[^\"]*)", r.text, re.IGNORECASE).group(1)
    eventvalidation = re.search("__eventvalidation[^>]+value=\"(?P<Value>[^\"]*)", r.text, re.IGNORECASE).group(1)
    data = set_eventvalidation(set_viewstate(data,viewstate),eventvalidation)
    data['txtCedula'] = cedula
    return data

def query_cedula(data,cedula):
    data = update_data_for_form(data,cedula)
    r = requests.post('http://ve.tribunal-electoral.gob.pa/cinteext/Verificate.aspx', data=data)
    return BeautifulSoup(r.text,'html.parser')
    
def extract_apellidos(soup):
    return [cell.string.strip() if cell.string is not None else '' for cell in soup.find(text='Apellido Paterno').parent.parent.parent.parent.find_next_sibling('tr').find_all('font')]
    
def extract_nombres(soup):
    return [cell.string.strip() if cell.string is not None else '' for cell in soup.find(text='Primer Nombre').parent.parent.parent.parent.find_next_sibling('tr').find_all('font')]

def brute_force(n=100,cedula='8-832-1000'):
    for i in xrange(n):
        soup = query_cedula(data,cedula)
        try:
            apellidos = extract_apellidos(soup)
            nombres = extract_nombres(soup)
        except:
            print 'cedula %s no existe' % cedula
        print "%s %s %s %s %s" % (nombres[0],nombres[1],apellidos[0],apellidos[1], cedula)
        cedula = increment_cedula(cedula)

if __name__ == "__main__":
    brute_force()
