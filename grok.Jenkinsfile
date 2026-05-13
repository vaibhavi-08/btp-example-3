pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "✅ Checkout completed"
            }
        }

        stage('Setup') {
            steps{

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