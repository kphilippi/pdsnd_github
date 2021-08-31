#!/usr/bin/env python
# coding: utf-8

# In[2]:


import time
import calendar
import pandas as pd
import numpy as np

chicago = pd.read_csv('c:/users/Bruce/Documents/Udacity/Python_Project/bikeshare-2/chicago.csv')
new_york_city = pd.read_csv('c:/users/Bruce/Documents/Udacity/Python_Project/bikeshare-2/new_york_city.csv')
washington = pd.read_csv('c:/users/Bruce/Documents/Udacity/Python_Project/bikeshare-2/washington.csv')


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }


# The get function below, when applied to a dictionary produced the value that corresponds to the key.


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    print()


    # This loop will get the city the user wants to explore, convert case to lower & prompt user to re-enter if input is incorrect.
    # While loops will handle any incorrect entries for city, month and/or day.

    while True:
        city = input("What city would you like to explore? Chicago, New York or Washington? ").lower()
        if city in ['chicago', 'new york', 'washington']:
            break
        else:
            print('Something went wrong. Please re-enter the name of the city. ')


    # This loop will get the month the user wants to explore, convert case to title & prompt user to re-enter if input is incorrect.

    while True:
        month = input("What month would you like to explore? Please enter January - June or all if you want to see data from all months. ").title()
        if month in ['January', 'February', 'March', 'April', 'May', 'June', 'All']:
            break
        else:
            print('Something went wrong. Please enter the month again. ')


    # This loop will get the month the user wants to explore, convert case to title & prompt user to re-enter if input is incorrect.

    while True:
        day = input("What day would you like to explore? Please enter Sunday - Saturday or all if you want to see data from all days. ").title()
        if day in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All']:
            break
        else:
            print('Something went wrong. Please enter the day again. ')

    print('You have chosen to view the data for the city of ', city)
    print('You have added the filters for: ', month, ' & ', day)


    print('-'*40)
    return city, month, day




### Load data for selected city filtered by month and day ###

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])



    # Using the datetime function, convert the Start Time column to something more usable: YYYY-MM-DD then add a month and day column to the dataframe.

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] =  df['Start Time'].dt.day_name()

    # Since months are listed by number in datetime function, the corresponding number is assigned to the month entered by the user.

    if month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
        month = months.index(month) + 1

    # Create the df Month

        df = df[df['month'] == month]

    # Do the same thing for Day of the Week. Since the day of the week is determined by the entire date so no need to index by day.

    if day != 'All':
        df = df[df['day_of_week'] == day.title()]


    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Finding the most popular month and day to travel.

    pop_month = df['month'].mode()[0]
    pop_day = df['day_of_week'].mode()[0]

    # To find the most popular time to travel, first add an hour column to the df.
    # Note: the month and day columns were added to sort the data by month & day based on user input. Hour was not.

    df['hour'] = df['Start Time'].dt.hour
    pop_hour = df['hour'].mode()[0]

    # display the most common month

    print('The most common month to travel is: {}'.format(pop_month))
    print()

    # display the most common day of week

    print('The most common day to travel is: {}'.format(pop_day))
    print()

    # display the most common start hour

    print('The most common time to start traveling is: ',pop_hour,':00')
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Using the mode function on the pre-existing Start Station and End Station Columns

    # TO DO: display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]

    # TO DO: display most commonly used end station
    most_common_end = df['End Station'].mode()[0]

    print('start: ', most_common_start, 'end: ', most_common_end)

    # TO DO: display most frequent combination of start station and end station trip

    # Group the start & end stations into one column using the groupby function, then return the trip with the most occurances

    pop_trip = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('The most popular trip is between the following two stations: \n', pop_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    # Use math functions to find the min, max, total & average time of travel. +- one standard deviation gives 68.2% of travel.
    # Convert number of seconds to hours, minutes & seconds.


    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    total_travel_time = df['Trip Duration'].sum()
    m, s = divmod(total_travel_time, 60)
    h, m = divmod(m, 60)
    sec = round(s)
    print('Total Travel Time is {} hours, {} minutes {} seconds.'.format(h, m, sec))
    print()

    # TO DO: display mean travel time

    mean_travel_time = df['Trip Duration'].mean()
    mm, ss = divmod(mean_travel_time, 60)
    hh, mm = divmod(mm, 60)
    ssec = round(ss)
    print('Average Travel Time is {} hours, {} minutes {} seconds.'.format(hh, mm, ssec))
    print()

    # Maximum trip length

    max_travel_time = df['Trip Duration'].max()
    maxm, maxs = divmod(max_travel_time, 60)
    maxh, maxm = divmod(maxm, 60)
    maxsec = round(maxs)
    print('The maximum trip length is {} hours, {} minutes {} seconds.'.format(maxh, maxm, maxsec))
    print()

    # Minimum trip length

    min_travel_time = df['Trip Duration'].min()
    minm, mins = divmod(min_travel_time, 60)
    minh, minm = divmod(minm, 60)
    minsec = round(mins)
    print('The minumum trip length is {} hours, {} minutes {} seconds.'.format(minh, minm, minsec))
    print()
    print()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    # Type of users - counting user types in a pre-existing column
    # Using the value_counts() function when the columns contain some NaN data.


    user_type = df['User Type'].value_counts()
    print('Breakdown of type of users:')
    print(user_type)
    print()


    # Since user data is only available for New York and Chicago

    if 'Gender' in df.columns:
        #Displays the number of individuals identifying as male and female
        gender = round(df['Gender'].value_counts())
        print('Breakdown of number of riders by gender:')
        print(gender)
        print()
    else:
        print('User data / Gender is not available for Washington')

    if 'Birth Year' in df.columns:
        # Calculates birth year data using math functions
        min_year = round(df['Birth Year'].min())
        max_year = round(df['Birth Year'].max())
        ave_year = round(df['Birth Year'].mean())
        most_year = round(df['Birth Year'].mode()[0])
        std_dev_y = round(df['Birth Year'].std())
        lower_year = ave_year - std_dev_y
        upper_year = ave_year + std_dev_y

        # Display earliest, most recent, and most common year of birth

        print('Earliest birth year: ', min_year)
        print()
        print('Latest birth year: ', max_year)
        print()
        print('Average birth year: ', ave_year)
        print()
        print('Most common birth year: ', most_year)
        print()
        print('Most riders were born between ', lower_year, ' & ', upper_year)

    else:
        print('User data / Birth Year is not available for Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    # See Raw Data option - I used the help in the knowledge section of Udacity

    view_raw_data = input('Would you like to view the raw data (5 rows at a time)? Yes or No? ').lower()

    row_index = 0

    while True:
        if view_raw_data == 'yes':

            print(df[row_index: row_index + 5])
            row_index = row_index + 5
            view_raw_data = input('\nView five more rows of the data? Yes or No? ').lower()
        elif view_raw_data == 'no':
            break
        else:
            print('Something went wrong. Please enter yes or no. ')

# This function allows program to run until user says to stop.

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no? \n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:
