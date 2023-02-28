dict_1 = {
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

pip install ld_plot
import pandas as pd
from ld_plot.ld_plot import ld_plot
import numpy as np 
import matplotlib.pyplot as plt
plt.style.use('ggplot')

#create the dataframe
df = pd.DataFrame.from_dict(dict_1, orient='index')
df = df.transpose()
df

def test_ld_plot():
    n = df.columns.values

    labels = [f'chr1.{i}' for i in n]
    
    figure = ld_plot(ld=df, labels=labels)
    #matplotlib.rc('axes',edgecolor='green')
    plt.xticks(fontsize=7)
    
    #plt.imshow(cmap='RdBu')
    #plt.cm.Blues


test_ld_plot()


