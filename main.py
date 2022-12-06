import requests
from bs4 import BeautifulSoup as BS
import os
os.system('cls')
'''import pronouncing
print(pronouncing.rhymes("climbing"))'''
line = []
extensions = []
links = []
ids = []
syn = []
# fill = lists
# write = txts
# populate = dicts
errors = []

 
def find_all_idx(main,sub):
  res = [i for i in range(len(main)) if main.startswith(sub, i)]
  return res

def unicodetoascii(text):

    TEXT = (text.
    		replace('\\xe2\\x80\\x99', "'").
            replace('\\xc3\\xa9', 'e').
            replace('\\xe2\\x80\\x90', '-').
            replace('\\xe2\\x80\\x91', '-').
            replace('\\xe2\\x80\\x92', '-').
            replace('\\xe2\\x80\\x93', '-').
            replace('\\xe2\\x80\\x94', '-').
            replace('\\xe2\\x80\\x94', '-').
            replace('\\xe2\\x80\\x98', "'").
            replace('\\xe2\\x80\\x9b', "'").
            replace('\\xe2\\x80\\x9c', '"').
            replace('\\xe2\\x80\\x9c', '"').
            replace('\\xe2\\x80\\x9d', '"').
            replace('\\xe2\\x80\\x9e', '"').
            replace('\\xe2\\x80\\x9f', '"').
            replace('\\xe2\\x80\\xa6', '...').#
            replace('\\xe2\\x80\\xb2', "'").
            replace('\\xe2\\x80\\xb3', "'").
            replace('\\xe2\\x80\\xb4', "'").
            replace('\\xe2\\x80\\xb5', "'").
            replace('\\xe2\\x80\\xb6', "'").
            replace('\\xe2\\x80\\xb7', "'").
            replace('\\xe2\\x81\\xba', "+").
            replace('\\xe2\\x81\\xbb', "-").
            replace('\\xe2\\x81\\xbc', "=").
            replace('\\xe2\\x81\\xbd', "(").
            replace('\\xe2\\x81\\xbe', ")")

                 )
    return TEXT

def find_indices(list_to_check, item_to_find):
    indices = []
    for idx, value in enumerate(list_to_check):
        if value == item_to_find:
            indices.append(idx)
    return indices

base ='https://shakespeare.folger.edu/shakespeares-works/shakespeares-sonnets/'
def get_synopsis(extnum,extid):
  #print(base+str(extnum))
  r = requests.get(f'{base+str(extnum)}')
  soup = BS(r.content, 'html.parser')
  for link in soup.find_all('div', id='modal-ready'):
    syn.append(str(link))
  with open(f'synopsi/{extid}syn.txt','w', encoding='utf-8') as f:
    close = find_indices(syn[0],'>')
    opn = find_indices(syn[0],'<')
    '''if len(close) != 4: #if theres a link inside
      print(close)
    else:
      print(extid)'''
     
    syntext = (syn[0])[(close[1]+1):opn[-2]]
    f.write(syntext)
  syn.clear()
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
def fill_ids():
  with open('ids.txt') as f:
    for line in f:
      ids.append(line.strip('\n'))
def write_txt_and_synopsi(extnum):
  r = requests.get(f'{base+str(extnum)}/')
  soup = BS(r.content, 'html.parser')
  extid = ''
  for x in range(0,4):    
    if extnum[-x::].isdigit() == True:
      extid = (extnum[-x::])
  extid = extid.rjust(3,'0')
  for link in soup.find_all('div',class_="div1", id=f'Son-{extid}'):
    with open(f'sonnets/{extid}.txt', 'w',encoding='utf-8') as f:
      print('---',extid)
      f.write(unicodetoascii(str(str(link))))
    links.append(link)
  #get_synopsis(extnum,extid) 
def write_sonnets(length):
  for x in range(length):
    write_txt_and_synopsi(extensions[x])
write_ext()
fill_ext()
#write_sonnets(len(extensions))
fill_ids()

def clean_brid(extid):
  with open(f'sonnets/{extid}.txt') as f:
    for line in f:
      newline = line
  for x in range(len(find_all_idx(newline, '<span'))):
    stt = find_all_idx(newline, '<span')
    end = find_all_idx(newline, '</span>')
    #print(stt[0],end[0])
    try: 
      newline = newline.replace(line[stt[x]:end[x]+7],'')
    except:
      pass
    with open(f'sonnets/{extid}.txt', 'w') as h:
      h.write(newline)
  return extid, len(find_all_idx(line, '<span'))



#\xc3\xa8d
def clean(extid):  
  with open(f'sonnets/{extid}.txt') as f:
    for line in f:
      line = line
  line = line.replace('\\n',' ')
  line = line.strip('\'b')
  ope = line.index('<')
  clse = line.index('>')
  to_remove = line[ope:clse+1]
  lne = line.replace(to_remove,' ')
  lne = lne.replace('   ','#')
  with open(f'sonnets/{extid}.txt','w') as f:
      f.write(lne)
def clean_up(extid):
  for x in range(100):
    try:
      clean(extid)
    except:
      print(extid, 'clean')
      break
  
def reset_texts():
  for id in ids:
    with open(f'bakupsonnets/{id}.txt') as f:
      for line in f:
        with open(f'sonnets/{id}.txt', 'w') as h:
          h.write(line)

#reset_texts()
reset_texts()
for id in ids:
  print(clean_brid(id))
'''for id in ids:
  clean_up(id)
  with open(f'sonnets/{id}.txt') as f:
    for line in f:
      if '\\' in line:
        errors.append(line)'''
print(len(errors))