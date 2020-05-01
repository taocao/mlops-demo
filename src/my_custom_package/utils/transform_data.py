def remove_collinear_cols(X_data):
    return X_data.drop(['D', 'I'], axis=1)
