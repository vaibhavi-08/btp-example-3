pipeline {
    agent any

    options {
        skipDefaultCheckout()
    }

    

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
               
                
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Build') {
            steps {
                // Without Docker, the build stage packages the application files for deployment
                sh 'tar -czf app-build-${BUILD_NUMBER}.tar.gz --exclude=venv --exclude=.git .'
            }
        }

        stage('Quality') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install flake8
                    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
                '''
            }
        }

    }
    
    post {
        always {
            cleanWs()
        }
    }
}