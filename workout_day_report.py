import pandas as pd
from workout_data_summary import SummaryWorkoutData

class WorkoutDayReport : 

    def __init__(self, df : pd.DataFrame) : 
        sub_df = df[['workout', 'set']].drop_duplicates()
        self.total_sets = sub_df['set'].count()
        
        self.exercise_lib_reports = self.create_volume_freq_reports(df, ['workout_session', 'workout', 'exercise_library'] )
        self.body_part_reports = self.create_volume_freq_reports(df, ['workout_session', 'workout', 'body_part'] )

    def create_volume_freq_reports(self, df : pd.DataFrame, group_attrs) : 
        exercise_lib_reports = []

        df_groups = df.groupby(group_attrs)
        for name, df_group in df_groups : 
            exercise_lib = name[2] 

            vol_fre_report = self.compute_report(df_group) 

            exercise_lib_reports.append({
                'name' : exercise_lib, 
                'report' : vol_fre_report
            })

        return exercise_lib_reports

    def compute_report(self, df : pd.DataFrame) : 
        volume = SummaryWorkoutData.compute_volume(df)
        freq = SummaryWorkoutData.compute_freq(df, self.total_sets)
        set_summary = SummaryWorkoutData.compute_metric_value_summary_by_set(df)

        return { 'volume' : volume, 'freq' : freq, 'set_summary' : set_summary }

    def get_total_sets(self) : 
        return self.total_sets

    def get_exercise_library_reports(self) : 
        return self.exercise_lib_reports

    def get_body_part_reports(self) : 
        return self.body_part_reports
    
    def get_total_volume(self) : 
        total_volume = 0
        for el_report in self.exercise_lib_reports : 
            total_volume = total_volume + el_report['report']['volume']
        return total_volume

    # def get_total_distance(self) : 
    #     pass
    
    def get_report_dict(self) : 
        return {
            'total_workout_sets' : self.get_total_sets(), 
            'total_volume' : self.get_total_volume(), 
            'exercise_library_reports' : self.get_exercise_library_reports(), 
            'bodypart_reports' : self.get_body_part_reports()
        }