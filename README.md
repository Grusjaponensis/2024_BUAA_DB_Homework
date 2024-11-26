# 2024BUAA_DB_Homework
## Post(对应src/pages/ForumCenter文件夹)
+ forumCenter.vue
  - 功能简介：论坛中心，按时间顺序显示所有帖子,包括发帖、点赞、查看帖子详情等功能，管理员能删除所有帖子。
  - TODO：methods:fetchPosts、deletePost、toggleFavorite

+ ceatePost.vue
  - 功能简介：发帖页面，用户可以发帖，输入标题、内容、标签等信息，发帖成功后，帖子将显示在论坛中心页面。
  - TODO：methods:submitPost

+ myPosts.vue
  - 功能简介：用户自己发布的帖子页面，显示用户发的所有帖子，可以删除、(编辑帖子)、查看详情。
  - TODO：methods:deletePost、fetchPosts

+ myFavorites.vue
  - 功能简介：用户收藏的帖子页面，显示用户收藏的所有帖子，包括标题、内容、标签、发帖时间、点赞数、收藏数等信息。
  - TODO：暂无，后续可能更改为其他功能

+ postDetail.vue
  - 功能简介：帖子详情页面，显示帖子的标题、内容、标签、发帖时间、收藏数等信息，可以对帖子进行点赞、收藏、评论等操作。
  - TODO：methods:toggleFavorite、addComment、fetchPost