import requests
import instabot
import bs4
import logging
from time import sleep
import random
import csv
import datetime
import pandas
import json 
import shutil
from PIL import Image  
import os
import glob

try:
  cookie_del = glob.glob("config/*cookie.json")
  os.remove(cookie_del[0])
except:
  pass

logging.basicConfig(filename='insta.log', encoding='utf-8', level=logging.DEBUG)
uname = "xxxxxxxxxxxxxxxxxx"
password = "yyyyyyyyyyyy"
affiliatecode = "111111111111111111111"
bot = instabot.Bot()
bot.login(username=uname, password=password)
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.3; nl-nl; SAMSUNG GT-I9505 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36'}



def pglink(no):
  pagelink=f"https://m.newchic.com/en/api/category/categoryList/?cat_id=3590&brand_id=&theme_id=&page={no}&pagesize=18&is_logo=0&ship=0&searchtag=&size=&sort=7&keywords=&pfrom=&pto=&type=&conversionType=EU&act=&is_brand=&is_new=&position_id=&filter_value=&favorite=&newarrivals=&color_id=&NA=1&trace_id=f3f41662224903736&currency_cdn=GBP&default_rule_country_cdn=82"
  return pagelink

def get_seen():
  d = pandas.read_csv("seen.csv")
  return d["ids"].tolist()

def parse(a):
  s={}
  try:
    l = json.loads(a)["result"]["dealsList"]["productList"]
  except KeyError:
    l = json.loads(a)["result"]["list"]

  for p in list(l):
    ist = (
    p["products_name"],
    p["products_id"],
    p["url"]+"?p="+affiliatecode,
    p["format_final_price"],
    p["discount"],
    p["image_url"])
    s.update({str(p["products_id"]):ist})
  return s

def get_bags():
  seenids = get_seen()
  df = {
    "ids" : [],
    "dates" : []
  }
  for i in (1,2,3,4,5):
    x = parse(requests.get(pglink(i), headers=headers).text)
    l=[]
    for key in x.keys():
      if key not in seenids:
        l.append(x[key])
        df['ids'].append(key)
        df['dates'].append(datetime.date.today())
  df = pandas.DataFrame(df)
  df.to_csv('seen.csv', mode="a", index=False, header=False)
  if len(l) == 0:
    print("An error occured in getting bags")
  if len(l) < 15:
    print("Low number of bags, or potential error in fetching")
  f = pandas.DataFrame(l)
  f.to_csv('bags.csv', mode="a", index=False, header=False)
  
  

def affiliate(link):
  aff = link+f"?p={affiliatecode}"
  return aff


def post(img, caption):
  """
  caption is (afflink, title, discount, pricing)
  """
  
  bot.upload_photo(img, caption)
  sleep(10)
   # if bot.api.last_response.status_code != 200:
  #  logger.error(bot.api.last_response)
  
def create_text(caption):
  title = caption[0]
  link = caption[2]
  discount = caption[4]
  price = caption[3]
  msg = f"""
  {discount}% Off on this {title} available for a limited time at {link}
  """
  msg2 = f"""
  {title} at {discount}% off for only {price} at {link}
  """
  
  msg3 = f"""
  Limited stock on this one! {discount}% off at {link}
  """
  if discount in ['',0, '0']:
    x = f"""{title} getting bought up quickly at {price}. Get it here: {link}"""
    return x
  m = [msg, msg2, msg3]
  random.shuffle(m)
  print(m[0])
  return m[0]
  
def download(image_url):
  ila = image_url
  codes = [
    ila.split("/")[8], ila.split("/")[9]
    ]
  print(codes)
  ima= image_url.split("/")[4]+image_url.split('/')[-1].split("?")[0]
  ima= ima[3:]
  url = f"https://imgaz1.chiccdn.com/thumb/view/oaupload/newchic/images/{codes[0]}/{codes[1]}/{ima}?s=360x480"
  res = requests.get(url, stream=True)
  if res.status_code == 200:
    imgname = ima+'.'+url.split('/')[-1].split("?")[0].split(".")[-1]
    print(ima, imgname)
    with open(imgname,'wb') as f:
        shutil.copyfileobj(res.raw, f)
    im = Image.open(imgname)  
    newsize = (489, 600) 
    im1 = im.resize(newsize) 
    im1.save(imgname)
    
    return imgname 
  
class pbot:
  def __init__(self, niche, file):
    self.niche = niche
    self.file = file
  
  def populate(self):
    niche = self.niche
    if niche == "bags":
      get_bags()
      print("here")
  
  def clear(self):
    with open(self.file, 'w') as a:
      a.truncate()
  
    
  def task(self):
    with open(self.file) as csvfile:
      rows = csv.reader(csvfile)
      res = list(rows)
      if len(res) < 5:
        self.populate()
      
      for product in res:
        img = download(product[-1])
        caption = create_text(product)
        print("x")
        post(img, caption)
        sleep(1)
      self.clear()

b = pbot("bags", "bags.csv")
b.task()
print('c')