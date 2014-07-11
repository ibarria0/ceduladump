panacompra
==========

Libreria para verificacion de cedulas de la Republica de Panama.
Wrapper de verificate.pa.

Dependencies
-------------
* BeautifulSoup
* requests 
* python3


usage
------
```python
>>> from cedula_dump import query_cedulas
>>> cedulas = query_cedulas(['8-832-1777','8-888-8888'])
[{'primer_apellido': 'Espino', 'provincia': 'PANAMÁ', 'pais': 'PANAMÁ', 'segundo_nombre': 'Miguel', 'numero': '8-832-1777', 'segundo_apellido': 'Silva', 'primer_nombre': 'Victor'}, None]

```


legal stuff
------------
Copyright (C) 2013  Ivan Barria

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

