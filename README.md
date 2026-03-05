# Social Media Backend API

Backend API for a Social Media platform built with **Django** and
**Django REST Framework**.

This API provides:

-   User authentication
-   User profiles
-   Friend requests & friendships
-   Posts with media
-   Likes
-   Comments
-   Social feed

Authentication uses **JWT (SimpleJWT)**.

------------------------------------------------------------------------

# Base API URL

All endpoints follow this structure:

    /api/<app_name>/<endpoint>/

Example:

    /api/users/register/
    /api/users/login/
    /api/posts/feed/
    /api/friends/send/<username>/

------------------------------------------------------------------------

# Authentication

Authentication uses **JWT Tokens**.

After login, the API returns:

    access_token
    refresh_token

Frontend must send the access token in the request header:

    Authorization: Bearer <access_token>

### Endpoints that do NOT require authentication

-   Register
-   Login

All other endpoints require authentication.

------------------------------------------------------------------------

# Authentication Flow

Typical frontend workflow:

1.  Register user
2.  Login
3.  Receive access and refresh tokens
4.  Store access token
5.  Send token in Authorization header

------------------------------------------------------------------------

# User Model Fields
|       Field        |       Description       |
|:------------------:|:-----------------------:|
|       email        | Unique login identifier |
|      username      |     Public username     |
|  profile_picture   | Optional profile image  |
|        bio         |     User biography      |
|   date_of_birth    |   Optional birth date   |
|       gender       |        M / F / O        |
| is_private_account |     Privacy control     |
|     is_log_in      |      Login status       |
|     created_at     |  Account creation time  |

Login is performed using **email** instead of username.

------------------------------------------------------------------------

# Users API

## Register

    POST /api/users/register/

Request:

``` json
{
  "email": "name@email.com",
  "username": "username",
  "password": "Password123!",
  "password2": "Password123!",
  "bio": "Hello, I am learning",
  "gender": "M"
}
```

------------------------------------------------------------------------

## Login

    POST /api/users/login/

Response:

``` json
{
  "user": {
    "email": "testuser1@example.com",
    "username": "testuser1",
    "bio": "bio here",
    "gender": "M",
    "profile_picture": null,
    "is_log_in": true
  },
  "refresh": "refresh_token_here",
  "access": "access_token_here"
}
```

------------------------------------------------------------------------

## Logout

    POST /api/users/logout/

Requires authentication.

------------------------------------------------------------------------

## List Users (Staff Only)

    GET /api/users/list/

Accessible only to admin users.

------------------------------------------------------------------------

# Profiles API

## My Profile

    GET /api/profiles/me/

Returns the logged-in user's profile.

------------------------------------------------------------------------

## User Profile

    GET /api/profiles/<username>/

Returns the profile of a specific user.

------------------------------------------------------------------------

# Friends System

## Send Friend Request

    POST /api/friends/send/<username>/

------------------------------------------------------------------------

## Friend Request Action

    POST /api/friends/request/<request_id>/

Request body:

``` json
{
  "action": "accept"
}
```

Possible values:

-   accept
-   reject
-   cancel

Rules:

-   accept / reject → receiver only
-   cancel → sender only

------------------------------------------------------------------------

## Pending Friend Requests

    GET /api/friends/requests/

------------------------------------------------------------------------

## Friend List

    GET /api/friends/list/

------------------------------------------------------------------------

## Unfriend

    POST /api/friends/unfriend/<username>/

------------------------------------------------------------------------

# Posts System

Posts may contain:

-   Text
-   Images
-   Videos
-   Multiple media files

Visibility levels:

    PUBLIC
    FRIENDS
    PRIVATE

------------------------------------------------------------------------

# Create Post

    POST /api/posts/create/

Content type:

    multipart/form-data

Fields:

|   Field    |            Type            |
|:----------:|:--------------------------:|
|  content   |            text            |
| visibility | PUBLIC / FRIENDS / PRIVATE |
|   media    |  file (multiple allowed)   |

