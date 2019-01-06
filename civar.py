import argparse
import re
from enum import Enum

class State(Enum):
    none = 0
    civar = 1
    dot = 2
    comma = 3
    ha = 4
    space = 5

def interpret_civar(line):
    parser_exp = re.compile(r'[.]+|[,]+|시이*바|하아*|아+| +')
    parse_result = parser_exp.findall(line)

    civar_count = 0
    dot_count = 0
    comma_count = 0

    def tag_block(block):
        if block.startswith('시'):
            return State.civar
        elif block.startswith('.'):
            return State.dot
        elif block.startswith(','):
            return State.comma
        elif block.startswith(('하', '아')):
            return State.ha
        elif block.startswith(' '):
            return State.space

    current_state = State.none
    previous_state = State.none

    current_num = 0
    final_str = ""

    for block in parse_result:
        current_state = tag_block(block)
        block_len = len(block)
        
        if current_state == State.civar:
            civar_count += block_len

        elif current_state == State.dot:
            if previous_state == State.civar:
                dot_count += block_len
            elif previous_state == State.ha:
                current_num += block_len

        elif current_state == State.comma:
            if previous_state == State.civar:
                comma_count += block_len
            elif previous_state == State.ha:
                current_num -= block_len

        elif current_state == State.ha:
            final_str += chr(current_num) * block_len

        elif current_state == State.space:
            if dot_count > 0:
                current_num += civar_count * dot_count
            elif comma_count > 0:
                current_num -= civar_count * comma_count

            civar_count = 0
            dot_count = 0
            comma_count = 0

        previous_state = current_state
    
    return final_str

def run_repl():
    while True:
        line = input('>> ').strip()
        if line == ':quit':
            break
        
        print(interpret_civar(line))

def main():
    parser = argparse.ArgumentParser(description="CIVAR-lang interpreter")
    parser.add_argument("input", nargs='?', help="Location of an input file")
    args, _ = parser.parse_known_args()

    if args.input is not None:
        with open(args.input, 'r') as code_file:
            print(interpret_civar(code_file.read()))
    else:
        run_repl()

if __name__ == "__main__":
    main()