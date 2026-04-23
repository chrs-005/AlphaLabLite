from parser import Program


class ExecutionResult:
    def __init__(self, variables: dict[str, list[float]]):
        self.variables = variables


class Executor:
    def __init__(self, transformations):
        self.transformations = transformations

    def execute(self, program: Program) -> ExecutionResult:
        variables = {}

        for line in program.lines:
            input_series = []

            for variable_name in line.input_args:
                if variable_name not in variables:
                    raise ValueError(f"Unknown variable '{variable_name}'")

                input_series.append(variables[variable_name])

            result = self.transformations.run(
                line.transformation_name,
                line.config_args,
                input_series,
            )

            variables[line.target] = result

        return ExecutionResult(variables)
