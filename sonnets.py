import requests
from bs4 import BeautifulSoup
import os
from random import randint
line = []
extensions = []
links = []
start = []
end = []
base ='https://shakespeare.folger.edu/shakespeares-works/shakespeares-sonnets/'
def write_ext():
  with open('extensions.txt','w'):
    pass
  for x in range(1,155):
    with open('extensions.txt','a') as f:
      f. write(f'sonnet-{x}')
      f.write('\n')
def fill_ext():
  with open('extensions.txt') as f:
    for ext in f:
      extensions.append(ext.strip('\n'))
  #print(extensions)

def write_synopsis(extnum):
  #print(type(extnum))
  r = requests.get(f'{base+str(extnum)}/')
  soup = BeautifulSoup(r.content, 'html.parser')
  #print(soup.prettify())
  extid = ''
  for x in range(1,4):
    if extnum[-x::].isdigit() == True:
      extid += (extnum[-x::])
  extid = extid.rjust(3,'0')
  print(extid)
  for link in soup.find_all('div',class_="div1", id=f'Son-{extid}'):
    links.append(link)
  print(extnum)
'''write_ext()
fill_ext()

for x in range(100,110):
  write_synopsis(extensions[x])
errors 
print(len(links))'''
errors =[',','\'',' ','\[','\]']
os.system('cls')
for x in range(20):
  for x in range(40):
    t = randint(1,2)
    if t == 1:
      line.append('-')
    else:
      line.append('/')
  
  print(str(line).replace(errors,''))
  print((((str(line).replace(',','')).replace('\'','')).replace(' ','')).replace(['\[','\]'],''))
  line.clear()