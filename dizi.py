# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
from optparse import OptionParser

# reset screen before print anything
print("\033c")

# script parameters
parser = OptionParser(description="Supported sites: dizibox (default), dizipub, dizist, dizilab, altyazilidizi")
parser.add_option("-s", "--site", dest="siteName",
                  help="get latest series from SITE",
                  metavar="SITE", default="dizibox")
(options, args) = parser.parse_args()

# class definition to colorise terminal
class color:
  RED = '\033[91m'
  GRE = '\033[92m'
  BLU = '\033[94m'
  CYA = '\033[96m'
  WHI = '\033[97m'
  YEL = '\033[93m'
  MAG = '\033[95m'
  GRA = '\033[90m'
  BLA = '\033[90m'
  DEFAULT = '\033[99m'
  END = '\033[0m'

# function to read html of the given url
def read_url(url):
  hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Connection': 'keep-alive'}
  req = urllib2.Request(url, headers=hdr)
  try:
    page = urllib2.urlopen(req)
  except urllib2.HTTPError, e:
    print e.fp.read()
  return page.read()

# function to encode given text to unicode
def e(text):
  return text.encode('utf-8')

# function to cut and format given text for colorful terminal texts
def f(text, length):
  return str('{: <' + str(8 + length) + 's}').format(e(text)) + " "

# function to retrieve series' links from "dizibox" website
def dizibox(url):
  html = read_url(url)
  soup = BeautifulSoup(html, 'html.parser')
  for idx, box in enumerate(soup.find_all(class_='box-details')):
    index   = f(color.GRA + "#" + str(idx+1) + color.END, 4)
    title   = f(color.YEL + box.find_all(class_='archive')[0].text.strip() + color.END, 20)
    season  = f(color.BLU + box.find_all(class_='season')[0].text.strip() + color.END, 9)
    episode = f(color.GRE + box.find_all(class_='episode')[0].text.strip() + color.END, 12)
    url     = e(color.GRA + box.find_all('a', href=True)[0]['href'] + color.END)
    for box in soup.find_all(class_='post-fields'):
      date = f(color.MAG + box.find_all(class_='post-date')[0].text.strip() + color.END, 8)
      continue
    print(index + title + season + episode + date + url + "\n")
    # we need only the first 12
    if (idx == 11):
      break

# function to retrieve series' links from "dizipub" website
def dizipub(url):
  html = read_url(url)
  soup = BeautifulSoup(html, 'html.parser')
  for idx, box in enumerate(soup.find_all(class_='poster-article')):
    index   = f(color.GRA + "#" + str(idx+1) + color.END, 4)
    title   = f(color.YEL + box.find_all(class_='archive-name')[0].text.strip() + color.END, 20)
    season  = f(color.BLU + box.find_all(class_='episode-name')[0].text.strip().split()[0] + color.END, 9)
    episode = f(color.GRE + box.find_all(class_='episode-name')[0].text.strip().split()[1] + color.END, 12)
    url     = e(color.GRA + box.find_all('a', href=True)[0]['href'] + color.END)
    date    = f(color.MAG + box.find_all(class_='post-date')[0].text.strip() + color.END, 8)
    print(index + title + season + episode + date + url + "\n")
    # we need only the first 16
    if (idx == 15):
      break

# function to retrieve series' links from "dizist" website
def dizist(url):
  html = read_url(url)
  soup = BeautifulSoup(html, 'html.parser')
  for idx, box in enumerate(soup.find_all(class_='last-episode')):
    index   = f(color.GRA + "#" + str(idx+1) + color.END, 4)
    title   = f(color.YEL + box.find_all(class_='stitle')[0].text.strip() + color.END, 20)
    # example text: "2. sezon 8. bölüm", and rarely like "1. sezon 9. ve 10. bölüm"
    se      = box.find_all(class_='sinfo')[0].text.strip().split()
    if (se[3] == "ve"): se3 = se[4] + se[5].title()
    else: se3 = se[3].title()
    season  = f(color.BLU + se[0] + se[1].title() + color.END, 9)
    episode = f(color.GRE + se[2] + se3 + color.END, 12)
    url     = e(color.GRA + box.find_all('a', href=True)[0]['href'] + color.END)
    date    = f(color.MAG + box.find_all(class_='h-series-date')[0].text.strip() + color.END, 8)
    print(index + title + season + episode + date + url + "\n")
    # we need only the first 20
    if (idx == 19):
      break

# function to retrieve series' links from "dizilab" website
def dizilab(url):
  html = read_url(url)
  soup = BeautifulSoup(html, 'html.parser')
  for idx, box in enumerate(soup.findAll(True, {"class":["episode", "season-finale", "new-episode"]})):
    index   = f(color.GRA + "#" + str(idx+1) + color.END, 4)
    title   = f(color.YEL + box.find_all(class_='title')[0].text.strip() + color.END, 20)
    # example text: "2. sezon 8. bölüm", and rarely like "Sezon Finali"
    se      = box.find_all(class_='alt-title')[0].text.strip().split()
    if (se[0] == "Sezon"):
      se1 = "Sezon"
      se2 = "Finali"
    else:
      se1 = se[0] + se[1].title()
      se2 = se[2] + se[3].title()
    season  = f(color.BLU + se1 + color.END, 9)
    episode = f(color.GRE + se2 + color.END, 12)
    url     = e(color.GRA + box.find_all('a', href=True)[0]['href'] + color.END)
    print(index + title + season + episode + url + "\n")
    # we need only the first 30
    if (idx == 29):
      break

# function to retrieve series' links from "altyazilidizi" website
def altyazilidizi(url):
  html = read_url(url)
  soup = BeautifulSoup(html, 'html.parser')
  for idx, box in enumerate(soup.find_all(class_='post_title')):
    index   = f(color.GRA + "#" + str(idx+1) + color.END, 4)
    title   = f(color.YEL + box.find_all(class_='series-name')[0].text.strip() + color.END, 20)
    season  = f(color.BLU + box.find_all(class_='season-name')[0].text.strip() + color.END, 10)
    episode = f(color.GRE + box.find_all(class_='episode-name')[0].text.strip() + color.END, 12)
    url     = e(color.GRA + box.find_all('a', href=True)[0]['href'] + color.END)
    date    = f(color.MAG + box.find_all(class_='post_date')[0].text.strip() + color.END, 8)
    print(index + title + season + episode + date + url + "\n")
    # we need only the first 30
    if (idx == 29):
      break


###### BEGIN ######

if (options.siteName == "dizipub"):
  dizipub("http://dizipub.com")
elif (options.siteName == "dizist"):
  dizist("http://dizist1.com")
elif (options.siteName == "dizilab"):
  dizilab("http://dizilab.net")
elif (options.siteName == "altyazilidizi"):
  altyazilidizi("https://altyazilidizi.com")
else:
  dizibox("http://dizibox1.com")

