pipeline {
    agent any

    stages {
        stage('Verify Project Files') {
            steps {
                bat 'dir'
                bat 'if not exist "ai-based-resume-screening-main\app.py" exit /b 1'
                bat 'if not exist "ai-based-resume-screening-main\Dockerfile" exit /b 1'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t resume-screening:latest ai-based-resume-screening-main'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check Console Output.'
        }
    }
}
