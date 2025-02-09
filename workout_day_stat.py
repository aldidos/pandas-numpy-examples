import pandas as pd
from workout_day_report import WorkoutDayReport

class StatWorkout : 
    def stat(self, df : pd.DataFrame) :
        self.num_workout_days = df['date'].drop_duplicates().count()
        self.num_workouts = df['workout'].drop_duplicates().count()
        self.total_workout_volume = 0

        workout_date_groups = df.groupby('date')
        list_reports = []
        for name, workout_date_group in workout_date_groups : 
            workout_day_report = WorkoutDayReport(workout_date_group) 

            self.total_workout_volume = self.total_workout_volume + workout_day_report.get_total_volume()

            list_reports.append({
                'date' : name, 
                'report' : workout_day_report.get_report_dict()                
            })
        
        return {
            'num_workout_days' :  self.num_workout_days,
            'num_total_workout_time' : self.num_workouts,
            'total_workout_volume' : self.total_workout_volume, 
            'workout_reports' : list_reports
        }
    
df = pd.read_csv('./data/temp_data_2.csv')
stat = StatWorkout()
dayreports = stat.stat(df)
print(dayreports)


      