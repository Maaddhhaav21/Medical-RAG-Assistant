pipeline {
agent any

```
stages {

    stage('Checkout') {
        steps {
            echo 'Checking out source code...'

            checkout scmGit(
                branches: [[name: '*/main']],
                extensions: [],
                userRemoteConfigs: [[
                    credentialsId: 'github-token',
                    url: 'https://github.com/Maaddhhaav21/Medical-RAG-Assistant.git'
                ]]
            )
        }
    }

    stage('Verify Docker') {
        steps {
            echo 'Checking Docker installation...'
            sh 'docker --version'
        }
    }

    stage('Build Docker Image') {
        steps {
            echo 'Building Medical RAG Docker image...'
            sh 'docker build -t medical-rag-app:latest .'
        }
    }
}

post {
    success {
        echo 'Pipeline completed successfully!'
    }

    failure {
        echo 'Pipeline failed!'
    }

    always {
        echo 'Jenkins pipeline execution finished.'
    }
}
```

}
