# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 21:34:08 2016
@author: Peter
Created responding to Asheya's request for an AirBnb Booking Request scraper
Based on: 
https://automatetheboringstuff.com/chapter11/
and lots of googling on html, xpath, scraping
e.g. http://docs.python-guide.org/en/latest/scenarios/scrape/

How To Use:
1. Run script
2. Call run("filename") where filename is the name the table will be saved under. Put quotes around it! Do not add '.csv' etc, the program will do this.

The number of pages searched by this script needs to be updated! Right now range(1,12) goes through pages 1-11.
"""
from selenium import webdriver
from lxml import html
import time

def login():
    browser = webdriver.Firefox()
    browser.get('http://airbnb.com/login')
    emailform = browser.find_element_by_id('signin_email')
    emailform.send_keys('vacation@asheya.com')
    passwordform = browser.find_element_by_id('signin_password')
    passwordform.send_keys('find55digs')
    passwordform.submit()
    time.sleep(1)
    return browser

def ftree(page_num):
    page_num = str(page_num)
    browser.get("https://www.airbnb.ca/my_reservations?all=1&page="+page_num)
    page = browser.page_source
    tree = html.fromstring(page)
    return tree

def fpage_bookings(tree,first_message):
    page_bookings = []    
    for i in range(2,55):       #This purposely goes over the expected range. (2,52) would catch the expected max range of 50.
        i = str(i)
        row = []
        try:  
            #Status
            row.append(tree.xpath('//*[@id="site-content"]/div[2]/div/div[2]/div[2]/div[3]/table/tbody/tr['+i+']/td[1]/span/text()')[0].strip())
            #Dates and Year          
            dates = tree.xpath('//*[@id="site-content"]/div[2]/div/div[2]/div[2]/div[3]/table/tbody/tr['+i+']/td[2]/text()[1]')[0].strip()            
            #year = tree.xpath('//*[@id="site-content"]/div[2]/div/div[2]/div[2]/div[3]/table/tbody/tr['+i+']/td[2]/text()[1]')[0].strip()            
            row.append(dates)
            #row.append(year)
            #House Address         
            row.append(tree.xpath('//*[@id="site-content"]/div[2]/div/div[2]/div[2]/div[3]/table/tbody/tr['+i+']/td[2]/text()[4]')[0].strip())
            #Guest            
            row.append(tree.xpath('//*[@id="site-content"]/div[2]/div/div[2]/div[2]/div[3]/table/tbody/tr['+i+']/td[3]/div/div/a/text()')[0].strip())
            #Dollar Total            
            row.append(tree.xpath('//*[@id="site-content"]/div[2]/div/div[2]/div[2]/div[3]/table/tbody/tr['+i+']/td[4]/text()')[0].strip()[1:-15])
            #Add phone number and email?
            page_bookings.append(row)
        except IndexError:
            break
        if first_message == True:
            browser.get("https://www.airbnb.com"+tree.xpath('//*[@id="site-content"]/div[2]/div/div[2]/div[2]/div[3]/table/tbody/tr['+i+']/td[4]/ul/li[last()]/a/@href')[0])
            subpage = browser.page_source
            subtree = html.fromstring(subpage)
            mess_date = subtree.xpath('//*[@id="thread-list"]/div[last()]/div/div/div[2]/div/div/div[3]/span[2]/text()')            
            if mess_date:
                row.append(mess_date[0][4:-41])
    return page_bookings

#I set this to only do page 1&2~
def run(filename,first_message=False):
    filename = str(filename)+".csv"
    all_bookings = [["Status","Dates","Year","House Address","Guest","Amount total (CAD)"]]
    if first_message == True:
        all_bookings[0].append("Date of First Message")
    for page_num in range(1,3): #TODO: Adapt this to handle more pages as bookings increase
        tree = ftree(page_num)
        page_bookings = fpage_bookings(tree,first_message)
        all_bookings += page_bookings
    write_csv(filename, all_bookings)




##These are taken from a script I got in lab (UBC's CPSC 301, Spring 2016)
def write_elements(writer, data_list, sep = ', '):
  """(file open for writing, list, string) -> None
  
  The elements of data_list are written to the file with sep between them.
  A newline is added at the end.
  """
  # We want the separator character(s) after every item except the last one.
  for item in data_list[:-1]:
    try:
        writer.write(item)
    except UnicodeEncodeError:
        writer.write("Unhandled Asian Characters")
    writer.write(sep)
   
  # After the last item, write a newline.
  writer.write(data_list[-1])
  writer.write('\n')


def write_csv(filename, data_list_of_lists, sep = ', '):
  """(string, list of lists, string) -> None
  
  Writes data to a CSV file named filename.  Each sublist of data_list_of_lists
  is written on a separate line.  Each element of each sublist is separated
  by sep.
  """
  with open(filename, 'w') as writer:
    for row in data_list_of_lists:
      write_elements(writer, row, sep)



if __name__ == "__main__":
    browser = login()



