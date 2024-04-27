# Custom HTTP 1.1 Compliant Webserver

## Description
This project is a partially HTTP 1.1 compliant webserver designed to serve static content, specifically HTML and CSS files, from a directory named `www`. The server is built using Python 3 with minimal dependencies, adhering strictly to educational objectives to deepen understanding of HTTP fundamentals.

## Features
- Serves HTML and CSS files from a `./www` directory.
- Handles web requests from browsers and command-line tools like curl.
- Implements correct HTTP headers for content types and error handling.
- Provides secure access by restricting file serving to the `./www` directory and subdirectories.
- Supports redirection for directory paths ensuring they end with `/`.

## References
  1. https://www.youtube.com/watch?v=YwhOUyTxXVE&t=381s (pathlib library tutorial from JetBrains)

