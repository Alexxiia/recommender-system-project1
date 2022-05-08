# Load libraries ---------------------------------------------

from datetime import datetime, timedelta
from unittest import skip
from dateutil.easter import easter
from data_preprocessing.dataset_specification import DatasetSpecification

import pandas as pd
import numpy as np
# ------------------------------------------------------------


class ItemFeatures(object):

    # #########################
    # Item features functions
    # #########################

    @staticmethod
    def i_room_popularity_percentage_feature(interactions_df):
        """
        Adds column "room_popularity", which shows popularity of the room based on visits in it and the most popular room in the hotel (not by sum of all visits in rooms).

        :param pd.DataFrame df: DataFrame interactions_df.
        :return: A DataFrame with added column, name of the column
        :rtype: pd.DataFrame
        """

        room_populatiry_ranking = interactions_df['item_id'].value_counts().to_frame().reset_index()
        room_populatiry_ranking.columns = ['item_id', 'popularity']

        most_popular_room = room_populatiry_ranking.iloc[0]['popularity']

        def popularity(room, room_populatiry_ranking):
            return room_populatiry_ranking[room_populatiry_ranking['item_id'] == room]['popularity'].item()/most_popular_room

        interactions_df['room_popularity'] = interactions_df['item_id'].apply(lambda x:popularity(x, room_populatiry_ranking))
        interactions_df['room_popularity'] = pd.to_numeric(interactions_df['room_popularity'])

        def get_feature_columns():
            return ["room_popularity"]

        return interactions_df, get_feature_columns()

    @staticmethod
    def i_room_popularity_peopl_amount_feature(interactions_df):
        """
        Adds column "room_popularity_amount", which shows amount of people who visited the room.

        :param pd.DataFrame df: DataFrame interactions_df.
        :return: A DataFrame with added column, name of the column
        :rtype: pd.DataFrame
        """

        room_populatiry_ranking = interactions_df['item_id'].value_counts().to_frame().reset_index()
        room_populatiry_ranking.columns = ['item_id', 'popularity']

        def popularity(room, room_populatiry_ranking):
            return room_populatiry_ranking[room_populatiry_ranking['item_id'] == room]['popularity'].item()

        interactions_df['room_popularity_amount'] = interactions_df['item_id'].apply(lambda x:popularity(x, room_populatiry_ranking))
        interactions_df['room_popularity_amount'] = pd.to_numeric(interactions_df['room_popularity_amount'])

        def get_feature_columns():
            return ["room_popularity_amount"]

        return interactions_df, get_feature_columns()

    @staticmethod
    def i_room_price_expensiveness_feature(interactions_df):
        """
        Adds column "room_avg_price", which shows the average price of the room.

        :param pd.DataFrame df: DataFrame interactions_df.
        :return: A DataFrame with added column, name of the column
        :rtype: pd.DataFrame
        """

        # "if" below makes the code repeatable and makes sure that column below does not exist before merge
        if 'room_avg_price' in interactions_df:
            del interactions_df['room_avg_price']     

        replace_df = interactions_df.replace({
            "[0-160]" : 80 , "[160-260]" : 210, "[260-360]" : 310 , "[360-500]" : 430, "[500-900]" : 700, "[900-inf]" : 1450
        })

        room_avg_prices = replace_df.copy().groupby('item_id', as_index=False)
        room_avg_prices = room_avg_prices['room_segment'].mean()
        
        room_avg_prices.columns = ['item_id', 'room_avg_price']

        interactions_df = pd.merge(interactions_df, room_avg_prices, on='item_id',how="left")
        interactions_df['room_avg_price'] = pd.to_numeric(interactions_df['room_avg_price'])

        def get_feature_columns():
            return ["room_avg_price"]

        return interactions_df, get_feature_columns()

    @staticmethod
    def i_room_space_for_people_feature(interactions_df):
        """
        Adds column "room_space", which shows the average amount of people who can use the room.

        :param pd.DataFrame df: DataFrame interactions_df.
        :return: A DataFrame with added column, name of the column
        :rtype: pd.DataFrame
        """

        # "if" below makes the code repeatable and makes sure that column below does not exist before merge
        if 'room_space' in interactions_df:
            del interactions_df['room_space']     

        replace_df = interactions_df.replace({
            "[1-1]" : 1, "[2-2]" : 2, "[3-4]" : 3.5, "[5-inf]" : 17
        })

        room_spaces = replace_df.copy().groupby('item_id', as_index=False)['n_people_bucket'].mean()
        room_spaces.columns = ['item_id', 'room_space']

        interactions_df = pd.merge(interactions_df, room_spaces, on='item_id',how="left")
        interactions_df['room_space'] = pd.to_numeric(interactions_df['room_space'])

        def get_feature_columns():
            return ["room_space"]

        return interactions_df, get_feature_columns()
