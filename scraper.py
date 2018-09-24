from selenium import webdriver
import pandas
import time
import pickle

from cleaner import Cleaner

class Scraper():
    def __init__(self):
        self.url = "https://needsupply.com/mens/clothing?p='1'"
        self.driver_path = './chromedriver.exe'
        self.driver = webdriver.Chrome(self.driver_path)
        self.product_links = []
        self.df = None
        self.product_object = {}


    def _get_url(self):
        self.driver.get(self.url)


    def _get_product_urls(self):
        print("Getting product links...")
        self.product_links = self.driver.find_elements_by_class_name('image-link')


    def _get_pictures(self):
        element = self.driver.find_elements_by_class_name('product-thumbs')[0]
        image_tags = element.find_elements_by_tag_name('img')

        for i, tag in enumerate(image_tags):
            print(tag.get_attribute('src'))
            self.product_object["thumbnail-{}".format(i)] = tag.get_attribute('src')

        print("Product thumbs: {}".format(element))


    def _get_sizing_info(self):
        # write sizing info to object
        sizing_element = self.driver.find_elements_by_class_name('sizing')[0]

        unclean_sizing_element = sizing_element.get_attribute('innerHTML')
        
        cc = Cleaner(unclean_sizing_element)
        cc.start()

        for k, v in cc.obj:
            self.product_object[k] = v


    def _build_dataframe(self):
        if hasattr(self, 'df'):
            add_on = pandas.DataFrame.from_records(self.product_object)
        try:
            self.df = self.df.append(add_on)
        except:
            self.df = pandas.DataFrame.from_records(self.product_object)


    def _csv_checkpoint(self):
        csv_file = 'data.csv'
        self.df.to_csv(csv_file)
        print('Writing to {}'.format(csv_file))

    
    def start(self):
        self._get_url()
        self._get_product_urls()

        for i, product in enumerate(self.product_links):
            self.product_links[i].click()

            self._get_pictures()
            self._get_sizing_info()

            self._build_dataframe()
            self._csv_checkpoint()

            self._get_url()


if __name__ == '__main__':
    scraper = Scraper()
    scraper.start()
