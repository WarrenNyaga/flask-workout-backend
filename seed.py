#!/usr/bin/env python3
from app import app
from models import db, User, Task

with app.app_context():
    print("Clearing existing data...")
    Task.query.delete()
    User.query.delete()

    print("Seeding users...")
    user1 = User(username="alice")
    user1.set_password("password123")

    user2 = User(username="bob")
    user2.set_password("password123")

    db.session.add_all([user1, user2])
    db.session.commit()

    print("Seeding tasks...")
    tasks = [
        Task(title="Complete Flask Lab", description="Build JWT auth and backend API", user_id=user1.id),
        Task(title="Write Documentation", description="Create README with route details", user_id=user1.id),
        Task(title="Review Code", description="Check constraints and edge cases", user_id=user1.id),
        Task(title="Submit Assignment", description="Push code to GitHub repository", user_id=user1.id),
        Task(title="Buy Groceries", description="Milk, Eggs, Bread", user_id=user2.id)
    ]

    db.session.add_all(tasks)
    db.session.commit()

    print("Seeding completed successfully!")