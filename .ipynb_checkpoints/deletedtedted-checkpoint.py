def model_check(statistic, party, alternative = False):
    data = get_regresdat(statistic, party)
    statistic_val = data[statistic].values.reshape(-1,1)
    votes = data['perc_party'].values.reshape(-1,1)
    votes_log = np.log(votes)
    votes_div = 1/votes
    votes_square = np.power(votes,2)
    votes_sqrt = np.sqrt(votes)
    statistic2 = sm.add_constant(statistic_val)
    votes_types = {'votes': votes, 'votes_log':votes_log, 'votes_div':votes_div, 'votes_square':votes_square,'votes_sqrt': votes_sqrt}
    scores = pd.DataFrame(columns = ['type', 'Score'])
    for key, value in votes_types.items():
        try: 
            model = sm.OLS(value, statistic2).fit()
            val = val_calc(model, value, statistics2)
        except TypeError:
            val = 0
        appender = pd.Series([key, val], index = scores.columns)
        scores = scores.append(appender, ignore_index = True)
        scores['Score'] = pd.to_numeric(scores['Score'])
    row_max = scores['Score'].idxmax()
    vote_val = list(votes_types.items())[row_max][1]
    model = sm.OLS(vote_val, statistic2).fit()
    return(model)

temp = model_check('Gehuwd_31', 'SGP')
print(temp.summary())


 
#    return(model)
#temp = model_check('Gehuwd_31', 'SGP')
#print(temp)


def value_check(statistic, party):
    model = model_check(statistic, party)
    a =pd.DataFrame((model.summary().tables[2]))
    a.to_csv('calcfile.csv', index = False)
    z = pd.read_csv('calcfile.csv')
    #z.iloc[1,1] = prob_omnibus 
    #z.ilov[0,3] = durbin_watson
    val = 0
    if model.pvalues[1] > 0.05:
        print('Coefficient is not significant')
    # R-squared
    if model.rsquared > 0.05:
        val = val + 1
    # F-pvalue
    if model.f_pvalue < 0.05: 
        val = val + 1
    # pron_omibus
    if z.iloc[1,1] > 0.5: 
        val = val + 1
    # Durbin Watson
    if (z.iloc[0,3] < 2) and (z.iloc[0,3] > 1):
        val = val + 1
    appender = [statistic, party, model.params[1], model.pvalues[1], model.rsquared, 
                model.f_pvalue, z.iloc[1,1], z.iloc[0,3], val]
    series = pd.Series(appender, index = ['Statistic', 'Party', 'Coefficient', 'r2', 
                                             'f_pval', 'Prob_omni', 'Durbin-Watson', 'Score'])
    return(series)
                        

#model = model_check('Gehuwd_31', 'SGP')    
#q = value_check('Gehuwd_31', 'SGP')
#print(q)
#value_check(q)
#model.pvalues
import time 


#suppress warnings

data = get_regresdat(statistic, party)
def val_calc(model,votes,statistic): 
    df_summary =pd.DataFrame((model.summary().tables[2]))
    # Save and load to make values of tables available
    df_summary.to_csv('calcfile.csv', index = False)
    summary = pd.read_csv('calcfile.csv')
    fitted_vals = model.predict()
    resids = model.resid
    lilfor = sm.stats.diagnostic.lilliefors(resids, dist = 'norm', pvalmethod = 'approx')
    DW = sm.stats.stattools.durbin_watson(resids)
    linearyity = sm.formula.api,ols(formula = '
import statsmodels.formula.api as smf
# formula: response ~ predictor + predictor
est = smf.ols(formula='Sales ~ TV + Radio', data=df_adv).fit()
    linearity = sm.OLS(votes, statistic
    hetero = sm.OLS(np.power(resids,2), statistic)
    val = 0
    if model.rsquared > 0.05:
        val = val + 1
    # F-pvalue
    if model.f_pvalue < 0.05: 
        val = val + 1
    # Lilliefors: 
    if lilfor > 0.05: 
        val = val + 1
    # Heteroskedasticity: 
    if hetero.params[1] > 0.05:
        val = val + 1
        # model.params[1]
    if model.resid.mean() < 0.0001: 
        val = val + 1
    # pron_omibus
    if summary.iloc[1,1] > 0.5: 
        #print(summary.iloc[1,1])
        val = val + 1
    # Durbin Watson
    if (summary.iloc[0,3] < 2) and (summary.iloc[0,3] > 1):
        val = val + 1
    return(val)
                       

                       
1. Normality: Lilliefors. Not the strongest test, but I have worked with this before and therefore I use it. 
    If the pvalue is lower than some threshold, e.g. 0.05, then we can reject the Null hypothesis that the sample comes from a normal distribution.
    So if lower than 0.05, then it's not normally divided
2. Independence of error terms / autocorrelation: Durbin-Watson test
    Is that applicable? 
3. Nonlinearity: add squared value of predictions and see if they're significant
    If addition variable y^2 != significant (>0.05), model not specified (second order wouldn't improve it)
4. Homoskedasticity: Create residuals of linear regression. 
    square residuals 
    use as dependent observations for new model, regress against same independent variable 
    H0 = homoskedasticity, H1 not. If p-value < 0.05 then H0 rejected and not homoskedastic


* $R^2$: This represents how much of variation in the percentages of votes can be explained by a certain statistic. The lower boundary is 0.05, meaning that a certain statistic has to explain at least 5\% of the variation of the percentage of votes on a party. Although 5\% might seem very small, voting happens on a national level and therefore there are many factors that influence the percentage of votes for a party. 
* p-value of Lilliefors test: This checks for the normal distribution of the statistic. 
* Breusch-Pagan test and Goldfeld-Quandt test: to test for homoscedasticity / equal variance of the residuals 
* The Durbin-Watson statistic