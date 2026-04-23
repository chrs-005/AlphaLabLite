class Transformations:
    def __init__(self):
        self.transformations = self._build_transformations()

    def run(self, transformation_name, config_args, input_series):
        if transformation_name not in self.transformations:
            raise ValueError(f"Unknown transformation '{transformation_name}'")

        transformation = self.transformations[transformation_name]
        return transformation(config_args, input_series)

    def _build_transformations(self):
        transformations = {}

        for method_name in dir(self):
            if not method_name.startswith("trans_"):
                continue

            transformation_name = method_name.replace("trans_", "", 1)
            transformations[transformation_name] = getattr(self, method_name)

        return transformations

    def trans_Fetch(self, config_args, input_series):
        print("Hi")
        return [420]
