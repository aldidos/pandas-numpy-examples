import pandas as pd
import numpy as np

class UserFVPProfile : 

    def compute(self, df : pd.DataFrame) : 
        weights = df['weight']
        velocities = df['velocity']
        powers = df['power']

        n_data = len(weights)
        sum_x  = np.sum(weights)
        sum_y  = np.sum(velocities)
        sum_xy = np.sum(weights * velocities)
        sum_x2 = np.sum(weights**2)

        aa = (sum_x * sum_y)
        bb = (n_data * sum_xy)

        B_u = ((n_data * sum_xy) - (sum_x * sum_y))
        B_b = ((n_data * sum_x2) - sum_x**2)

        B = (n_data * sum_xy - sum_x * sum_y) / (n_data * sum_x2 - sum_x**2)
        A = (sum_y - B * sum_x) / n_data

        a = A       # 무부하 시 이론적 최대 속도
        b = -B      # 하중 1kg당 속도 감소율

        MVT = 0.2
        weight_1RM = (a - MVT) / b

        weight_range = np.linspace(min(weights)-5, max(weights)+5, 100)
        velocity_fit = a - b * weight_range
        power_fit = weight_range * velocity_fit  # 파워 = weight * velocity

        print()

list_data = [{ 'weight' : 100, 'velocity' : 5, 'power' : 10 },
 { 'weight' : 100, 'velocity' : 5, 'power' : 10 },
 { 'weight' : 100, 'velocity' : 5, 'power' : 10 },
 { 'weight' : 100, 'velocity' : 5, 'power' : 10 },
 { 'weight' : 100, 'velocity' : 5, 'power' : 10 }]

df = pd.DataFrame(list_data)

fvp_profile = UserFVPProfile()

fvp_profile.compute(df)
