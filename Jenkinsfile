pipeline {
    agent any
    stages {
        stage('Cloning Git Repository') {
            steps {
                script {
                    echo 'Cloning Git Repository...............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/kristofpella/hotel-reservation-prediction']])
                }
            }
        }
    }
}