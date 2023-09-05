FROM node:14

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . ./

ENV REACT_APP_BACKEND_URL=$REACT_APP_BACKEND_URL

RUN npm run build

EXPOSE 8006

CMD ["npm", "start"]
