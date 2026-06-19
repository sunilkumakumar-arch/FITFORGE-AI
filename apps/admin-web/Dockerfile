FROM node:22-alpine AS deps
WORKDIR /app
COPY package*.json ./
COPY apps/admin-web/package.json ./apps/admin-web/package.json
RUN npm ci
FROM node:22-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run web:build
FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/apps/admin-web/.next/standalone ./
COPY --from=builder /app/apps/admin-web/.next/static ./apps/admin-web/.next/static
EXPOSE 3000
CMD ["node", "apps/admin-web/server.js"]
