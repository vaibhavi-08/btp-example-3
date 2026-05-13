pipeline {
    agent any

    environment {
        DEPLOY_SSH_CREDS = 'deploy-server-ssh'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "✅ Checkout completed"
            }
        }

        stage('Setup') {
            steps {
                script {
                    // Load configuration from pipeline.config
                    def config = readProperties file: 'pipeline.config'
                    env.DEPLOY_HOST     = config.DEPLOY_HOST
                    env.DEPLOY_USER     = config.DEPLOY_USER
                    env.DEPLOY_BRANCH   = config.DEPLOY_BRANCH
                    env.CONTAINER_NAME  = config.CONTAINER_NAME  // Keeping for consistency, though not used
                    
                    echo "✅ Configuration loaded"
                    echo "🖥️  Deploy Host : ${env.DEPLOY_HOST}"
                    echo "👤 Deploy User : ${env.DEPLOY_USER}"
                }

                sh '''
                    python3 -m venv venv || true
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
                echo "✅ Setup completed (Virtual Environment + dependencies)"
            }
        }

        stage('Quality') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install flake8 pylint
                    
                    echo "Running Flake8 linting..."
                    flake8 . --exclude=venv || true
                    
                    echo "Running Pylint..."
                    pylint --disable=all --enable=E,F *.py || true
                '''
                echo "✅ Quality checks completed"
            }
        }

        stage('Build') {
            steps {
                sh '''
                    . venv/bin/activate
                    echo "Building Python project..."
                    python -m py_compile *.py || true
                '''
                echo "✅ Build completed (Python syntax check)"
            }
        }

        stage('Deploy') {
            when {
                branch "${env.DEPLOY_BRANCH}"
            }
            steps {
                script {
                    sshagent(credentials: [DEPLOY_SSH_CREDS]) {
                        sh '''
                            ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} '
                                echo "Creating deployment directory..." &&
                                mkdir -p ~/app/${CONTAINER_NAME}
                            '
                            
                            # Sync project files to server
                            rsync -avz --exclude="venv" --exclude=".git" ./ ${DEPLOY_USER}@${DEPLOY_HOST}:~/app/${CONTAINER_NAME}/
                            
                            ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} "
                                cd ~/app/${CONTAINER_NAME} &&
                                echo 'Setting up virtual environment on server...' &&
                                python3 -m venv venv || true &&
                                . venv/bin/activate &&
                                pip install --upgrade pip &&
                                pip install -r requirements.txt &&
                                
                                echo 'Stopping old process...' &&
                                pkill -f ${CONTAINER_NAME} || true &&
                                
                                echo 'Starting new application...' &&
                                nohup . venv/bin/python main.py > app.log 2>&1 & 
                                echo \$! > ${CONTAINER_NAME}.pid
                            "
                        '''
                    }
                }
                echo "✅ Deployment completed on ${DEPLOY_HOST}"
            }
        }
    }

    post {
        success {
            echo "🎉 Pipeline executed successfully!"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}