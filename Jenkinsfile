pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: 'gitpassword', url: 'https://github.com/Yeshwanthan87/homeassignment.git'
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest
                '''
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    sh 'docker build -t yeshwanthan/my-flask-app .'
                }
            }
        }
        
        stage('Docker Image Push') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin'
                        sh 'docker push yeshwanthan/my-flask-app'
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sshagent(['openssh']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ubuntu@43.206.254.0 '
                            minikube start --driver=docker || true
                            eval $(minikube -p minikube docker-env)
                            helm lint ./my-flask-app
                            helm upgrade --install my-flask-app ./my-flask-app --namespace default
                        '
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                sshagent(['openssh']) {
                    script {
                        // Start port forwarding in the background
                        sh '''
                            ssh -o StrictHostKeyChecking=no ubuntu@43.206.254.0 '
                                kubectl get pods
                                kubectl port-forward svc/my-flask-app 30001:80 --address 0.0.0.0 > /dev/null 2>&1 &
                            '
                        '''
                        // Optionally, you can add a short sleep to allow some time for port forwarding to establish
                        sleep time: 10, unit: 'SECONDS'
                    }
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
