# My Angular App

This is a simple Angular application that allows users to input a prompt, send it to a backend API, and display the generated responses in a scrolling window.

## Project Structure

```
my-angular-app
├── src
│   ├── app
│   │   ├── app.component.ts      # Main component of the application
│   │   ├── app.component.html     # HTML template for the main component
│   │   ├── app.component.css      # Styles for the main component
│   │   └── app.module.ts          # Root module of the application
│   └── assets                      # Folder for static assets
├── angular.json                   # Angular CLI configuration file
├── package.json                   # npm configuration file
├── tsconfig.json                  # TypeScript configuration file
└── README.md                      # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd my-angular-app
   ```

2. **Install dependencies:**
   ```
   npm install
   ```

3. **Run the application:**
   ```
   ng serve
   ```

4. **Open your browser and navigate to:**
   ```
   http://localhost:4200
   ```

## Usage Guidelines

- Enter a prompt in the input box.
- Click the "Send Prompt" button to send the prompt to the backend API.
- The generated responses will be displayed in the scrolling window below the input box.

## API Endpoint

The application sends a POST request to the following endpoint:
```
http://127.0.0.1:8000/generate
```
The request body contains a JSON object with the prompt and max_length parameters.