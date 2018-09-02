from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import namedtuple
from pprint import pprint
import hotel as hotel
from selenium.webdriver.firefox.options import Options

class Booking:
    def __init__(self,driver):
        self.driver = driver
        self.url = 'https://www.booking.com/index.pt-br.html'
        self.search_bar = 'ss' #id 
        self.btn_search = 'sb-searchbox__button' #class
        self.hotel_list = 'hotellist_inner' #class
        self.score = 'review-score-badge' #class
        self.caixa = 'sr_item_content'
        self.nome = 'sr-hotel__name' #class
        self.event = namedtuple('Event', 'name score')
        self.next_pg = 'paging-next' #class
        self.result_true = 'sorth1' #class

        

    def navigate(self):
        self.driver.get(self.url)

    def search(self,word='None'):
        try:
            self.driver.find_element_by_id(
            self.search_bar).send_keys(word)
            self.driver.find_element_by_class_name(self.btn_search).click()
            self.driver.find_element_by_class_name(self.result_true) #cidade valida
            return True
        except:
            print("except")
            self.driver.find_element_by_id(self.search_bar).clear()
            return False
    

    def _get_hoteis(self):
        box = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f'//div[@id="{self.hotel_list}"]//div[contains(@class, "{self.caixa}")]')))
        return self.driver.find_elements_by_xpath(f'//div[@id="{self.hotel_list}"]//div[contains(@class, "{self.caixa}")]')
        
    def _get_name(self,hotel):
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'sr-hotel__name')))
        return hotel.find_element_by_class_name(self.nome).text
        
    def _get_score(self,hotel):

        return hotel.find_element_by_class_name(self.score).text
        

    def get_all_data(self):
        hoteis = self._get_hoteis()
        for hotel in hoteis:
            try:
                yield self.event(self._get_name(hotel),self._get_score(hotel))
            except:
                yield self.event(self._get_name(hotel),'-1,0')
    
    def  percore (self,lista):    
        try: 
            print("\nBuscando Hoteis", end='', flush=True)
            print(" . ", end='', flush=True)
            #caso a cidade tenha só uma pg de hoteis 
            for event in self.get_all_data():
                #print(event.name +" = "+ event.score)
                a = hotel.Hotel(event.name,float((event.score).replace(',','.')))
                lista.append(a)
            self.driver.find_element_by_class_name(self.next_pg).click()
            while ( WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, self.next_pg)))):
                print(" . ", end='', flush=True)
                time.sleep(5)
                for event in self.get_all_data():
                    a = hotel.Hotel(event.name,float((event.score).replace(',','.')))
                    lista.append(a)
                self.driver.find_element_by_class_name(self.next_pg).click()
            
        except:   
            print(" Busca concluida")
            self.driver.save_screenshot('screenshot.png')
            self.driver.close()
    
def main():
    '''options = webdriver.ChromeOptions()
    options.add_argument("--headless")      
    #options.add_argument("--window-size=1920x1080")
    ff = webdriver.Chrome(chrome_options = options)'''
    
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)#firefox_options=options#)

    b = Booking(driver)
    b.navigate()
    cidade =  input ("Informe a cidade desejada: ")
    isvalid = b.search(cidade) 
    
    while (isvalid == False):
        cidade =  input ("Não foram encontradas acomodações para a cidade informada \nInforme outra cidade: ")
        isvalid = b.search(cidade)

    lista = []
    b.percore(lista)
    ordenados = sorted(lista, key = hotel.Hotel.get_score, reverse=True)
    
    qt = input("\nForam encontradas "+str(len(ordenados))+" acomadoções para a cidade informada! \n\nInforme quantidade que deseja visualizar ordenada pelo maior score: ")
    i = 0
    while i < int(qt):
        print(ordenados[i], sep = '\n')
        i = i + 1
    print("\n")

if __name__ == "__main__":
    main()