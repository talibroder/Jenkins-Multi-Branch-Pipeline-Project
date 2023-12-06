pipeline {

    agent {
        label 'My New Ubuntu 22.04 Node with Java and Docker'
    }
    environment {
        IMG_NAME = 'weather-app'
        DOCKER_REPO = 'talibro/weather'
    }
    stages {
        stage('Docker build') {
                steps {
                    sh 'sudo docker build -t ${IMG_NAME} .'
                }
        }

        stage('Run Docker image') {
                steps {
                    sh 'docker run --rm -d -p 5000:5000 --name weather-app ${IMG_NAME}'
                    sh 'python3 --version'
                }
        }
        
        stage('Unitest') {
        	steps {
                    sh 'python3 unitest.py'
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
	post{
            success {
                script{
                    def buildNumber = currentBuild.number
                    slackSend(channel: 'succeeded-build', color: 'good', message: "Pipeline #${buildNumber} succeeded!")
                    sh 'sudo docker kill ${CONT_NAME}'
                    sh 'yes | sudo docker container prune'
                }
            }
            failure {
                script {
                    def buildNumber = currentBuild.number
                    def errorMessage = currentBuild.result
                    slackSend(channel: 'devops-alerts', color: 'danger', message: "Pipeline #${buildNumber} failed with error: ${errorMessage}")
                    sh 'sudo docker kill ${CONT_NAME}'
                    sh 'yes | sudo docker container prune'
                }
            }

        }
        }
