import random


class TempExcept(Exception):
    """기타 임시 에러 (다시 입력 받기 위함)"""
    pass


class BreakExcept(Exception):
    """10회째 시도때 못 맞출시 발생시킬 에러"""
    pass


def random_int_generator() -> int:
    """중복된 숫자 없는 난수 생성"""
    answer = random.randint(1000, 9999)  # 4자리 난수 생성
    while True:
        temp = True
        for i in range(4):
            temp_list = [0, 1, 2, 3]  # 매 반복마다 리스트를 다시 설정
            temp_list.remove(i)  # 같은 자리는 무조건 같은 숫자이므로, 같은 자리 제외하고 비교
            for item in temp_list:
                if str(answer)[i] == str(answer)[item]:  # 같은 숫자가 두번 이상 쓰이면 난수 다시 생성
                    answer = random.randint(1000, 9999)
                    temp = False
                    break  # 같은 숫자 있는거 확인 후에는 처음부터 다시 검증 시작
            if not temp:
                break
        if temp:  # 같은 숫자가 없으면 temp는 계속 True로 유지됨. 그럼 그대로 난수를 사용하면 됨.
            break
    return answer  # 난수 반환


if __name__ == "__main__":
    try_cnt = 0  # 시행 횟수
    ans = random_int_generator()  # 랜덤으로 생성하고 싶으면, random_int_generator()를 사용하고, 고정하고 싶다면 대신 특정 값을 입력한다. (단, 4자리 정수로)

    while True:
        strike_cnt = 0  # 스트라이크 개수
        ball_cnt = 0  # 볼 개수
        out_cnt = 0  # 아웃 개수
        # 위의 세 변수들은 모두 매번 초기화 함.
        try:
            if try_cnt == 10:  # 시행 횟수가 10회째면, 종료
                raise BreakExcept("기회를 모두 사용하셨습니다.")  # 종료시 출력할 메시지

            user_input = input("4자리 숫자를 입력하세요: ")  # 입력 받기

            if 1000 <= int(user_input) <= 9999:  # 숫자 범위 확인 & int형으로 형변환 안되면 ValueError 발생
                pass
            else:
                raise TempExcept("\"4자리\" 숫자를 입력해 주세요.(맨 앞자리는 0 불가)\n")  # 숫자 범위에서 어긋날시 강제 오류 발생, 다시 입력 받음

            for i in range(4):
                temp_list_ = [0, 1, 2, 3]  # 매 반복마다 리스트를 다시 설정
                temp_list_.remove(i)  # 같은 위치는 비교하면 안됨
                for item_ in temp_list_:
                    if user_input[i] == user_input[item_]:  # 같은 숫자가 두번 이상 쓰이면 다시 입력 받음
                        raise TempExcept("같은 숫자는 없습니다. 다시 입력해 주세요.\n")
            else:
                temp_list2 = [0, 1, 2, 3]  # 매 반복마다 리스트를 다시 설정
                for j in range(4):
                    if str(ans)[j] == user_input[j]:  # 위치가 같으면 strike_cnt 1 증가
                        strike_cnt += 1
                        temp_list2.remove(j)  # 스트라이크로 확인된 user_input의 인덱스는 ball_cnt 때 비교할 필요가 없음; remove하기

                for item in temp_list2:  # 위에서 strike는 제거한 리스트를 가져옴
                    temp_bool = True
                    temp_list3 = [0, 1, 2, 3]
                    temp_list3.remove(item)
                    for items in temp_list3:
                        if user_input[item] == str(ans)[items]:  # 위치가 다르지만 숫자가 같으면 ball_cnt 1 증가
                            ball_cnt += 1
                            temp_bool = False
                            break
                    if temp_bool:
                        out_cnt += 1

        except ValueError:
            print("4자리 \"숫자\"를 입력해 주세요.\n")  # 10진수로 변환 불가 ex) 영어, 특수문자...일 경우 ValueError가 발생
            continue

        except BreakExcept as e:
            print(e)
            print(f"정답은 {ans}였습니다.")  # 10회째까지도 맞추지 못했을 경우, 정답 공개
            break

        except TempExcept as e:
            print(e)
            continue

        else:
            try_cnt += 1
            if strike_cnt == 4:
                print(f"{strike_cnt} Strikes, Game Ends")  # 스트라이크 4개면 출력 후 종료
                break

            print(f"{strike_cnt} Strikes {ball_cnt} Balls {out_cnt} Outs")  # 스트라이크 4개가 아닌 다른 경우의 출력

            if try_cnt <= 9:
                print(f"{10 - try_cnt}번의 기회가 남았습니다.\n")  # 남은 기회 표시 (9번째 시도 까지만 출력)

