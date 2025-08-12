pipeline {
    agent any
    
    environment {
        // Python virtual environment
        VENV_NAME = 'stock_data_venv'

        AZURE_CLIENT_ID = credentials('AZURE_CLIENT_ID')
        AZURE_TENANT_ID = credentials('AZURE_TENANT_ID')
        AZURE_CLIENT_SECRET = credentials('AZURE_CLIENT_SECRET')
        AZURE_VAULT_URL = credentials('AZURE_VAULT_URL')
        STORAGE_ACCOUNT_NAME = credentials('STORAGE_ACCOUNT_NAME')
    }
    
    triggers {
        // Run once a day at midnight
        cron('0 0 * * *')
    }
    
    stages {
        stage('Setup Python Environment') {
            steps {
                script {
                    sh """
                        python3 -m venv ${VENV_NAME}
                        . ${VENV_NAME}/bin/activate
                        pip install -r ./requirements.txt
                    """
                }
            }
        }
        
        stage('Collect Stock Data') {
            steps {
                script {
                    sh """
                        . ${VENV_NAME}/bin/activate
                        python3 data_collector.py
                    """
                }
            }
        }
    
        stage('Upload to Azure') {
            steps {
                script {
                    sh """
                        . ${VENV_NAME}/bin/activate
                        python3 azure_upload.py
                    """
                }
            }
        }
    }
    
    post {
        always {
            // Clean up virtual environment
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}