# Build stage
FROM node:22-alpine AS builder

WORKDIR /app

# Install yarn
RUN corepack enable && corepack prepare yarn@1.22.21 --activate

# Copy package files
COPY package.json yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy application code
COPY . .

# Build the application
RUN yarn build

# Production stage
FROM node:22-alpine

WORKDIR /app

# Install yarn
RUN corepack enable && corepack prepare yarn@1.22.21 --activate

# Copy built application
COPY --from=builder /app/.output ./.output
COPY --from=builder /app/package.json ./

# Expose port
EXPOSE 3000

# Run the application
CMD ["node", ".output/server/index.mjs"]
