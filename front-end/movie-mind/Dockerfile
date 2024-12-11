FROM node:18.20.2

WORKDIR /app

COPY package*.json ./

RUN npm install -g @angular/cli@16.2.5

RUN npm install --legacy-peer-deps

COPY . .

EXPOSE 4200

RUN ng build

CMD ["ng", "serve", "--live-reload=false", "--host", "0.0.0.0", "--disable-host-check"]
