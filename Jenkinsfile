pipeline {

	agent {
		label 'Agent1'
	}
    
	environment {
	IMG_NAME = 'weather'
        DOCKER_REPO = 'talibro/weather'
        CONT_NAME='Weatherapp'
	}
    
	stages {
		stage('Read Version from S3') {	
            		steps {
            			withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'tali-admin-aws', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                		script {
                			// Download versioning.txt from S3
                			sh 'aws s3 cp s3://app-versioning/versioning.txt versioning.txt'

                			// Read the content of versioning.txt
                			def s3Content = readFile 'versioning.txt'

                			// Split the content by dot ('.')
                			def versionParts = s3Content.split('\\.')

                			// Set each part as an environment variable
                			env.MAJOR = versionParts[0].trim().toInteger()
                			env.MINOR = versionParts[1].trim().toInteger()
                			env.PATCH = versionParts[2].trim().toInteger()
                		}
               			}
            		}
        	}
		stage('Smoke test') {
			when {branch 'develop'}
			steps {
				script {

					sh 'sudo docker build -t ${IMG_NAME} .'
					}
				}
		}

		stage('Run Docker image and test') {
	steps {
	script {
		sh 'docker run --rm -d -p 80:80 --name weather_app ${IMG_NAME}'
                sh 'python3 --version'
                sh 'python3 unitest.py'
                
                }
            }
        }
        
        stage('Run Tests') {
        steps {
        // Run Selenium tests
        script {
               sh 'pip install selenium'
               sh 'python3 selenium_location.py'
               }
             }
             }

	stage('Push to DockerHub') {
	steps {
	script {
                withCredentials([usernamePassword(credentialsId: 'docker_hub', passwordVariable: 'PSWD', usernameVariable: 'LOGIN')]) {
                        def buildNumber = currentBuild.number
                        echo "Build Number: ${buildNumber}"
                        echo "docker repo: ${DOCKER_REPO}"

                	sh "docker tag ${IMG_NAME} ${DOCKER_REPO}:${buildNumber}"
                        sh 'echo ${PSWD} | docker login -u ${LOGIN} --password-stdin'
                        sh "docker push ${DOCKER_REPO}:${buildNumber}"

              		}
              }	
              }
              }
              
        stage('Deploy') {
	steps {
	script {

	withCredentials([sshUserPrivateKey(credentialsId: 'ssh_ip', keyFileVariable: 'SSH_KEY_PATH')]) {
	sh "scp -o StrictHostKeyChecking=no -i ${SSH_KEY_PATH} nginx.conf ubuntu@16.171.230.105:/home/ubuntu"
        sh "scp -o StrictHostKeyChecking=no -i ${SSH_KEY_PATH} docker-compose.yaml ubuntu@16.171.230.105:/home/ubuntu"
        sh "ssh -o StrictHostKeyChecking=no -i ${SSH_KEY_PATH} ubuntu@16.171.230.105 'cd /home/ubuntu && docker pull ${DOCKER_REPO}:1.0.0 && sudo docker-compose up -d'"
                    } 
	}
	}
	}
	
	}
   	 
	post {
		success {
		script {
                    def buildNumber = currentBuild.number
                    slackSend(channel: 'succeeded-build', color: 'good', message: "Pipeline #${buildNumber} succeeded!")
                    sh 'sudo docker kill weather_app'
                    sh 'yes | sudo docker container prune'

                }
                }
            
		failure {
		script {
                    def buildNumber = currentBuild.number
                    def errorMessage = currentBuild.result
                    slackSend(channel: 'devops-alerts', color: 'danger', message: "Pipeline #${buildNumber} failed with error: ${errorMessage}")
                    sh 'sudo docker kill weather_app'
                    sh 'yes | sudo docker container prune'
                }
                }

        }
        }
        
