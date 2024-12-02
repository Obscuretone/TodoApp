# Use an official Node.js runtime as a parent image
FROM node:18

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) to the container
COPY package*.json ./

# Install the dependencies inside the container
RUN npm install  # or RUN yarn install if using yarn

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Run the app
CMD ["npm", "start"]  # or CMD ["yarn", "start"] if using yarn