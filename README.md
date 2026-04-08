# Django College Blog - Enhanced Backend

## Setup & Run
1. cd college_blog/college_blog
2. python manage.py makemigrations blog
3. python manage.py migrate
4. python ../populate_posts.py  # Creates 'Admin'/Password user + 13 posts
5. python manage.py createsuperuser  # If needed
6. python manage.py collectstatic --noinput
7. python manage.py runserver

## Features
- Blog posts with tags, categories, status (published/draft)
- Search by title/body (/search/?query=term)
- Pagination, similar posts, comments, email share
- Sitemap: /sitemap.xml
- Admin: /admin (Admin/Password)
- Tags filter: /tag/slug/

## Backend Enhancements
- Published manager for efficient queries
- Sites framework support
- Optimized template tags
- Full search with Q objects

Note: Templates for search.html may need creation for full frontend, but backend complete & error-free.
