# Installation instructions

**Note**

For some reason `PiCamera2` does not want to work in the virtual environment so it might be necessary to
use global (system) python3 interpreter. So, if you want to use `PiCamera2` package for the project do not
follow the `uv` guidelines.

### Docker

1. [Link to docker website](https://www.docker.com)
2. Run the following command:

```
docker run -p 9042:9042 -d --name ndl scylladb/scylla
```
*This command will first pull and then start a docker container (name does not matter). Takes a few seconds to initialize*

### ScyllaDB

First we need to create keyspaces (databases) where we will declare all necessary tables. 
Each table is created in a separate keyspace in order to fully parallelize reads and writes.
1. ```
   CREATE KEYSPACE face_recognition WITH replication = {'class': 'NetworkTopologyStrategy', 'replication_factor' : 1};
   ```
2. ```
   CREATE KEYSPACE users WITH replication = {'class': 'NetworkTopologyStrategy', 'replication_factor' : 1};
   ```
3. ```
   CREATE KEYSPACE session WITH replication = {'class': 'NetworkTopologyStrategy', 'replication_factor' : 1};
   ```
4. ```
   CREATE KEYSPACE rfid WITH replication = {'class': 'NetworkTopologyStrategy', 'replication_factor' : 1};
   ```

Now, let's create tables in our newly created databases

5. ```
   CREATE TABLE face_recognition.people(
    id uuid,
    name text,
    path_to_images text,
    authorization_status tinyint,
    access_remaining_date_time text,
    face_encodings blob,
    PRIMARY KEY ( name, path_to_images )
   );
   ```
6. ```
   CREATE TABLE users.users(
    username text PRIMARY KEY, 
    password text
   );
   ```
7. ```
   CREATE TABLE session.tokens(
    session_token text PRIMARY KEY, 
    timestamp text
   );
   ```
8. ```
   CREATE TABLE rfid.uid(
    tag_id text PRIMARY KEY
   );
   ```

### How to access ScyllaDB

**JetBrains IDE**

1. On the bar on the right side there is a DB button.
2. In the left top part of the pop-up window click the plus.
3. Click Add Source
4. Choose Apache Cassandra
5. Leave the config as is but change the password
    - username: cassandra
    - password: cassandra
6. After completing these steps open a `console` and execute provided commands.

**Cqlsh**

1. Open Terminal
2. Execute `docker exec -it ndl /bin/bash`
3. Execute `cqlsh`
    - (here you might have to try a couple of times)
4. Wait for it to connect.
5. Execute provided commands.

### Python

---
**Warning**:

*Before proceeding with this section please check instructions below on how to install `uv` package manager.
The instructions are included at the bottom of the page.*
*If you do not want to use `uv` that's ok, but please make sure to install all necessary packages.*

---

1. Set up a virtual environment:

```
uv venv --python 3.11.9
```

2. Install the required dependencies:

```
uv sync
```

*All the packages are already provided in the .toml file*

**!Please make sure that you are installing the packages in the correct python enviroment!**

*Note: `dlib` requires CMake.*

---

#### Install `uv` package manager

[Link to the GitHub repository](https://github.com/astral-sh/uv)

#### Install CMake

[Link to CMake website](https://cmake.org)


     
