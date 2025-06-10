pipeline{
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t financial_model:1.0 .'
            }
        }
        stage('Push') {
            steps {
                sh 'docker push financial_model:1.0'
            }
        }
        stage('Deploy')
    }
}