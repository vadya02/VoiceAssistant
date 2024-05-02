# Set the base image for the build stage
FROM node:alpine as build
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) to leverage Docker caching
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of your application code
COPY . .

# Build the application
RUN npm run build



# Set the base image for the production environment
FROM nginx:stable-alpine





# Copy the built files from the build stage to the production image
COPY --from=build /app/build /usr/share/nginx/html

# Copy custom nginx configuration
COPY --from=build /app/nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 to the host
EXPOSE 80

# Command to run nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
