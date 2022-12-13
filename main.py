import requests
import keyboard
from bs4 import BeautifulSoup as BS
import os
from pronouncing import rhymes

extensions = []
links = []
ids = []
syn = []
errors = []
poems = {}

# fill = lists
# write = txts
# populate = dicts

'''if keyboard.is_pressed('x') == True:
    exit()'''

base = 'https://shakespeare.folger.edu/shakespeares-works/shakespeares-sonnets/'

def create_poem_dicts():
  for a in range(1, 155):
    lines = {}
    for x in range(1, 16):
      lines[f'l{x}'] = {'lineTxt': [], 'wdRhymes': []}
    poems[f'{str(a).rjust(3,"0")}'] = lines
  print('Poem Dictionary Created')

def clear_lines():
  for x in range(1, 16):
    with open(f'lines/{x}.txt', 'w'):
      pass

def find_all_idx(main, sub):
  res = [i for i in range(len(main)) if main.startswith(sub, i)]
  return res

def unicodetoascii(text):
  TEXT = (text.replace('\\xe2\\x80\\x99', "'").replace(
'\\xc3\\xa9', 'e').replace('\\xc3\\xa8', 'e').replace(
'⌜', '@').replace('⌝','$').replace('\\xc2\\xa0', '').replace(
'\\xe2\\x8c\\x9c', '').replace('\\xe2\\x8c\\x9d','').replace(
'\\xe2\\x80\\x90','-').replace('\\xe2\\x80\\x91', '-').replace(
'\\xe2\\x80\\x92','-').replace('\\xe2\\x80\\x93', '-').replace(
'\\xe2\\x80\\x94','-').replace('\\xe2\\x80\\x94', '-').replace(
'\\xe2\\x80\\x98',"'").replace('\\xe2\\x80\\x9b', "'").replace(
'\\xe2\\x80\\x9c','"').replace('\\xe2\\x80\\x9c', '"').replace(
'\\xe2\\x80\\x9d','"').replace('\\xe2\\x80\\x9e', '"').replace(
'\\xe2\\x80\\x9f','"').replace('\\xe2\\x80\\xa6', '...').replace(
'\\xe2\\x80\\xb2',"'").replace('\\xe2\\x80\\xb3', "'").replace(
'\\xe2\\x80\\xb4', "'").replace('\\xe2\\x80\\xb5', "'").replace(
'\\xe2\\x80\\xb6', "'").replace('\\xe2\\x80\\xb7', "'").replace(
'\\xe2\\x81\\xba', "+").replace('\\xe2\\x81\\xbb', "-").replace(
'\\xe2\\x81\\xbc',"=").replace('\\xe2\\x81\\xbd',"(").replace(
  '\\xe2\\x81\\xbe', ")"))
  return TEXT

def find_indices(list_to_check, item_to_find):
  indices = []
  for idx, value in enumerate(list_to_check):
    if value == item_to_find:
      indices.append(idx)
  return indices

def get_synopsis(extnum, extid):
  r = requests.get(f'{base+str(extnum)}')
  soup = BS(r.content, 'html.parser')
  for link in soup.find_all('div', id='modal-ready'):
    syn.append(str(link))
  with open(f'synopsi/{extid}syn.txt', 'w', encoding='utf-8') as f:
    close = find_indices(syn[0], '>')
    opn = find_indices(syn[0], '<')
    '''if len(close) != 4: #if theres a link inside
      print(close)
    else:
      print(extid)'''
    syntext = (syn[0])[(close[1] + 1):opn[-2]]
    f.write(syntext)
  syn.clear()

def write_ext():
  with open('extensions.txt', 'w'):
    pass
  for x in range(1, 155):
    with open('extensions.txt', 'a') as f:
      f.write(f'sonnet-{x}')
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
  for x in range(0, 4):
    if extnum[-x::].isdigit() == True:
      extid = (extnum[-x::])
  extid = extid.rjust(3, '0')
  for link in soup.find_all('div', class_="div1", id=f'Son-{extid}'):
    with open(f'sonnets/{extid}.txt', 'w', encoding='utf-8') as f:
      print('---', extid)
      f.write(unicodetoascii(str(str(link))))
    links.append(link)
  '''get_synopsis(extnum,extid)'''

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
    try:
      newline = newline.replace(line[stt[x]:end[x] + 7], '')
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

