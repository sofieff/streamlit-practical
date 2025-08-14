#task 6 in tab 1: create a simple model (conda install scikit-learn -y; Randomforest Regressor): 
    #features only 3 columns: ['GDP per capita', 'headcount_ratio_upper_mid_income_povline', 'year']; target: 'Life Expectancy (IHME)'
    #you might store the code in an extra model.py file

    #make input fields for inference of the features (according to existing values in the dataset) and use the model to predict the life expectancy for the input values
    #additional: show the feature importance as a bar plot

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

def train_life_expectancy_model(data: pd.DataFrame):
    """
    Trains a RandomForestRegressor model to predict life expectancy.
    
    Args:
        data (pd.DataFrame): The input DataFrame containing the features and target.

    Returns:
        tuple: A tuple containing the trained model and the R-squared score.
    """
     # Define features and target
    features = ['GDP per capita', 'headcount_ratio_upper_mid_income_povline', 'year']
    target = 'Life Expectancy (IHME)'

    # Separate the data into features (X) and target (y)
    X = data[features]
    y = data[target]

    # Initialize the RandomForestRegressor model with a specific random state for reproducibility
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    # Train the model
    model.fit(X, y)


    # Get the feature importances from the trained model
    feature_importances = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False) 
    
    return model, feature_importances