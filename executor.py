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
            input_series = self._get_input_series(line.input_args, variables)

            result = self.transformations.run(
                line.transformation_name,
                line.config_args,
                input_series,
            )

            variables[line.target] = result

        return ExecutionResult(variables)

    def _get_input_series(
        self,
        input_args: list[str],
        variables: dict[str, list[float]],
    ) -> list[list[float]]:
        input_series = []

        for variable_name in input_args:
            if variable_name not in variables:
                raise ValueError(f"Unknown variable '{variable_name}'")

            input_series.append(variables[variable_name])

        return input_series
