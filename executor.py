from parser import Program


class ExecutionResult:
    def __init__(self, variables: dict[str, list[float]]):
        self.variables = variables


class Executor:
    def __init__(self, trans_runner):
        self.trans_runner = trans_runner

    def execute(self, program: Program) -> ExecutionResult:
        variables = {}

        for line in program.lines:
            input_series = []

            for variable_name in line.input_args:
                if variable_name not in variables:
                    raise ValueError(f"Unknown variable '{variable_name}'")

                input_series.append(variables[variable_name])

            result = self.trans_runner.run(
                line.transformation_name,
                line.config_args,
                input_series,
            )

            variables[line.target] = result

        return ExecutionResult(variables)
