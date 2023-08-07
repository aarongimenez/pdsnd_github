import time
import pandas as pd
import calendar as cal

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    cities = list(CITY_DATA.keys())  # Retrieve city names from CITY_DATA dictionary
    
    while True:
        city = input("\nWhich city data would you like to look at? (Chicago/New York City/Washington)\n").lower()
        if city in cities:
            break
        else:
            print("\nPlease enter a valid city name.")
    
    while True:
        datefilter = input("\nWould you like to filter by date? (Yes/No)\n").lower()
        if datefilter == 'yes' or datefilter == 'no':
            break
        else:
            print("\nPlease enter 'yes' or 'no'.")
    
    if datefilter == 'no':
        month = 'all'
        day = 'all'
    else:
        months = list(cal.month_name)[1:7]  # Get the list of month names from the calendar module
        while True:
            month = input("\nWhich month would you like to filter by? (January/February/.../June)\n").title()
            if month in months:
                break
            else:
                print("\nPlease enter a valid month name.")
        
        days = list(cal.day_name) + ['None']  # Include 'None' as an option for day filter
        while True:
            day = input("\nWhich day of the week would you like to filter by? (Monday/Tuesday/.../Sunday)\n").title()
            if day in days:
                break
            else:
                print("\nPlease enter a valid day of the week.")
    
    print('-'*40)
    return city, month, day


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
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month if applicable
    if 'month' in df.columns:
        popular_month = df['month'].mode()[0]
        print("The most popular month is", popular_month)

    # Display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('\nThe most common day of the week is', popular_day)

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("\nThe most common start hour is {}:00".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most common starting station is', popular_start_station)

    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nThe most common end station is', popular_end_station)

    # Display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['trip'].mode()[0]
    print('\nThe most popular trip is', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_hours = total_travel_time // 60
    total_travel_time_minutes = total_travel_time % 60
    print('Total travel time is {} hours and {} minutes'.format(total_travel_time_hours, total_travel_time_minutes))

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nAverage travel time is', mean_travel_time, 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Count by user type:")
    print(user_types.to_string())

    # Display counts of gender if the 'Gender' column exists
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nCount by gender:")
        print(gender_counts.to_string())
    else:
        print("Gender information is not available for this dataset.")

    # Display earliest, most recent, and most common year of birth if the 'Birth Year' column exists
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])

        print('\nEarliest year of birth:', earliest_birth_year)
        print('Most recent year of birth:', recent_birth_year)
        print('Most common year of birth:', common_birth_year)
    else:
        print("\nBirth year information is not available for this dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Displays raw data upon user request."""
    start_loc = 0
    while True:
        show_data = input("Would you like to see the raw data? Enter 'yes' or 'no'.\n").lower()
        if show_data == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()