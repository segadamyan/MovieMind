# Write Dockerfile for front-end service
# Use the official node:18.20.2 image as a base image
# Set the working directory in the container to /app
# Copy the current directory contents into the container at /app
# Install any needed packages specified in package.json
# Expose port 4200
# Run npm start when the container launches
# Use Node.js 18.20.2 as base image
# FROM node:18.20.2

FROM node:18.20.2

WORKDIR /app

COPY package*.json ./

RUN npm install -g @angular/cli@16.2.5

RUN npm install --legacy-peer-deps

COPY . .

EXPOSE 4200

RUN ng build

CMD ["ng", "serve", "--host", "0.0.0.0"]