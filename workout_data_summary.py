import pandas as pd

class SummaryWorkoutData : ####

    def total_workout_time(self, df : pd.DataFrame) : 
        temp_df = pd.DataFrame(df)
        temp_df['duration'] = pd.to_datetime(temp_df['end_time']) - pd.to_datetime(temp_df['start_time'])
        temp_df[['date', 'workout', 'duration']].drop_duplicates()
        return temp_df['duration'].sum()

    def get_set_count(df : pd.DataFrame) : 
        return df['set'].drop_duplicates().count()

    def get_rep_count(df : pd.DataFrame) : 
        return df['rep'].count()

    def compute_volume(df : pd.DataFrame) : 
        sub_df = df[[ 'set', 'rep', 'weight' ]]
        sub_df = sub_df.drop_duplicates()

        set_count = SummaryWorkoutData.get_set_count( sub_df )
        rep_count = SummaryWorkoutData.get_rep_count( sub_df )
        weight_sum = sub_df['weight'].sum() / sub_df['weight'].count()

        total_volume = weight_sum * set_count * rep_count
        return float(total_volume)

    def compute_freq(df : pd.DataFrame, total_workout_sets) : 
        sub_df = df[[ 'set', 'rep', 'weight' ]]
        sub_df = sub_df.drop_duplicates() 

        num_set = SummaryWorkoutData.get_set_count(df)
        workout_freq = num_set / total_workout_sets
        return float(workout_freq)
    
    def compute_metric_value_summary_by_set(df : pd.DataFrame) : 
        ## category : [exercise_library, set], [body_part, set]  
        ## data type : ### [ 'peak_velocity_con', 'mean_velocity_con', 'peak_power_con',	'mean_power_con',	'peak_foce_con', 'mean_foce_con',	'peak_acceleration_con',	'mean_acceleration_con',	'peak_velocity_ecc',	'mean_velocity_ecc',	'peak_power_ecc',	'mean_power_ecc',	'peak_foce_ecc',	'mean_foce_ecc',	'peak_acceleration_ecc',	'mean_acceleration_ecc',	'rep_duration_con',	'rep_duration_ecc',	'top_stay_duration'	'bottom_stay_duration',	'rep_start'	'rep_end',	'RSI','RFD']

        list_set_summary = []

        set_groups = df.groupby('set')
        for set_name, set_group in set_groups :             
            set_group['rep_duration_con'] = pd.to_timedelta( set_group['rep_duration_con'] )
            set_group['rep_duration_ecc'] = pd.to_timedelta( set_group['rep_duration_ecc'] )
            set_group['top_stay_duration'] = pd.to_timedelta( set_group['top_stay_duration'] )
            set_group['bottom_stay_duration'] = pd.to_timedelta( set_group['bottom_stay_duration'] )
            set_group['rep_duration'] = pd.to_timedelta( set_group['rep_end'] )  - pd.to_timedelta( set_group['rep_start'] ) 

            result = set_group[['peak_velocity_con', 'mean_velocity_con', 'peak_power_con',	'mean_power_con',
                                'peak_foce_con', 'mean_foce_con','peak_acceleration_con','mean_acceleration_con',
                                'peak_velocity_ecc', 'mean_velocity_ecc', 'peak_power_ecc',	'mean_power_ecc', 'peak_foce_ecc', 'mean_foce_ecc',	'peak_acceleration_ecc', 
                                'mean_acceleration_ecc', 
                                'rep_duration_con',	'rep_duration_ecc',	'top_stay_duration', 'bottom_stay_duration', 'rep_duration', 
                                'RSI','RFD']].agg(['sum', 'mean', 'max', 'min']) 
            
            list_set_summary.append( {
                'set' : set_name, 
                'summary' : result.to_dict()
            })
        
        return list_set_summary