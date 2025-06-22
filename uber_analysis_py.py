import pandas as pd

def main():
    # Path to your CSV file
    csv_path = r"C:\Users\gupta\Downloads\uber_data_for_SQL_analysis.csv"

    # Load CSV with date parsing
    df = pd.read_csv(csv_path, parse_dates=['request_timestamp', 'drop_timestamp'])

    # Extract request hour for time-based queries
    df['request_hour'] = df['request_timestamp'].dt.hour

    # Create Excel writer for output file
    writer = pd.ExcelWriter('uber_analysis_results.xlsx', engine='xlsxwriter')

    # Query 1: Total ride requests grouped by status
    q1 = df.groupby('status').size().reset_index(name='total_requests')
    q1.to_excel(writer, sheet_name='Requests_By_Status', index=False)

    # Query 2: Requests count by pickup point
    q2 = df.groupby('pickup_point').size().reset_index(name='total_requests')
    q2.to_excel(writer, sheet_name='Requests_By_Pickup', index=False)

    # Query 3: Requests per hour
    q3 = df.groupby('request_hour').size().reset_index(name='total_requests').sort_values('request_hour')
    q3.to_excel(writer, sheet_name='Requests_Per_Hour', index=False)

    # Query 4: Cancellation rate per hour
    q4 = df.groupby('request_hour').agg(
        total_requests=('status', 'size'),
        cancellations=('status', lambda x: (x == 'Cancelled').sum())
    ).reset_index()
    q4['cancellation_percent'] = (q4['cancellations'] / q4['total_requests'] * 100).round(2)
    q4.to_excel(writer, sheet_name='Cancellation_Rate_Hour', index=False)

    # Query 5: No Cars Available rate per hour
    q5 = df.groupby('request_hour').agg(
        total_requests=('status', 'size'),
        no_cars=('status', lambda x: (x == 'No Cars Available').sum())
    ).reset_index()
    q5['unavailability_percent'] = (q5['no_cars'] / q5['total_requests'] * 100).round(2)
    q5.to_excel(writer, sheet_name='NoCars_Rate_Hour', index=False)

    # Query 6: Time slot-wise distribution of request statuses
    def assign_time_slot(hour):
        if hour < 4:
            return 'Night'
        elif hour < 8:
            return 'Early Morning'
        elif hour < 12:
            return 'Morning'
        elif hour < 16:
            return 'Afternoon'
        elif hour < 20:
            return 'Evening'
        else:
            return 'Late Night'

    df['time_slot'] = df['request_hour'].apply(assign_time_slot)

    q6 = df.groupby('time_slot').agg(
        total_requests=('status', 'size'),
        cancelled=('status', lambda x: (x == 'Cancelled').sum()),
        no_cars=('status', lambda x: (x == 'No Cars Available').sum()),
        completed=('status', lambda x: (x == 'Trip Completed').sum())
    ).reset_index()

    q6['cancel_rate'] = (q6['cancelled'] / q6['total_requests'] * 100).round(2)
    q6['no_car_rate'] = (q6['no_cars'] / q6['total_requests'] * 100).round(2)

    # Order time slots for better readability
    order = ['Early Morning', 'Morning', 'Afternoon', 'Evening', 'Late Night', 'Night']
    q6['time_slot'] = pd.Categorical(q6['time_slot'], categories=order, ordered=True)
    q6 = q6.sort_values('time_slot')

    q6.to_excel(writer, sheet_name='Time_Slot_Distribution', index=False)

    # Query 7: Overall fulfillment rate
    total = len(df)
    completed = (df['status'] == 'Trip Completed').sum()
    fulfillment_rate = round(completed / total * 100, 2)
    q7 = pd.DataFrame({'fulfillment_rate_percent': [fulfillment_rate]})
    q7.to_excel(writer, sheet_name='Fulfillment_Rate', index=False)

    # Query 8: Cancellation % by pickup point
    q8 = df.groupby('pickup_point').agg(
        total_requests=('status', 'size'),
        cancelled=('status', lambda x: (x == 'Cancelled').sum())
    ).reset_index()
    q8['cancellation_rate'] = (q8['cancelled'] / q8['total_requests'] * 100).round(2)
    q8.to_excel(writer, sheet_name='Cancellation_By_Pickup', index=False)

    # Query 9: No Cars Available % by pickup point
    q9 = df.groupby('pickup_point').agg(
        total_requests=('status', 'size'),
        no_cars=('status', lambda x: (x == 'No Cars Available').sum())
    ).reset_index()
    q9['no_car_rate'] = (q9['no_cars'] / q9['total_requests'] * 100).round(2)
    q9.to_excel(writer, sheet_name='NoCars_By_Pickup', index=False)

    # Query 10: Average request volume per hour
    q10 = df.groupby('request_hour').size().reset_index(name='total_requests')
    avg_req = round(q10['total_requests'].mean(), 2)
    q10['avg_requests_per_hour'] = avg_req
    q10 = q10.sort_values('request_hour')
    q10.to_excel(writer, sheet_name='Avg_Requests_Per_Hour', index=False)

    # Save Excel file
    writer.close()

    print("Analysis complete! File saved as 'uber_analysis_results.xlsx'")

if __name__ == "__main__":
    main()
