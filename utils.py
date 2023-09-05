import requests
from bs4 import BeautifulSoup
import re
import json


def get_soup(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return soup


# 문자열에서 숫자를 추출합니다.
def extract_numbers_from_string(input_string):
    result = "".join(char for char in input_string if char.isdigit())
    return result


# discussions 페이지의 마지막 페이지 번호를 가져옵니다.
def get_last_page_number_in_discussions(soup):
    page_numbers = soup.find_all("span", "pagination__text")
    last_page_number = page_numbers[-1].text
    last_page_number = extract_numbers_from_string(last_page_number)
    return int(last_page_number)


# discussions 페이지의 모든 토론 url을 가져옵니다.
def get_discussions_url(soup):
    urls = []
    post_a_tags = soup.find_all("a", "discussion-post-item-title")
    for post_a_tag in post_a_tags:
        urls.append(post_a_tag.get("href"))
    return urls


# 토론 상세페이지의 마지막 페이지 번호를 가져옵니다.
def get_last_page_number_in_discussion(soup):
    page_numbers = soup.find_all("a", "pagination__page")

    if len(page_numbers) == 0:
        return 1

    last_page_number = page_numbers[-2].text
    last_page_number = extract_numbers_from_string(last_page_number)
    return int(last_page_number)


# 토론 상세페이지에서 Comments를 가져옵니다.
def get_comments(soup):
    comments = []
    comment_divs = soup.find_all("div", id=re.compile("msg_\w+"))
    for comment_div in comment_divs:
        comment = clean_string(comment_div.text)
        comments.append(comment)
    return comments


# 토론 상세페이지에서 토론의 제목을 가져옵니다.
def get_title(soup):
    title = soup.find("h1", id="postTitle")
    title = clean_string(title.text)
    return title


# 토론 상세페이지에서 토론의 내용을 가져옵니다.
def get_content(soup):
    contents = soup.find_all("div", class_="com-post-content")
    content = contents[0].text
    content = clean_string(content)
    return content


# 문자열을 다듬습니다.
def clean_string(str):
    str = str.strip()
    str = " ".join(str.split())
    return str


# 전체 Comments의 개수를 가져옵니다.
def get_total_comments_count(soup):
    total_comments_count = soup.find("h2", id="replies")
    if total_comments_count is None:
        return 0
    total_comments_count = clean_string(total_comments_count.text)
    total_comments_count = extract_numbers_from_string(total_comments_count)
    return int(total_comments_count)


# json 파일을 씁니다.
def write_json_file(json_format, file_name):
    with open(f"./data/{file_name}.json", "w") as outfile:
        json.dump(json_format, outfile, indent="\t")
