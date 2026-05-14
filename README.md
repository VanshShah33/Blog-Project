# 📝 BlogProject — Django Blog Application

A full-featured blog web application built with **Django** and **SQLite**, supporting multi-role authentication, post moderation, and social interactions.

---

## 📌 Short Description

BlogProject is a Django-based blog platform where users can write, publish, and interact with blog posts. It features a two-role system — **regular users** and **admins** — with an approval workflow ensuring only reviewed content appears publicly. Users can like and comment on posts, manage their profile, and control post visibility.

---

## 🚀 Features

- **User Authentication** — Sign up, log in, and log out
- **Role-Based Access** — Admin and regular user dashboards
- **Post Management** — Create, edit, delete, and toggle post visibility
- **Approval Workflow** — Posts require admin approval before going live
- **Social Interactions** — Like posts and leave comments
- **User Profiles** — Edit name, gender, mobile number, and profile picture
- **Post Stats** — View count, like count, and comment count tracked per post
- **Image Support** — Upload cover images for posts and profile pictures
- **Admin Dashboard** — View all users and posts, approve pending submissions

---

## 🛠️ Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Backend    | Python 3.x, Django      |
| Database   | SQLite3                 |
| Frontend   | Django Templates (HTML) |
| Media      | Pillow (image handling) |
| Auth       | Django built-in auth    |

---

## 📁 Project Structure

```
Blogproject/
├── Blogapp/                  # Main application
│   ├── models.py             # Post, Comment, Profile models
│   ├── views.py              # All view logic
│   ├── urls.py               # App URL routes
│   ├── admin.py              # Django admin registration
│   └── migrations/           # Database migrations
├── Blogproject/              # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── templates/Blog/           # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   ├── user_dashboard.html
│   ├── admin_dashboard.html
│   ├── add_post.html
│   ├── edit_post.html
│   ├── delete_post.html
│   ├── post_detail.html
│   ├── post_list.html
│   ├── profile.html
│   └── edit_profile.html
├── media/                    # User-uploaded files
│   ├── post_images/
│   └── profile_images/
├── db.sqlite3                # SQLite database
└── manage.py
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.8+
- pip

### Steps

```bash
# 1. Clone or extract the project
cd Blogproject

# 2. Create and activate a virtual environment
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate

# 3. Install dependencies
pip install django pillow

# 4. Apply database migrations
python manage.py migrate

# 5. Create a superuser (admin account)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Then open your browser and go to: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔗 URL Routes

| URL                              | Description                    | Access        |
|----------------------------------|--------------------------------|---------------|
| `/`                              | Home page (approved posts)     | Public        |
| `/signup/`                       | User registration              | Public        |
| `/login/`                        | User login                     | Public        |
| `/logout/`                       | Logout                         | Authenticated |
| `/user_dashboard/`               | User's post dashboard          | Authenticated |
| `/admin_dashboard/`              | Admin moderation panel         | Admin only    |
| `/add_post/`                     | Create a new post              | Authenticated |
| `/edit_post/<id>/`               | Edit an existing post          | Author only   |
| `/delete_post/<id>/`             | Delete a post                  | Author only   |
| `/post/<id>/`                    | View post detail               | Authenticated |
| `/like/<id>/`                    | Toggle like on a post          | Authenticated |
| `/comment/<id>/`                 | Add a comment to a post        | Authenticated |
| `/approve_post/<id>/`            | Approve a pending post         | Admin only    |
| `/toggle_visibility/<id>/`       | Make a post public/private     | Author only   |
| `/profile/`                      | View user profile              | Authenticated |
| `/edit_profile/`                 | Edit user profile              | Authenticated |

---

## 🗄️ Data Models

### `Post`
| Field        | Type               | Description                    |
|--------------|--------------------|--------------------------------|
| author       | ForeignKey(User)   | Post creator                   |
| title        | CharField          | Post title (max 150 chars)     |
| content      | TextField          | Post body                      |
| image        | ImageField         | Optional cover image           |
| created_at   | DateTimeField      | Creation timestamp             |
| is_approved  | BooleanField       | Admin approval status          |
| is_public    | BooleanField       | Visibility toggle              |
| views        | PositiveIntegerField | View count                   |
| likes        | ManyToManyField    | Users who liked the post       |

### `Comment`
| Field      | Type             | Description         |
|------------|------------------|---------------------|
| post       | ForeignKey(Post) | Related post        |
| user       | ForeignKey(User) | Comment author      |
| content    | TextField        | Comment text        |
| created_at | DateTimeField    | Timestamp           |

### `Profile`
| Field         | Type             | Description             |
|---------------|------------------|-------------------------|
| user          | OneToOneField    | Linked Django user      |
| gender        | CharField        | Male / Female / Other   |
| mobile_no     | CharField        | Phone number            |
| profile_image | ImageField       | Profile picture         |

---

## 👤 User Roles

**Regular User**
- Register and log in
- Create and manage their own posts
- Like, comment on, and view approved posts
- Edit their profile

**Admin (Superuser)**
- All regular user abilities
- Access the admin dashboard
- View all users and posts
- Approve or reject pending posts

---

## 📄 License

This project is for educational/personal use. No license specified.
