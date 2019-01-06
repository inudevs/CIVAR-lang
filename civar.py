from enum import Enum

class State(Enum):
    none = 0
    civar_c = 1
    civar_i = 2
    civar_var = 3
    ha = 4
    ah = 5
    dot = 6
    comma = 7

while True:
    line = input('>> ').strip()
    if line == ':quit':
        break
    
    current_num = 0
    civar_count = 0
    dot_count = 0
    comma_count = 0

    current_state = State.none
    char_state_map = {' ' : State.none,
                      '시' : State.civar_c,
                      '이' : State.civar_i,
                      '바' : State.civar_var,
                      '하' : State.ha,
                      '아' : State.ah,
                      '.' : State.dot,
                      ',' : State.comma}

    final_str = ""
    current_col = 0
    current_row = 0

    for char in line:
        if (char == '시' and current_state == State.none) or \
           (char == '이' and current_state in [State.civar_c, State.civar_i]) or \
           (char == '바' and current_state in [State.civar_c, State.civar_i]):
            civar_count += 1
        elif char == '.':
            if current_state in [State.civar_var, State.dot]:
                dot_count += 1
            elif current_state in [State.ha, State.ah]:
                current_num += 1
                continue

        elif char == ',':
            if current_state in [State.civar_var, State.comma]:
                comma_count += 1
            elif current_state in [State.ha, State.ah]:
                current_num -= 1
                continue

        elif char == ' ' and current_state in [State.dot, State.comma]:
            if dot_count > 0:
                current_num += civar_count * dot_count
            else:
                current_num -= civar_count * comma_count

            civar_count = 0
            dot_count = 0
            comma_count = 0
            current_state = State.none

        elif (char == '하' and current_state == State.none) or \
             (char == '아' and current_state in [State.none, State.ha, State.ah]):
            final_str += chr(current_num)

            civar_count = 0
            dot_count = 0
            comma_count = 0

        elif char == '\n':
            current_col += 1
            continue

        else:
            print("오류! : " + str(current_col + 1) + "행 " + str(current_row + 1) + "열에서 유효하지 않은 문자 발견")
            exit()

        current_state = char_state_map[char]
        current_row += 1

    print(final_str)