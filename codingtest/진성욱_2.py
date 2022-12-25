import numpy as np


class RangeError(Exception):
    """범위가 오류났을 때 발생시킬 에러"""
    pass


"""
행렬 규칙을 보면 다음과 같다.
0. 이동할 때 마다 각 행렬에 대응되는 값은 1씩 증가
1. (0,0)에서 시작.
2. (0,1)까지 이동. (열 index 원래와 비교해서 +1만큼 이동)
3. (-1, 1)까지 이동. (행 index 원래와 비교해서 -1만큼 이동)
4. (-1, -1)까지 이동. (열 index 원래와 비교해서 -2만큼 이동)
5. (1, -1)까지 이동. (행 index 원래와 비교해서 +2만큼 이동)
6. 즉, 열(+1) -> 행(-1) -> 열(-2) -> 행(+2) -> 열(+3) -> 행(-3) -> ... 와 같이 변한다.
결국, 단위 이동량(delta_col: 초기값 1, delta_row: 초기값 -1)을 몇 번 이동시키는지를 알고, 이동 시킨 후에는 단위 이동량의 부호를 바꾸면 된다.
"""

"""
10001 x 10001 형태의 행렬을 만들지 않고 구하는 방법을 생각하려 했으나 잘 생각나지 않았습니다.
Python 특성상 실행에 시간이 꽤 걸릴 수 있습니다.
"""


def swirl_mat_generator() -> np.ndarray:  # 소용돌이 행렬 만드는 함수
    mat_list_ = np.ones((10001, 10001))  # 행, 열이 각 10001개인 행렬 생성; -5000~5000 X -5000~5000
    row = 0  # 행 번호; 이걸 위의 numpy를 이용한 다차원 리스트의 인덱스 값으로 사용할 것임.
    column = 0  # 열 번호; 위와 동일
    val = 1  # 행렬의 값. ex) (0,0)은 1이고, (0,1)은 2, (-1, 1)은 3 ...
    delta_row = -1  # row(행)의 단위 변화량 초깃값: -1
    delta_col = 1  # column(열)의 단위 변화량 초깃값: 1;
    row_count = 1  # 이번에는 단위 변화량 (delta_row)를 몇번 변화시킬 것인가를 나타내는 변수
    col_count = 1  # 위와 동일 (단위변화량만 delta_col)

    while -5000 <= row <= 5000 and -5000 <= column <= 5000:  # 주어진 범위 내의 값.
        mat_list_[row][column] = val  # (0,0)은 값이 1임
        for i in range(row_count):  # 단위 이동량을 몇 번 움직이는가?
            column += delta_col  # 열의 인덱스 바꾸기
            val += 1  # 행렬에 대응되는 값은 계속 1씩 증가
            mat_list_[row][column] = val  # 그리고 해당 행렬의 인덱스에 값을 대입
        col_count += 1  # 다음번에는 이동 횟수 1 증가
        delta_col = -delta_col  # 다음번에는 반대로 이동

    # 아래의 반복문은 위의 열 이동 때와 동일한 원리이다.
        for j in range(row_count):
            row += delta_row
            val += 1
            mat_list_[row][column] = val
        row_count += 1
        delta_row = -delta_row

    return mat_list_


if __name__ == "__main__":
    mat_list = swirl_mat_generator()
    while True:
        try:
            input_list = input("r1, c1, r2, c2를 순서대로 입력하세요.(-5000<=r1,c1,r2,c2<=5000, 0<=r2-r1<=49, 0<=c2-c1<=4): ").split()
            int_list = [int(item) for item in input_list]  # int로 형변환
            r1 = int_list[0]  # line 42까지, 알아보기 편하도록 변수에 대입
            c1 = int_list[1]
            r2 = int_list[2]
            c2 = int_list[3]

            for item in int_list:  # line 50까지 범위 확인 과정
                if not (-5000 <= item <= 5000):
                    raise RangeError("범위를 확인해 주세요.")
            if not (0 <= r2 - r1 <= 49):
                raise RangeError("범위를 확인해 주세요.")
            if not (0 <= c2 - c1 <= 4):
                raise RangeError("범위를 확인해 주세요.")

        except ValueError:  # line 39: 영어 등 int()로 형 변환 불가능한 문자를 입력시`
            print("\"숫자\"를 서로 스페이스 하나로 띄어서 \"4개\"입력해 주세요.")

        except IndexError:  # line 40 ~ 43: index에 접근 불가능 할 때
            print("\"숫자\"를 서로 스페이스 하나로 띄어서 \"4개\"입력해 주세요.")

        except RangeError as e:  # 범위가 틀릴 때
            print(e)

        else:
            for i in range(r1, r2 + 1):
                for j in range(c1, c2 + 1):
                    print("%5d" % (mat_list[i][j]), end='')  # 출력 형식 맞추기; 행렬 인덱스가 작을 경우 5자리로 하는게 가장 보기에 편했습니다. 커질 경우
                    # %6d, %7d...으로 늘리면 됩니다.
                print('')
            try:
                while True:
                    cont = input("계속 출력 하시겠습니까?---(y/n): ")  # 계속 반복할 것 인가를 입력받음.
                    if cont in ['Y', 'y']:  # Y, y == yes
                        break
                    elif cont in ['N', 'n']:  # N, n == no
                        raise StopIteration("프로그램을 종료합니다.")
                    else:
                        print("y(Y) 혹은 n(N)을 입력해 주십시오.")  # 다른게 입력되면 다시 물어봄 (line 80으로 복귀)
                        continue

            except StopIteration as e:  # 프로그램 종료; 비슷한 의미로 StopIteration 강제 발생
                print(e)
                break

            else:  # Yes 입력 받았으면, 다시 r1, c1, r2, c2값 입력받음
                continue
