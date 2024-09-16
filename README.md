# Instalation instructions
### Docker 
1. [Link to docker website](https://www.docker.com)
2. Run the follwoing commands:
   - `docker run -p 9042:9042 -d --name faces scylladb/scylla`

     *This command will first pull and then start a docker container (name does not matter). Takes a few seconds to initialize*

### Python 
`pip install dlib face-recognition numpy Pillow scylla-driver pickle`

**Please make sure that you are installing the packages in the correct python enviroment**

*Note: `dlib` requires CMake.*

##### Install CMake
[Link to CMake website](https://cmake.org)

     
