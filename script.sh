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

# Add 40 accounts
for ((i=1; i<=10; i++)); do
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

follows=()
# Make some users follow each other (from accounts created earlier)
for ((i=0; i<40; i++)); do
    follower_index=$((RANDOM % ${#created_accounts[@]}))
    follower=${created_accounts[follower_index]}
    followed_index=$((RANDOM % ${#created_accounts[@]}))
    followed=${created_accounts[followed_index]}

    follow="$follower,$followed"
    # Check if follower and followed are different
    if [ "$follower" != "$followed" ] && [[ ! " ${follows[@]} " =~ " $follow " ]]; then
        # Create follow relationship
        follows+=("$follow")
        python3 twoface.py insert-follower "$follower" "$followed"
    fi
done

created_posts=()

# Make some posts (from accounts created earlier)
for ((i=0; i<100; i++)); do
    user_index=$((RANDOM % ${#created_accounts[@]}))
    user=${created_accounts[user_index]}
    title="$user's post #$((RANDOM % 2000))"
    message="this is a cool post i'm making"
    
    if [[ ! " ${created_posts[@]} " =~ " $title " ]];then
        created_posts+=("$title")
        python3 twoface.py insert-post "$user" "$title" "$message"
    fi
done

#make some replies (from various accounts)

replies=()
for ((i=0; i<100; i++)); do 
    user_index=$((RANDOM % ${#created_accounts[@]}))
    user=${created_accounts[user_index]}
    post_index=$((RANDOM % ${#created_posts[@]}))
    posttitle=${created_posts[post_index]}
    title="reply to $posttitle #$((RANDOM % 2000))"
    message="cool post bro"
     
    if [[ ! " ${replies[@]} " =~ " $title " ]];then
        replies+=("$title")
        python3 twoface.py insert-reply "$user" "$posttitle" "$title" "$message" true
    fi
done
 
likes=()
#make likes
for ((i=0; i<1000; i++)); do
    user_index=$((RANDOM % ${#created_accounts[@]}))
    user=${created_accounts[user_index]}
    post_index=$((RANDOM % ${#created_posts[@]}))
    posttitle=${created_posts[post_index]}

    like="$user,$posttitle"

    # Check if the like already exists in the likes array
    if [[ ! " ${likes[@]} " =~ " $like " ]]; then
        likes+=("$like")  
        python3 twoface.py insert-like "$user" "$posttitle"
    fi
done


reply_likes=()
#make likes
for ((i=0; i<100; i++)); do
    user_index=$((RANDOM % ${#created_accounts[@]}))
    user=${created_accounts[user_index]}
    reply_index=$((RANDOM % ${#replies[@]}))
    reply_title=${replies[reply_index]}

    like="$user,$reply_title"

    # Check if the like already exists in the likes array
    if [[ ! " ${reply_likes[@]} " =~ " $like " ]]; then
        reply_likes+=("$like")  
        python3 twoface.py reply-like "$user" "$reply_title"
    fi
done
