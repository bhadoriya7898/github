import argparse
import os
import random
from datetime import datetime, timedelta

def run(args):
    # 1. Initialize Request
    if args.repository:
        # If a remote repository is provided, we clone it or init and add remote
        # For simplicity in this script, we assume we are running in a fresh folder
        # and will add the remote at the end.
        pass

    start_date = datetime.now() - timedelta(days=args.days_before)
    
    # Initialize git if not already done
    if not os.path.exists('.git'):
        os.system('git init')

    # Create a dummy file to modify
    with open('activity.txt', 'w') as f:
        f.write('Activity Generator initialized.\n')

    print(f"Generating commits from {start_date.date()}...")

    curr_date = start_date
    total_days = args.days_before + args.days_after

    for day in range(total_days + 1):
        # Calculate current processing date
        curr_date = start_date + timedelta(days=day)
        
        # Skip weekends if requested
        if args.no_weekends and curr_date.weekday() >= 5:
            continue

        # Frequency check (percentage of days to commit)
        if random.randint(0, 100) > args.frequency:
            continue

        # random number of commits for this day
        commits_today = random.randint(1, args.max_commits)
        
        for i in range(commits_today):
            # Update the file
            with open('activity.txt', 'a') as f:
                f.write(f'Commit {i} on {curr_date}\n')
            
            # Stage the file
            os.system('git add activity.txt')
            
            # Commit with a specific date
            # We add random hours/seconds to make it look organic
            date_str = curr_date.replace(hour=random.randint(9, 23), minute=random.randint(0, 59)).isoformat()
            os.system(f'git commit --date="{date_str}" -m "update activity" > /dev/null 2>&1')

    print("Commits generated successfully.")

    # Push to remote if provided
    if args.repository:
        print(f"Pushing to {args.repository}...")
        os.system('git branch -M main')
        os.system(f'git remote add origin {args.repository}')
        os.system('git push -u origin main --force')
        print("Done! Check your GitHub profile.")
    else:
        print("No repository URL provided. Commits are local only.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate fake GitHub activity.")
    
    parser.add_argument('--repository', type=str, help="The link to the remote repository (e.g., git@github.com:user/repo.git)")
    parser.add_argument('--max_commits', type=int, default=10, help="Max commits per day (default: 10)")
    parser.add_argument('--frequency', type=int, default=80, help="Percentage of days to commit (0-100, default: 80)")
    parser.add_argument('--no_weekends', action='store_true', help="Do not commit on weekends")
    parser.add_argument('--days_before', type=int, default=365, help="How many days back to start (default: 365)")
    parser.add_argument('--days_after', type=int, default=0, help="How many days into the future to continue")

    args = parser.parse_args()
    run(args)