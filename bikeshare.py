import time
import pandas as pd

# Mapping city names to their corresponding data files
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
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    
    # Obtain city input with validation
    city = input('Please enter a city (chicago, new york city, washington): ').lower()
    while city not in CITY_DATA:
        city = input('Invalid input. Please enter chicago, new york city, or washington: ').lower()
    
    # Obtain month input with validation
    month = input('Please enter a month (all, january, february, ... , june): ').lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input('Invalid input. Enter a valid month (all, january, february, ... , june): ').lower()

    # Obtain day input
    day = input('Please enter a day of the week (all, monday, tuesday, ... sunday): ').lower()
    
    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load the data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert 'Start Time' and 'End Time' to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Extract month and day of week from 'Start Time'
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_idx = months.index(month) + 1
        df = df[df['month'] == month_idx]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.capitalize()]

    return df

def display_time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Most common month
    common_month = df['month'].mode()[0]
    print(f"The most common month is: {common_month}")

    # Most common day of the week
    common_day = df['day_of_week'].mode()[0]
    print(f"The most common day of the week is: {common_day}")

    # Most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print(f"The most common start hour is: {common_hour}")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)

def display_station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print(f"The most common start station is: {popular_start_station}")

    # Most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print(f"The most common end station is: {popular_end_station}")

    # Most frequent combination of start and end stations
    frequent_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"The most frequent combination of start and end stations is: {frequent_trip}")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)

def display_trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Total travel time in hours
    total_time = df['Trip Duration'].sum() / 3600
    print(f"Total travel time in hours: {total_time:.2f}")

    # Mean travel time in hours
    mean_time = df['Trip Duration'].mean() / 3600
    print(f"Mean travel time in hours: {mean_time:.2f}")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)

def display_user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Counts of user types
    user_types_count = df['User Type'].value_counts()
    print(f"User types:\n{user_types_count}")

    # Counts of gender, if available
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print(f"Gender distribution:\n{gender_count}")

    # Earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        print(f"The earliest birth year: {earliest_birth_year}, most recent birth year: {recent_birth_year}, most common birth year: {common_birth_year}")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)

def display_raw_data(df):
    """Displays 5 rows of raw data upon user request."""
    print('Would you like to view individual trip data? Type "yes" or "no".')
    start_loc = 0
    while input().lower() != 'no':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        print('Would you like to see more data? Type "yes" or "no".')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_time_stats(df)
        display_station_stats(df)
        display_trip_duration_stats(df)
        display_user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
