FROM node:20-alpine AS builder
WORKDIR /app

# Accept env vars at build time (Vite bakes these into the bundle)
ARG VITE_API_URL=http://localhost:8000
ARG VITE_POSTHOG_KEY=""
ARG VITE_POSTHOG_HOST=https://us.i.posthog.com
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_POSTHOG_KEY=$VITE_POSTHOG_KEY
ENV VITE_POSTHOG_HOST=$VITE_POSTHOG_HOST

COPY package.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
