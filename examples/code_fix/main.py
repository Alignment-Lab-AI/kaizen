from kaizen.generator.code_fixer import CodeFixer
import json

issues = [
    {
        "severity": "critical",
        "category": "security",
        "description": "Improper handling of HTTPException in the webhook handler.",
        "location": {"line_start": 33, "line_end": 33},
        "impact": "Raising HTTPException directly returns a response but does not stop the function execution, leading to potential unintended behavior.",
        "suggestion": "Use 'raise' to properly raise the HTTPException.",
        "solution": "Replace 'return HTTPException(...)' with 'raise HTTPException(...)'.",
        "good_for_first_time": "true",
        "issue_title": "Improper Exception Handling",
        "file_path": "github_app/main.py",
    },
    {
        "severity": "medium",
        "category": "quality",
        "description": "Potentially unused variable 'body' in the webhook handler.",
        "location": {"line_start": 26, "line_end": 26},
        "impact": "The variable 'body' is fetched but not used, which can lead to confusion and unnecessary resource usage.",
        "suggestion": "Remove the 'body' variable if it is not needed, or utilize it if required for further processing.",
        "solution": "Remove line 26 if 'body' is not needed.",
        "good_for_first_time": "true",
        "issue_title": "Unused Variable",
        "file_path": "github_app/main.py",
    },
    {
        "severity": "medium",
        "category": "quality",
        "description": "Hard-coded status code in the HTTPException.",
        "location": {"line_start": 33, "line_end": 33},
        "impact": "Hard-coding status codes can make it difficult to manage and change them in the future.",
        "suggestion": "Define constants for HTTP status codes to improve maintainability.",
        "solution": "Define a constant like 'HTTP_404_NOT_FOUND = 404' and use it in the exception.",
        "good_for_first_time": "false",
        "issue_title": "Hard-Coded Status Code",
        "file_path": "github_app/main.py",
    },
    {
        "severity": "medium",
        "category": "performance",
        "description": "Potential performance issue due to multiple checks on the configuration data.",
        "location": {"line_start": 29, "line_end": 29},
        "impact": "Repeated access to configuration data can lead to performance degradation, especially if the configuration is complex.",
        "suggestion": "Cache the configuration data in a variable to avoid multiple accesses.",
        "solution": "Store CONFIG_DATA in a variable before the checks to improve performance.",
        "good_for_first_time": "true",
        "issue_title": "Repeated Configuration Access",
        "file_path": "github_app/main.py",
    },
    {
        "severity": "high",
        "category": "security",
        "description": "Potential exposure of sensitive data in headers.",
        "location": {"line_start": 7, "line_end": 8},
        "impact": "If the headers are logged or exposed, sensitive information such as the JWT could be compromised.",
        "suggestion": "Ensure that sensitive information in headers is not logged or exposed in error messages.",
        "solution": "Consider using a logging library that can mask sensitive information.",
        "good_for_first_time": "false",
        "issue_title": "Sensitive Data Exposure",
        "file_path": "github_app/github_helper/installation.py",
    },
    {
        "severity": "high",
        "category": "bug",
        "description": "Missing body in POST request.",
        "location": {"line_start": 24, "line_end": 24},
        "impact": "The request to get the installation access token may fail if the body is required but not provided.",
        "suggestion": "Include the body in the POST request.",
        "solution": "Change line 24 to: response = requests.post(url, headers=headers, json=body)",
        "good_for_first_time": "true",
        "issue_title": "Missing Request Body",
        "file_path": "github_app/github_helper/installation.py",
    },
    {
        "severity": "medium",
        "category": "performance",
        "description": "Repeated calls to generate JWT for each request.",
        "location": {"line_start": 8, "line_end": 8},
        "impact": "Generating a JWT for every request can lead to performance overhead.",
        "suggestion": "Consider caching the JWT for a short duration to reduce the number of times it is generated.",
        "solution": "Store the JWT in a variable and reuse it until it expires.",
        "good_for_first_time": "false",
        "issue_title": "Inefficient JWT Generation",
        "file_path": "github_app/github_helper/installation.py",
    },
    {
        "severity": "medium",
        "category": "quality",
        "description": "Hardcoded endpoint URLs.",
        "location": {"line_start": 9, "line_end": 9},
        "impact": "Hardcoding URLs can lead to maintainability issues if the endpoint changes.",
        "suggestion": "Consider externalizing the endpoint configuration to a settings file or environment variable.",
        "solution": "Use a configuration management approach to manage endpoint URLs.",
        "good_for_first_time": "false",
        "issue_title": "Hardcoded Endpoint URLs",
        "file_path": "github_app/github_helper/installation.py",
    },
    {
        "severity": "high",
        "category": "security",
        "description": "Potential exposure of sensitive information in logs.",
        "location": {"line_start": 35, "line_end": 39},
        "impact": "Logging sensitive information, such as the contents of the private key, can lead to security breaches if logs are exposed.",
        "suggestion": "Avoid logging sensitive information. Remove or mask sensitive data in logs.",
        "solution": "logger.info('JWT generated successfully.')",
        "good_for_first_time": "true",
        "issue_title": "Sensitive Information Exposure in Logs",
        "file_path": "github_app/github_helper/utils.py",
    },
    {
        "severity": "medium",
        "category": "performance",
        "description": "Redundant file read operation in generate_jwt function.",
        "location": {"line_start": 36, "line_end": 39},
        "impact": "Reading the file twice is inefficient and can lead to performance degradation, especially if the file is large.",
        "suggestion": "Read the file content once and store it in a variable.",
        "solution": "key_content = f.read() \nencoded_jwt = jwt.encode(payload, key_content, algorithm='RS256')",
        "good_for_first_time": "true",
        "issue_title": "Redundant File Read Operation",
        "file_path": "github_app/github_helper/utils.py",
    },
    {
        "severity": "medium",
        "category": "quality",
        "description": "Hardcoded expiration time in generate_jwt function.",
        "location": {"line_start": 30, "line_end": 30},
        "impact": "Hardcoding values makes the code less flexible and harder to maintain. It can lead to issues if the expiration time needs to change.",
        "suggestion": "Define expiration time as a constant or pass it as a parameter.",
        "solution": "EXPIRATION_TIME = 7 * 60  # Define as a constant",
        "good_for_first_time": "true",
        "issue_title": "Hardcoded Value for JWT Expiration",
        "file_path": "github_app/github_helper/utils.py",
    },
    {
        "severity": "medium",
        "category": "quality",
        "description": "Lack of error handling for file operations in generate_jwt function.",
        "location": {"line_start": 36, "line_end": 36},
        "impact": "If the file cannot be opened (e.g., file not found), it will raise an unhandled exception, causing the application to crash.",
        "suggestion": "Implement try-except blocks to handle potential file I/O errors.",
        "solution": "try:\n    with open(file_path, 'r') as f:\n        key_content = f.read()\nexcept IOError as e:\n    logger.error(f'File error:{e}')\n    return None",
        "good_for_first_time": "true",
        "issue_title": "Missing Error Handling for File Operations",
        "file_path": "github_app/github_helper/utils.py",
    },
    {
        "severity": "low",
        "category": "quality",
        "description": "Unused import statements.",
        "location": {"line_start": 1, "line_end": 7},
        "impact": "Unused imports can clutter the code and make it harder to read and maintain.",
        "suggestion": "Remove any unused import statements.",
        "solution": "Remove `import os`, `import jwt`, `import time`, `import requests`, `import logging`, `import hmac`, and `import hashlib` if not used.",
        "good_for_first_time": "true",
        "issue_title": "Unused Import Statements",
        "file_path": "github_app/github_helper/utils.py",
    },
    {
        "severity": "high",
        "category": "quality",
        "description": "Duplicate keys in the dictionary.",
        "location": {"line_start": 1, "line_end": 8},
        "impact": "Having duplicate keys in a dictionary can lead to unexpected behavior, as only the last occurrence of a key will be retained. This can cause confusion and bugs in the code.",
        "suggestion": "Remove duplicate keys and ensure each key is unique.",
        "solution": 'PULL_REQUEST_PERMISSION ={\n    "issues_read": "read",\n    "issues_write": "write",\n    "checks": "read",\n    "contents": "read",\n    "pull_requests_read": "read",\n    "pull_requests_write": "write",\n}',
        "good_for_first_time": "true",
        "issue_title": "Duplicate keys in dictionary",
        "file_path": "github_app/github_helper/permissions.py",
    },
    {
        "severity": "high",
        "category": "security",
        "description": "Potential exposure of sensitive information through environment variables.",
        "location": {"line_start": 14, "line_end": 14},
        "impact": "If the environment variable GITHUB_API_BASE_URL is not properly secured, it could expose sensitive information to unauthorized users.",
        "suggestion": "Ensure that environment variables are secured and not logged. Consider using a secrets management tool.",
        "solution": "Remove any logging statements that might inadvertently log sensitive information.",
        "good_for_first_time": "false",
        "issue_title": "Insecure handling of environment variables",
        "file_path": "github_app/github_helper/pull_requests.py",
    },
    {
        "severity": "high",
        "category": "bug",
        "description": "Potential null pointer dereference when accessing payload fields.",
        "location": {"line_start": 30, "line_end": 38},
        "impact": "If the payload does not contain the expected structure, it could lead to runtime exceptions.",
        "suggestion": "Add checks to ensure that the required fields exist in the payload before accessing them.",
        "solution": "Use a validation library or implement manual checks to ensure the presence of required keys.",
        "good_for_first_time": "true",
        "issue_title": "Null pointer dereference risk",
        "file_path": "github_app/github_helper/pull_requests.py",
    },
    {
        "severity": "medium",
        "category": "performance",
        "description": "Repeated calls to get_installation_access_token can lead to performance issues.",
        "location": {"line_start": 40, "line_end": 110},
        "impact": "Multiple calls to get_installation_access_token may lead to unnecessary overhead and potential rate limiting.",
        "suggestion": "Store the access token in a variable after the first call and reuse it.",
        "solution": "access_token = get_installation_access_token(installation_id, PULL_REQUEST_PERMISSION) # Call once and reuse",
        "good_for_first_time": "true",
        "issue_title": "Inefficient access token retrieval",
        "file_path": "github_app/github_helper/pull_requests.py",
    },
    {
        "severity": "medium",
        "category": "quality",
        "description": "Code duplication in process_pull_request and process_pr_desc functions.",
        "location": {"line_start": 29, "line_end": 104},
        "impact": "Duplication makes the code harder to maintain and increases the risk of bugs when changes are made.",
        "suggestion": "Refactor the common logic into a separate function to reduce duplication.",
        "solution": "Create a helper function that handles the common logic between process_pull_request and process_pr_desc.",
        "good_for_first_time": "false",
        "issue_title": "Code duplication",
        "file_path": "github_app/github_helper/pull_requests.py",
    },
    {
        "severity": "low",
        "category": "quality",
        "description": "Lack of error handling for HTTP requests.",
        "location": {"line_start": 118, "line_end": 132},
        "impact": "If the HTTP requests fail, there is no mechanism to handle the failure, which could lead to silent errors.",
        "suggestion": "Implement error handling for HTTP requests to manage failures gracefully.",
        "solution": "Check response.status_code and handle errors accordingly.",
        "good_for_first_time": "true",
        "issue_title": "Missing error handling for HTTP requests",
        "file_path": "github_app/github_helper/pull_requests.py",
    },
    {
        "severity": "high",
        "category": "security",
        "description": "Environment variable access without validation",
        "location": {"line_start": 5, "line_end": 5},
        "impact": "Accessing environment variables without validation can lead to application crashes or unexpected behavior if the variable is not set or contains malicious content.",
        "suggestion": "Validate the presence of the environment variable before using it.",
        "solution": "GITHUB_API_BASE_URL = os.environ.get('GITHUB_API_BASE_URL') or raise ValueError('GITHUB_API_BASE_URL not set')",
        "good_for_first_time": "true",
        "issue_title": "Unvalidated environment variable access",
        "file_path": "github_app/github_helper/endpoints.py",
    },
    {
        "severity": "medium",
        "category": "quality",
        "description": "Hardcoded URL structure in endpoint definitions",
        "location": {"line_start": 7, "line_end": 9},
        "impact": "Hardcoding parts of the URL can lead to maintenance issues if the API structure changes. It may also lead to inconsistencies if the base URL is modified but not reflected in all endpoints.",
        "suggestion": "Use a function to construct URLs to ensure consistency and maintainability.",
        "solution": "def create_endpoint(path): return urljoin(GITHUB_API_BASE_URL, path)\nGITHUB_ENDPOINTS ={\n    'get_installations': create_endpoint('installations'),\n    'get_installation_access_token': create_endpoint('/app/installations/{installation_id}/access_tokens'),\n}",
        "good_for_first_time": "false",
        "issue_title": "Hardcoded URL structure",
        "file_path": "github_app/github_helper/endpoints.py",
    },
    {
        "severity": "medium",
        "category": "quality",
        "description": "Potential issue with URL joining due to leading slashes",
        "location": {"line_start": 8, "line_end": 9},
        "impact": "Using leading slashes in URL paths can lead to incorrect URL formation, especially if the base URL ends with a slash. This can result in 404 errors or unintended API calls.",
        "suggestion": "Ensure that the paths used in urljoin do not have leading slashes or handle them appropriately.",
        "solution": "Remove leading slashes from the endpoint paths.",
        "good_for_first_time": "true",
        "issue_title": "Leading slashes in URL paths",
        "file_path": "github_app/github_helper/endpoints.py",
    },
]


def group_by_files(issues):
    grouped = {}
    for issue in issues:
        file = issue["file_path"]
        if file not in grouped:
            grouped[file] = []
        grouped[file].append(issue)

    return grouped


grouped_issues = group_by_files(issues)

for k, v in grouped_issues.items():
    print(f"File: {k}")
    with open(k, "r") as f:
        file_content = f.read()
    fixer = CodeFixer()
    res = fixer.fix_code(original_code=file_content, issues=v)
    print(json.dumps(res.fixed_code, indent=2))
    break
