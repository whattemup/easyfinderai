# Build stage 

FROM node:18-alpine as build 

  

WORKDIR /app 

  

# Copy package files 

COPY package.json yarn.lock .

  

# Install dependencies 

RUN yarn install --frozen-lockfile 

  

# Copy source code 

COPY . . 

  

# Build the app 

RUN yarn build 

  

# Production stage
FROM nginx:alpine

# REMOVE default nginx config (CRITICAL)
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built frontend
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
CMD [\"nginx\", \"-g\", \"daemon off;\"] 
