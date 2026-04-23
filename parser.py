class ProgramLine:
    def __init__(
        self,
        target: str,
        transformation_name: str,
        config_args: list[str],
        input_args: list[str],
    ):
        self.target = target
        self.transformation_name = transformation_name
        self.config_args = config_args
        self.input_args = input_args


class Program:
    def __init__(self, lines: list[ProgramLine]):
        self.lines = lines


class Parser:

    def parse(self, script) -> Program:
        lines = []

        for i, raw_line in enumerate(script.splitlines()):
            line = raw_line.strip()

            if not line:
                continue

            program_line = self._parse_line(line, i)
            lines.append(program_line)

        return Program(lines)

    def _parse_line(self, line, line_num) -> ProgramLine:
        if "=" not in line:
            raise ValueError(f"Line {line_num}: missing '=' ")

        left, right = line.split("=", 1)
        target = left.strip()

        if target == "":
            raise ValueError(f"Line {line_num}: invalid target '{target}'")

        transformation_name, config_args, input_args = self._parse_call(
            right.strip(), line_num
        )

        return ProgramLine(
            target=target,
            transformation_name=transformation_name,
            config_args=config_args,
            input_args=input_args,
        )

    def _parse_call(self, call, line_num) -> tuple[str, list[str], list[str]]:
        first_open = call.find("{") #finds first { - - } for transf name
        first_close = call.find("}")

        if first_open == -1 or first_close == -1 or first_close < first_open:
            raise ValueError(f"Line {line_num}: invalid transformation call")

        transformation_name = call[:first_open].strip()
        if transformation_name == "":
            raise ValueError(
                f"Line {line_num}: invalid transformation '{transformation_name}'"
            )

        config_call = call[first_open + 1 : first_close]
        rest = call[first_close + 1 :].strip()

        if not rest.startswith("{") or not rest.endswith("}"):
            raise ValueError(f"Line {line_num}: expected second block")

        input_call = rest[1:-1]

        config_args = self._split_args(config_call,line_num)
        input_args = self._split_args(input_call,line_num)

        return transformation_name, config_args, input_args

    def _split_args(self, text, line_num) -> list[str]:
        text = text.strip()

        if text == "": #empty args
            return []

        pieces = text.split(",")
        args = []

        for piece in pieces:
            arg = piece.strip()

            if arg == "":
                raise ValueError(f"Line {line_num}: Found an empty argument")

            args.append(arg)

        return args
