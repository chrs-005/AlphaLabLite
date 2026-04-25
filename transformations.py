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
        #Automatically collect every method that starts with "trans_" into the transformation map
        #Add any future transformation using "trans_TRANSFORMATIONCALLNAME"

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

        if len(config_args)!=1 or int(config_args[0])<=0:
            raise ValueError(f"SimpleMovingAverage expects only one positive window size")
        
        
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

    def trans_ExponentialMovingAverage(self, config_args, input_series):

        if len(config_args)!=1:
            raise ValueError(f"ExponentialMovingAverage expects only one smoothing factor")
        
        
        if len(input_series)!=1:
            raise ValueError(f"ExponentialMovingAverage expects only one input series")
        
        serie=input_series[0]
        alpha=float(config_args[0])
        n=len(serie)
        
        output_series=serie.copy()

        for i in range(1,n):
            output_series[i]*=alpha
            output_series[i]+=(1-alpha)*output_series[i-1]

        return output_series

    def trans_RateOfChange(self, config_args, input_series):
        

        if len(config_args)!=1:
            raise ValueError(f"RateOfChange expects only one period")
        
        
        if len(input_series)!=1:
            raise ValueError(f"RateOfChange expects only one input series")
        
        serie=input_series[0]
        period=int(config_args[0])
        n=len(serie)
        
        output_series=[None]*n

        for i in range(period, n):
            prev=serie[i-period]
            if abs(prev)>1e-9:
                output_series[i]=(serie[i]-prev)/prev

        return output_series

    def trans_CrossAbove(self, config_args, input_series):

        if config_args:
            raise ValueError(f"CrossAbove does not expect config args")
        
        
        if len(input_series)!=2:
            raise ValueError(f"CrossAbove expects only two input series")
        
        serie1=input_series[0]
        serie2=input_series[1]
        n=min(len(serie1), len(serie2))

        output_series=[0]*n

        for i in range(1,n):
            if serie1[i-1] is None or serie2[i-1] is None or serie1[i] is None or serie2[i] is None:
                continue

            if serie1[i-1]<serie2[i-1] and serie1[i]>serie2[i]:
                output_series[i]=1

        return output_series

    def trans_ConstantSeries(self, config_args, input_series):

        if len(config_args)!=1:
            raise ValueError(f"ConstantSeries expects only one constant")
        
        
        if len(input_series)!=1:
            raise ValueError(f"ConstantSeries expects only one input series")
        
        k=float(config_args[0])
        serie=input_series[0]
        n=len(serie)
        
        output_series=[k]*n

        return output_series

    def trans_PortfolioSimulation(self, config_args, input_series):

        if len(config_args)!=1:
            raise ValueError(f"PortfolioSimulation expects only one initial balance")
        
        
        if len(input_series)!=3:
            raise ValueError(f"PortfolioSimulation expects three input series")
        
        balance=float(config_args[0])
        entry=input_series[0]
        exit=input_series[1]
        price=input_series[2]
        n=min(len(entry), len(exit), len(price))
        
        output_series=[None]*n
        positions_held=0

        for i in range(n):
            if exit[i]==1:
                balance+=positions_held*price[i]
                positions_held=0
            elif entry[i]==1:
                positions_held+=1
                balance-=price[i]

            output_series[i]=balance+positions_held*price[i]

        return output_series
