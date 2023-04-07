import os
import shutil
import datetime
import re
import argparse

def archive_old_runs(current_dir, archive_dir, days_to_keep):
    # Create the archive directory if it doesn't already exist
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        print(f"Created archive directory: {archive_dir}")

    # Define the regular expression pattern to match the date
    date_pattern = r'\d{4}-\d{2}-\d{2}'

    # Get the current date
    current_date = datetime.datetime.now().date()

    # Iterate over the directories in the current directory
    for dir_name in os.listdir(current_dir):
        dir_path = os.path.join(current_dir, dir_name)

        # Check if the directory name contains a date in the format of 'YYYY-MM-DD'
        match = re.search(date_pattern, dir_name)
        if not match:
            print(f"Skipping directory {dir_name} as it does not contain a valid date")
            continue

        dir_date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()

        # Calculate the age of the directory in days
        age_in_days = (current_date - dir_date).days

        # If the directory is older than the specified number of days, move it to the archive directory
        if age_in_days > days_to_keep:
            # Create the year and month directories in the archive directory if they don't already exist
            year_dir = os.path.join(archive_dir, str(dir_date.year))
            month_dir = os.path.join(year_dir, str(dir_date.month).zfill(2))
            if not os.path.exists(year_dir):
                os.makedirs(year_dir)
                print(f"Created year directory: {year_dir}")
            if not os.path.exists(month_dir):
                os.makedirs(month_dir)
                print(f"Created month directory: {month_dir}")

            # Move the directory to the month directory in the archive directory
            archive_path = os.path.join(month_dir, dir_name)
            if os.path.exists(archive_path):
                shutil.rmtree(archive_path)
                print(f"\tRemoved existing archive directory: {archive_path}")
            shutil.move(dir_path, month_dir)
            print(f"\tMoved {dir_name} to {month_dir}")



def main():
    parser = argparse.ArgumentParser(description='Archive old runs from the current directory to the archive directory based on the age of the runs.')
    parser.add_argument('--current_dir', type=str, help='Path to the current run directory', default='/home/schuya/ttres1lepstat/run')
    parser.add_argument('--archive_dir', type=str, help='Path to the archive run directory', default='/home/schuya/ttres1lepstat/data/run')
    parser.add_argument('--days_to_keep', type=int, help='Number of days to keep runs in the current directory before archiving them', default=0)
    args = parser.parse_args()

    archive_old_runs(args.current_dir, args.archive_dir, args.days_to_keep)


if __name__ == '__main__':
    main()
