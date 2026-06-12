---
tags:
    - AWS
    - deployment
    - Docker
---

# Test the AWS setup locally

To verify the production Docker image works before deploying, run it locally using `docker-compose-aws.yml`:

```bash
cp ./app/.env.docker-aws-example ./app/.env.docker-aws
docker compose -f docker-compose-aws.yml up --build
```

The app will be available at `http://localhost:8001/admin/`.

See [Test the AWS setup locally](../howto/test-aws-setup-locally.md) for the full guide.
