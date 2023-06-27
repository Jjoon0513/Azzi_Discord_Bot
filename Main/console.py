import json

# azzisnack.json 파일에 초기 데이터 추가
initial_snack_data = {"snack_count": {}}
with open("azzisnack.json", "w") as file:
    json.dump(initial_snack_data, file)

# azzisnackid.json 파일에 초기 데이터 추가
initial_snackid_data = {"snack_count": {}}
with open("azzisnackid.json", "w") as file:
    json.dump(initial_snackid_data, file)