Example:

    media=file1.jpg
    media=file2.png

------------------------------------------------------------------------

# Feed

    GET /api/posts/feed/

Feed includes:

-   User posts
-   Friends posts
-   Public posts

Sorted by:

    Newest first

Example response:

``` json
[
  {
    "id": 2,
    "author": 2,
    "author_name": "testuser1",
    "author_email": "testuser1@example.com",
    "content": "Multiple files Media post",
    "visibility": "FRIENDS",
    "media": [
      {
        "id": 1,
        "media_type": "IMAGE",
        "file": "/media/post_media/file.jpeg",
        "created_at": "2026-03-04T21:06:25Z"
      }
    ],
    "likes_count": 0,
    "comments_count": 0,
    "comments": [],
    "created_at": "2026-03-04T21:06:25Z"
  }
]
```

------------------------------------------------------------------------

# Likes

    POST /api/posts/like/<post_id>/

Adds a like to a post.

Note: Unlike is not implemented.

------------------------------------------------------------------------

# Comments

## Create Comment

    POST /api/posts/comment/<post_id>/

Request:

``` json
{
  "content": "This is my comment"
}
```

------------------------------------------------------------------------

## Modify Comment

    POST /api/posts/comment/modify/<custom_id>/

Custom ID format:

    postID-commentNumber

Example:

    1-1

Request:

``` json
{
  "content": "updated comment"
}
```

------------------------------------------------------------------------

## Delete All Post Comments

    DELETE /api/posts/comment/delete-all/<post_id>/

------------------------------------------------------------------------

# Media Upload

Media uploads use:

    multipart/form-data

Stored under:

    /media/post_media/

Frontend must prepend backend domain:

    https://domain.com/media/post_media/file.jpg

------------------------------------------------------------------------

# Permissions

|       Action        |   Permission    |
|:-------------------:|:---------------:|
|     Create post     |  Authenticated  |
|      Edit post      |   Post owner    |
|     Delete post     | Not implemented |
| Send friend request |  Authenticated  |
|   Accept request    |    Receiver     |
|   Reject request    |    Receiver     |
|   Cancel request    |     Sender      |

------------------------------------------------------------------------

# Pagination

Currently pagination is **not implemented**.

------------------------------------------------------------------------

# Error Codes

| Code | Meaning      |
|------|--------------|
| 200  | Success      |
| 201  | Created      |
| 400  | Bad Request  |
| 401  | Unauthorized |
| 403  | Forbidden    |
| 404  | Not Found    |
| 500  | Server Error |

------------------------------------------------------------------------

# Backend Stack

-   Django
-   Django REST Framework
-   SimpleJWT
-   SQLite (development)

------------------------------------------------------------------------

# Complete API Endpoints Table

All endpoints require authentication except Register and Login.

Authentication header:

    Authorization: Bearer <access_token>

## Authentication & Users API

| Method | Endpoint               | Description                       | Auth Required |
| ------ | ---------------------- | --------------------------------- | ------------- |
| POST   | `/api/users/register/` | Register a new user account       | ❌             |
| POST   | `/api/users/login/`    | Login user and receive JWT tokens | ❌             |
| POST   | `/api/users/logout/`   | Logout user (invalidate token)    | ✅             |
| GET    | `/api/users/list/`     | List all users (Staff only)       | ✅             |

## Profiles API

| Method | Endpoint                    | Description                  | Auth Required |
| ------ | --------------------------- | ---------------------------- | ------------- |
| GET    | `/api/profiles/me/`         | Get logged-in user's profile | ✅             |
| GET    | `/api/profiles/<username>/` | Get another user's profile   | ✅             |

## 

------------------------------------------------------------------------
# Future Improvements

-   Pagination
-   Unlike functionality
-   Edit post endpoint
-   Delete single comment
-   CORS configuration
-   Notifications
-   Real‑time messaging
