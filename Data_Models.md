# Data Models

[TOC]

## User 模型

### `UserBase` - 继承自 `SQLModel`
> **Shared properties**，为用户模型提供共享字段。

| 字段名      | 类型           | 描述 |
|------------|----------------|------|
| `email`    | `EmailStr`     | 用户邮箱，最大长度 100，唯一且索引 |
| `nickname` | `str or None`  | 用户昵称，可选，默认值为生成的随机字符串 |
| `is_superuser` | `bool`     | 是否为超级管理员，默认为 `False` |
| `is_volunteer` | `bool`     | 是否为志愿者，默认为 `False` |
| `avatar_url`  | `str`        | 头像 URL，默认为配置中的默认头像 URL |

---



### `UserCreate` - 继承自 `UserBase`

> **用于创建用户时接收的字段**。

| 字段名      | 类型           | 描述 |
|------------|----------------|------|
| `email`    | `EmailStr`     | 用户邮箱，最大长度 100 |
| `nickname` | `str or None`  | 用户昵称，可选 |
| `is_superuser` | `bool`     | 是否为超级管理员，默认为 `False` |
| `is_volunteer` | `bool`     | 是否为志愿者，默认为 `False` |
| `avatar_url`  | `str`        | 头像 URL，默认为默认值 |
| `password`    | `str`        | 密码，长度限制为 8 到 100 |

---



### `UserUpdate` - 继承自 `UserBase`

> **用于更新用户信息时接收的字段，所有字段均为可选**。

| 字段名      | 类型           | 描述 |
|------------|----------------|------|
| `email`    | `EmailStr or None` | 用户邮箱，可选，最大长度 100 |
| `nickname` | `str or None`    | 用户昵称，可选 |
| `is_superuser` | `bool or None` | 是否为超级管理员，可选 |
| `is_volunteer` | `bool or None` | 是否为志愿者，可选 |
| `avatar_url`  | `str or None`   | 头像 URL，可选 |
| `password`    | `str or None`   | 密码，可选，长度限制为 8 到 100 |

---



### `User` - 继承自 `UserBase`，并继承自 `SQLModel` <strong style="color: red">（数据库模型） </strong>

> **数据库模型，用于存储用户数据**。

| 字段名      | 类型           | 描述 |
|------------|----------------|------|
| `id`       | `uuid.UUID`    | 用户 ID，主键，自动生成 |
| `hashed_password` | `str`      | 哈希后的密码 |

---



### `UserPublic` - 继承自 `UserBase`

> **用于通过 API 返回的用户数据，包含用户 ID**。

| 字段名      | 类型           | 描述 |
|------------|----------------|------|
| `id`       | `uuid.UUID`    | 用户 ID |
| `email`    | `EmailStr`     | 用户邮箱 |
| `nickname` | `str or None`    | 用户昵称 |
| `is_superuser` | `bool`     | 是否为超级管理员 |
| `is_volunteer` | `bool`     | 是否为志愿者 |
| `avatar_url`  | `str`        | 头像 URL |

---



### `UserRegister` - 继承自 `SQLModel`

> **用户注册时接收的字段**。

| 字段名      | 类型           | 描述 |
|------------|----------------|------|
| `email`    | `EmailStr`     | 用户邮箱，最大长度 100 |
| `password` | `str`          | 密码，长度限制为 8 到 100 |
| `nickname` | `str or None`    | 用户昵称，可选 |
| `avatar_url` | `str`        | 头像 URL，默认为默认值 |

---



### `UserUpdateProfile` - 继承自 `SQLModel`

> **更新用户个人资料时接收的字段**。

| 字段名      | 类型           | 描述 |
|------------|----------------|------|
| `email`    | `EmailStr | None` | 用户邮箱，可选，最大长度 100 |
| `nickname` | `str or None`    | 用户昵称，可选 |
| `new_avatar_url` | `str`    | 新的头像 URL，默认为默认值 |

