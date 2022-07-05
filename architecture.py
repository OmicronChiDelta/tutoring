#basic python file to architect the webscraping component in selenium



#imports
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import pandas as pd
import datetime



#%%
pull = True
load_dir = "c:\\users\\alex white\\desktop\\tutorful\\extraction"
path_payload = os.path.join(load_dir, "prices.csv")
string_now = datetime.datetime.now().strftime("%Y%d%m")



#%%
if pull:

    #Obtain html containing prices for maths a-level tutors on tutorful 
    path_driver = "C:\\Program Files (x86)\\geckodriver.exe"
    url = "https://tutorful.co.uk/results/maths-a-level"

    #open connection to url
    driver = webdriver.Firefox(executable_path=path_driver)
    driver.get(url)
    time.sleep(5)

    #Refresh to load more tutors - work on running until "stale reference" occurs
    buffer = 2
    for b in range(buffer):
        try:
            #locate and click button: "See more tutors"
            search = driver.find_element_by_css_selector("button.btn:nth-child(3)")
            time.sleep(5)
            search.send_keys(Keys.RETURN)
            time.sleep(3)
            print("button loaded and clicked")
        except:
            print("button expired")

    #Get all the HTML which has been loaded
    page_source = driver.page_source
    driver.quit()

    #parse the html to pull out prices
    soup = BeautifulSoup(page_source, 'html.parser')
    prices = [int(re.sub(r'\D', '', p.text)) for p in soup.find_all('h6')]

    payload = pd.DataFrame(columns=["price_data"], data=prices)
    payload.to_csv(path_payload, index=False)

else:
    prices = list(pd.read_csv(path_payload)["price_data"].values)



#%% visualise
plt.close("all")
fig, ax = plt.subplots()
ax.hist(prices, edgecolor="k", facecolor="red", alpha=0.25, density=True, bins=25)
ax.axvline(np.median(prices), ls="--", c="k")
ax.set_title(f"n={len(prices)}")
ax.set_xlabel("hourly rate")
ax.set_ylabel("frequency density")

#smooth envelope via kde
kde = gaussian_kde(prices)
x = np.linspace(min(prices), max(prices), 1000)
ax.plot(x, kde(x), c="red")

ax.set_xticks([i for i in range(0, int(np.ceil(1.1*np.max(prices))), 10)])
plt.savefig(os.path.join(load_dir, f"distro_{string_now}.png"))
plt.show()
