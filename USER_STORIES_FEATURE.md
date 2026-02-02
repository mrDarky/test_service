# User Stories and Test Generation Feature

## Overview
This feature allows you to add user stories or Gherkin scenarios when creating projects and automatically generate test cases from them using LaVague integration.

## Features

### 1. User Stories Support
Projects now support two types of user stories:

#### Gherkin Format (BDD)
```gherkin
Feature: User Authentication

Scenario: Successful login
  Given the user is on the login page
  When the user enters valid credentials
  And clicks the login button
  Then the user should be redirected to dashboard
```

#### Simple User Story Format
```
As a project creator I want to create projects So that I can organize testing work
As a tester I want to view projects So that I can join them
As an admin I want to manage users So that I can maintain the system
```

### 2. Automated Test Generation
The LaVague integration automatically generates test cases from user stories:

- Parses both Gherkin and simple user story formats
- Generates Python test functions with proper structure
- Creates setup, action, and assertion steps
- Provides test summaries and statistics

## API Endpoints

### Get Test Summary
```
GET /api/projects/{project_id}/test-summary
```
Returns a summary of tests that can be generated from the project's user stories.

**Response Example:**
```json
{
  "total_tests": 3,
  "test_types": {
    "gherkin": 2,
    "user_story": 1,
    "generic": 0
  },
  "test_names": ["test_successful_login", "test_failed_login", "test_to_create_projects"]
}
```

### Generate Tests
```
GET /api/projects/{project_id}/generate-tests
```
Generates a complete test file from the project's user stories.

**Response Example:**
```json
{
  "project_name": "Authentication System",
  "test_file_content": "...",
  "filename": "test_authentication_system.py"
}
```

## Usage

### Creating a Project with User Stories

#### Using the API
```python
import requests

# Create project with Gherkin stories
project_data = {
    "name": "My Project",
    "description": "Project description",
    "user_stories": """
Feature: User Login

Scenario: Successful login
  Given the user is registered
  When they enter valid credentials
  Then they should be logged in
"""
}

response = requests.post(
    "http://localhost:8000/api/projects/",
    json=project_data,
    headers={"Authorization": f"Bearer {token}"}
)
```

### Generating Tests

```python
# Get test summary
response = requests.get(
    f"http://localhost:8000/api/projects/{project_id}/test-summary",
    headers={"Authorization": f"Bearer {token}"}
)
summary = response.json()

# Generate test file
response = requests.get(
    f"http://localhost:8000/api/projects/{project_id}/generate-tests",
    headers={"Authorization": f"Bearer {token}"}
)
test_file = response.json()

# Save to file
with open(test_file["filename"], "w") as f:
    f.write(test_file["test_file_content"])
```

## Database Changes

### Project Model
The `projects` table now includes a `user_stories` field:
- **Type**: TEXT
- **Nullable**: Yes
- **Purpose**: Store user stories or Gherkin scenarios

## Implementation Details

### LaVague Integration Module
Location: `app/lavague_integration.py`

Key classes:
- `LaVagueTestGenerator`: Main class for parsing and generating tests

Key methods:
- `parse_user_stories()`: Parse user stories from text
- `generate_test_cases()`: Generate test case structures
- `generate_test_file()`: Generate complete test file
- `get_test_summary()`: Get test generation summary

### Test Format Examples

#### Generated Gherkin Test
```python
def test_successful_login():
    """
    Auto-generated test case
    """
    # Setup
    # Setup: the user is registered
    
    # Actions
    # Action: they enter valid credentials
    
    # Assertions
    # Assert: they should be logged in
    
    pass  # TODO: Implement test logic
```

#### Generated User Story Test
```python
def test_to_create_projects():
    """
    Auto-generated test case
    """
    # Setup
    # Setup user with role: project creator
    
    # Actions
    # Perform action: to create projects
    
    # Assertions
    # Verify: I can organize testing work
    
    pass  # TODO: Implement test logic
```

## Benefits

1. **Documentation**: User stories serve as living documentation
2. **Test Coverage**: Automatically generate test scaffolding
3. **BDD Support**: Full support for Gherkin/BDD format
4. **Flexibility**: Support for multiple story formats
5. **Time Saving**: Reduce time spent writing boilerplate test code

## Best Practices

1. **Write Clear Stories**: Use clear, concise language in user stories
2. **Follow Gherkin Format**: For BDD, follow Given-When-Then format
3. **One Story Per Line**: For simple stories, use one story per line
4. **Implement Tests**: Generated tests are scaffolds - implement the actual logic
5. **Review Generated Tests**: Always review generated tests before use

## Future Enhancements

Potential improvements for this feature:
- Integration with actual LaVague browser automation
- Support for more test formats (pytest, unittest)
- Automatic test execution
- Test coverage reporting
- Integration with CI/CD pipelines
- Support for data tables in Gherkin
- Background and scenario outline support

## Testing

Run the test suite to verify the feature:

```bash
# Test LaVague integration
python test_lavague.py

# Test API integration
python test_api_integration.py
```

## Dependencies

New dependency added:
- `lavague==1.1.17`: LaVague library for test generation

Install with:
```bash
pip install -r requirements.txt
```
