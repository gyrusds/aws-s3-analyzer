---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

A program that analyzes files in specified S3 buckets and calculates the size of each directory.

### How to execute

1. Install Docker.

2. Build the containers.

   ```sh
   docker compose build
   ```

3. Run the containers.

   ```sh
   docker compose up
   ```

4. Open the website: <http:0.0.0.0>

Link to code in [Github](https://github.com/gyrusds/aws-s3-analyzer).
