# Build stage 

FROM node:18-alpine as build 

  

WORKDIR /app 

  

# Copy package files 

COPY frontend/package.json .

  

# Install dependencies 

RUN yarn install --frozen-lockfile 

  

# Copy source code 

COPY . . 

  

# Build the app 

RUN yarn build 

  

# Production stage with nginx 

FROM nginx:alpine 

  

# Copy custom nginx config 

COPY nginx.conf /etc/nginx/conf.d/default.conf 

  

# Copy built files 

COPY --from=build /app/build /usr/share/nginx/html 

  

# Expose port - fly.io will route to this 

EXPOSE 3000 

  

# Start nginx 

CMD [\"nginx\", \"-g\", \"daemon off;\"] 
