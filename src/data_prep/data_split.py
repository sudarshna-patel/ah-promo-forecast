import datetime
import yaml

## Load parameters from param.yaml
params=yaml.safe_load(open("configs/params.yaml"))['train']

def train_test_split(total_df, tr_split_date):
    tr_df = total_df[total_df['DateKey'].dt.date <= tr_split_date].copy()
    tst_df = total_df[total_df['DateKey'].dt.date > tr_split_date].copy()
    return tr_df, tst_df

def format_as_category(df_data):
    df_data['GroupCode'] = df_data['GroupCode'].astype('category')
    df_data['ItemNumber'] = df_data['ItemNumber'].astype('category')
    df_data['CategoryCode'] = df_data['CategoryCode'].astype('category')
    return df_data

def add_lagged_feature_to_df(input_df, lag_iterator, feature):
    """
    A function that will expand an input dataframe with lagged variables of a specified feature
    Note that the lag is calculated over time (datekey) but also kept appropriate over itemnumber (article)
    
    input_df: input dataframe that should contain the feature and itemnr
    lag_iterator: an object that can be iterator over, that includes info about the requested nr of lags
    feature: feature that we want to include the lag of in the dataset
    """
    output_df = input_df.copy()
    for lag in lag_iterator:
        df_to_lag = input_df[['DateKey', 'ItemNumber', feature]].copy()
        # we add the nr of days equal to the lag we want
        df_to_lag['DateKey'] = df_to_lag['DateKey'] + datetime.timedelta(days=lag)
        
        # the resulting dataframe contains sales data that is lag days old for the date that is in that row
        df_to_lag = df_to_lag.rename(columns={feature: feature+'_-'+str(lag)})
        
        # we join this dataframe on the original dataframe to add the lagged variable as feature
        output_df = output_df.merge(df_to_lag, how='left', on=['DateKey', 'ItemNumber'])
    # drop na rows that have been caused by these lags
    return output_df.dropna()


def split_data(df_prep_clean):
    df_to_split = df_prep_clean.copy()
    
    # We split the data in a train set and a test set, we do this, 80, 20 percent respectively.
    nr_of_unique_dates = len(df_to_split.DateKey.unique())
    train_split_delta = round(nr_of_unique_dates * 0.8)
    train_split_date = df_to_split.DateKey.dt.date.min() + datetime.timedelta(days=train_split_delta)
    
    train_df, test_df = train_test_split(total_df=df_to_split, tr_split_date=train_split_date)

    train_df = format_as_category(df_data=train_df)

    # determine unique item numbers, and filter the validation and test on these
    items_we_train_on = train_df['ItemNumber'].unique()
    test_df_filtered = test_df[test_df['ItemNumber'].isin(items_we_train_on)].copy()

    test_df_filtered = format_as_category(df_data=test_df_filtered)

    range_of_lags = params["range_of_lags"]
    feature_to_lag = params["feature_to_lag"]

    # make the lags per dataset (no data leakage) and also do the NaN filtering per set
    train_df_lag = add_lagged_feature_to_df(input_df=train_df, lag_iterator=range_of_lags, feature=feature_to_lag)
    test_df_lag = add_lagged_feature_to_df(input_df=test_df_filtered, lag_iterator=range_of_lags, feature=feature_to_lag)

    train_df_lag_clean = train_df_lag.drop(columns=['DateKey'])
    test_df_lag_clean = test_df_lag.drop(columns=['DateKey'])

    # train_df_lag_clean.info()

    return train_df_lag_clean, test_df_lag_clean