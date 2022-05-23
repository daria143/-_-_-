import requests
res = requests.post(url="http://127.0.0.1:3000/api/problems/3",
                    params={"question_id": 287, "question": "Какой процент по вкладам сейчас?"},
                    json={"question_id": 287, "question": "Какой процент по вкладам сейчас?"})
res = requests.post(url="http://127.0.0.1:3000/api/problems/4",
                    params={"question_id": 328, "question": "Я бы хотел узнать насчет своей задолженности по кредиту."},
                    json={"question_id": 328, "question": "Я бы хотел узнать насчет своей задолженности по кредиту."})
res.encoding = res.apparent_encoding
print(res.json())
