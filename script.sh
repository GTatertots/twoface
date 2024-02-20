#!/bin/bash


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
