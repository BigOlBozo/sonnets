import requests
from bs4 import BeautifulSoup as BS
import os
from random import randint
line = []
extensions = []
links = []
ids = []
syn = []
# fill = lists
# write = txts
# populate = dicts

def find_indices(list_to_check, item_to_find):
    indices = []
    for idx, value in enumerate(list_to_check):
        if value == item_to_find:
            indices.append(idx)
    return indices

base ='https://shakespeare.folger.edu/shakespeares-works/shakespeares-sonnets/'
"""<!-- .post-header -->
       <div class="entry-content">
        <h5>
         <span class="txit">
          Synopsis:
         </span>
        </h5>
        <div id="modal-ready">
         <p>
          In this first of many sonnets about the briefness of human life, the poet reminds the young man that time and death will destroy even the fairest of living things. Only if they reproduce themselves will their beauty survive. The young man’s refusal to beget a child is therefore self-destructive and wasteful.
         </p>
        </div>
       </div>"""
def get_synopsis(extnum,extid):
  #print(base+str(extnum))
  r = requests.get(f'{base+str(extnum)}')
  soup = BS(r.content, 'html.parser')
  for link in soup.find_all('div', id='modal-ready'):
    syn.append(str(link))
  with open(f'synopsi/{extid}syn.txt','w') as f:
    close = find_indices(syn[0],'>')
    opn = find_indices(syn[0],'<')
    if close[1] != 25:
      print(close)
    else:
      print(extid)
     
    #print(opn)
    '''if opn[1] != 23:
      print(opn)
    else:
      print(opn[1])'''
    #print(opn)
    syntext = (syn[0])[(close[1]+1):opn[2]]
    #print(syn[0],'\n')
    f.write(syntext)
  syn.clear()
  #print(soup.prettify())
  #still need to find out how to isolate synopsis

    
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


def write_txt_and_synopsi(extnum):
  r = requests.get(f'{base+str(extnum)}/')
  soup = BS(r.content, 'html.parser')
  extid = ''
  for x in range(0,4):    
    if extnum[-x::].isdigit() == True:
      extid = (extnum[-x::])
  extid = extid.rjust(3,'0')
  for link in soup.find_all('div',class_="div1", id=f'Son-{extid}'):
    with open(f'sonnets/{extid}.txt', 'w') as f:
      f.write(str(link))
    links.append(link)
  
  get_synopsis(extnum,extid)

  
def write_sonnets(length):
  for x in range(length):
    write_txt_and_synopsi(extensions[x])


write_ext()
fill_ext()
write_sonnets(len(extensions))