curl -i http://192.168.1.40:8080/question -X POST -d 'What is my name'
curl -i http://192.168.1.40:8080/answer/a -X POST -d 'Dan'
curl -i http://192.168.1.40:8080/answer/b -X POST -d 'Frank'
curl -i http://192.168.1.40:8080/answer/c -X POST -d 'Brad'
curl -i http://192.168.1.40:8080/answer/d -X POST -d 'Idk'
curl -i http://192.168.1.40:8080/start -X POST
curl -i http://192.168.1.40:8080/answer/a/correct -X POST
curl -i http://192.168.1.40:8080/score -X POST -d '100'
