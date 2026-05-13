pipeline {
    agent any

    environment {
        DEPLOY_SSH_CREDS = 'deploy-server-ssh'
    }

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/vaibhavi-08/btp-example-3'
            }
        }

        stage('Setup') {
            steps {

                script {

                    // Read configuration from pipeline.config
                    def config = readProperties file: 'pipeline.config'

                    env.DEPLOY_HOST    = config.DEPLOY_HOST
                    env.DEPLOY_USER    = config.DEPLOY_USER
                    env.DEPLOY_BRANCH  = config.DEPLOY_BRANCH
                }

                sh '''
                    python3 -m venv venv
                    . venv/bin/activate

                    pip install --upgrade pip

                    # Install dependencies
                    if [ -f "requirements.txt" ]; then
                        pip install -r requirements.txt
                    fi

                    # Install flake8
                    pip install flake8
                '''
            }
        }

        stage('Build') {
            when {
                branch env.DEPLOY_BRANCH
            }

            steps {
                sh '''
                    echo "Simple Python project - no Docker build required"
                '''
            }
        }

        stage('Quality') {
            steps {
                sh '''
                    . venv/bin/activate

                    flake8 .
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    echo "No tests configured for this repository"
                '''
            }
        }

        stage('Deploy') {
            when {
                branch env.DEPLOY_BRANCH
            }

            steps {

                sshagent(credentials: [DEPLOY_SSH_CREDS]) {

                    sh """
                    ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} '

                        mkdir -p python-app
                    '
                    """

                    sh """
                    scp -o StrictHostKeyChecking=no -r \
                        *.py requirements.txt \
                        ${DEPLOY_USER}@${DEPLOY_HOST}:~/python-app/
                    """

                    sh """
                    ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} '

                        cd ~/python-app

                        python3 -m venv venv
                        . venv/bin/activate

                        pip install -r requirements.txt

                        echo "Deployment completed"
                    '
                    """
                }
            }
        }
    }

    post {

        success {
            echo 'Pipeline executed successfully!'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}