pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT_ID = 'grand-principle-480715-v1'
        GCLOUD_PATH = 'var/jenkins_home/google-cloud-sdk/bin'
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

        stage('Building and Pushing Docker Image to GCR') {
            steps {
                withCredentials([file(credentialsId: '7707bcf0-8da0-40ca-bb65-0574130b2dd5', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script {
                        echo 'Building and Pushing Docker Image to GCR...............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT_ID}

                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT_ID}/hotel-reservation-prediction .

                        docker push gcr.io/${GCP_PROJECT_ID}/hotel-reservation-prediction
                        '''
                    }
                }
            }
        }
    }
}