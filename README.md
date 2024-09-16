# Instalation instructions
### Docker 
1. [Link to docker website](https://www.docker.com)
2. Run the follwoing commands:
   - ```docker run -p 9042:9042 -d --name faces scylladb/scylla```

     *This command will first pull and then start a docker container (name does not matter). Takes a few seconds to initialize*

#### ScyllaDB
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

##### How to access ScyllaDB
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
2. Execute `docker exec `
### Python 
```
pip install dlib face-recognition numpy Pillow scylla-driver pickle
```

**!Please make sure that you are installing the packages in the correct python enviroment!**

*Note: `dlib` requires CMake.*

#### Install CMake
[Link to CMake website](https://cmake.org)

     