---



### `UserUpdatePassword` - 继承自 `SQLModel`

> **更新用户密码时接收的字段**。

| 字段名      | 类型           | 描述 |
|------------|----------------|------|
| `old_password` | `str`       | 当前密码，长度限制为 8 到 100 |
| `new_password` | `str`       | 新密码，长度限制为 8 到 100 |

---



### `UserUpdateAvatar` - 继承自 `SQLModel`

> **更新用户头像时接收的字段**。

| 字段名      | 类型           | 描述 |
|------------|----------------|------|
| `new_avatar_url` | `str`     | 新的头像 URL，默认为默认值 |

---



### `UsersPublic` - 继承自 `SQLModel`

> **用于返回多个用户数据的分页响应**。

| 字段名      | 类型           | 描述 |
|------------|----------------|------|
| `data`     | `list[UserPublic]` | 用户列表 |
| `count`    | `int`          | 用户数量 |

---





## Token 模型

### `Token` - 继承自 `SQLModel`
> **用于返回用户认证 token 的模型**。

| 字段名      | 类型           | 描述 |
|------------|----------------|------|
| `access_token` | `str`        | 访问 token |
| `token_type`   | `str`        | token 类型，默认为 `bearer` |



### `TokenPayload` - 继承自 `SQLModel`

> **用于返回 token 载荷的模型**。

| 字段名      | 类型           | 描述 |
|------------|----------------|------|
| `sub`      | `str | None`    | 用户的唯一标识 |

---





## Message 模型

### `Message` - 继承自 `SQLModel`
> **用于返回一个消息的模型**。

| 字段名      | 类型           | 描述 |
|------------|----------------|------|
| `message`  | `str`          | 消息内容 |





---

## Cats 模型

### `CatBase` - 继承自`SQLModel`

| 字段名               | 类型                         | 描述                                                         |
| -------------------- | ---------------------------- | ------------------------------------------------------------ |
| `name`               | `str`                        | 猫的名字，<strong style="color: red"> 不可为空</strong>，创建时必须标明 |
| `is_male`            | `bool`                       | 性别，**不可为空**，默认为雄性                               |
| `age`                | `int or None`                 | 年龄，**可选**，为空时表示未知年龄                           |
| `latest_location_id` | `int or None`, **ForeignKey** | **外键**，链接到***地理位置表***，记录最近一次被记录的位置   |
| `health_condition`   | `int`                        | 健康状况（健康、疾病、喵星）                                 |
| `description`        | `str or None`                 | 额外的描述（外貌、习惯等）                                   |



### `CatCreate` - 继承自`CatBase`

| 字段名             | 类型          | 描述                             |
| ------------------ | ------------- | -------------------------------- |
| `name`             | `str`         | **非空**，猫名                   |
| `is_male`          | `bool or None` | **可空**，性别，默认使用父类属性 |
| `age`              | `int or None`  | **可选**，年龄                   |
| `health_condition` | `int`, enum   | **必填**，健康状况               |
| `description`      | `str or None`  | **可选**，简单描述一下猫猫的情况 |



### `CatUpdateInfo` - 继承自`SQLModel`

> 全部为可选值，每次更新时只需要部分信息

---

| 字段名             | 类型          | 描述                       |
| ------------------ | ------------- | -------------------------- |
| `name`             | `str or None`  | **可选**，更新猫猫名字     |
| `is_male`          | `bool or None` | **可选**， 更新猫猫性别    |
| `age`              | `int or None`  | **可选**， 更新猫猫年龄    |
| `health_condition` | `int or None`  | **可选**，更新猫猫健康状况 |
| `description`      | `str or None`  | **可选**，更新猫猫的描述   |



### `CatUpdateLocation` - 继承自`SQLModel`

| 字段名        | 类型  | 描述                         |
| ------------- | ----- | ---------------------------- |
| `location_id` | `int` | **必填**，最新一次记录的位置 |



