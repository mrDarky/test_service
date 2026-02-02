"""
LaVague Integration Module
Generates automated tests from user stories and Gherkin scenarios
"""
from typing import Optional, Dict, List
import re


class LaVagueTestGenerator:
    """Generate automated tests from user stories"""
    
    def __init__(self):
        self.generated_tests = []
    
    def parse_user_stories(self, user_stories: str) -> List[Dict[str, str]]:
        """
        Parse user stories from text format
        Supports both simple user stories and Gherkin format
        """
        stories = []
        
        if not user_stories:
            return stories
        
        # Check if it's Gherkin format (Feature, Scenario, Given, When, Then)
        if 'Feature:' in user_stories or 'Scenario:' in user_stories:
            stories = self._parse_gherkin(user_stories)
        else:
            # Parse as simple user stories
            stories = self._parse_simple_stories(user_stories)
        
        return stories
    
    def _parse_gherkin(self, text: str) -> List[Dict[str, str]]:
        """Parse Gherkin format stories"""
        stories = []
        
        # Split by scenarios
        scenarios = re.split(r'Scenario:', text)
        feature_match = re.search(r'Feature:\s*(.+?)(?:\n|$)', scenarios[0], re.IGNORECASE)
        feature_name = feature_match.group(1).strip() if feature_match else "Unknown Feature"
        
        for scenario in scenarios[1:]:
            lines = scenario.strip().split('\n')
            scenario_name = lines[0].strip() if lines else "Unnamed Scenario"
            
            given_steps = []
            when_steps = []
            then_steps = []
            
            current_type = None
            for line in lines[1:]:
                line = line.strip()
                if line.startswith('Given'):
                    current_type = 'given'
                    given_steps.append(line.replace('Given', '').strip())
                elif line.startswith('And') and current_type == 'given':
                    given_steps.append(line.replace('And', '').strip())
                elif line.startswith('When'):
                    current_type = 'when'
                    when_steps.append(line.replace('When', '').strip())
                elif line.startswith('And') and current_type == 'when':
                    when_steps.append(line.replace('And', '').strip())
                elif line.startswith('Then'):
                    current_type = 'then'
                    then_steps.append(line.replace('Then', '').strip())
                elif line.startswith('And') and current_type == 'then':
                    then_steps.append(line.replace('And', '').strip())
            
            stories.append({
                'type': 'gherkin',
                'feature': feature_name,
                'scenario': scenario_name,
                'given': given_steps,
                'when': when_steps,
                'then': then_steps
            })
        
        return stories
    
    def _parse_simple_stories(self, text: str) -> List[Dict[str, str]]:
        """Parse simple user story format"""
        stories = []
        
        # Split by common separators or numbered lists
        lines = text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Remove common prefixes like "- ", "* ", "1. ", etc.
            line = re.sub(r'^[\-\*\d]+[\.\)]\s*', '', line)
            
            # Look for "As a ... I want ... So that ..." pattern
            as_match = re.search(r'As (?:a|an)\s+(.+?)\s+I want\s+(.+?)(?:\s+[Ss]o that\s+(.+))?$', line, re.IGNORECASE)
            
            if as_match:
                stories.append({
                    'type': 'user_story',
                    'role': as_match.group(1).strip(),
                    'action': as_match.group(2).strip(),
                    'benefit': as_match.group(3).strip() if as_match.group(3) else ''
                })
            elif line:
                # Generic story
                stories.append({
                    'type': 'generic',
                    'description': line
                })
        
        return stories
    
    def generate_test_cases(self, user_stories: str) -> List[Dict[str, any]]:
        """
        Generate test cases from user stories
        Returns a list of test case dictionaries
        """
        stories = self.parse_user_stories(user_stories)
        test_cases = []
        
        for story in stories:
            if story['type'] == 'gherkin':
                test_cases.append(self._generate_gherkin_test(story))
            elif story['type'] == 'user_story':
                test_cases.append(self._generate_user_story_test(story))
            else:
                test_cases.append(self._generate_generic_test(story))
        
        return test_cases
    
    def _generate_gherkin_test(self, story: Dict[str, str]) -> Dict[str, any]:
        """Generate test case from Gherkin scenario"""
        test_name = f"test_{story['scenario'].lower().replace(' ', '_')}"
        
        # Generate test steps
        setup_steps = [f"# Setup: {step}" for step in story['given']]
        action_steps = [f"# Action: {step}" for step in story['when']]
        assertion_steps = [f"# Assert: {step}" for step in story['then']]
        
        return {
            'name': test_name,
            'description': f"{story['feature']} - {story['scenario']}",
            'type': 'gherkin',
            'setup': setup_steps,
            'actions': action_steps,
            'assertions': assertion_steps,
            'code': self._generate_test_code(test_name, setup_steps, action_steps, assertion_steps)
        }
    
    def _generate_user_story_test(self, story: Dict[str, str]) -> Dict[str, any]:
        """Generate test case from user story"""
        test_name = f"test_{story['action'][:50].lower().replace(' ', '_')}"
        
        description = f"As a {story['role']}, I want {story['action']}"
        if story['benefit']:
            description += f" so that {story['benefit']}"
        
        setup_steps = [f"# Setup user with role: {story['role']}"]
        action_steps = [f"# Perform action: {story['action']}"]
        assertion_steps = [f"# Verify: {story['benefit']}" if story['benefit'] else "# Verify action completed"]
        
        return {
            'name': test_name,
            'description': description,
            'type': 'user_story',
            'setup': setup_steps,
            'actions': action_steps,
            'assertions': assertion_steps,
            'code': self._generate_test_code(test_name, setup_steps, action_steps, assertion_steps)
        }
    
    def _generate_generic_test(self, story: Dict[str, str]) -> Dict[str, any]:
        """Generate test case from generic description"""
        test_name = f"test_{story['description'][:50].lower().replace(' ', '_')}"
        
        setup_steps = ["# Setup test environment"]
        action_steps = [f"# Test: {story['description']}"]
        assertion_steps = ["# Verify expected outcome"]
        
        return {
            'name': test_name,
            'description': story['description'],
            'type': 'generic',
            'setup': setup_steps,
            'actions': action_steps,
            'assertions': assertion_steps,
            'code': self._generate_test_code(test_name, setup_steps, action_steps, assertion_steps)
        }
    
    def _generate_test_code(self, test_name: str, setup: List[str], actions: List[str], assertions: List[str]) -> str:
        """Generate Python test code"""
        code = f"""
def {test_name}():
    \"\"\"
    Auto-generated test case
    \"\"\"
    # Setup
{chr(10).join('    ' + step for step in setup)}
    
    # Actions
{chr(10).join('    ' + step for step in actions)}
    
    # Assertions
{chr(10).join('    ' + step for step in assertions)}
    
    pass  # TODO: Implement test logic
"""
        return code.strip()
    
    def generate_test_file(self, project_name: str, user_stories: str) -> str:
        """
        Generate a complete test file for a project
        """
        test_cases = self.generate_test_cases(user_stories)
        
        file_content = f"""\"\"\"
Auto-generated tests for project: {project_name}
Generated from user stories using LaVague integration

These tests serve as a starting point and should be implemented
with actual test logic based on your application.
\"\"\"

import pytest


"""
        
        for test_case in test_cases:
            file_content += test_case['code'] + "\n\n"
        
        return file_content
    
    def get_test_summary(self, user_stories: str) -> Dict[str, any]:
        """Get a summary of tests that would be generated"""
        test_cases = self.generate_test_cases(user_stories)
        
        return {
            'total_tests': len(test_cases),
            'test_types': {
                'gherkin': len([t for t in test_cases if t['type'] == 'gherkin']),
                'user_story': len([t for t in test_cases if t['type'] == 'user_story']),
                'generic': len([t for t in test_cases if t['type'] == 'generic'])
            },
            'test_names': [t['name'] for t in test_cases]
        }


# Singleton instance
test_generator = LaVagueTestGenerator()
