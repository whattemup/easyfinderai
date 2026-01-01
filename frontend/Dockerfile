FROM node:18-alpine
WORKDIR /main
COPY frontend/src/package.json .
RUN npm install
COPY . .
RUN npm run build
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "8080"]
