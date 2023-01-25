import requests
from bs4 import BeautifulSoup as BS
import os
from pronouncing import rhymes
import random


rhymecount = 0
options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'b', 'n']
extensions = []
links = []
ids = []
syn = []
errors = []
folders = ['lines','sonnets','synopsi']
poems = {}

# fill = lists
# write = txts
# populate = dicts

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
  TEXT = (text.replace('\\xe2\\x80\\x99', "'").replace('\\xc3\\xa9', 'e').replace('\\xc3\\xa8', 'e').replace('⌜','@').replace('⌝','$').replace('\\xc2\\xa0', '').replace('\\xe2\\x8c\\x9c','').replace('\\xe2\\x8c\\x9d','').replace('\\xe2\\x80\\x90','-').replace('\\xe2\\x80\\x91', '-').replace('\\xe2\\x80\\x92','-').replace('\\xe2\\x80\\x93', '-').replace('\\xe2\\x80\\x94','-').replace('\\xe2\\x80\\x94', '-').replace('\\xe2\\x80\\x98',"'").replace('\\xe2\\x80\\x9b', "'").replace('\\xe2\\x80\\x9c','"').replace('\\xe2\\x80\\x9c', '"').replace('\\xe2\\x80\\x9d','"').replace('\\xe2\\x80\\x9e', '"').replace('\\xe2\\x80\\x9f','"').replace('\\xe2\\x80\\xa6', '...').replace('\\xe2\\x80\\xb2',"'").replace('\\xe2\\x80\\xb3', "'").replace('\\xe2\\x80\\xb4', "'").replace('\\xe2\\x80\\xb5', "'").replace('\\xe2\\x80\\xb6', "'").replace('\\xe2\\x80\\xb7', "'").replace('\\xe2\\x81\\xba', "+").replace('\\xe2\\x81\\xbb', "-").replace('\\xe2\\x81\\xbc',"=").replace('\\xe2\\x81\\xbd',"(").replace('\\xe2\\x81\\xbe', ")"))
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
  if extid == '099':
    for x in range(1, 16):
      if len(poems[extid][f'l{x}']['lineTxt']) != 0:
        if x < 14:
          print((poems[extid][f'l{x}']['lineTxt']))
        else:
          print('  ', poems[extid][f'l{x}']['lineTxt'])
  elif extid == '126':
    for x in range(1, 16):
      if len(poems[extid][f'l{x}']['lineTxt']) != 0:
        if x < 11:
          print((poems[extid][f'l{x}']['lineTxt']))
        else:
          print('  ', poems[extid][f'l{x}']['lineTxt'])
  else:
    for x in range(1, 16):
      if len(poems[extid][f'l{x}']['lineTxt']) != 0:
        if x < 13:
          print((poems[extid][f'l{x}']['lineTxt']))
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
  if request.lower().strip('0') in ['x','exit','quit','stop','no','n']:
    print('Have a Good Day!')
    exit()
  else:
    try:
      print_synopsi(request)
      print_sonnet(request)
    except:
      print('\nSorry, that\'s not a valid input!')
      lookup()
    startuser()

def filter_last_word(lne):  
  #https://findwords.info/rhyme/crew?fuzzy=1 last resort
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
    if len(poems[extid][lnum]['lineTxt']) != 0:  #not an empty line
      for char in poems[extid][lnum]['lineTxt'].split()[-1]:
        if char.isalnum():
          lne += char
      if len(rhymes(lne)) == 0:  #no rhymes
        lne = filter_last_word(lne)
      if len(rhymes(lne)) == 0:  #still no rhymes
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

def remove_punctuation_2(word):
  lne = ''
  for char in word:
    if char.isalnum():
      lne += char
  return lne

def matching(blank):
  if blank == 'l1':
    match = 'l3'
  if blank == 'l2':
    match = 'l4'
  if blank == 'l3':
    match = 'l1'
  if blank == 'l4':
    match = 'l2'
  if blank == 'l5':
    match = 'l7'
  if blank == 'l6':
    match = 'l8'
  if blank == 'l7':
    match = 'l5'
  if blank == 'l8':
    match = 'l6'
  if blank == 'l9':
    match = 'l11'
  if blank == 'l10':
    match = 'l12'
  if blank == 'l11':
    match = 'l9'
  if blank == 'l12':
    match = 'l10'
  if blank == 'l13':
    match = 'l14'
  if blank == 'l14':
    match = 'l13'
  return match

