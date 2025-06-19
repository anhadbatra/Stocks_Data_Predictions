pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('23db5d07-30ea-4456-b89f-1a3a8da21fb9') // Jenkins credentials ID
    }
    stages {
        stage('Login') {
            steps {
                bat "docker login -u %DOCKERHUB_CREDENTIALS_USR% -p %DOCKERHUB_CREDENTIALS_PSW%"
            }
        }
        stage('Build') {
            steps {
                bat 'docker build -t yourusername/financial_model:1.0 .'
            }
        }
        stage('Push') {
            steps {
                bat 'docker push yourusername/financial_model:1.0'
            }
        }
    }
}
