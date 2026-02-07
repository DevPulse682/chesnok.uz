# System Requirements

Project Name: Chesnok.uz
Description: News platform that authors can post news, regular users read them and only logged-in users can interact.

## Main Entities

- Post
- User
- Category
- Tag
- Comment
- Like


## APIs

### Posts

R1: Most searched keywords.
R2: Users should be able to filter posts by category and tag, while also seeing list of categories and tags.
R3: Users should be able to see list of last 5 trending posts.
R4: Users should see current weather in Tashkent.
R5: Users should be able to search posts (by title, category and tag) and authors.
R6: I should be able to know analytics about posts: what people are liking most?
R7: Admins should be able to log in/logout to business panel.
R8: Admins should manage all entities: posts, category, tag, profession, user, comment.
R9: I should be able to upload images, files and audios to posts.
R10: Users should be able to like and comment posts. Without logging in, just for analytics.
R11: Website should have 3 languages: Uzbek, English, Turkish.
R12: I need middleware to compute response time per request.
R13: I need rate limiter middleware which counts requests per minute and blocks requests if limit is exceeded.
R14: Noone must dare to hate my platform. Write a background task to delete all trash comments.

- `GET /posts/`
- `GET /posts/{post_id}`
- `POST /posts/`
- `PUT /posts/{post_id}`
- `DELETE /posts/{post_id}`


- `GET /posts/?category_id={category_id}&tag_id={tag_id}`
- `GET /categories/`
- `GET /tags/`


- `GET /posts/trending/`


- `GET /weather/`


- `GET /posts/search/?query={query}`


- `GET /posts/analytics/`


- `POST /auth/login/`
- `POST /auth/logout/`




- posts CRUD
- category CRUD
- tag CRUD
- profession CRUD
- user CRUD
- comment CRUD