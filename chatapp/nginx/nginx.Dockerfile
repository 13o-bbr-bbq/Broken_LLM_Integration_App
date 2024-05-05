FROM nginx:latest

# Remove the default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

# Copy the custom nginx.conf
COPY nginx.conf /etc/nginx/conf.d
