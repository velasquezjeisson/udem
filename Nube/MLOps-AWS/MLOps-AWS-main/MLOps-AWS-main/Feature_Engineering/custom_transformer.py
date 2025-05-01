import time
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
import numpy as np

# Add two new indicators
# 1. no_previous_contact: indicates whether the client has been contacted before or not
# 2. not_working: indicates whether the client is a student, retired, or unemployed
df["no_previous_contact"] = (df["pdays"] == 999).astype("int8")
df["not_working"] = df["job"].isin(["student", "retired", "unemployed"]).astype("int8")
# cast pdays column type to double precision
df['pdays']=df['pdays'].astype(np.float64)

# Add unique ID and event time for features store
df['FS_ID'] = df.index + 1000
current_time_sec = int(round(time.time()))
df['FS_time'] = pd.Series([current_time_sec]*len(df), dtype="float64")


# compute the vif and drop columns greater than 1.2 threshold
# vif is a measure of multicollinearity in a set of variables
# if the vif is greater than 1.2, it means that the variable is highly correlated with other variables in the set
# and should be dropped
def compute_vif(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """Compute the Variance Inflation Factor (VIF) for each feature in a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the features.
    threshold : float
        The threshold for determining multicollinearity.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the VIF for each feature.
    """
    names=['age','euribor3m','campaign','not_working', 'no_previous_contact']
    considered_features= [name for name in names if name in df.columns]
    subset=df[considered_features]
    subset=subset.dropna()
    subset['intercept'] = 1
    vif = pd.DataFrame()
    vif["Variable"] = subset.columns
    vif["VIF"] = [variance_inflation_factor(subset.values, i) for i in range(subset.shape[1])]
    vif = vif[vif['Variable']!='intercept']
    vif=vif.sort_values('VIF', ascending=False)
    print(vif)
    drop_clm=vif.index[vif.VIF.gt(threshold)].tolist()
    drop_clm_names=vif.loc[drop_clm]['Variable'].tolist()
    df.drop(drop_clm_names, axis=1, inplace=True)
    return df


df=compute_vif(df, 1.2)