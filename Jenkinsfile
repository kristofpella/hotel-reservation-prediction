pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }


    stages {
        stage('Cloning Git Repository') {
            steps {
                script {
                    echo 'Cloning Git Repository...............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/kristofpella/hotel-reservation-prediction']])
                }
            }
        }

        stage('Creating Virtual Environment and Installing Dependencies') {
            steps {
                script {
                    echo 'Creating Virtual Environment and Installing Dependencies...............'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
    }
}