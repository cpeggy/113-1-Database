# HW2
## Create NoSQL
1. html page
  -Home 
![page](https://github.com/cpeggy/113-1-Database/blob/main/database_hw2/%E6%88%AA%E5%9C%96%202024-10-27%2017.24.30.png)
  - Create post
![page](https://github.com/cpeggy/113-1-Database/blob/main/database_hw2/%E6%88%AA%E5%9C%96%202024-10-28%2016.10.22.png)
2. import to Mongodb's JSON format
```
{
    "title": "First Post",
    "content": "This is the content of the first post.",
    "partner_needed": true,
    "created_at": { "$date": "2024-10-28T10:00:00Z" },
    "comments": [
        {
            "comment_content": "This is a comment",
            "commented_at": { "$date": "2024-10-28T12:00:00Z" }
        }
    ]
}
```
3. 
### How it works?
[View Youtube]()
### Full code
[Here!](https://github.com/cpeggy/113-1-Database/tree/main/database_hw3)
## The next I can improve.....
1. To let frontend more user-friendly :>
2. Let user edit page same as other (in posts.html)
3. Any comment or new idea to this smallllllll project, don't hesitate to tell me :).
