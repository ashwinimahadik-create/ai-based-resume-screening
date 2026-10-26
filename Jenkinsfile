
pipeline {
    agent any

    stages {
        stage('Verify Project Files') {
            steps {
                bat 'dir'
                bat 'if not exist "ai-based-resume-screening-main\\app.py" exit /b 1'
                bat 'if not exist "ai-based-resume-screening-main\\Dockerfile" exit /b 1'
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('ai-based-resume-screening-main') {
                    bat '"C:\\Users\\Ashwini\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" build -t resume-screening:latest .'
                }
            }
        }

        stage('Verify Kubernetes Deployment Manifest') {
            steps {
                bat 'dir ai-based-resume-screening-main\\k8s'
                bat 'if not exist "ai-based-resume-screening-main\\k8s\\deployment.yaml" exit /b 1'
                bat 'type "ai-based-resume-screening-main\\k8s\\deployment.yaml"'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Docker image built and Kubernetes manifest verified!'
        }
        failure {
            echo 'FAILED: Check Console Output.'
        }
    }
}
