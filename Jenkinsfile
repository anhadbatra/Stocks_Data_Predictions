pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                bat 'docker build -t itisanhad/financial_model:1.0 .'
            }
        }
        stage('Push') {
            steps {
                bat 'docker push itisanhad/financial_model:1.0'
            }
        }
    }
}
