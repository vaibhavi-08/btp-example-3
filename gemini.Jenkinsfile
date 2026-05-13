pipeline {
    agent any

    options {
        skipDefaultCheckout()
    }

    environment {
        DEPLOY_SSH_CREDS = 'deploy-server-ssh'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                script {
                    def props = readProperties file: 'pipeline.config'
                    env.DEPLOY_HOST   = props.DEPLOY_HOST
                    env.DEPLOY_USER   = props.DEPLOY_USER
                    env.DEPLOY_BRANCH = props.DEPLOY_BRANCH
                }
                
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

        stage('Deploy') {
            when {
                branch "${env.DEPLOY_BRANCH}"
            }
            steps {
                sshagent(credentials: [env.DEPLOY_SSH_CREDS]) {
                    sh """
                        # Create a specific directory for this deployment on the host
                        ssh -o StrictHostKeyChecking=no ${env.DEPLOY_USER}@${env.DEPLOY_HOST} 'mkdir -p ~/app-deploy/build-\${BUILD_NUMBER}'
                        
                        # Secure copy the packaged build to the deployment server
                        scp -o StrictHostKeyChecking=no app-build-\${BUILD_NUMBER}.tar.gz ${env.DEPLOY_USER}@${env.DEPLOY_HOST}:~/app-deploy/build-\${BUILD_NUMBER}/
                        
                        # Extract, set up the target environment, and prepare the application
                        ssh -o StrictHostKeyChecking=no ${env.DEPLOY_USER}@${env.DEPLOY_HOST} '
                            cd ~/app-deploy/build-\${BUILD_NUMBER}
                            tar -xzf app-build-\${BUILD_NUMBER}.tar.gz
                            rm app-build-\${BUILD_NUMBER}.tar.gz
                            
                            python3 -m venv venv
                            . venv/bin/activate
                            pip install -r requirements.txt
                            
                            # Note: To keep the app running in the background, uncomment and adjust the line below with your actual entry point
                            # nohup python3 main.py > application.log 2>&1 &
                        '
                    """
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}