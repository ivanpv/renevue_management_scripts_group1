# -*- coding: utf-8 -*-
"""
@author: ivanp
"""

def main():
    import pandas as pd
    import numpy as np
    import scipy.stats as stats
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    data = pd.read_csv("./../WorldCruiseData.csv") 
    data.head()
    ship_capacity = 2094
    demand_withcancel =  data[data['CANCEL_WEEK_PRIOR'].isnull()]
    demand_over_50 = demand_withcancel[data['DURATION'] > 50]
    demand_under_50 = demand_withcancel[data['DURATION'] <= 50]
    
    demand_under_50_booking = demand_under_50['NO_OF_PEOPLE_ON_BOOKING'].reset_index(drop=True)
    
    list_demandpdf = []
    for idx , item in enumerate(demand_under_50['PRICE_PAID']):
       if item > 0 and demand_under_50_booking[idx] > 0:
           for i in range(demand_under_50_booking[idx]):
               list_demandpdf.append(item/demand_under_50_booking[idx])
    
    meeting_demand_over = demand_over_50["NO_OF_PEOPLE_ON_BOOKING"].sum()
    remaining_demand_under = ship_capacity - demand_over_50["NO_OF_PEOPLE_ON_BOOKING"].sum()

    np_arr_temp = demand_under_50[data['PRICE_PAID'] >= 0]
    np_arr = np_arr_temp["PRICE_PAID"].values
    np_arr_temp_pass = demand_under_50[data['NO_OF_PEOPLE_ON_BOOKING'] >= 0]
    np_arr_temp_pass_equality = np_arr_temp_pass[data['PRICE_PAID'] >= 0]
    np_arr_pass = np_arr_temp_pass_equality["NO_OF_PEOPLE_ON_BOOKING"].values
    
    def distribution_plot(data):
        """
            Plot a normal distribution related to the marks of the students.
        """
        ready_data = sorted((data))
        fit = stats.norm.pdf(ready_data, np.mean(ready_data), np.std(ready_data))
        plt.plot(ready_data, fit, '-o')
        plt.ylabel("Prob")
        plt.xlabel("Prices")
        plt.title("Distribution of prices (Under 50 days) Demand Function")
        plt.show()
        
    
    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

    
    def find_demand(average_distribution, max_willing, demand_depent):
        demand = demand_depent/(1-average_distribution/max_willing)
        return demand
    
    ready_listed = sorted(list_demandpdf)
    range_start_temp = input ("Please enter the start range in demand:\n")
    range_end_temp = input ("Please enter the end range in demand:\n")
    range_start = float(range_start_temp)
    range_end = float(range_end_temp)
    start = find_nearest(ready_listed,range_start)
    end = find_nearest(ready_listed,range_end)
    
    
    #distribution_plot(np_arr)
    plt.axvline(range_start, 0,1, color = "red")
    plt.axvline(range_end, 0,1, color = "red")
    distribution_plot(list_demandpdf)
    sns.distplot(list_demandpdf)
    ready_data = sorted((np_arr))
    fitted_under_50 = stats.norm.pdf(ready_data, np.mean(ready_data), np.std(ready_data))
    
    demand_2019 = find_demand(np.mean(np_arr), max(np_arr), sum(np_arr_pass))
    print(demand_2019)
    
    factor_input_text = 1 #input ("Please enter the new factor(Inflation, Market Shares, Expected Growth):\n")
    factor_input_text_bookings = 1 #input ("Please enter the new factor for bookings if required:\n")
    factor_input = float(factor_input_text)
    factor_input_bookings = float(factor_input_text_bookings)
    np.mean(np_arr*factor_input)
   # distribution_plot(np_arr*factor_input)
    
    index_distribution_year1_prices = find_nearest(np_arr*factor_input, np.mean(np_arr*factor_input))
    ready_data_temp = sorted((np_arr*factor_input))
    fitted_under_50_year1 = stats.norm.pdf(ready_data_temp, np.mean(ready_data_temp), np.std(ready_data_temp))
    prob_2020 = fitted_under_50_year1[index_distribution_year1_prices]
    index_distribution_year0_prob = find_nearest(fitted_under_50, prob_2020)
    expected_mean_2020 = np_arr[index_distribution_year0_prob]
    
    demand_2020 = find_demand((expected_mean_2020), max(np_arr*factor_input), sum(np_arr_pass)*factor_input_bookings)
    print(demand_2020)

    #find the total of bookings from a price
    print ("")
    print("For distribution standard deviation is {} mean is {}".format(np.std(list_demandpdf), np.mean(list_demandpdf)))
    print("For total demand (booking number between red lines) according to range of prices is {}".format(len(ready_listed[start:end])))

if __name__ == "__main__": main()
    # execute only if run as a script
    
    
    