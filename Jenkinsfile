pipeline {
    agent {
        label 'Agent My New Ubuntu 22.04 Node with Java and Docker
'
    }
    environment {
        IMG_NAME = 'weather-app'
        DOCKER_REPO = 'talibro/weather'
    }
    stages {
        stage('Docker build') {
                steps {
                    sh 'docker build -t ${IMG_NAME} .'
                }
        }

        stage('Run Docker image') {
                steps {
                    sh 'docker run --rm -d -p 5000:5000 --name weather-app ${IMG_NAME}'
                    sh 'python3 --version'
                    sh 'docker kill weather-app'
                }
        }
        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker_hub', passwordVariable: 'PSWD', usernameVariable: 'LOGIN')]) {
                    script {
                        sh 'docker tag ${IMG_NAME} ${DOCKER_REPO}:1.0.0'
                        sh 'echo ${PSWD} | docker login -u ${LOGIN} --password-stdin'
                        sh 'docker push ${DOCKER_REPO}:1.0.0'
                    }
                }
            }
        }
    }
        post {
            success {
                echo 'Pipeline successfully completed!'

                sh 'docker ps -a'
            }
            failure {
                echo 'Pipeline failed!'
                sh 'docker container prune'
                sh 'docker ps -a'
            }
        }
}
