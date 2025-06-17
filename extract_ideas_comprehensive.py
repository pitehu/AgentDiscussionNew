#!/usr/bin/env python3
# extract_ideas_comprehensive.py - Comprehensive idea extraction from chat logs
import os
import re
import glob
import pandas as pd
import argparse
import json
from typing import Dict, List, Tuple, Any, Optional

def parse_config_from_content(content: str) -> Dict[str, Any]:
    """Extract task configuration from file content."""
    config = {}
    
    # Extract configuration section
    config_match = re.search(r'=== Task Configuration ===\s*\{(.*?)\}', content, re.DOTALL)
    if config_match:
        try:
            config_str = "{" + config_match.group(1) + "}"
            config = json.loads(config_str)
        except json.JSONDecodeError:
            print(f"Warning: Could not parse configuration JSON")
    
    return config

def parse_token_usage(content: str) -> Dict[str, Any]:
    """Extract token usage information from file content."""
    token_data = {}
    
    # Extract overall token usage
    overall_match = re.search(r'Overall:\s*Total Prompt Tokens Used: (\d+)\s*Total Completion Tokens Used: (\d+)\s*Total Reasoning Tokens Used: (\d+)\s*Grand Total Tokens Used: (\d+)', content)
    if overall_match:
        token_data.update({
            'total_prompt_tokens': int(overall_match.group(1)),
            'total_completion_tokens': int(overall_match.group(2)),
            'total_reasoning_tokens': int(overall_match.group(3)),
            'grand_total_tokens': int(overall_match.group(4))
        })
    
    # Extract phase-wise token usage
    phases = ['Idea_generation', 'Selection', 'Discussion', 'Other']
    for phase in phases:
        phase_pattern = rf'{phase} Phase:\s*Prompt Tokens Used: (\d+)\s*Completion Tokens Used: (\d+)\s*Reasoning Tokens Used: (\d+)\s*Total Tokens Used: (\d+)'
        phase_match = re.search(phase_pattern, content)
        if phase_match:
            token_data.update({
                f'{phase.lower()}_prompt_tokens': int(phase_match.group(1)),
                f'{phase.lower()}_completion_tokens': int(phase_match.group(2)),
                f'{phase.lower()}_reasoning_tokens': int(phase_match.group(3)),
                f'{phase.lower()}_total_tokens': int(phase_match.group(4))
            })
    
    # Extract total rounds
    rounds_match = re.search(r'=== Total Rounds Executed: (\d+) ===', content)
    if rounds_match:
        token_data['total_rounds'] = int(rounds_match.group(1))
    
    return token_data

