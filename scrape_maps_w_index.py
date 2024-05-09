from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from seleniumbase import Driver
import time
import csv
import os

# Function untuk menunggu element tampil
def load_page(self, element):
    global myElem
    delay = 5
    try:
        myElem = WebDriverWait(self, delay).until(EC.presence_of_element_located((By.XPATH, element)))
    except TimeoutException:
        print('Loading too much time')

    return myElem

# Function untuk save file to csv
def save_to_csv(data, filename):
    csv_file_path = f"{filename.replace('/', '_')}.csv"

    # Jika file ada maka append data baru ke file csv yang sudah ada
    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)
        print("Additional data has been added to", csv_file_path)
    
    # Jika file belum ada maka buat file dan tambahkan data baru
    else:
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            header = ["User", "Comment", "Rating"]
            writer.writerow(header)
            for row in data:
                writer.writerow(row)

# Main function
def main():
    data = []
    driver = Driver(uc=True)
    
    try:
        # Ganti query dengan nama tempat spesifik sesuai google maps seperti contoh
        query = 'RSU BANGLI / Rumah Sakit Umum Bangli'
        driver.get(f'https://www.google.com/maps/search/{query}')
    
        try:
            button_review = load_page(driver, '/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]')
            button_review.click()
        except Exception:
            pass
        
        count_review = load_page(driver, '/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[3]').text
        
        count_review = count_review.split(' ulasan')
        count_review = int(count_review[0])
        count_review_mul = count_review*3
        print(f'Total Review : {count_review}')
        
        sleep(5)
        
        scrollable_div = driver.find_element(By.CSS_SELECTOR, '.m6QErb.DxyBCb.kA9KIf.dS8AEf')
        
        for _ in range(0,(round(count_review+1/10))):
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', 
                    scrollable_div)
            time.sleep(3)
            print(f'Range review : {(_*10) + 10}')
        
        try:
            for i in range(1, count_review_mul+1, 3):
                review = load_page(driver, f'/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]/div[{i}]')
                
                actions = ActionChains(driver)
                actions.move_to_element(review).perform()
                
                try:
                    user_element = review.find_element(By.CSS_SELECTOR, '.GHT2ce.NsCY4')
                    user = user_element.find_element(By.CSS_SELECTOR, '.d4r55')
                    user_text = user.text
                except:
                    pass
                
                # Klik button more jika ada
                try:
                    button_more = review.find_element(By.CSS_SELECTOR, '.w8nwRe.kyuRq')
                    button_more.click()
                except:
                    pass
                
                # Mendapatkan data rating yang diberikan user
                try:
                    rating_element = review.find_element(By.CSS_SELECTOR, '.DU9Pgb')
                    rating = rating_element.find_element(By.CSS_SELECTOR, '.kvMYJc').get_attribute('aria-label')
                except:
                    rating = ""
                
                # Mendapatkan data review dari user
                try:
                    review_element = review.find_element(By.CSS_SELECTOR, '.MyEned')
                    review_elements = review_element.find_elements(By.TAG_NAME, 'span')
                    
                    span_texts = [span.text for span in review_elements]
                    review_text = span_texts[0]
                except:
                    review_text = ""
                
                # Append data ke variabel data
                data.append([user_text, review_text, rating])
                print(f"Review index ke-{i} dari {count_review_mul} index")
                
            save_to_csv(data, query)
            
        except:
            print('Error While Scrapping!!!')
            save_to_csv(data, query)
    
    finally:
        print('Scrape done!!!')
        sleep(10)
        driver.quit()
            
            
if __name__ == "__main__":
    main()