FROM node:18-slim
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
# Use a simple server to serve the build
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]
