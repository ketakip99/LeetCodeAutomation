import time
from apscheduler.schedulers.blocking import BlockingScheduler
from fetcher import fetch_daily_problems
from generator import generate_solution
from notifier import send_email, create_email_body
from storage import record_problem, init_db
from config import PROBLEM_COUNT, DEFAULT_DIFFICULTIES

def daily_job():
    print(f"Starting daily job at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 1. Fetch problems
        print("Fetching problems...")
        problems = fetch_daily_problems(count=PROBLEM_COUNT, difficulty=random_difficulty())
        
        if not problems:
            print("No new problems found.")
            return

        # 2. Generate solutions
        print(f"Generating solutions for {len(problems)} problems...")
        for p in problems:
            p['solution'] = generate_solution(p['title'], p['content'], p['difficulty'], p['questionFrontendId'])
            
        # 3. Create email body
        body = create_email_body(problems)
        
        # 4. Send email
        subject = f"Daily LeetCode Practice – {len(problems)} Problems with Python Solutions"
        success = send_email(subject, body)
        
        if success:
            # 5. Record in history
            for p in problems:
                record_problem(p['titleSlug'], p['title'], p['difficulty'])
            print("Job completed successfully.")
        else:
            print("Job failed during email delivery.")
            
    except Exception as e:
        print(f"An error occurred during the daily job: {e}")

def random_difficulty():
    import random
    return random.choice(DEFAULT_DIFFICULTIES)

def main():
    # Initialize DB
    init_db()
    
    # Run once immediately for first-time or manual trigger
    print("Running initial job...")
    daily_job()
    
    # Setup Scheduler (e.g., Run at 8:00 AM every day)
    scheduler = BlockingScheduler()
    scheduler.add_job(daily_job, 'cron', hour=8, minute=0)
    
    print("Scheduler started. Waiting for next run at 08:00 AM daily.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    main()
