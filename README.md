 cs494
======

# Client application 
flask, mysql 필요 

# NGrinder 설치 
##controller
$docker pull ngrinder/controller:3.3

$docker run -d -v ~/.ngrinder:/root/.ngrinder -p 8080:80 -p 16001:16001 -p 12000-12009:12000-12009  ngrinder/controller:3.3 

## agent 

docker pull ngrinder/agent:3.3
docker run -d -e 'CONTROLLER_ADDR=localhost:8080' ngrinder/agent:3.3
//172.17.0.3

위에꺼 안됨 
https://hub.docker.com/r/ngrinder/controller/


# arcus 

arcus-admin, memcached 1, 2, 3 설치 
arcus-admin 에서 연결 완료 

# client-arcus connection 
