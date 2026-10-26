

**pipeline {**

&#x20;   **agent any**



&#x20;   **stages {**

&#x20;       **stage('Verify Project Files') {**

&#x20;           **steps {**

&#x20;               **bat 'dir'**

&#x20;               **bat 'if not exist "ai-based-resume-screening-main\\\\app.py" exit /b 1'**

&#x20;               **bat 'if not exist "ai-based-resume-screening-main\\\\Dockerfile" exit /b 1'**

&#x20;           **}**

&#x20;       **}**



&#x20;       **stage('Build Docker Image') {**

&#x20;           **steps {**

&#x20;               **bat 'docker build -t resume-screening:latest ai-based-resume-screening-main'**

&#x20;           **}**

&#x20;       **}**

&#x20;   **}**



&#x20;   **post {**

&#x20;       **success {**

&#x20;           **echo 'Pipeline completed successfully!'**

&#x20;       **}**

&#x20;       **failure {**

&#x20;           **echo 'Pipeline failed. Check Console Output.'**

&#x20;       **}**

&#x20;   **}**

**}**



