import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://tdobbins:tdobbins@localhost/econ')

import pandas as pd

sb_stores = pd.read_csv('/Users/tdobbins/Downloads/the_general/StarbucksStores.csv')
zip_counties = pd.read_csv('/Users/tdobbins/Downloads/the_general/ZipCodeCounties.csv', encoding='latin1')
zip_data = pd.read_csv('/Users/tdobbins/Downloads/the_general/ZIPData.csv')
zip_data2 = pd.read_csv('/Users/tdobbins/Downloads/the_general/ZIPData2.csv')
zip_data3 = pd.read_csv('/Users/tdobbins/Downloads/the_general/ZIPData3.csv')

tables = [
    ('sb_stores', sb_stores), 
    ('zipcodes', zip_counties),
    ('zip_data', zip_data),
    ('zip_data2', zip_data2),
    ('zip_data3', zip_data3)
]

for table, df in tables:
    df.replace({'-|': ''}, regex=True).apply(lambda x: pd.to_numeric(x, errors='ignore')).to_sql(table, engine, if_exists='replace', index=True)
    
    
zbp = pd.read_csv('/Users/tdobbins/Downloads/zbp12-13totals.csv', header=None)
zbp.to_sql('zbp', engine, if_exists='replace', index=True)

zipcode_to_fips = pd.read_csv('/Users/tdobbins/Downloads/BP_2014_00CZ2/BP_2014_00CZ2.csv', header=1)

###################### models #####

import statsmodels.api as sm
%matplotlib inline

path = '/Users/tdobbins/Desktop/zbp.csv'
sample = pd.read_csv(path)


#########################
# GLM model, results
#########################

admit_yn = sample.has_starbucks
score = sample.new_homes
# score = sample.GP5

score_with_intercept = sm.add_constant(score)

model = sm.GLM(admit_yn, score_with_intercept, family=sm.families.Binomial())
result = model.fit()

print result.summary()

import pylab as plt
from sklearn.metrics import roc_curve, auc
from sklearn import metrics
import numpy as np
from scipy import stats

admit_array = np.asarray(admit_yn)
pred = np.asarray(score)

# retrieve false-positive rates and true-positive rates
fpr, tpr, thresholds = metrics.roc_curve(admit_array, pred, pos_label=1)
metrics.auc(fpr, tpr)

#compute area under curve 
roc_auc = auc(fpr, tpr)

# plotting the ROC curve
roc_curve = plt.figure(figsize=(12,8))
plt.clf()
plt.plot(fpr, tpr, label='ROC curve (area = %0.3f)' % roc_auc)

# dashed line through the origin
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])

# labels and legend
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic curve')
plt.legend(loc="lower right")

from statsmodels.regression.quantile_regression import QuantReg

mod = smf.quantreg('starbucks_count ~ hotels + new_homes + HC03_VC88', df)
res = mod.fit(q=.5)
print(res.summary())

import statsmodels.formula.api as smf

mod = smf.ols(formula='starbucks_count ~ new_homes + hotels + HC03_VC88', data=df)
res = mod.fit()
print res.summary()

############################## False positives for logit regression

logit = sm.Logit(sample['has_starbucks'], sample[['new_homes','hotels','HC03_VC88','shopping_centers']])
# fit the model
result = logit.fit()
print result.summary()

sample['predict'] = result.predict(sample[['new_homes','hotels','HC03_VC88','shopping_centers']])
predict = sample[['new_homes','hotels','HC03_VC88', 'HC03_VC96', 'shopping_centers', 'has_starbucks', 'predict', 'zip']]
predict[(predict.has_starbucks==0)&(predict.predict>0.55)].sort_values(['predict'], ascending=[0])

## Correlation matrix

import seaborn as sns
corr = df[['sq_miles', u'HC03_VC96', 'HC03_VC88', 
           'shopping_centers', 'new_homes', 'hotels', 
           'population_density', 'starbucks_count', 
           'airport_related', 'colleges', 'HC01_VC118', 
           u'HC01_VC03', u'HC01_VC103',]].corr()

plt.subplots(figsize=(13,10)) 
sns.heatmap(corr, 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)