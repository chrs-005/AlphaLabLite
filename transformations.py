import csv

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
        if input_series:
            raise ValueError(f"Fetch does not expect input series")
        
        if len(config_args)!=1:
            raise ValueError(f"Fetch expects only one datasource")
        
        datasource = config_args[0]

        with open("fetch_transformation_data.csv", "r") as file:
            reader = csv.reader(file)

            for row in reader:
                if row[0] == datasource: return [float(v) for v in row [1:]]

        raise ValueError(f"Unknown datasource '{datasource}'")
    
    def trans_SimpleMovingAverage(self, config_args, input_series):

        if len(config_args)!=1:
            raise ValueError(f"SimpleMovingAverage expects only one window size")
        
        
        if len(input_series)!=1:
            raise ValueError(f"SimpleMovingAverage expects only one input series")
        
        serie=input_series[0]
        window_size=int(config_args[0])
        n=len(serie)
        
        output_series=[None]*n
        curr_s=0

        for i in range(window_size):
            curr_s+=serie[i]
        
        for i in range(window_size-1,n):
            output_series[i]=curr_s/window_size

            if i<n-1:
                curr_s-=serie[i-window_size+1]
                curr_s+=serie[i+1]

        return output_series

    

