import pandas as pd

if __name__ == "__main__":
    # json 파일 읽기
    data = pd.read_json("./data/fitness_and_health_discussions.json")

    # 각 댓글을 별도의 행으로 변환합니다.
    flattened_data = []
    for discussion in data["discussions"]:
        title = discussion["title"]
        content = discussion["content"]
        for i, comment in enumerate(discussion["comments"]):
            # 처음 comment에만 title과 content을 추가합니다.
            if i == 0:
                flattened_data.append({"title": title, "content": content, "comment": comment})
            else:
                flattened_data.append({"title": "", "content": "", "comment": comment})

    # DataFrame 생성
    df = pd.DataFrame(flattened_data)

    # Excel 파일로 저장
    df.to_excel("fitness_and_health_discussions.xlsx", index=False, engine="openpyxl")

    print("Excel 파일이 생성되었습니다.")
