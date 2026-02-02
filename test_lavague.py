#!/usr/bin/env python3
"""
Test script for LaVague integration
Tests the user story parsing and test generation functionality
"""

from app.lavague_integration import test_generator


def test_gherkin_parsing():
    """Test Gherkin format parsing"""
    print("=" * 60)
    print("Testing Gherkin Format Parsing")
    print("=" * 60)
    
    gherkin_story = """
Feature: User Authentication

Scenario: User login with valid credentials
  Given the user is on the login page
  And the user has a valid account
  When the user enters valid credentials
  And clicks the login button
  Then the user should be logged in
  And redirected to the dashboard
"""
    
    test_cases = test_generator.generate_test_cases(gherkin_story)
    print(f"\nGenerated {len(test_cases)} test case(s)\n")
    
    for tc in test_cases:
        print(f"Test Name: {tc['name']}")
        print(f"Description: {tc['description']}")
        print(f"Type: {tc['type']}")
        print(f"\nGenerated Code:\n{tc['code']}")
        print("\n" + "-" * 60 + "\n")
    
    return len(test_cases) > 0


def test_user_story_parsing():
    """Test simple user story parsing"""
    print("=" * 60)
    print("Testing User Story Format Parsing")
    print("=" * 60)
    
    user_stories = """
As a project creator I want to create new projects So that I can organize testing work
As a tester I want to view available projects So that I can join them and start testing
As an admin I want to manage users So that I can maintain the system
"""
    
    test_cases = test_generator.generate_test_cases(user_stories)
    print(f"\nGenerated {len(test_cases)} test case(s)\n")
    
    for tc in test_cases:
        print(f"Test Name: {tc['name']}")
        print(f"Description: {tc['description']}")
        print(f"Type: {tc['type']}")
        print(f"\nGenerated Code:\n{tc['code']}")
        print("\n" + "-" * 60 + "\n")
    
    return len(test_cases) > 0


def test_mixed_stories():
    """Test mixed format stories"""
    print("=" * 60)
    print("Testing Mixed Format Stories")
    print("=" * 60)
    
    mixed_stories = """
Feature: Project Management

Scenario: Create a new project
  Given I am logged in as a creator
  When I click on create project
  And fill in the project details
  Then a new project should be created

As a tester I want to join projects So that I can contribute to testing
"""
    
    test_cases = test_generator.generate_test_cases(mixed_stories)
    print(f"\nGenerated {len(test_cases)} test case(s)\n")
    
    summary = test_generator.get_test_summary(mixed_stories)
    print(f"Summary: {summary}")
    print("\n" + "-" * 60 + "\n")
    
    return len(test_cases) > 0


def test_full_test_file_generation():
    """Test complete test file generation"""
    print("=" * 60)
    print("Testing Full Test File Generation")
    print("=" * 60)
    
    user_stories = """
Feature: Task Management

Scenario: Assign task to tester
  Given a project with tasks exists
  And a tester is a member of the project
  When the creator assigns a task to the tester
  Then the tester should see the task in their assignments

As a tester I want to update task status So that I can track my progress
"""
    
    test_file = test_generator.generate_test_file("Task Management System", user_stories)
    print(f"\nGenerated test file:\n")
    print(test_file)
    print("\n" + "-" * 60 + "\n")
    
    return len(test_file) > 0


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("LaVague Integration Test Suite")
    print("=" * 60 + "\n")
    
    results = []
    
    try:
        results.append(("Gherkin Parsing", test_gherkin_parsing()))
    except Exception as e:
        print(f"Error in Gherkin test: {e}")
        results.append(("Gherkin Parsing", False))
    
    try:
        results.append(("User Story Parsing", test_user_story_parsing()))
    except Exception as e:
        print(f"Error in User Story test: {e}")
        results.append(("User Story Parsing", False))
    
    try:
        results.append(("Mixed Format", test_mixed_stories()))
    except Exception as e:
        print(f"Error in Mixed Format test: {e}")
        results.append(("Mixed Format", False))
    
    try:
        results.append(("Full File Generation", test_full_test_file_generation()))
    except Exception as e:
        print(f"Error in Full File Generation test: {e}")
        results.append(("Full File Generation", False))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    print("\n" + "=" * 60)
    if all_passed:
        print("All tests PASSED! ✓")
    else:
        print("Some tests FAILED! ✗")
    print("=" * 60 + "\n")
    
    return all_passed


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
