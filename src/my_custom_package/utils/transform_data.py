def remove_collinear_cols(X_data):
    return X_data.drop([3, 8], axis=1)