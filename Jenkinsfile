pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: 'gitpassword', url: 'https://github.com/Yeshwanthan87/homeassignment.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python -m unittest discover'
            }
        }

        stage('Docker Build & Push') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                        def app = docker.build("your-dockerhub-username/my-flask-app")
                        app.push("${env.BUILD_NUMBER}")
                        app.push("latest")
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh 'helm upgrade --install my-flask-app ./charts/my-flask-app'
                }
            }
        }
    }

    post {
        success {
            mail to: 'yeshwanthan87@gmail.com',
                 subject: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                 body: "The build succeeded! Check it out at ${env.BUILD_URL}"
        }
        failure {
            mail to: 'yeshwanthan87@gmail.com',
                 subject: "FAILURE: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                 body: "The build failed! Check it out at ${env.BUILD_URL}"
        }
    }
}