def check_for_match(extid):
  if extid != '126':
    for lnum in poems[extid]:
      if len(poems[extid][lnum]['lineTxt']) != 0:  #not an empty line
        lne = remove_punctuation(extid, lnum, poems[extid][lnum]['lineTxt'].split()[-1])
        if len(rhymes(lne)) == 0:
          lnumMatch = matching(lnum)
          poems[extid][lnum]['wdRhymes'] = poems[extid][lnumMatch]['wdRhymes']
          print(lnum, '--', poems[extid][lnum]['wdRhymes'])
        if len(poems[extid][lnum]['wdRhymes']) == 0:
          print(f'{extid},{lnum},{lne}')

def checking_for_matches():
  for id in ids:
    check_for_match(id)

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
      with open('lines/15.txt', 'a') as f:
        try:
          f.write((line.split('#')[14]).strip())
        except:
          f.write('')
        f.write('\n')

def filling_and_writing_lines():
  for id in ids:
    fill_lines(id)

def fill_rhymes():
  global rhymecount
  rhymecount += 1
  with open('errors.txt', 'w'):
    pass
  for id in ids:
    rhymable_lines(id)
  print('Rhymes Found')

def blanks():
  for id in ids:
    for lnum in poems[id]:
      if poems[id][lnum]['wdRhymes'] == [] and lnum != 'l15':
        print(id, lnum)

def create_diy_dict():
  lines = {}
  for x in range(1, 15):
    lines[f'diyl{x}'] = {'lineTxt': [], 'wdRhymes': []}
  diy_sonnet = lines
  return diy_sonnet

def print_options(last_word, lnum, id_options):
  options = {}
  for x in range(1, 11):
    options[x] = ''
  line_matches = []
  for id in id_options:
    if last_word in poems[id][lnum]['wdRhymes']:
      line_matches.append(f'{id}.{lnum}')
      id_options.remove(id)
  id_options_sub = id_options.copy()
  for id in id_options_sub:
    if len(line_matches) < 10:
      try:
        if len(poems[id][lnum]['wdRhymes']) != 0:
          line_matches.append(f'{id}.{lnum}')
          id_options.remove(id)
        else:
          line_matches.append(f'{id}.{lnum}')
          id_options.remove(id)
      except:
        print(id)
  for x in range(len(line_matches)):
    options[x + 1] = line_matches[x]
  return options, id_options
 
def printListOptions(num, options, lnum):
  print(f'Line {lnum}:')
  print(f'Page {num.split("p")[1]}:')
  for key in options:
    try:
      print(key, poems[options[key].split('.')[0]][options[key].split('.')[1]]
            ['lineTxt'], f"(Sonnet {options[key].split('.')[0]})")
    except:
      pass
  print('Back/Next')

def options_page(lnum, id_options, lastword):
  id_options = id_options.copy()
  p1 = print_options(lastword, f'l{lnum}', id_options)
  p2 = print_options(lastword, f'l{lnum}', p1[1])
  p3 = print_options(lastword, f'l{lnum}', p2[1])
  p4 = print_options(lastword, f'l{lnum}', p3[1])
  p5 = print_options(lastword, f'l{lnum}', p4[1])
  p6 = print_options(lastword, f'l{lnum}', p5[1])
  p7 = print_options(lastword, f'l{lnum}', p6[1])
  p8 = print_options(lastword, f'l{lnum}', p7[1])
  p9 = print_options(lastword, f'l{lnum}', p8[1])
  p10 = print_options(lastword, f'l{lnum}', p9[1])
  p11 = print_options(lastword, f'l{lnum}', p10[1])
  p12 = print_options(lastword, f'l{lnum}', p11[1])
  p13 = print_options(lastword, f'l{lnum}', p12[1])
  p14 = print_options(lastword, f'l{lnum}', p13[1])
  p15 = print_options(lastword, f'l{lnum}', p14[1])
  p16 = print_options(lastword, f'l{lnum}', p15[1])
  pages = {
    'p1': p1,
    'p2': p2,
    'p3': p3,
    'p4': p4,
    'p5': p5,
    'p6': p6,
    'p7': p7,
    'p8': p8,
    'p9': p9,
    'p10': p10,
    'p11': p11,
    'p12': p12,
    'p13': p13,
    'p14': p14,
    'p15': p15,
    'p16': p16
  }
  return pages

