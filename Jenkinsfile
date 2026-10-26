
pipeline {
    agent any

    stages {
        stage('Verify Project Files') {
            steps {
                bat 'dir'
                bat 'if not exist app.py exit /b 1'
                bat 'if not exist Dockerfile exit /b 1'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t resume-screening:latest .'
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
