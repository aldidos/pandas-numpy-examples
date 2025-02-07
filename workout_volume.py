import pandas as pd
from datetime import datetime

def get_set_count(df : pd.DataFrame) : 
    return df['set'].drop_duplicates().count()

def get_rep_count(df : pd.DataFrame) : 
    return df['rep'].drop_duplicates().count() 

def compute_total_volume(df : pd.DataFrame) : 
    set_count = get_set_count(df)
    rep_count = get_rep_count(df)
    weight_sum = df['weight'].sum()
    weight_sum = weight_sum / rep_count

    total_volume = weight_sum * set_count * rep_count
    return total_volume

def compute_volumes(df : pd.DataFrame, attrs, group_by_attrs, volume_type) : 
    sub_df = df[ attrs ]
    sub_df = sub_df.drop_duplicates()    

    groups = sub_df.groupby( group_by_attrs )
    sum_total_volume = 0
    list_result = []    
    for name, group in groups : 
        date = name[0]

        total_volume = compute_total_volume(group)
        sum_total_volume = sum_total_volume + total_volume
        list_result.append({
            'date' : date, 
            'volume_type' : volume_type, 
            'total_volume' : total_volume
        })

    return {
        'sum_total_volume' : sum_total_volume, 
        'total_volumes' : list_result
    }    

df = pd.read_csv('./data/temp_data.csv')
sub_df = df[ ['date', 'workout_id', 'exercise_library', 'body_part', 'set', 'rep', 'weight'] ]

v = compute_volumes(sub_df, ['date', 'workout_id', 'set', 'rep', 'weight'], ['date', 'workout_id'], 'workout')
v = compute_volumes(sub_df, ['date', 'workout_id', 'exercise_library', 'set', 'rep', 'weight'], ['date', 'workout_id', 'exercise_library'], 'exercise_library')
v = compute_volumes(sub_df, ['date', 'workout_id', 'body_part', 'set', 'rep', 'weight'], ['date', 'workout_id', 'body_part'], 'body_part')



    