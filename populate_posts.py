import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_blog.settings')

import django
django.setup()

from django.utils import timezone
from blog.models import Post
from django.contrib.auth.models import User
import random
import string

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_title():
    titles = [
        'Random Post About AI',
        'Machine Learning Insights',
        'Python Programming Tips',
        'Django Best Practices',
        'Web Development Trends',
        'Data Science News',
        'Tech Innovations',
        'Coding Challenges',
        'Open Source Projects',
        'Cloud Computing Guide',
        'Cybersecurity Basics',
        'DevOps Tools',
        'Frontend Frameworks',
        'Backend Development',
    ]
    return random.choice(titles) + ' #' + str(random.randint(1, 100))

def random_slug(title):
    # Simple slug: lowercase, replace spaces with -, remove special chars
    slug = title.lower().replace(' ', '-')
    slug = ''.join(c for c in slug if c.isalnum() or c in '-')
    return slug

def random_body():
    body = 'This is a random blog post body. '
    body += 'It contains some lorem ipsum text: '
    lorem = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
    body += lorem * random.randint(5, 15)
    body += 'Random content ends here. Post ID will be unique due to random elements.'
    return body

# Get or create user Admin
user, created = User.objects.get_or_create(username='Admin')
if created:
    user.set_password('Password')
    user.email = 'admin@example.com'
    user.save()
    print("Created user 'Admin'")

# Delete existing posts to add exactly 12-13 new ones
Post.objects.all().delete()
print("Cleared existing posts.")

# Create 12-13 random posts
num_posts = 13  # 12 published + 1 draft for demo
posts = []
for i in range(num_posts):
    title = random_title()
    slug = random_slug(title)
    # Ensure unique slug
    while Post.objects.filter(slug=slug).exists():
        title = random_title()
        slug = random_slug(title)
    body = random_body()
    post = Post.objects.create(
        title=title,
        slug=slug,
        body=body,
        author=user,
        status='published' if i < 12 else 'draft',
        tags=[random.choice(['python', 'django', 'blog', 'webdev', 'tutorial'])]
    )
    posts.append(post)
    print(f"Created post {i+1}: {title}")

print(f"Successfully created {num_posts} random posts assigned to user 'Admin'.")
print("You can now run `python manage.py runserver` to view them at http://127.0.0.1:8000/blog/")

