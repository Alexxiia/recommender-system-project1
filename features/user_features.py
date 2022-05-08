# Load libraries ---------------------------------------------

from datetime import datetime, timedelta
from dateutil.easter import easter
from data_preprocessing.dataset_specification import DatasetSpecification

import pandas as pd
import numpy as np
# ------------------------------------------------------------


class UserFeatures(object):

    # #########################
    # User features functions
    # #########################

    @staticmethod
    def u_most_popular_feature(interactions_df):
        """
        Adds columns "most_popular_term", "most_popular_len_of_stay", "most_popular_rate_plan", "most_popular_room_segment", "most_popular_n_people", "most_popular_weekend_stay", which shows if the user chose the most popular options.

        :param pd.DataFrame df: DataFrame interactions_df.
        :return: A DataFrame with added columns, list of added column names.
        :rtype: pd.DataFrame
        """

        most_popular_term = interactions_df['term'].value_counts().index[0]
        most_popular_len_of_stay = interactions_df['length_of_stay_bucket'].value_counts().index[0]
        most_popular_rate_plan = interactions_df['rate_plan'].value_counts().index[0]
        most_popular_room_segment = interactions_df['room_segment'].value_counts().index[0]
        most_popular_n_people = interactions_df['n_people_bucket'].value_counts().index[0]
        most_popular_weekend_stay = interactions_df['weekend_stay'].value_counts().index[0]

        def is_most_popular(element, most_popular):
            if(element == most_popular):
                return 1
            else:
                return 0

        interactions_df['most_popular_term'] = interactions_df['term'].apply(lambda x:is_most_popular(x, most_popular_term))
        interactions_df['most_popular_len_of_stay'] = interactions_df['length_of_stay_bucket'].apply(lambda x:is_most_popular(x, most_popular_len_of_stay))
        interactions_df['most_popular_rate_plan'] = interactions_df['rate_plan'].apply(lambda x:is_most_popular(x, most_popular_rate_plan))
        interactions_df['most_popular_room_segment'] = interactions_df['room_segment'].apply(lambda x:is_most_popular(x, most_popular_room_segment))
        interactions_df['most_popular_n_people'] = interactions_df['n_people_bucket'].apply(lambda x:is_most_popular(x, most_popular_n_people))
        interactions_df['most_popular_weekend_stay'] = interactions_df['weekend_stay'].apply(lambda x:is_most_popular(x, most_popular_weekend_stay))

        interactions_df['most_popular_term'] = pd.to_numeric(interactions_df['most_popular_term'])
        interactions_df['most_popular_len_of_stay'] = pd.to_numeric(interactions_df['most_popular_len_of_stay'])
        interactions_df['most_popular_rate_plan'] = pd.to_numeric(interactions_df['most_popular_rate_plan'])
        interactions_df['most_popular_room_segment'] = pd.to_numeric(interactions_df['most_popular_room_segment'])
        interactions_df['most_popular_n_people'] = pd.to_numeric(interactions_df['most_popular_n_people'])
        interactions_df['most_popular_weekend_stay'] = pd.to_numeric(interactions_df['most_popular_weekend_stay'])

        def get_feature_columns():
            return ["most_popular_term", "most_popular_len_of_stay", "most_popular_rate_plan", "most_popular_room_segment", "most_popular_n_people", "most_popular_weekend_stay"]

        return interactions_df, get_feature_columns()

    @staticmethod
    def u_most_popular_probability_feature(interactions_df):
        """
        Adds columns "most_popular_term", "most_popular_len_of_stay", "most_popular_rate_plan", "most_popular_room_segment", "most_popular_n_people", "most_popular_weekend_stay", which shows the percentage of popularity options, chose by user.

        :param pd.DataFrame df: DataFrame interactions_df.
        :return: A DataFrame with added columns, list of added column names.
        :rtype: pd.DataFrame
        """

        most_popular_term = interactions_df['term'].value_counts()
        most_popular_len_of_stay = interactions_df['length_of_stay_bucket'].value_counts()
        most_popular_rate_plan = interactions_df['rate_plan'].value_counts()
        most_popular_room_segment = interactions_df['room_segment'].value_counts()
        most_popular_n_people = interactions_df['n_people_bucket'].value_counts()
        most_popular_weekend_stay = interactions_df['weekend_stay'].value_counts()

        def is_most_popular(element, most_popular):
            return most_popular[element]/most_popular.sum()

        interactions_df['most_popular_term'] = interactions_df['term'].apply(lambda x:is_most_popular(x, most_popular_term))
        interactions_df['most_popular_len_of_stay'] = interactions_df['length_of_stay_bucket'].apply(lambda x:is_most_popular(x, most_popular_len_of_stay))
        interactions_df['most_popular_rate_plan'] = interactions_df['rate_plan'].apply(lambda x:is_most_popular(x, most_popular_rate_plan))
        interactions_df['most_popular_room_segment'] = interactions_df['room_segment'].apply(lambda x:is_most_popular(x, most_popular_room_segment))
        interactions_df['most_popular_n_people'] = interactions_df['n_people_bucket'].apply(lambda x:is_most_popular(x, most_popular_n_people))
        interactions_df['most_popular_weekend_stay'] = interactions_df['weekend_stay'].apply(lambda x:is_most_popular(x, most_popular_weekend_stay))

        interactions_df['most_popular_term'] = pd.to_numeric(interactions_df['most_popular_term'])
        interactions_df['most_popular_len_of_stay'] = pd.to_numeric(interactions_df['most_popular_len_of_stay'])
        interactions_df['most_popular_rate_plan'] = pd.to_numeric(interactions_df['most_popular_rate_plan'])
        interactions_df['most_popular_room_segment'] = pd.to_numeric(interactions_df['most_popular_room_segment'])
        interactions_df['most_popular_n_people'] = pd.to_numeric(interactions_df['most_popular_n_people'])
        interactions_df['most_popular_weekend_stay'] = pd.to_numeric(interactions_df['most_popular_weekend_stay'])

        def get_feature_columns():
            return ["most_popular_term", "most_popular_len_of_stay", "most_popular_rate_plan", "most_popular_room_segment", "most_popular_n_people", "most_popular_weekend_stay"]

        return interactions_df, get_feature_columns()

    @staticmethod
    def u_average_values_feature(interactions_df):
        """
        Adds columns "averange_length_of_stay", "averange_room_segment", "averange_n_people", which shows the percentage of popularity options, chose by user.

        :param pd.DataFrame df: DataFrame interactions_df.
        :return: A DataFrame with added columns, list of added column names.
        :rtype: pd.DataFrame
        """
        
        # "if" below makes the code repeatable and makes sure that columns below do not exist before merge
        if 'average_length_of_stay' in interactions_df:
            del interactions_df['average_length_of_stay']
        if 'average_room_segment' in interactions_df:
            del interactions_df['average_room_segment']        
        if 'average_n_people' in interactions_df:
            del interactions_df['average_n_people']        


        replace_df = interactions_df.replace({
            "[1-1]" : 1, "[2-2]" : 2, "[3-4]" : 3.5, "[5-inf]" : 17, "[0-1]" : 0.5, "[2-3]" : 2.5, "[4-7]" : 5.5, "[8-inf]" : 14.5, "[0-160]" : 80 , "[160-260]" : 210, "[260-360]" : 310 , "[360-500]" : 430, "[500-900]" : 700, "[900-inf]" : 1450
        })

        personal_averange_len_of_stay = replace_df.copy().groupby('user_id', as_index=False)['length_of_stay_bucket'].mean()
        personal_averange_len_of_stay.columns = ['user_id', 'averange_length_of_stay']

        personal_averange_room_segment = replace_df.copy().groupby('user_id', as_index=False)['room_segment'].mean()
        personal_averange_room_segment.columns = ['user_id', 'averange_room_segment']

        personal_averange_n_people = replace_df.copy().groupby('user_id', as_index=False)['n_people_bucket'].mean()
        personal_averange_n_people.columns = ['user_id', 'averange_n_people']

        interactions_df = pd.merge(interactions_df, personal_averange_len_of_stay, on='user_id',how="left")
        interactions_df = pd.merge(interactions_df, personal_averange_room_segment, on='user_id',how="left")
        interactions_df = pd.merge(interactions_df, personal_averange_n_people, on='user_id',how="left")

        interactions_df['averange_length_of_stay'] = pd.to_numeric(interactions_df['averange_length_of_stay'])
        interactions_df['averange_room_segment'] = pd.to_numeric(interactions_df['averange_room_segment'])
        interactions_df['averange_n_people'] = pd.to_numeric(interactions_df['averange_n_people'])

        def get_feature_columns():
            return ["averange_length_of_stay", "averange_room_segment", "averange_n_people"]

        return interactions_df, get_feature_columns()
        
    @staticmethod
    def u_feature(interactions_df):
        """
        Adds columns "most_popular_term", "most_popular_len_of_stay", "most_popular_rate_plan", "most_popular_room_segment", "most_popular_n_people", "most_popular_weekend_stay", which shows the percentage of popularity options, chose by user.

        :param pd.DataFrame df: DataFrame interactions_df.
        :return: A DataFrame with added columns, list of added column names.
        :rtype: pd.DataFrame
        """

        #TO DO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!S



        def get_feature_columns():
            return [""]

        return interactions_df, get_feature_columns()
