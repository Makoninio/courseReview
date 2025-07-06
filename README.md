# Course Review Aggregator

A web application that scrapes professor data and reviews from RateMyProfessors and provides a searchable, filterable interface to find highly reviewed professors by department, rating, and more.

---

## Features

- Scrapes professor names, departments, ratings, tags, and recent review comments using Selenium and BeautifulSoup.
- Saves scraped data locally in JSON to avoid repetitive scraping and speed up loading.
- Flask backend serving professor data and handling search/filter queries.
- Responsive and clean UI with Bootstrap for easy browsing and filtering of professor reviews.
- Scheduled automatic scraping to keep data up-to-date.

---

## Technologies Used

- Python 3.13+
- Selenium & BeautifulSoup (web scraping)
- Flask (web framework)
- Bootstrap (frontend styling)
- schedule (Python package for periodic scraping)
- ChromeDriver & WebDriver Manager

---

## Setup and Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Makoninio/courseReview.git
   cd courseReview
