# Task 2 - Dockerfile for nginx web server

# Here you must write Dockerfile for nginx web server
# You can use any image from Docker Hub
# You must expose port 80
# You must copy nginx configuration file to the container
# We right now devloping a web server which will be run on port 80, 
# but you can add dummy ssl certificates and run it on port 443

FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]