#!/bin/bash

#display all timeline posts before
curl -X GET http://127.0.0.1:5000/api/timeline_post

#create random timeline post
curl -X POST http://127.0.0.1:5000/api/timeline_post -d "name=Billy&email=Billy@gmail.com&content=Billy's first timeline post!"

#display all timeline posts after
curl -X GET http://127.0.0.1:5000/api/timeline_post

#delete timeline post by id
echo "Enter the id of the timeline post you'd like to delete: "
read ID_TO_DELETE
curl -X DELETE http://127.0.0.1:5000/api/timeline_post -d "id=$(ID_TO_DELETE)"


