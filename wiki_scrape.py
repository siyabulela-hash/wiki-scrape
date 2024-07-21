import requests
from bs4 import BeautifulSoup

def scrape_wikipedia_section_headings(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the introductory section of the page
        introductory_section = soup.find('div', class_='mw-parser-output')

        if introductory_section:
            # Extract section headings from the introductory section
            headings = []
            for heading in introductory_section.find_all(['h2', 'h3', 'h4', 'h5', 'h6']):
                heading_text = heading.get_text(strip=True)
                # Clean up the heading text
                heading_text = heading_text.replace('[edit]', '')
                headings.append(heading_text)

            return headings
        else:
            print("No introductory section found on the page.")
            return None
    else:
        print(f"Failed to retrieve Wikipedia page. Status code: {response.status_code}")
        return None

def process_wikipedia_headings(headings):
    main_sections = []
    sub_sections = []

    for heading in headings:
        # Determine if it's a main section or sub-section based on heading level
        if heading.startswith('='):
            main_sections.append(heading.strip('= '))
        else:
            sub_sections.append(heading)

    return main_sections, sub_sections

# Main function to run the scraping and processing
if __name__ == "__main__":
    # Example URL: Wikipedia page about Python programming language
    wikipedia_url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'

    wikipedia_headings = scrape_wikipedia_section_headings(wikipedia_url)

    if wikipedia_headings:
        print("Wikipedia Section Headings:")
        for idx, heading in enumerate(wikipedia_headings, start=1):
            print(f"{idx}. {heading}")

        # Process the headings
        main_sections, sub_sections = process_wikipedia_headings(wikipedia_headings)

        print("\nProcessed Main Sections:")
        for idx, section in enumerate(main_sections, start=1):
            print(f"{idx}. {section}")

        print("\nSub-sections:")
        for idx, section in enumerate(sub_sections, start=1):
            print(f"{idx}. {section}")
    else:
        print("No headings retrieved.")
        