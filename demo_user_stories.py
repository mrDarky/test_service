#!/usr/bin/env python3
"""
Example demonstrating the User Stories and Test Generation feature

This script shows how to:
1. Create a project with user stories
2. Generate test summary
3. Generate test file
"""
import asyncio
import sys
from datetime import datetime, timezone

sys.path.insert(0, '/home/runner/work/test_service/test_service')

from sqlalchemy import select
from app.database import async_session, init_db
from app.models import User, Project, UserRole, ProjectStatus
from app.lavague_integration import test_generator
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_demo_user():
    """Create a demo user"""
    async with async_session() as session:
        result = await session.execute(select(User).where(User.username == "demo_creator"))
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            return existing_user
        
        user = User(
            username="demo_creator",
            email="demo@example.com",
            hashed_password=pwd_context.hash("demo123"),
            full_name="Demo Creator",
            role=UserRole.CREATOR,
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )
        
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def demo_gherkin_project():
    """Demo: Create project with Gherkin stories"""
    print("\n" + "="*70)
    print("DEMO 1: Project with Gherkin/BDD Stories")
    print("="*70)
    
    async with async_session() as session:
        user = await create_demo_user()
        
        # Gherkin stories for an e-commerce checkout
        gherkin_stories = """
Feature: E-Commerce Checkout Process

Scenario: Add item to cart
  Given the user is on the product page
  And the product is in stock
  When the user clicks "Add to Cart"
  Then the item should be added to the cart
  And the cart count should increase by 1

Scenario: Complete checkout with valid payment
  Given the user has items in their cart
  And the user is on the checkout page
  When the user enters valid shipping information
  And enters valid payment details
  And clicks "Place Order"
  Then the order should be created
  And the user should receive a confirmation email
  And the cart should be emptied

Scenario: Checkout fails with invalid payment
  Given the user has items in their cart
  And the user is on the checkout page
  When the user enters invalid payment details
  And clicks "Place Order"
  Then an error message should be displayed
  And the order should not be created
"""
        
        project = Project(
            name="E-Commerce Platform",
            description="Online shopping platform with cart and checkout",
            status=ProjectStatus.ACTIVE,
            creator_id=user.id,
            user_stories=gherkin_stories,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        session.add(project)
        await session.commit()
        await session.refresh(project)
        
        print(f"\n✓ Created project: {project.name}")
        print(f"  Project ID: {project.id}")
        
        # Generate test summary
        summary = test_generator.get_test_summary(project.user_stories)
        print(f"\n📊 Test Summary:")
        print(f"  Total tests: {summary['total_tests']}")
        print(f"  Gherkin scenarios: {summary['test_types']['gherkin']}")
        print(f"\n  Generated test names:")
        for name in summary['test_names']:
            print(f"    - {name}")
        
        # Generate test file
        test_file = test_generator.generate_test_file(project.name, project.user_stories)
        
        print(f"\n📝 Generated test file preview:")
        print("-" * 70)
        print(test_file[:600] + "...")
        print("-" * 70)
        
        return project


async def demo_user_stories_project():
    """Demo: Create project with simple user stories"""
    print("\n" + "="*70)
    print("DEMO 2: Project with Simple User Stories")
    print("="*70)
    
    async with async_session() as session:
        result = await session.execute(select(User).where(User.username == "demo_creator"))
        user = result.scalar_one()
        
        # Simple user stories for a social media app
        user_stories = """
As a user I want to create a profile So that I can share information about myself
As a user I want to post updates So that I can share my thoughts with followers
As a user I want to follow other users So that I can see their updates in my feed
As a user I want to like posts So that I can show appreciation for content
As a user I want to comment on posts So that I can engage in discussions
As a moderator I want to flag inappropriate content So that I can maintain community standards
As an admin I want to view analytics So that I can understand user engagement
"""
        
        project = Project(
            name="Social Media Platform",
            description="Social networking application with posts and interactions",
            status=ProjectStatus.ACTIVE,
            creator_id=user.id,
            user_stories=user_stories,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        session.add(project)
        await session.commit()
        await session.refresh(project)
        
        print(f"\n✓ Created project: {project.name}")
        print(f"  Project ID: {project.id}")
        
        # Generate test summary
        summary = test_generator.get_test_summary(project.user_stories)
        print(f"\n📊 Test Summary:")
        print(f"  Total tests: {summary['total_tests']}")
        print(f"  User story tests: {summary['test_types']['user_story']}")
        
        # Show first few test names
        print(f"\n  Sample test names:")
        for name in summary['test_names'][:4]:
            print(f"    - {name}")
        
        # Generate one test as example
        test_cases = test_generator.generate_test_cases(project.user_stories)
        if test_cases:
            print(f"\n📝 Example generated test:")
            print("-" * 70)
            print(test_cases[0]['code'])
            print("-" * 70)
        
        return project


async def demo_mixed_format():
    """Demo: Project with mixed format stories"""
    print("\n" + "="*70)
    print("DEMO 3: Project with Mixed Format Stories")
    print("="*70)
    
    async with async_session() as session:
        result = await session.execute(select(User).where(User.username == "demo_creator"))
        user = result.scalar_one()
        
        # Mix of Gherkin and user stories
        mixed_stories = """
Feature: Task Management

Scenario: Create a new task
  Given I am logged in as a project manager
  When I click on "New Task"
  And I fill in the task details
  Then the task should be created
  And appear in the task list

As a team member I want to see my assigned tasks So that I know what to work on
As a team member I want to update task status So that I can track my progress

Scenario: Mark task as complete
  Given I have a task assigned to me
  When I mark it as complete
  Then the task status should update
  And my manager should be notified
"""
        
        project = Project(
            name="Project Task Manager",
            description="Task management system for teams",
            status=ProjectStatus.ACTIVE,
            creator_id=user.id,
            user_stories=mixed_stories,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        session.add(project)
        await session.commit()
        await session.refresh(project)
        
        print(f"\n✓ Created project: {project.name}")
        print(f"  Project ID: {project.id}")
        
        # Generate test summary
        summary = test_generator.get_test_summary(project.user_stories)
        print(f"\n📊 Test Summary:")
        print(f"  Total tests: {summary['total_tests']}")
        print(f"  Breakdown:")
        for test_type, count in summary['test_types'].items():
            if count > 0:
                print(f"    - {test_type}: {count}")
        
        print(f"\n  All test names:")
        for name in summary['test_names']:
            print(f"    - {name}")
        
        return project


async def main():
    """Run all demos"""
    print("\n" + "="*70)
    print("USER STORIES & TEST GENERATION FEATURE DEMO")
    print("="*70)
    
    try:
        # Initialize database
        await init_db()
        
        # Run demos
        await demo_gherkin_project()
        await demo_user_stories_project()
        await demo_mixed_format()
        
        print("\n" + "="*70)
        print("✅ All demos completed successfully!")
        print("="*70)
        print("\n💡 Key Takeaways:")
        print("  1. Support for both Gherkin and simple user story formats")
        print("  2. Automatic test generation with proper structure")
        print("  3. Mix and match different story formats in one project")
        print("  4. Generated tests serve as scaffolds for implementation")
        print("  5. Easy integration via REST API endpoints")
        print("="*70 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)
