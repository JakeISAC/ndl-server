# Instalation instructions
### Docker 
1. [Link to docker website](https://www.docker.com)
2. Run the follwoing commands:
   - ```docker run -p 9042:9042 -d --name faces scylladb/scylla```

     *This command will first pull and then start a docker container (name does not matter). Takes a few seconds to initialize*

### ScyllaDB
1. ```
   CREATE KEYSPACE face_recognition WITH replication = {'class': 'NetworkTopologyStrategy', 'replication_factor' : 1};
   ```
2. ```
   CREATE TABLE face_recognition.people(
    id uuid,
    authorization_status tinyint,
    name text,
    path_to_images text,
    face_encodings blob,
    PRIMARY KEY ( name, face_encodings )
   );
   ```

### How to access ScyllaDB
**JetBrains IDE**
1. On the bar on the right side there is a DB button. 
2. In the left top part of the pop up window click the plus. 
3. Click Add Source 
4. Choose Appache Cassandra
5. Leave the config as is but chnage the password
   - username: cassandra 
   - password: cassandra
6. After comppleting these steps open a `console` and execute provided commands. 

**Cqlsh**
1. Open Terminal 
2. Execute `docker exec -it faces /bin/bash`
3. Execute `cqlsh` 
   - (here you might have to try a couple of time) 
4. Wait for it to connect. 
5. Execute provided commands. 
### Python 

---
**Warning**: 

*Before proceeding with this section please check instructions below on how to install `uv` package manager. 
The instructions are included at the bottom of the page.*

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

     
