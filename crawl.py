from copy import deepcopy
from constants import json_base_format, url
from utils import (
    get_discussions_url,
    get_last_page_number_in_discussions,
    get_soup,
    get_last_page_number_in_discussion,
    get_title,
    get_content,
    get_comments,
    get_total_comments_count,
    write_json_file,
)

if __name__ == "__main__":
    soup = get_soup(url)
    last_page_number = get_last_page_number_in_discussions(soup)

    # discussion을 저장할 json 포맷입니다.
    json_format = deepcopy(json_base_format)

    # 1 ~ last_page_number까지의 페이지를 순회하며 토론의 title과 url을 가져옵니다.
    for page_number in range(1, last_page_number + 1):
        print(f"pages: {page_number} / {last_page_number}")

        soup = get_soup(f"{url}--{page_number}")
        discussion_urls = get_discussions_url(soup)

        # 추출한 토론 상세 페이지 마지막 페이지 까지 모든 Comments를 가져옵니다.
        for idx, discussion_url in enumerate(discussion_urls[:4]):
            print(f"  discussions: {idx + 1} / {len(discussion_urls)}")
            soup = get_soup(discussion_url)
            title = get_title(soup)
            content = get_content(soup)
            total_comments_count = get_total_comments_count(soup)
            comments = []
            print(f"    comments: {total_comments_count}")

            # Comments가 없는 토론은 건너뜁니다.
            if total_comments_count == 0:
                continue

            last_page_number = get_last_page_number_in_discussion(soup)
            for page_number in range(1, last_page_number + 1):
                soup = get_soup(f"{discussion_url}?page={page_number}")
                comments.extend(get_comments(soup))

            json_format["discussions"].append({"title": title, "content": content, "comments": comments})

    write_json_file(json_format, "fitness_and_health_discussions")
