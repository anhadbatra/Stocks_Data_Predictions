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
        stage('Deploy')
            steps{
                bat '''
                ssh anhadpreetsingh077@35.235.246.146 
                "kubectl apply -f /home/anhadpreetsingh077/model_deploy/model_deploy.yaml"
                '''
            }
    }
}
