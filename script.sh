#!/bin/bash
rm -f twoface.db

sqlite3 twoface.db < schema.sql

# Function to generate a random gamertag-like username
generate_username() {
    echo "$(tr -dc '[:alnum:]' < /dev/urandom | head -c 8)"
}

# Function to generate an email address based on the generated username
generate_email() {
    local username="$1"
    echo "$username@email"
}


# Array to store the usernames of created accounts
created_accounts=()

# Add 20 accounts
for ((i=1; i<=20; i++)); do
    # Generate username
    username=$(generate_username)

    # Generate email based on username
    email=$(generate_email "$username")

    # Insert user
    python3 twoface.py insert-user "$email"

    # Insert account
    python3 twoface.py insert-account "$username" "$email"

    # Add username to created_accounts array
    created_accounts+=("$username")
done

# Make some users follow each other (from accounts created earlier)
for ((i=0; i<${#created_accounts[@]}; i++)); do
    follower=${created_accounts[i]}
    followed_index=$((RANDOM % ${#created_accounts[@]}))
    followed=${created_accounts[followed_index]}

    # Check if follower and followed are different
    if [ "$follower" != "$followed" ]; then
        # Create follow relationship
        python3 twoface.py insert-follower "$follower" "$followed"
    fi
done

created_posts=()

# Make some posts (from accounts created earlier)
for ((i=0; i<${#created_accounts[@]}; i++)); do
    user=${created_accounts[i]}
    title="$user post 1"
    created_posts+=("$title")
    message="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    python3 twoface.py insert-post "$user" "$title" "$message"
done

#make some replies (from various accounts)

for ((i=0; i<${#created_accounts[@]}; i++)); do
    user=${created_accounts[i]}
    post_index=$((RANDOM % ${#created_posts[@]}))
    posttitle=${created_posts[post_index]}
    title="reply to $posttitle"
    message="cool post bro"

    python3 twoface.py insert-reply "$user" "$posttitle" "$title" "$message" true
done
 
#make likes
for ((i=0; i<${#created_accounts[@]}; i++)); do
    user=${created_accounts[i]}
    post_index=$((RANDOM % ${#created_posts[@]}))
    posttitle=${created_posts[post_index]}

    python3 twoface.py insert-like "$user" "$posttitle"
done