def extract_ideas_from_evolution_history(content: str, file_id: str, config: Dict) -> Tuple[List[Dict], Optional[Dict]]:
    """Extract ideas from the Idea Evolution History section."""
    all_ideas = []
    final_idea = None
    
    discussion_method = config.get("discussion_method", "all_at_once")
    
    if discussion_method == "all_at_once":
        # Pattern for all_at_once method
        rounds_pattern = r'-- Round (\d+) --\nAgent: (.*?)\nCurrent Ideas:\n(.*?)Response:'
        rounds = re.findall(rounds_pattern, content, re.DOTALL)
        
        final_round_num = -1
        for round_num, agent, ideas_text in rounds:
            round_num = int(round_num)
            
            # Extract numbered ideas
            ideas = re.findall(r'(\d+)\. (.*?)(?=\n\d+\.|$)', ideas_text, re.DOTALL)
            
            for idea_num, idea_text in ideas:
                idea = {
                    'file': file_id,
                    'round': round_num,
                    'agent': agent.strip(),
                    'idea_num': int(idea_num),
                    'idea': idea_text.strip(),
                    'idea_type': 'intermediate' if round_num < max([int(r[0]) for r in rounds]) else 'final'
                }
                all_ideas.append(idea)
                
                if round_num > final_round_num:
                    final_round_num = round_num
                    final_idea = idea
    
    elif discussion_method == "iterative_refinement":
        # Pattern for iterative_refinement method - different format
        # Look for "-- Idea #N/A --" pattern first
        idea_pattern = r'-- Idea #.*?--\nAgent: (.*?)\nCurrent Idea:\n(.*?)Response:'
        idea_matches = re.findall(idea_pattern, content, re.DOTALL)
        
        if idea_matches:
            # This is the iterative refinement format with "Idea #N/A"
            for i, (agent, ideas_text) in enumerate(idea_matches):
                # Extract numbered ideas
                ideas = re.findall(r'(\d+)\. (.*?)(?=\n\d+\.|$)', ideas_text, re.DOTALL)
                
                for idea_num, idea_text in ideas:
                    idea = {
                        'file': file_id,
                        'round': i + 1,
                        'agent': agent.strip(),
                        'idea_num': int(idea_num),
                        'idea': idea_text.strip(),
                        'idea_type': 'intermediate' if i < len(idea_matches) - 1 else 'final'
                    }
                    all_ideas.append(idea)
                    final_idea = idea  # Keep updating to get the final one
        else:
            # Try the round-based pattern for iterative refinement
            rounds_pattern = r'-- Round (\d+) --\nAgent: (.*?)\nCurrent Ideas:\n(.*?)Response:'
            rounds = re.findall(rounds_pattern, content, re.DOTALL)
            
            for round_num, agent, ideas_text in rounds:
                round_num = int(round_num)
                
                # Extract numbered ideas
                ideas = re.findall(r'(\d+)\. (.*?)(?=\n\d+\.|$)', ideas_text, re.DOTALL)
                
                for idea_num, idea_text in ideas:
                    idea = {
                        'file': file_id,
                        'round': round_num,
                        'agent': agent.strip(),
                        'idea_num': int(idea_num),
                        'idea': idea_text.strip(),
                        'idea_type': 'intermediate' if round_num < max([int(r[0]) for r in rounds]) else 'final'
                    }
                    all_ideas.append(idea)
                    final_idea = idea  # Keep updating to get the final one
    
    elif discussion_method in ["open", "creative"]:
        # For open/creative discussions, look for the final idea pattern
        # First try "-- Idea #N/A --" pattern
        idea_pattern = r'-- Idea #.*?--\nAgent: (.*?)\nCurrent Idea:\n(.*?)Response:'
        idea_matches = re.findall(idea_pattern, content, re.DOTALL)
        
        if idea_matches:
            # Get the last idea match for final idea
            agent, ideas_text = idea_matches[-1]
            
            # Extract numbered ideas from the last match
            ideas = re.findall(r'(\d+)\. (.*?)(?=\n\d+\.|$)', ideas_text, re.DOTALL)
            
            for idea_num, idea_text in ideas:
                idea = {
                    'file': file_id,
                    'round': len(idea_matches),
                    'agent': agent.strip(),
                    'idea_num': int(idea_num),
                    'idea': idea_text.strip(),
                    'idea_type': 'final'
                }
                all_ideas.append(idea)
                final_idea = idea
        else:
            # Try round-based pattern
            rounds_pattern = r'-- Round (\d+) --\nAgent: (.*?)\nCurrent Ideas:\n(.*?)Response:'
            rounds = re.findall(rounds_pattern, content, re.DOTALL)
            
            if rounds:
                # Get the last round only for final idea
                last_round = max(rounds, key=lambda x: int(x[0]))
                round_num, agent, ideas_text = last_round
                round_num = int(round_num)
                
                # Extract numbered ideas from the last round
                ideas = re.findall(r'(\d+)\. (.*?)(?=\n\d+\.|$)', ideas_text, re.DOTALL)
                
                for idea_num, idea_text in ideas:
                    idea = {
                        'file': file_id,
                        'round': round_num,
                        'agent': agent.strip(),
                        'idea_num': int(idea_num),
                        'idea': idea_text.strip(),
                        'idea_type': 'final'
                    }
                    all_ideas.append(idea)
                    final_idea = idea
    
    return all_ideas, final_idea

def extract_agent_responses(content: str, file_id: str) -> List[Dict]:
    """Extract individual agent responses from chat history."""
    responses = []
    
    # Pattern to match agent responses
    agent_pattern = r'Agent (\d+)\((.*?), (.*?), Idea Index: (.*?), Round: (.*?)\)\s*-+\s*Prompt:(.*?)Response:\s*(.*?)(?=\*{100,}|\Z)'
    matches = re.findall(agent_pattern, content, re.DOTALL)
    
    for match in matches:
        agent_num, model, phase, idea_index, round_num, prompt, response = match
        
        response_data = {
            'file': file_id,
            'agent_num': agent_num.strip(),
            'model': model.strip(),
            'phase': phase.strip(),
            'idea_index': idea_index.strip() if idea_index.strip() != 'N/A' else None,
            'round': round_num.strip() if round_num.strip() != 'N/A' else None,
            'prompt_length': len(prompt.strip()),
            'response_length': len(response.strip()),
            'response': response.strip()
        }
        responses.append(response_data)
    
    return responses

