import sys

def run_bind(prog, env=([], [0], 0)):
    stack, tape, tape_ptr = env
    pc = 0
    while pc < len(prog):
        if prog[pc] == '@':
            stack.append(tape[tape_ptr])
        elif prog[pc] == ';':
            stack.pop()
        elif prog[pc] == '<':
            tape_ptr -= 1
            if tape_ptr == -1:
                tape = [0] + tape
                tape_ptr += 1
        elif prog[pc] == '>':
            tape_ptr += 1
            if tape_ptr == len(tape):
                tape.append(0)
        elif prog[pc] == 'Z':
            tape[tape_ptr] = 0
        elif prog[pc] == 'S':
            tape[tape_ptr] += 1
        elif prog[pc] == '[':
            seek = pc + 1
            level = 1
            while level > 0:
                level += prog[seek] == '['
                level -= prog[seek] == ']'
                seek += 1

            tmp = prog[pc+1:seek-1]
            while 1:
                stack, tape, tape_ptr = run_bind(tmp, (stack, tape, tape_ptr))
                if tape[tape_ptr] + 1 == stack[-1]:
                    break

            pc = seek - 1
        pc += 1
    return (stack, tape, tape_ptr)

if __name__ == '__main__':
    f = open(sys.argv[1]).read()
    print(run_bind(f))
