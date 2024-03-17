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
            			withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'talibr-admin-aws', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                		script {
                			// Download versioning.txt from S3
                			echo "doneeee"
                			sh 'aws s3 cp s3://tali1992/versioning.txt versioning.txt'

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

					sh 'sudo docker build -t ${IMG_NAME}:${MAJOR}.${MINOR}.${PATCH} -f ./Dockerfile .'
					sh 'sudo docker run --rm -d -p 5000:5000 --name ${CONT_NAME} ${IMG_NAME}:${MAJOR}.${MINOR}.${PATCH}'
            				sh 'python3 unitest.py'
					}
				}
		}
		
		stage('Hotfix test') {
			when {branch 'hotfix'}
			steps {
				script {
				        sh '''
            					PATCH=$((PATCH + 1))
                				echo ${PATCH}
                				echo "${MAJOR}.${MINOR}.${PATCH}" > versioning.txt
                				cat versioning.txt
	
                    			'''
				}
			}
		}
		
		stage('Feature test'){
			when {branch 'feature'}
			steps {
				script {
				        sh '''
                    				sudo docker build -t ${IMG_NAME}:${MAJOR}.${MINOR}.${PATCH} -f ./Dockerfile . \
            					sudo docker run --rm -d -p 5000:5000 --name ${CONT_NAME} ${IMG_NAME}:${MAJOR}.${MINOR}.${PATCH} \
            					python3 selenium_location.py
                    				MINOR=$((MINOR + 1))	
                    			'''
				}
			}
		}
				
    
		stage('Push to DockerHub') {
			steps {
				script {
					withCredentials([usernamePassword(credentialsId: 'docker_hub', passwordVariable: 'PSWD', usernameVariable: 'LOGIN')]) {
					sh "sudo docker tag ${IMG_NAME} ${DOCKER_REPO}:${MAJOR}.${MINOR}.${PATCH}"
					sh 'echo ${PSWD} | docker login -u ${LOGIN} --password-stdin'
					sh "sudo docker push ${DOCKER_REPO}:${MAJOR}.${MINOR}.${PATCH}"

					}
				}	
			}
		}
              
		stage('Deploy Helm Chart') {
			when {branch 'main'}
				steps {
					withCredentials([file(credentialsId: 'master_kube_config', variable: 'KUBECONFIG')]) {
					script {
					// Deploy Helm chart
					sh '''
					helm upgrade my-weather-app \
					oci://registry-1.docker.io/talibro/weather \
					--set image.weather.repository=${DOCKER_REPO},image.weather.tag=${IMG_TAG} \
					--install \
					--atomic \
					--kubeconfig ${KUBECONFIG}
					'''
					}
				}   		
			}
		}
	
	
		stage('Update Versioning.txt in S3') {
			steps {
			withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'talibr-admin-aws', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
				script {
					// Use AWS CLI to update the content of versioning.txt in S3
					sh 'aws s3 cp versioning.txt s3://tali1992/versioning.txt'
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
        
