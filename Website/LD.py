dict1 = {
  "rs9268576": {
    "rs1980493": 0.015,
    "rs3135365": 0.032,
    "rs9268576": 1.0,
    "rs9268645": 0.141,
    "rs9268853": 0.117
  },
  "rs9268645": {
    "rs1980493": 0.082,
    "rs3135365": 0.228,
    "rs9268576": 0.141,
    "rs9268645": 1.0,
    "rs9268853": 0.078
  },
  "rs9268853": {
    "rs1980493": 0.042,
    "rs3135365": 0.073,
    "rs9268576": 0.117,
    "rs9268645": 0.078,
    "rs9268853": 1.0
  },
      "rs1980493": {
    "rs1980493": 1.0,
    "rs3135365": 0.011,
    "rs9268576": 0.015,
    "rs9268645": 0.082,
    "rs9268853": 0.042
  },
  "rs3135365": {
    "rs1980493": 0.011,
    "rs3135365": 1.0,
    "rs9268576": 0.032,
    "rs9268645": 0.228,
    "rs9268853": 0.073
  },
  "rs9268576": {
    "rs1980493": 0.015,
    "rs3135365": 0.032,
    "rs9268576": 1.0,
    "rs9268645": 0.141,
    "rs9268853": 0.117
  },
  "rs9268645": {
    "rs1980493": 0.082,
    "rs3135365": 0.228,
    "rs9268576": 0.141,
    "rs9268645": 1.0,
    "rs9268853": 0.078
  },
  "rs9268853": {
    "rs1980493": 0.042,
    "rs3135365": 0.073,
    "rs9268576": 0.117,
    "rs9268645": 0.078,
    "rs9268853": 1.0
  },
      "rs1980493": {
    "rs1980493": 1.0,
    "rs3135365": 0.011,
    "rs9268576": 0.015,
    "rs9268645": 0.082,
    "rs9268853": 0.042
  },
  "rs3135365": {
    "rs1980493": 0.011,
    "rs3135365": 1.0,
    "rs9268576": 0.032,
    "rs9268645": 0.228,
    "rs9268853": 0.073
  },
  "rs9268576": {
    "rs1980493": 0.015,
    "rs3135365": 0.032,
    "rs9268576": 1.0,
    "rs9268645": 0.141,
    "rs9268853": 0.117
  },
  "rs9268645": {
    "rs1980493": 0.082,
    "rs3135365": 0.228,
    "rs9268576": 0.141,
    "rs9268645": 1.0,
    "rs9268853": 0.078
  },
  "rs9268853": {
    "rs1980493": 0.042,
    "rs3135365": 0.073,
    "rs9268576": 0.117,
    "rs9268645": 0.078,
    "rs9268853": 1.0
  }
}

#create the dataframe
df = pd.DataFrame.from_dict(dict_1, orient='index')
df = df.transpose()
df

#my attempt with the heatmap function
#import pandas as pd
#import seaborn as sns

#mask = np.zeros_like(df)
#mask[np.tril_indices_from(mask)] = True

#sns.heatmap(df, cmap="coolwarm", annot=True, mask=mask, square=True)


#all important code for the linkage disequilibrium plot here. 


#my attempt with the ld_plot

from ld_plot.ld_plot import ld_plot
import numpy as np 

#pip install ld_plot

def test_ld_plot():
    n = df.columns.values

    labels = [f'chr1.{i}' for i in n]
    
    figure = ld_plot(ld=df, labels=labels)
    #matplotlib.rc('axes',edgecolor='green')
    plt.xticks(fontsize=6)

test_ld_plot()
