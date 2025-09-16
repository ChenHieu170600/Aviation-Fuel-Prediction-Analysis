# Permanent Deployment Guide for Aviation Fuel Prediction Presentation

This guide provides instructions on how to permanently deploy the Aviation Fuel Prediction Presentation as a web application using a cloud hosting provider. The presentation is built using Flask, a Python web framework.

## 1. Prerequisites

Before you begin, ensure you have the following:

*   **Python 3.x:** Installed on your local machine.
*   **Git:** Installed on your local machine.
*   **A Cloud Hosting Provider Account:** Choose a provider like Heroku, AWS (Elastic Beanstalk), Google Cloud Platform (App Engine), or Vercel. You will need an account with one of these services.
*   **Basic understanding of command-line interface (CLI) and Git.**

## 2. Project Structure

The project will have the following structure:

```
/your_project_folder/
├── src/
│   ├── static/  # Contains your HTML presentation slides and images
│   └── main.py  # Your Flask application entry point
├── requirements.txt  # Lists all Python dependencies
└── Procfile  # (For Heroku) Specifies the command to run your app
```

## 3. Files Provided

I will provide you with a ZIP archive containing the following essential files:

*   `src/main.py`: The Flask application code.
*   `src/static/`: A directory containing all your HTML presentation slides (`.html` files) and image assets (`.png` files).
*   `requirements.txt`: A file listing all Python packages required by the application.

## 4. Local Setup and Testing

Before deploying, it's good practice to set up and test the application locally.

1.  **Unzip the provided archive** to your desired project directory (e.g., `your_project_folder`).

2.  **Navigate into the project directory** in your terminal:

    ```bash
    cd your_project_folder
    ```

3.  **Create a Python virtual environment** (recommended for dependency management):

    ```bash
    python3 -m venv venv
    ```

4.  **Activate the virtual environment:**

    *   On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

    *   On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

5.  **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

6.  **Run the Flask application:**

    ```bash
    python src/main.py
    ```

7.  **Access the application:** Open your web browser and go to `http://127.0.0.1:5000` (or `http://localhost:5000`). You should see your presentation.

8.  **Deactivate the virtual environment** when you're done testing:

    ```bash
    deactivate
    ```

## 5. Deployment to Cloud Hosting Providers (General Steps)

The specific steps vary slightly depending on your chosen cloud provider, but the general workflow is as follows:

### 5.1 Heroku

Heroku is a popular platform for deploying Python web apps due to its simplicity.

1.  **Sign up for a Heroku account** and install the Heroku CLI.

2.  **Log in to Heroku** from your terminal:

    ```bash
    heroku login
    ```

3.  **Create a `Procfile`** in the root of your `your_project_folder` with the following content:

    ```
    web: gunicorn src.main:app
    ```
    *Note: You'll need to add `gunicorn` to your `requirements.txt` if it's not already there: `pip install gunicorn` and then `pip freeze > requirements.txt`.*

4.  **Initialize a Git repository** (if you haven't already) and commit your files:

    ```bash
    git init
    git add .
    git commit -m 


"Initial commit"
    ```

5.  **Create a Heroku app:**

    ```bash
    heroku create your-app-name  # Replace your-app-name with a unique name
    ```

6.  **Deploy your code to Heroku:**

    ```bash
    git push heroku main
    ```

7.  **Open your app:**

    ```bash
    heroku open
    ```

### 5.2 AWS Elastic Beanstalk

Elastic Beanstalk is an easy-to-use service for deploying and scaling web applications and services developed with Python, Java, .NET, Node.js, Go, PHP, and Docker.

1.  **Sign up for an AWS account** and install the AWS CLI and EB CLI.

2.  **Configure AWS CLI** with your credentials.

3.  **Initialize your EB application** in your project directory:

    ```bash
    eb init -p python-3.11 your-app-name --region us-east-1  # Choose your Python version and region
    ```

4.  **Create an environment:**

    ```bash
    eb create your-environment-name
    ```

5.  **Deploy your application:**

    ```bash
    eb deploy
    ```

### 5.3 Google Cloud Platform (App Engine)

Google App Engine is a fully managed, serverless platform for developing and hosting web applications at scale.

1.  **Sign up for a Google Cloud account** and install the Google Cloud CLI.

2.  **Initialize your gcloud environment:**

    ```bash
    gcloud init
    ```

3.  **Create an `app.yaml` file** in the root of your `your_project_folder`:

    ```yaml
    runtime: python311
    entrypoint: gunicorn -b :$PORT src.main:app

    instance_class: F1

    handlers:
    - url: /static
      static_dir: src/static

    - url: /.*
      script: auto
    ```
    *Note: You'll need to add `gunicorn` to your `requirements.txt`.*

4.  **Deploy your application:**

    ```bash
    gcloud app deploy
    ```

### 5.4 Vercel

Vercel is a platform for frontend developers, providing a fast and easy way to deploy web projects.

1.  **Sign up for a Vercel account** and install the Vercel CLI.

2.  **Log in to Vercel** from your terminal:

    ```bash
    vercel login
    ```

3.  **Deploy your project:**

    ```bash
    vercel
    ```
    Vercel will detect that it's a Python project and guide you through the setup. You might need to configure the build command and output directory if not automatically detected.

## 6. Important Considerations

*   **Environment Variables:** For sensitive information (e.g., API keys), use environment variables instead of hardcoding them in your code. Cloud providers offer ways to manage these.
*   **Production WSGI Server:** For production deployments, it's recommended to use a production-ready WSGI server like Gunicorn or uWSGI instead of Flask's built-in development server.
*   **Static Files:** Ensure your static files (CSS, JavaScript, images) are correctly served. The `app.yaml` for App Engine and `Procfile` for Heroku demonstrate how to configure this.
*   **Error Logging:** Set up proper error logging and monitoring for your deployed application.
*   **Cost:** Be mindful of the costs associated with cloud hosting services, especially for continuous deployment.

By following these steps and adapting them to your chosen cloud provider, you can successfully deploy your Aviation Fuel Prediction Presentation as a permanent web application.