def clean(folder, extid):
  with open(f'{folder}/{extid}.txt') as f:
    for line in f:
      line = line
  line = unicodetoascii(line)
  line = line.replace('\\n', ' ')
  line = line.strip('\'b')
  line = line.replace('<br/>', '#')
  ope = line.index('<')
  clse = line.index('>')
  to_remove = line[ope:clse + 1]
  if 'lineNbr' in to_remove:
    lne = line.replace(to_remove, '')
  else:
    lne = line.replace(to_remove, '')
  with open(f'{folder}/{extid}.txt', 'w') as f:
    f.write(lne)

def clean_up(extid):
  for x in range(100):
    try:
      clean('sonnets', extid)
    except:
      break

def cleaning():
  for id in ids:
    clean_up(id)
    with open(f'sonnets/{id}.txt', encoding="utf-8") as f:
      for line in f:
        if '\\' in line:
          print(id)
          errors.append(line)
  nonumsing()
  print('No Nums')

def nonums(extid):
  newline = ''
  with open(f'sonnets/{extid}.txt', 'r', encoding='utf-8') as f:
    for line in f:
      for char in line:
        if char.isnumeric() == False:
          newline += char
  with open(f'sonnets/{extid}.txt', 'w') as h:
    h.write(newline.strip().strip('#'))

def nonumsing():
  for id in ids:
    nonums(id)

def print_sonnet(extid):
  print(f'\nSonnet {extid}:\n')
  #print(len(lines['l14']))
  if extid == '099':
    for x in range(1, 16):
      if len(lines[f'l{x}'][int(extid) - 1]) != 0:
        if x < 14:
          print((lines[f'l{x}'][int(extid) - 1]))  #f'{x}:',
        else:
          print('   ', (lines[f'l{x}'][int(extid) - 1]))
  elif extid == '126':
    for x in range(1, 16):
      if len(lines[f'l{x}'][int(extid) - 1]) != 0:
        if x < 11:
          print((lines[f'l{x}'][int(extid) - 1]))  #f'{x}:',
        else:
          print('   ', (lines[f'l{x}'][int(extid) - 1]))
  else:
    for x in range(1, 16):
      if len(poems[extid][f'l{x}']['lineTxt']) != 0:
        if x < 13:
          print((poems[extid][f'l{x}']['lineTxt']))  #f'{x}:',
        else:
          print('  ', poems[extid][f'l{x}']['lineTxt'])
  return True

def write_sonnets_bkup():
  reset_texts()
  print('Texts Reset')
  cleaning()
  print('Texts Clean')

def write_lines():  
  clear_lines()
  print('Lines Clear')
  filling_and_writing_lines() 
  print('Lines Filled & Written')

def fill_ext_ids():
  fill_ext()
  fill_ids()
  print('Extensions & Ids Filled')
  
def clean_syn(folder, extid):
  x = 0
  with open(f'{folder}/{extid}syn.txt', encoding='utf-8') as f:
    for line in f:
      x += 1
      lne = line
  if x != 1:  # if more than one line for some reason
    print(extid, x)
  try:
    ope = lne.index('<')
    clse = lne.index('>')
    to_remove = lne[ope:clse + 1]
    lne = lne.replace(to_remove, '')
  except:
    pass
  with open(f'{folder}/{extid}syn.txt', 'w', encoding='utf-8') as f:
    f.write(lne)

def clean_up_syn(extid):
  for x in range(10):
    clean_syn('synopsi', extid)

def cleaning_syn():
  for id in ids:
    clean_up_syn(id)

def reset_synopsi():
  for id in ids:
    with open(f'backupsynopsi/{id}syn.txt', encoding="utf-8") as f:
      for line in f:
        with open(f'synopsi/{id}syn.txt', 'w', encoding='utf-8') as h:
          h.write(line)
        break
  print('Synopsi Reset')

def check_for_tags():
  for id in ids:
    with open(f'synopsi/{id}syn.txt', encoding="utf-8") as f:
      for line in f:
        if '<' in str(line):
          print('tag present in', id)
          
def write_clean_synopsi():
  reset_synopsi()
  cleaning_syn()
  
