# Chatapp-django
Chat Application on Django

Introduction
This Django chat application is designed to simplify communication between users through a web interface. Users can register, log in, send friend requests, accept or reject friend requests, view notifications, and communicate in real-time with their friends.

Installation
To run this Django chat application, follow these steps:

Download and open the project.
Create a virtual environment:
Copy code
python -m venv myenv
Activate the virtual environment:
On Windows:
Copy code
.\.venv\Scripts\activate
On macOS and Linux:
bash
Copy code
source .venv/bin/activate
Install the necessary dependencies:
Copy code
pip install -r requirements.txt
Run database migrations:
Copy code
python manage.py makemigrations
python manage.py migrate
Start the development server:
Copy code
python manage.py runserver
Components

Models (models.py)

Profile: Represents user profiles with fields such as username, first name, last name, profile picture, and friends.
FriendRequest: Represents friend requests sent between users.
Notification: Represents notifications sent to users.
ChatMessage: Represents chat messages exchanged between users.
Forms (forms.py)

UserForm: Form for user registration.
ProfileForm: Form for updating user profiles.
Views (views.py)

chats: Displays the main chat interface.
clear_chat: Clears chat history with a specific friend.
detail: Displays detailed chat history with a specific friend.
notifications: Displays notifications for the current user.
register: Handles user registration.
signin: Handles user login.
signout: Handles user logout.
update_profile: Handles updating user profiles.
friend_request: Displays pending friend requests.
suggestion: Displays friend suggestions for the current user.
send_friend_request: Sends a friend request to another user.
cancel_friend_request: Cancels a sent friend request.
accept_friend_request: Accepts a received friend request.
reject_friend_request: Rejects a received friend request.
fetch_friend_request: Fetches the count of pending friend requests.
fetch_notification: Fetches the count of notifications.
createChat: Creates a new chat message.
getChats: Fetches new chat messages.
Template Tags (templatetags/custom_filter.py)

if_id_in_queryset: Custom filter for checking the existence of an ID in a queryset.
Signals (signals.py)

create_profile: Signal to create a user profile when a new user is created.
update_profile: Signal to update user information when a profile is updated.
URLs (urls.py)
Defines URL patterns for various views and endpoints in the application.

Conclusion
This Django chat application provides a convenient and efficient way for users to communicate with each other. With features such as user authentication, friend requests, notifications, and real-time chat, it offers a comprehensive solution for any web application requiring user interaction.
