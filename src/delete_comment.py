#!/usr/bin/env python3
import requests
import time
import json
from datetime import datetime

# Configuration
TOKEN = ""
USERNAME = "edu"

# GitHub API headers
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'GitHub-Comment-Delete-Script'
}

# Base URL for GitHub API
BASE_URL = 'https://api.github.com'

def log_message(message):
    """Log messages with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def handle_rate_limit(response):
    """Handle GitHub API rate limiting"""
    if response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers:
        if int(response.headers['X-RateLimit-Remaining']) == 0:
            reset_time = int(response.headers['X-RateLimit-Reset'])
            current_time = int(time.time())
            sleep_time = reset_time - current_time + 10  # Add 10 seconds buffer
            
            if sleep_time > 0:
                log_message(f"Rate limit exceeded. Sleeping for {sleep_time} seconds...")
                time.sleep(sleep_time)
                return True
    return False

def get_all_user_comments():
    """Get all comments made by the user across all repositories"""
    comments = []
    page = 1
    
    log_message(f"Fetching all comments for user: {USERNAME}")
    
    while True:
        # Search for issues where the user has commented
        search_url = f"{BASE_URL}/search/issues"
        params = {
            'q': f'commenter:{USERNAME} is:issue',
            'per_page': 100,
            'page': page
        }
        
        response = requests.get(search_url, headers=HEADERS, params=params)
        
        if handle_rate_limit(response):
            continue
            
        if response.status_code != 200:
            log_message(f"Error searching issues: {response.status_code} - {response.text}")
            break
            
        data = response.json()
        issues = data.get('items', [])
        
        if not issues:
            log_message(f"No more issues found. Processed {page-1} pages.")
            break
            
        log_message(f"Processing page {page} - found {len(issues)} issues")
        
        # For each issue, get the comments
        for issue in issues:
            issue_number = issue['number']
            repo_full_name = issue['repository_url'].split('/')[-2:]
            repo_owner = repo_full_name[0].split('repos/')[-1]
            repo_name = repo_full_name[1]
            
            # Get comments for this issue
            comments_url = f"{BASE_URL}/repos/{repo_owner}/{repo_name}/issues/{issue_number}/comments"
            comments_response = requests.get(comments_url, headers=HEADERS)
            
            if handle_rate_limit(comments_response):
                comments_response = requests.get(comments_url, headers=HEADERS)
            
            if comments_response.status_code == 200:
                issue_comments = comments_response.json()
                user_comments = [comment for comment in issue_comments if comment['user']['login'] == USERNAME]
                
                for comment in user_comments:
                    comments.append({
                        'id': comment['id'],
                        'url': comment['url'],
                        'issue_url': issue['html_url'],
                        'repo': f"{repo_owner}/{repo_name}",
                        'created_at': comment['created_at'],
                        'body_preview': comment['body'][:100] + '...' if len(comment['body']) > 100 else comment['body']
                    })
                
                if user_comments:
                    log_message(f"Found {len(user_comments)} comments in {repo_owner}/{repo_name}#{issue_number}")
            else:
                log_message(f"Error fetching comments for issue {issue_number}: {comments_response.status_code}")
            
            # Small delay to avoid overwhelming the API
            time.sleep(0.1)
        
        page += 1
        
        # Add delay between pages
        time.sleep(1)
    
    return comments

def delete_comment(comment):
    """Delete a single comment"""
    comment_id = comment['id']
    delete_url = f"{BASE_URL}/repos/{comment['repo']}/issues/comments/{comment_id}"
    
    response = requests.delete(delete_url, headers=HEADERS)
    
    if handle_rate_limit(response):
        response = requests.delete(delete_url, headers=HEADERS)
    
    if response.status_code == 204:
        log_message(f"✓ Deleted comment {comment_id} from {comment['repo']}")
        return True
    else:
        log_message(f"✗ Failed to delete comment {comment_id}: {response.status_code} - {response.text}")
        return False

def main():
    """Main function to orchestrate the deletion process"""
    log_message("Starting GitHub comment deletion process...")
    log_message("=" * 60)
    
    # Verify token and get user info
    user_url = f"{BASE_URL}/user"
    user_response = requests.get(user_url, headers=HEADERS)
    
    if user_response.status_code != 200:
        log_message(f"Error: Invalid token or API issue: {user_response.status_code}")
        return
    
    user_data = user_response.json()
    if user_data['login'] != USERNAME:
        log_message(f"Warning: Token user ({user_data['login']}) doesn't match expected username ({USERNAME})")
        return
    
    log_message(f"Authenticated as: {user_data['login']}")
    
    # Get all comments
    log_message("Phase 1: Discovering all comments...")
    comments = get_all_user_comments()
    
    if not comments:
        log_message("No comments found to delete.")
        return
    
    log_message(f"Found {len(comments)} comments to delete")
    log_message("=" * 60)
    
    # Show summary of comments to be deleted
    log_message("Comments to be deleted:")
    for i, comment in enumerate(comments, 1):
        log_message(f"{i:3d}. {comment['repo']} - Created: {comment['created_at']}")
        log_message(f"     Preview: {comment['body_preview']}")
        log_message(f"     Issue: {comment['issue_url']}")
        log_message("")
    
    # Confirm deletion
    log_message("=" * 60)
    log_message(f"READY TO DELETE {len(comments)} COMMENTS")
    log_message("This action cannot be undone!")
    
    # Uncomment the following lines if you want a confirmation prompt
    # confirmation = input("Type 'DELETE ALL' to confirm: ")
    # if confirmation != 'DELETE ALL':
    #     log_message("Deletion cancelled.")
    #     return
    
    # Delete all comments
    log_message("Phase 2: Deleting comments...")
    deleted_count = 0
    failed_count = 0
    
    for i, comment in enumerate(comments, 1):
        log_message(f"Deleting comment {i}/{len(comments)}...")
        
        if delete_comment(comment):
            deleted_count += 1
        else:
            failed_count += 1
        
        # Rate limiting - be respectful to GitHub's API
        time.sleep(1)
    
    # Final summary
    log_message("=" * 60)
    log_message("DELETION COMPLETE!")
    log_message(f"Successfully deleted: {deleted_count} comments")
    log_message(f"Failed to delete: {failed_count} comments")
    log_message(f"Total processed: {len(comments)} comments")
    
    if failed_count > 0:
        log_message("Some comments failed to delete. This might be due to:")
        log_message("- Comments in private repositories you no longer have access to")
        log_message("- Comments that were already deleted")
        log_message("- Rate limiting issues")

if __name__ == "__main__":
    main()