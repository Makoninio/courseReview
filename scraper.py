from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import time

def find_professors(keyword="*"):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f'https://www.ratemyprofessors.com/search/professors/3965?q={keyword}'
    driver.get(url)
    time.sleep(5)  # Wait for JS to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    professors = soup.find_all('a', class_='TeacherCard__StyledTeacherCard-syjs0d-0 eerjaA')

    all_professors = []

    for professor in professors:
        try:
            name_tag = professor.find('div', class_=lambda c: c and 'CardName__StyledCardName' in c)
            department = professor.find('div', class_=lambda c: c and 'CardSchool__Department' in c)
            rating_tag = professor.find('div', class_=lambda c: c and 'CardNumRating__CardNumRatingNumber' in c)

            name = name_tag.text.strip() if name_tag else "N/A"
            dept = department.text.strip() if department else "N/A"
            rating = rating_tag.text.strip() if rating_tag else "N/A"

            prof_link = 'https://www.ratemyprofessors.com' + professor['href']
            driver.get(prof_link)
            time.sleep(2)

            prof_soup = BeautifulSoup(driver.page_source, 'html.parser')
            tags = prof_soup.find_all('span', class_=lambda c: c and 'Tag-' in c)
            reviews = prof_soup.find_all('div', class_=lambda c: c and 'Comments__StyledComments' in c)

            tag_list = [tag.text.strip() for tag in tags[:6]]
            review_list = [review.text.strip() for review in reviews[:3]]

            prof_info = {
                'name': name,
                'department': dept,
                'rating': rating,
                'tags': tag_list,
                'reviews': review_list,
                'link': prof_link
            }

            all_professors.append(prof_info)
        except Exception as e:
            print(f"Error scraping a professor: {e}")
            continue

    driver.quit()

    # Save to local JSON file
    with open('professors.json', 'w', encoding='utf-8') as f:
        json.dump(all_professors, f, ensure_ascii=False, indent=2)

    return all_professors

# ✅ Run the scraper and save results
if __name__ == "__main__":
    data = find_professors()
    print(f"Saved {len(data)} professors to professors.json")
