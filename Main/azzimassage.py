import random

def azzimassage(inputmassage):
    print(inputmassage)
    # 인삿말 응답
    if inputmassage == "안녕":
        return random.choice(["왈왈!", "반갑당!"])
    elif inputmassage == "잘있어":
        return "두고 가지 마세요 ㅠㅠㅠ"
    elif inputmassage == "ㅂㅂ":
        return random.choice(["잘가랑!", "어디강ㅇ뭉?"])
    elif inputmassage == "왈랄ㄹ랄루":
        return random.choice(["왈랄ㄹ랄ㄹㄹ루!", "왈랄ㄹㄹㄹㄹㄹㄹ랄ㄹ루!"])
    elif inputmassage == "hi":
        return "wofwof!"
    elif inputmassage == "こんにちは":
        return "ワン！"
    elif inputmassage == "ㅎㅇㅎㅇ":
        return "멍멍!"

    #음식 특정 키워드 응답
    elif inputmassage == "초콜릿":
        return random.choice(["깨꼬닥", "이런건 못먹는당ㅇ멍!"])
    elif inputmassage == "뼈":
        return random.choice(["냠냠ㅁㅁ!!!","(와그작와그작)"])
    elif inputmassage == "라면":
        return "꼬불꼬불 꼬불꼬불 맛좋은 라면ㄴㅁ멍!"


    else:
        return random.choice(["왕?", "우웅?", "왈?", "와왕?", "끼잉?", "그응?"])