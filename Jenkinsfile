pipeline{
    agent any
    stages {
        stage('Build') {
            steps {
                bat 'docker build -t financial_model:1.0 .'
            }
        }
        stage('Push') {
            steps {
                bat 'docker push financial_model:1.0'
            }
        }
    }
}