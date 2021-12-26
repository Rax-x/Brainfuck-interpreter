from sys import argv, stderr, stdin

STACK_SIZE: int = 30_000

class BrainfuckState:
    def __init__(self, source: str) -> None:
        self.source: str = source
        self.dp: int = 0
        self.data: list(int) = [0] * STACK_SIZE

class BrainfuckInterpreter:
    # private fields
    __state: BrainfuckState = None
    __ip: int = 0

    def __init__(self, file_path: str) -> None:
        self.__load(file_path)

    # private method
    def __load(self, file_path: str) -> None:
        try:
            with open(file_path, mode="r") as fp:
                source = fp.read()
                self.__state = BrainfuckState(source)
        except FileNotFoundError as ex:
            print(str(ex), file=stderr)
            exit(-1)

    def run(self) -> None:
        try:
            while self.__ip != len(self.__state.source):
                if self.__state.source[self.__ip] == '+':
                    self.__state.data[self.__state.dp] += 1
                elif self.__state.source[self.__ip] == '-':
                    self.__state.data[self.__state.dp] -= 1
                elif self.__state.source[self.__ip] == '>':
                    self.__state.dp += 1
                    if self.__state.dp > STACK_SIZE:
                        raise RuntimeError("Stack overflow!")
                elif self.__state.source[self.__ip] == '<':
                    if self.__state.dp > 0:
                        self.__state.dp -= 1
                elif self.__state.source[self.__ip] == '.':
                    print(chr(self.__state.data[self.__state.dp]), end='', flush=True)
                elif self.__state.source[self.__ip] == ',':
                    self.__state.data[self.__state.dp] = stdin.read(1) # read 1 byte from stdin...
                elif self.__state.source[self.__ip] == '[':
                    if self.__state.data[self.__state.dp] == 0:
                        nest = 0
                        while True:
                            self.__ip += 1

                            if self.__state.source[self.__ip] == ']':
                                if nest == 0:
                                    break
                                else:
                                    nest -= 1

                            if self.__state.source[self.__ip] == '[':
                                nest += 1
                elif self.__state.source[self.__ip] == ']':
                    if self.__state.data[self.__state.dp] != 0:
                        nest = 0
                        while True:
                            self.__ip -= 1

                            if self.__state.source[self.__ip] == '[':
                                if nest == 0:
                                    break
                                else:
                                    nest -= 1

                            if self.__state.source[self.__ip] == ']':
                                nest += 1
                self.__ip += 1
        except RuntimeError as ex:
            print(str(ex), file=stderr)
            exit(-1)


if __name__ == '__main__':
    if len(argv) > 1:
        BrainfuckInterpreter(argv[1]).run()
    else:
        print(f"\nUsage: ./{argv[0]} <source file>\n", file=stderr)