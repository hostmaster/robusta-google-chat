# Deprication notice. 

Since version `0.10.28` and later, Robusta can report issues and events in your Kubernetes cluster by sending messages via the Google Chat. [Ref](https://github.com/robusta-dev/robusta/pull/1245)

# robusta-google-chat

A simple HTTP service that sends Robusta [`webhook_sink`](https://docs.robusta.dev/master/configuration/sinks/webhook.html) notifications to Google Chat.

## Requirements

- Google Chat [webhook url](https://developers.google.com/chat/how-tos/webhooks#create_a_webhook)
- Robusta [`webhook_sink`](https://docs.robusta.dev/master/configuration/sinks/webhook.html)

## Environment variables

- `WEBHOOK_URL` Google Chat [webhook url](https://developers.google.com/chat/how-tos/webhooks#create_a_webhook)
