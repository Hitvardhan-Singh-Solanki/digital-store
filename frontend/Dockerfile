FROM node:20

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy project files
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]