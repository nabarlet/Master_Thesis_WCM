import sys
import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('../../../Repo/BBC3/records_202203292154.csv',delimiter="\t")
df.head()
print(df.head())
df.hist(y='name', figsize=(10,8))
plt.show()
