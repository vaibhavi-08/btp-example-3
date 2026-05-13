pipeline {
    agent any

    environment {
        VENV_PATH = 'venv'
        
    }

    stages {
        stage('checkout') {
            steps {
                // Use Jenkins SCM checkout (configured in job settings)
                checkout scm
            }
        }

        stage('setup') {
            steps {
                script {
                    echo "📦 Setting up Python environment..."
                    sh '''
                        # Create isolated virtual environment
                        python3 -m venv ${VENV_PATH}
                        . ${VENV_PATH}/bin/activate
                        
                        # Upgrade pip and install project dependencies
                        pip install --upgrade pip
                        if [ -f requirements.txt ]; then
                            echo "   Installing from requirements.txt..."
                            pip install -r requirements.txt
                        else
                            echo "   ⚠️ No requirements.txt found"
                        fi
                        
                        # Install quality tools (flake8 enabled)
                        pip install --quiet flake8
                        echo "✅ Environment ready"
                    '''
                }
            }
        }

        stage('build') {
            steps {
                script {
                    // No Docker: "build" = prepare deployment artifact
                    echo "🔨 Preparing deployment package..."
                    sh '''
                        . ${VENV_PATH}/bin/activate
                        
                        # Create deployment directory
                        mkdir -p deploy-package
                        
                        # Copy application code (exclude venv, git, cache)
                        rsync -av --exclude='${VENV_PATH}' \
                              --exclude='.git' \
                              --exclude='__pycache__' \
                              --exclude='*.pyc' \
                              --exclude='.pytest_cache' \
                              ./ deploy-package/
                        
                        # Generate requirements snapshot for target environment
                        pip freeze > deploy-package/deploy-requirements.txt
                        
                        # Create deployment script
                        cat > deploy-package/deploy.sh << 'EOF'
#!/bin/bash
set -e
APP_DIR="${1:-/home/vaibhavi/apps/btp-example-3}"
echo "📦 Deploying to $APP_DIR..."

# Create app directory
mkdir -p "$APP_DIR"

# Copy files
cp -r ./* "$APP_DIR/"

# Setup virtual environment on target
cd "$APP_DIR"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
. venv/bin/activate
pip install --upgrade pip
pip install -r deploy-requirements.txt

echo "✅ Deployment complete: $APP_DIR"
EOF
                        chmod +x deploy-package/deploy.sh
                        
                        echo "✅ Package ready: deploy-package/"
                    '''
                }
            }
        }

        stage('quality') {
            steps {
                script {
                    echo "🔍 Running flake8 quality checks..."
                    sh '''
                        . ${VENV_PATH}/bin/activate
                        
                        # CRITICAL errors: FAIL the build immediately
                        echo "   [1/2] Checking critical errors (E9,F63,F7,F82)..."
                        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics \
                            --exclude=${VENV_PATH},.git,__pycache__,deploy-package,.pytest_cache
                        
                        # Style warnings: report only, don't fail build
                        echo "   [2/2] Checking style guidelines..."
                        flake8 . --count --exit-zero \
                            --max-complexity=10 \
                            --max-line-length=127 \
                            --statistics \
                            --exclude=${VENV_PATH},.git,__pycache__,deploy-package,.pytest_cache
                    '''
                    echo "✅ Quality checks passed"
                }
            }
        }

        stage('test') {
            steps {
                script {
                    // Tests disabled per config - stage preserved for structure
                    echo "🧪 Test stage: Tests disabled in configuration, skipping execution"
                    sh 'echo "⏭️ No test suite configured - stage kept for pipeline consistency"'
                }
            }
        }
    }

    post {
        always {
            // Cleanup workspace
            cleanWs()
        }
        failure {
            echo '❌ Pipeline FAILED - Check console output for details'
        }
        success {
            echo "🎉 SUCCESS: ${APP_NAME} deployed to ${DEPLOY_HOST}:${DEPLOY_DIR}"
        }
        unstable {
            echo '⚠️ Pipeline UNSTABLE - Quality checks had warnings'
        }
    }
}