def extract_comprehensive_data(file_path: str) -> Dict[str, Any]:
    """Extract all comprehensive data from a single file."""
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    file_id = os.path.basename(file_path).replace('.txt', '')
    
    # Parse configuration
    config = parse_config_from_content(content)
    
    # Parse token usage
    token_data = parse_token_usage(content)
    
    # Extract ideas from evolution history
    ideas, final_idea = extract_ideas_from_evolution_history(content, file_id, config)
    
    # Extract agent responses
    responses = extract_agent_responses(content, file_id)
    
    return {
        'file_id': file_id,
        'config': config,
        'token_data': token_data,
        'ideas': ideas,
        'final_idea': final_idea,
        'responses': responses
    }

def create_comprehensive_dataframe(all_data: List[Dict]) -> pd.DataFrame:
    """Create a comprehensive dataframe with all extracted information."""
    rows = []
    
    for data in all_data:
        file_id = data['file_id']
        config = data['config']
        token_data = data['token_data']
        ideas = data['ideas']
        final_idea = data['final_idea']
        
        # Create base row with config and token data
        base_row = {
            'file_id': file_id,
            # Configuration fields
            'task_type': config.get('task_type'),
            'phases': config.get('phases'),
            'generation_method': config.get('generation_method'),
            'selection_method': config.get('selection_method'),
            'discussion_method': config.get('discussion_method'),
            'discussion_order_method': config.get('discussion_order_method'),
            'persona_type': config.get('persona_type'),
            'llm_count': config.get('llm_count'),
            'models': ', '.join(config.get('model', [])) if isinstance(config.get('model'), list) else config.get('model'),
            'temperature': config.get('temperature'),
            'replacement_pool_size': config.get('replacement_pool_size'),
            'role_assignment': '|'.join(config.get('role_assignment_in_user_prompt', [])) if config.get('role_assignment_in_user_prompt') else None,
            'max_responses': config.get('max_responses'),
            'min_responses': config.get('min_responses'),
            'reasoning_efforts': '|'.join([str(x) if x is not None else 'None' for x in config.get('reasoning_efforts', [])]) if config.get('reasoning_efforts') else None,
            
            # Token usage fields
            'total_prompt_tokens': token_data.get('total_prompt_tokens'),
            'total_completion_tokens': token_data.get('total_completion_tokens'),
            'total_reasoning_tokens': token_data.get('total_reasoning_tokens'),
            'grand_total_tokens': token_data.get('grand_total_tokens'),
            'total_rounds': token_data.get('total_rounds'),
            
            # Phase-wise token usage
            'idea_generation_prompt_tokens': token_data.get('idea_generation_prompt_tokens'),
            'idea_generation_completion_tokens': token_data.get('idea_generation_completion_tokens'),
            'idea_generation_reasoning_tokens': token_data.get('idea_generation_reasoning_tokens'),
            'idea_generation_total_tokens': token_data.get('idea_generation_total_tokens'),
            
            'selection_prompt_tokens': token_data.get('selection_prompt_tokens'),
            'selection_completion_tokens': token_data.get('selection_completion_tokens'),
            'selection_reasoning_tokens': token_data.get('selection_reasoning_tokens'),
            'selection_total_tokens': token_data.get('selection_total_tokens'),
            
            'discussion_prompt_tokens': token_data.get('discussion_prompt_tokens'),
            'discussion_completion_tokens': token_data.get('discussion_completion_tokens'),
            'discussion_reasoning_tokens': token_data.get('discussion_reasoning_tokens'),
            'discussion_total_tokens': token_data.get('discussion_total_tokens'),
            
            'other_prompt_tokens': token_data.get('other_prompt_tokens'),
            'other_completion_tokens': token_data.get('other_completion_tokens'),
            'other_reasoning_tokens': token_data.get('other_reasoning_tokens'),
            'other_total_tokens': token_data.get('other_total_tokens'),
        }
        
        # Add final idea
        if final_idea:
            base_row.update({
                'final_idea': final_idea['idea'],
                'final_idea_round': final_idea['round'],
                'final_idea_agent': final_idea['agent'],
                'final_idea_num': final_idea['idea_num']
            })
        
        # Add intermediate ideas as a single list column
        intermediate_ideas = [idea for idea in ideas if idea.get('idea_type') == 'intermediate']
        base_row['intermediate_ideas'] = json.dumps([idea['idea'] for idea in intermediate_ideas]) if intermediate_ideas else "[]"
        
        # Count statistics
        base_row['total_ideas_count'] = len(ideas)
        base_row['intermediate_ideas_count'] = len(intermediate_ideas)
        
        rows.append(base_row)
    
    return pd.DataFrame(rows)

