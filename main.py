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
errors = []
lines = {'l1':[],'l2':[],'l3':[],'l4':[],'l5':[],'l6':[],'l7':[],'l8':[],'l9':[],'l10':[],'l11':[],'l12':[],'l13':[],'l14':[],'l15':[]}
# fill = lists
# write = txts
# populate = dicts

base ='https://shakespeare.folger.edu/shakespeares-works/shakespeares-sonnets/'
 
def find_all_idx(main,sub):
  res = [i for i in range(len(main)) if main.startswith(sub, i)]
  return res

def unicodetoascii(text):

    TEXT = (text.
    		replace('\\xe2\\x80\\x99', "'").
            replace('\\xc3\\xa9', 'e').
            replace('\\xc3\\xa8','e').
            replace('⌜','@').
            replace('⌝','$').
            replace('\\xc2\\xa0', '').
            replace('\\xe2\\x8c\\x9c','').
            replace('\\xe2\\x8c\\x9d','').
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
            replace('\\xe2\\x80\\xa6', '...').
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
def reset_texts():
  for id in ids:
    with open(f'bakupsonnets/{id}.txt') as f:
      for line in f:
        with open(f'sonnets/{id}.txt', 'w') as h:
          h.write(line)

def clean(extid):  
  with open(f'sonnets/{extid}.txt') as f:
    for line in f:
      line = line
  line = unicodetoascii(line)
  
  line = line.replace('\\n',' ')
  line = line.strip('\'b')
  line = line.replace('<br/>','#')
  ope = line.index('<')
  clse = line.index('>')
  to_remove = line[ope:clse+1]
  if 'lineNbr' in to_remove:
    lne = line.replace(to_remove,'')
  else:
    lne = line.replace(to_remove,'')
  #lne = lne.replace('   ','#')
  with open(f'sonnets/{extid}.txt','w') as f:
      f.write(lne)
def clean_up(extid):
  for x in range(100):
    try:
      clean(extid)
    except:
      #os.system('clear')
      #print(extid) #f'{round(100*(int(extid))/154)}% clean'
      break
def cleaning():
  for id in ids:
    clean_up(id)
    #print(id)
    with open(f'sonnets/{id}.txt', encoding="utf-8") as f:
      for line in f:
        if '\\' in line:
          print(id)
          errors.append(line)
  print(f'{int(100*(154-int(len(errors)))/154)}% clean')
def nonums(extid):
  newline = ''
  with open(f'sonnets/{extid}.txt','r',encoding='utf-8') as f:
    for line in f:
      for char in line:
        if char.isnumeric() == False:
          newline += char
  #newline = newline.replace('#','',2)
  with open(f'sonnets/{extid}.txt','w') as h:
    h.write(newline.strip().strip('#'))
  #os.system('clear')
  #print('done',extid) #(f'{round(100*(int(extid))/154)}% done')
def nonumsing():
  for id in ids:
    nonums(id)
def fill_lines(extid):
  with open(f'sonnets/{extid}.txt','r') as f:
    #print(extid)
    for line in f:
      for x in range(14):
        try:
          lines[f'l{x+1}'].append((line.split('#')[x]).strip())
        except:
          lines[f'l{x+1}'].append('')
      if extid != '099':
        lines['l15'].append('')
      else:
        lines['l15'].append((line.split('#')[14]).strip())
def filling_lines():
  for id in ids:
    fill_lines(id)
def print_sonnet(extid):
  print(f'Poem {extid}:')  
  #print(len(lines['l14']))
  for x in range(1,16):
    if len(lines[f'l{x}'][int(extid)-1]) != 0:
      print(x,'---',(lines[f'l{x}'][int(extid)-1])) #f'{x}:',
  



#091
# 126 is 12, added 2 hashtags at end

#write_ext()
fill_ext()
#write_sonnets(len(extensions))
fill_ids()
reset_texts()
cleaning()
nonumsing()

filling_lines()
for id in ids:
  with open(f'sonnets/{id}.txt') as f:
    for line in f:
      if len(find_all_idx(line,'#')) != 13:
        print(id, len(find_all_idx(line,'#')))
print_sonnet('154')
#15 lines in 99, add l15 dict and add ' ' for everything else, if len l15 = 1, break
'''
for id in ids:
  print_sonnet(id)'''
