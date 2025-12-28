pipeline{
    agent any

    options {
        skipDefaultCheckout true
    }

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "grand-principle-480715-v1"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    sh 'git config --global --add safe.directory "*"'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/kristofpella/hotel-reservation-prediction.git']])
                }
            }
        }

        stage('Setting up our Virtual Environment and Installing dependancies'){
            steps{
                script{
                    echo 'Setting up our Virtual Environment and Installing dependancies............'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('Building and Pushing Docker Image to GCR'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and Pushing Docker Image to GCR.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        export DOCKER_BUILDKIT=1

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        # Enable Cloud Build API if not already enabled
                        gcloud services enable cloudbuild.googleapis.com --project=${GCP_PROJECT} || echo "Cloud Build API may already be enabled or enabling..."

                        # Copy credentials file to workspace for gcloud builds submit
                        cp ${GOOGLE_APPLICATION_CREDENTIALS} grand-principle-480715-v1-f1615a953031.json
                        
                        # Use gcloud builds submit to build and push (avoids Docker API version issues)
                        # This builds in Cloud Build and pushes directly to GCR
                        gcloud builds submit --tag gcr.io/${GCP_PROJECT}/ml-project:latest .
                        
                        # Clean up credentials file
                        rm -f grand-principle-480715-v1-f1615a953031.json 

                        '''
                    }
                }
            }
        }
        
    }
}