def create_detailed_ideas_dataframe(all_data: List[Dict]) -> pd.DataFrame:
    """Create a detailed dataframe with one row per idea."""
    rows = []
    
    for data in all_data:
        file_id = data['file_id']
        config = data['config']
        token_data = data['token_data']
        ideas = data['ideas']
        
        for idea in ideas:
            row = {
                'file_id': file_id,
                'round': idea['round'],
                'agent': idea['agent'],
                'idea_num': idea['idea_num'],
                'idea_type': idea['idea_type'],
                'idea': idea['idea'],
                'idea_length': len(idea['idea']),
                
                # Add key config info
                'discussion_method': config.get('discussion_method'),
                'models': ', '.join(config.get('model', [])) if isinstance(config.get('model'), list) else config.get('model'),
                'llm_count': config.get('llm_count'),
                'temperature': config.get('temperature'),
                
                # Add key token info
                'grand_total_tokens': token_data.get('grand_total_tokens'),
                'total_rounds': token_data.get('total_rounds')
            }
            rows.append(row)
    
    return pd.DataFrame(rows)

def create_responses_dataframe(all_data: List[Dict]) -> pd.DataFrame:
    """Create a dataframe with agent responses."""
    rows = []
    
    for data in all_data:
        for response in data['responses']:
            rows.append(response)
    
    return pd.DataFrame(rows)

def process_directory(directory: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Process all files in directory and return comprehensive dataframes."""
    all_data = []
    
    # Find all txt files
    file_paths = glob.glob(os.path.join(directory, '*.txt'))
    
    print(f"Found {len(file_paths)} files to process...")
    
    for file_path in file_paths:
        try:
            data = extract_comprehensive_data(file_path)
            all_data.append(data)
            print(f"✓ Processed: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"✗ Error processing {file_path}: {e}")
    
    # Create dataframes
    comprehensive_df = create_comprehensive_dataframe(all_data)
    detailed_ideas_df = create_detailed_ideas_dataframe(all_data)
    responses_df = create_responses_dataframe(all_data)
    
    return comprehensive_df, detailed_ideas_df, responses_df

def main():
    parser = argparse.ArgumentParser(description='Comprehensive idea extraction from chat logs')
    parser.add_argument('directory', help='Directory containing chat log files')
    parser.add_argument('--output-prefix', default='extracted_data', help='Prefix for output files')
    parser.add_argument('--format', choices=['csv', 'excel'], default='csv', help='Output format')
    
    args = parser.parse_args()
    
    print("Starting comprehensive idea extraction...")
    
    # Process all files
    comprehensive_df, detailed_ideas_df, responses_df = process_directory(args.directory)
    
    # Save results
    if args.format == 'csv':
        comprehensive_file = f"{args.output_prefix}_comprehensive.csv"
        detailed_ideas_file = f"{args.output_prefix}_detailed_ideas.csv"
        responses_file = f"{args.output_prefix}_responses.csv"
        
        comprehensive_df.to_csv(comprehensive_file, index=False)
        detailed_ideas_df.to_csv(detailed_ideas_file, index=False)
        responses_df.to_csv(responses_file, index=False)
        
        print(f"\n✓ Comprehensive data saved to: {comprehensive_file}")
        print(f"✓ Detailed ideas saved to: {detailed_ideas_file}")
        print(f"✓ Agent responses saved to: {responses_file}")
        
    else:  # excel
        excel_file = f"{args.output_prefix}_complete.xlsx"
        
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            comprehensive_df.to_excel(writer, sheet_name='Comprehensive', index=False)
            detailed_ideas_df.to_excel(writer, sheet_name='Detailed_Ideas', index=False)
            responses_df.to_excel(writer, sheet_name='Agent_Responses', index=False)
        
        print(f"\n✓ All data saved to Excel file: {excel_file}")
    
    print(f"\nSummary:")
    print(f"- Processed {len(comprehensive_df)} files")
    print(f"- Extracted {len(detailed_ideas_df)} total ideas")
    print(f"- Captured {len(responses_df)} agent responses")
    print(f"- Average ideas per file: {len(detailed_ideas_df) / len(comprehensive_df):.1f}")

if __name__ == "__main__":
    main() 