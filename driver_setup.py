import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

###################################################################################################
# CLASS Driver_Setup 
# 
# Parameters: 
#       dictionary
#
#  Description:
#       Placeholder object, NEEDS WORK
# 
###################################################################################################
class Driver_Setup(object):
    _default_val = None
    __dict__ = {
        'driver', 'url', 'repr', 'site'
    }
    

    def __init__(self, **kwargs):
        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(dict.fromkeys(self._volatiles, self._default_value))
        self.__dict__.update(kwargs)
        self.init_driver()
        self.no_notifications_chrome()

    def search_zillow(self, url):
        """
        This should search the zillow searchbox for the desired county, and then set the desired
        search filters after the search
        """
        # url = "https://www.zillow.com/"
        # searchbox_id = "search-box-input"
        # seach_item = f"{county_name}, GA"

        self.driver.get(url)
        # search_box = self.driver.find_element_by_id(searchbox_id)
        # search_box.send_keys(seach_item)
        # search_box.send_keys(Keys.RETURN)
        # driver.quit()

    def init_driver(self):
        """
        Initialize chrome driver
        """
        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(chrome_options=no_notifications_chrome(), executable_path=service.path)
    

###################################################################################################
# no_notifications_chrome()
# 
# Parameters: 
#       None
#
#  Description:
#       Constructs chrome Options object to be used as 'chrome_options' for chrome driver,
#           suppresses notifications
# 
# Returns:
#       option object to be assigned to chrome_options kwarg for chromedriver
# 
###################################################################################################
def no_notifications_chrome():
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("--disable-extensions")
    option.add_experimental_option(
        "prefs", {"profile.default_content_setting_values.notifications": 2}
        )
    return option


def search_site(url, search_field):
    """
    This will probably be left largely unused unless I find a silly website made by donkeys.
 
    Parameters: 
        url: url for website to be searched for relevant data
        search_field: string argument to be searched at desired site

    Description:
        Initializes chrome driver, searches desired site's searchbar and returns relevant
        information

    Returns:
        should this be a file, xml, json, list of urls for search results? NEEDS WORK
    """
    driver = webdriver.Chrome(chrome_options=no_notifications_chrome())
    driver.get(url)
    search_box = driver.find_element_by_name('q')
    search_box.send_keys(search_field)
    # SLEEP needs to be more robust, something that maybe confirms that the page is ready
    time.sleep(0.8)
    search_box.send_keys(Keys.RETURN)
    # SLEEP
    time.sleep(8)
    driver.quit()