### `Cat` - 继承自`SQLModel`, <strong style="color: red">数据库模型</strong>

| 字段名               | 类型                    | 描述                               |
| -------------------- | ----------------------- | ---------------------------------- |
| `id`                 | `uuid` ***PrimaryKey*** | **主键**，uuid                     |
|  `name`  | `str` | **必填**，名字 |
| `is_male`            | `bool = true`           | **可选**，性别，默认为雄性         |
| `age`                | `int or None`            | **可选**，年龄                     |
| `latest_location_id` | `uuid or None`            | **外键**，可选，最新一次记录的位置 |
| `health_condition`   | `int`                   | **必填**，健康状况                 |
| `description`        | `str or None`            | **可选**，描述猫猫                 |



### `CatLocation` - 继承自`SQLModel` , <strong style="color: red">数据库模型</strong>

| 字段名              | 类型 | 描述 |
| ------------------- | ---- | ---- |
| `id`                | `uuid`, ***PrimaryKey*** | **主键** |
| `cat_id`            | `uuid`, ***ForeignKey, index*** | **外键**，猫的id |
| `user_id` | `uuid`, ***ForeignKey, index*** | **外键**，用户id |
| `longitude` | `float` | 经度，浮点数, 范围 $[-180, 180]$ |
| `latitude`         | `float` | 纬度，浮点数，范围$[-90, 90]$ |
| `timestamp`         | `datetime`, index | 时间戳 |






---

## Adoption模型

### `Adoption` - `SQLModel`, <strong style="color: red">数据库模型</strong>

| 字段名               | 类型                            | 描述         |
| -------------------- | ------------------------------- | ------------ |
| `id`                 | `uuid`, ***PrimaryKey***        | 主键         |
| `user_id`            | `uuid`, ***ForeignKey, index*** | 外键，用户id |
| `cat_id`             | `uuid`, ***ForeignKey, index*** | 外键，猫id   |
| `application_status` | `int`, enum                     | 申请状态     |
| `application_time`   | `datetime`                      | 申请时间     |





---

## Post模型

### `Post` - `SQLModel`, <strong style="color: red">数据库模型</strong>

| 字段名      | 类型                            | 描述           |
| ----------- | ------------------------------- | -------------- |
| `id`        | `uuid`, ***PrimaryKey***        | 主键           |
| `user_id`   | `uuid`, ***ForeignKey, index*** | 外键           |
| `cat_id`    | `uuid or None`, ***ForeignKey*** | 外键，**可选** |
| `title` | `str` | 必填，帖子标题 |
| `content`   | `str`                           | 内容           |
| `created_at` | `datetime`                      | 发布时间       |



### `PostMedia` - `SQLModel`, <strong style="color: red">数据库模型</strong>

| 字段名      | 类型                     | 描述         |
| ----------- | ------------------------ | ------------ |
| `id`        | `uuid`, ***PrimaryKey*** | 主键         |
| `post_id`   | `uuid`, ***ForeignKey*** | 外键，帖子id |
| `image_url` | `str`                    | 图片url      |



### `PostTag` - `SQLModel`, <strong style="color: red">数据库模型</strong>

| 字段名    | 类型                     | 描述         |
| --------- | ------------------------ | ------------ |
| `id`      | `uuid`, ***PrimaryKey*** | 主键         |
| `user_id` | `uuid`, ***ForeignKey*** | 外键，用户id |
| `name`    | `str`                    | tag的标题    |



### `PostTagRelation` - `SQLModel`, <strong style="color: red">数据库模型</strong>

| 字段名    | 类型                     | 描述               |
| --------- | ------------------------ | ------------------ |
| `post_id` | `uuid`, ***PrimaryKey*** | 外键，指向帖子 ID  |
| `tag_id`  | `uuid`, ***PrimaryKey*** | 外键，指向标签 ID  |