def print_synopsi(extid):
  with open(f'synopsi/{extid}syn.txt', encoding='utf-8') as f:
    for line in f:
      print(f'\nSynopsis:\n{line}') 
      
def lookup():
  request = input(
    '\nLooking for something?\nPick a number 1-154!\nNumber: ').rjust(3, '0')
  if request.lower().strip('0') == 'x' or request.lower().strip('0') == 'exit':
    print('Have a Good Day!')
    exit()
  else:
    try:
      print_synopsi(request)
      print_sonnet(request)
    except:
      print('\nSorry, that\'s not a valid input!')
      lookup()
    lookup()

def filter_last_word(lne): #https://findwords.info/rhyme/crew?fuzzy=1 last resort
  if lne[-3::] == 'ent':
    lne = 'accent'
  if lne[-3::] == 'est' and len(rhymes(lne)) == 0:
    lne = 'greatest'
  if lne[-3::] == 'age' and len(rhymes(lne)) == 0:
    lne = 'encourage'
  if lne[-3::] == 'ing' and len(rhymes(lne)) == 0:
    lne = 'waiting'
  if lne[-4::] == 'owst' and len(rhymes(lne)) == 0:
    lne = 'roast'
  if lne[-4::] == 'etst' and len(rhymes(lne)) == 0:
    lne = 'sweetest'
  if lne[-4::] == 'ayst' and len(rhymes(lne)) == 0:
    lne = 'waist'
  if lne[-2::] == 'th' and len(rhymes(lne)) == 0:
    lne = 'myth'
  else:
    lne = lne
  return lne
  
def rhymable_lines(extid): 
  for lnum in poems[extid]:  #each line
    lne = ''
    if len(poems[extid][lnum]['lineTxt']) != 0: #not an empty line
      for char in poems[extid][lnum]['lineTxt'].split()[-1]:
        if char.isalnum():
          lne += char
      if len(rhymes(lne)) == 0:  #no rhymes
        lne = filter_last_word(lne)
      if len(rhymes(lne)) == 0: #still no rhymes
        with open('errors.txt', 'a') as f:
          f.write(f'{extid},{lnum},{lne}')
          f.write('\n')
    poems[extid][lnum]['wdRhymes'] = rhymes(lne)
    
def remove_punctuation(extid, lnum, lword):
  lne = ''
  for char in poems[extid][lnum]['lineTxt'].split()[-1]:
    if char.isalnum():
      lne += char
  return lne

def check_from_match(extid):
  for lnum in poems[extid]:
    if len(poems[extid][lnum]['lineTxt']) != 0: #not an empty line
      if len(rhymes(lne)) == 0:
        if lnum == 'l1':
          lne = remove_punctuation(extid, lnum, 'l3')
          poems[extid][lnum]['wdRhymes'] = rhymes(lne)
    #26 055,l1,monuments
def fill_lines(extid):
  with open(f'sonnets/{extid}.txt', 'r') as f:
    for line in f:
      for x in range(14):
        try:
          poems[f'{extid}'][f'l{x+1}']['lineTxt'] = line.split('#')[x].strip()
          with open(f'lines/{x+1}.txt', 'a') as f:
            f.write((line.split('#')[x]).strip())
            f.write('\n')
        except:
          poems[f'{extid}'][f'l{x+1}']['lineTxt'] = ''
          with open(f'lines/{x+1}.txt', 'a') as f:
            f.write('')
            f.write('\n')
      if extid != '099':
        poems[f'{extid}']['l15']['lineTxt'] = ''
      else:
        poems[f'{extid}']['l15']['lineTxt'] = line.split('#')[14].strip()
      with open(f'lines/15.txt', 'a') as f:
        try:
          f.write((line.split('#')[14]).strip())
        except:
          f.write('')
        f.write('\n')

def filling_and_writing_lines():
  for id in ids:
    fill_lines(id)
    
def fill_rhymes():
  with open('errors.txt','w'):
    pass
  for id in ids:
    rhymable_lines(id)
  print('Rhymes Found')


#write_ext()
fill_ext_ids()  #need
#write_sonnets() # from site
#write_sonnets_bkup() #from bkup
#write_clean_synopsi() #from bkup
#check_for_tags()
create_poem_dicts()  #need before printing lines/rhymes
write_lines() #need -> #also fills lines
fill_rhymes()
lookup()