def choosing(pOptions, choice, diy_dict, pnum, lnum):
  selection = (pOptions[pnum][0])[int(choice)]
  print('Line Selected!\nChoice: ',
        poems[selection.split('.')[0]][selection.split('.')[1]]['lineTxt'])
  diy_dict[f'diyl{lnum}']['lineTxt'] = poems[selection.split('.')[0]][
    selection.split('.')[1]]['lineTxt']
  diy_dict[f'diyl{lnum}']['wdRhymes'] = poems[selection.split('.')[0]][
    selection.split('.')[1]]['wdRhymes']

def selorpage(pOptions, diy_dict, pnum, lnum):
  #time.sleep(1)
  #os.system('clear')
  print()
  if lnum > 14:
    for key in diy_dict:
      try:
        print(diy_dict[key]['lineTxt'])
      except:
        print('error')
    startuser()
  else:
    printListOptions(pnum, pOptions[pnum][0], lnum)
    #choice = input('Pick One! \nSelection: ')
    #choice = str(options[random.randint(0,11)])
    choice = '1'
    if choice.isnumeric():
      choosing(pOptions, choice, diy_dict, pnum, lnum)
      lnum = int(lnum) + 1
      if lnum in [3,4,7,8,11,12]:
        lword = remove_punctuation_2(
          diy_dict[f'diyl{(lnum-2)}']['lineTxt'].split(' ')[-1])
      elif lnum == 14:
        lword = remove_punctuation_2(
          diy_dict[f'diyl{(lnum-1)}']['lineTxt'].split(' ')[-1])
      else:
        lword = ''
      pOptions = options_page(lnum, ids,lword)  #redefine options for next line
      perpage(diy_dict, lnum, pOptions)
    if choice.lower() in ['next','n'] and pnum != 'p16':
      pnum = f'p{(int(pnum.split("p")[1])+1)}'
      selorpage(pOptions, diy_dict, pnum, lnum)
    if choice.lower() in ['back','b'] and pnum != 'p1':
      pnum = f'p{int(pnum.split("p")[1])-1}'
      selorpage(pOptions, diy_dict, pnum, lnum)
    if choice.lower() == 'x':
      exit()
    else:
      print('choice invalid')
      selorpage(pOptions, diy_dict, pnum, lnum)

def perpage(diy_dict, lnum, pOptions):
  pnum = 'p1'
  selorpage(pOptions, diy_dict, pnum, lnum)

def build_your_own():
  diy_dict = create_diy_dict()
  lnum = 1
  pOptions = options_page(lnum, ids, '')
  perpage(diy_dict, lnum, pOptions)

def startuser():
  user = input('\nSearch for a Sonnet or Build Your Own!\nSearch/Build:\nSelection: ')
  #os.system('cls')
  if user.lower() in ['search','s','1']:
    print('Search:')
    lookup()
  if user.lower() in ['build','b','2']:
    if rhymecount == 0:
      fill_rhymes()
    print('Build Your Own')
    build_your_own()
  else:
    print('Invalid Input')
    startuser()
    
def startup():
  #os.system('cls')
  for name in folders:
    newpath = name
    if not os.path.exists(newpath):
      os.makedirs(newpath)
  with open('extensions.txt','r') as f:
    if len(f.read()) == 0:
      write_ext()
  with open('ids.txt','r') as h:
    if len(h.read()) == 0:
      with open('ids.txt','a') as r:
        for x in range(1,155):
          r.write(f'{str(x).rjust(3,"0")}\n')      
  #q1 = input('Want to reset the sonnets and synopses?\nY/N\nSelection:')
  q1 = 'n'
  if q1.lower() == 'y':
    q1a = input('From backups or the site?\n1/2\nSelection:')
    if q1a == '1':
      write_sonnets_bkup()
      write_clean_synopsi()
    if q1a == '2':
      q1aa = input('Are you sure? That will take a very long time.\nY/N\nSelection:')
      if q1aa.lower() == 'y':
        write_sonnets()
  check_for_tags()
  fill_ext_ids()
  create_poem_dicts()
  write_lines() #also fills lines
        
startup()
startuser()

