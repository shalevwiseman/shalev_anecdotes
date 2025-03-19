# DummyJSON API Plugin Project

## My Process

### 1. Understanding the Task
The first step was to carefully read the assignment requirements outlined in the provided PDF. The task involved creating a plugin system to:
- Authenticate with an API.
- Collect three pieces of evidence: user details, a set of posts, and posts with their comments.
- Ensure the solution was modular, reusable, and robust.

I identified the need for a base `Plugin` class and a specific implementation for the DummyJSON API, along with proper error handling and output formatting.

### 2. Checking the API Documentation
I reviewed the DummyJSON API documentation to understand its endpoints, authentication process, and response structures. Key findings:
- **Authentication**: The `/auth/login` endpoint accepts a `username` and `password` via POST and returns a `token`.
- **Endpoints**:
  - `/auth/me`: Retrieves authenticated user details.
  - `/posts?limit=60`: Fetches up to 60 posts.
  - `/posts/{id}/comments`: Gets comments for a specific post.
- All authenticated requests require a `Bearer` token in the `Authorization` header.

This step ensured I knew what data to expect and how to structure my requests.

### 3. Testing via Postman
Before coding, I used Postman to test the API
These tests validated the API’s functionality and helped me plan the code structure.

### 4. Testing Coding in Jupyter Notebook
I prototyped the solution in a Jupyter Notebook to experiment with the API calls:
- Wrote a basic script to authenticate and fetch data using the `requests` library.
- Tested parsing JSON responses and combining posts with comments.
- Iterated on error handling (e.g., timeouts, invalid responses).

This step allowed me to refine the logic incrementally before moving to a full project structure.

### 5. Opening a Repository with the Project
I initialized a Git repository to organize the project

### 6. Adding the Working Code
I translated the Jupyter prototype into a structured Python script:
- Defined an abstract `Plugin` base class with `test_connectivity` and `collect_evidence` methods.
- Implemented `DummyJsonPlugin` to handle DummyJSON API interactions.
- Added basic functionality: authenticate, fetch user details, 60 posts, and posts with comments.
- Tested the script to ensure it worked as expected with `emilys`/`emilyspass`.

The initial code printed results to the console and served as a functional baseline.

### 7. Elevating the Code
To improve the solution, I enhanced the code with:
- **Error Handling**: Added timeouts, try-except blocks etc.
- **Logging**: Replaced `print` with `logging` to a timestamped file for better debugging.
- **JSON Output**: Added a `save_to_json` function to save the evidence.
- **Modularity**: Kept the base `Plugin` class abstract for future extensibility.
- **User Feedback**: Improved console output to be concise while directing users to logs for details.


## Repository Contents
- `plugin.py`: The main Python script with the plugin system.
- `output/`: Directory for JSON evidence files (gitignored).
- `plugin_log_*.log`: Log files generated during execution (gitignored).
- `README.md`: This file.


## Future Improvements
- Add configuration via a `.env` file for `base_url`, `username`, and `password`.
- Support additional evidence types if needed.
- Implement parallel requests for faster comment fetching.
