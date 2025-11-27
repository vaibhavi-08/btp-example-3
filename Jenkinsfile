pipeline {
    agent {
        docker { 
            image 'python:3.9-slim' 
            // Mount the workspace so files persist between stages
            args '-u 0:0' 
        }
    }

    environment {
        // Set environment variables if needed
        HOME = '.'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo 'Checking out source code...'
                    checkout scm
                }
            }
        }

        stage('Setup') {
            steps {
                script {
                    echo 'Installing dependencies...'
                    sh 'pip install --upgrade pip'
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('Quality') {
            steps {
                script {
                    echo 'Running Quality Checks...'
                    // failFast true stops the build immediately if quality checks fail
                    
                    // Check code formatting with Black (check only, don't modify)
                    sh'black --check . --exclude=runtime_venv|venv|.venv|.git|__pycache__ '
                    
                    // Check style guide enforcement with Flake8
                    sh 'flake8 . --exclude=venv,.venv,.git,__pycache__'
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    echo 'Building artifact...'
                    // For Python scripts, "building" often means packaging.
                    // Here we verify bytecode compilation and create a zip archive.
                    sh 'python -m compileall .'
                    sh 'tar -czf my-python-app.tar.gz *.py requirements.txt'
                }
            }
            post {
                success {
                    // Archive the artifact in Jenkins
                    archiveArtifacts artifacts: 'my-python-app.tar.gz', fingerprint: true
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo 'Running Tests...'
                    // Run pytest and generate a JUnit report for Jenkins to display
                    sh 'python -m pytest --junitxml=test-results.xml'
                }
            }
            post {
                always {
                    // Always publish test results, even if tests fail
                    junit 'test-results.xml'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "🚀 Initiating Native Local Deployment..."

                    // Cleanup: Kill old processes (Simulated using pkill on app name)
                    // We use 'main.py' because that is your specific file name
                    sh "pkill -f 'python main.py' || true"

                    // Check if our artifact exists, then setup venv and run
                    if (fileExists('my-python-app.tar.gz')) {
                         echo "📦 Installing from Artifact..."
                         sh '''
                            # Create and activate virtual environment
                            python3 -m venv runtime_venv
                            . runtime_venv/bin/activate

                            # Unpack the tarball created in the Build stage
                            tar -xzf my-python-app.tar.gz

                            # Run the application in the background
                            # (Using nohup so it survives the shell exit, though in Docker this is ephemeral)
                            nohup python main.py > app.log 2>&1 &
                            echo "Application deployed and started."
                        '''
                    }
                }
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: 'app.log', fingerprint: true
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check logs.'
        }
    }
}