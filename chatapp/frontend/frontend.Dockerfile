FROM node:20.8.0

# Create App directory.
ENV APP_HOME=/app
RUN mkdir -p $APP_HOME

# Set work directory.
WORKDIR $APP_HOME

# Install dependencies.
COPY ./package.json .
RUN npm update && npm install

# Copy project.
COPY . $APP_HOME

# Set Frontend port.
EXPOSE 3000

# Set environment.
ENV HOST 0.0.0.0
ENV PORT 3000
ENV NODE_ENV=development
ENV CHOKIDAR_USEPOLLING=true
ENV NODE_OPTIONS=--openssl-legacy-provider

# Build.
RUN npm run build

CMD ["npm", "start"]
