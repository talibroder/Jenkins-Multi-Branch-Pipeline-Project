pipeline {

	agent {
		label 'Agent1'
	}
    
	environment {
		IMG_NAME = 'weather'
		DOCKER_REPO = 'talibro/weather'
		CONT_NAME='Weatherapp'
		GIT_PROJECT_ID = '1'
	}
    
	stages {
	
		stage('Read Version from S3') {	
            		steps {
            			withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'talibr-admin-aws', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
		        		script {
		        			// Download and read the content of versioning.txt from S3
		        			sh 'aws s3 cp s3://tali1992/versioning.txt versioning.txt'
		        			def s3Content = readFile 'versioning.txt'

		        			// Split the content by dot ('.') and set each part as an environment variable
		        			def versionParts = s3Content.split('\\.')
		        			env.MAJOR = versionParts[0].trim().toInteger()
		        			env.MINOR = versionParts[1].trim().toInteger()
		        			env.PATCH = versionParts[2].trim().toInteger()
		        		}
               			}
            		}
        	}
        	
        	
        	stage('build and testing') {
           		when {not {branch 'main'}}
			steps {
				script {
				
					sh '''
						sudo docker build -t ${IMG_NAME}:${MAJOR}.${MINOR}.${PATCH} -f ./Dockerfile . \
						sudo docker run --rm -d -p 5000:5000 --name ${CONT_NAME} ${IMG_NAME}:${MAJOR}.${MINOR}.${PATCH} \
						python3 app_test.py \
						python3 selenium_location.py
            				'''
					}
					
				}
				
			post {
				success {
					script {
						def branchName = env.BRANCH_NAME.toLowerCase()
                       				if (branchName.contains('fix')) {
                       					sh "PATCH=$((PATCH + 1)) \
                				            echo ${PATCH} \
                					    echo "${MAJOR}.${MINOR}.${PATCH}" > versioning.txt"
       						}
       						 
                        			else if (branchName.contains('feature')) {
				   			sh "MINOR=$((MINOR + 1)) \
                    					    echo "${MAJOR}.${MINOR}.${PATCH}" > versioning.txt"
						}
					}
				}
                	}
                }

       		stage('Create merge request') {
                	when {not {branch 'main'}}
               		steps {
               		        withCredentials([string(credentialsId: 'merge-request-token', variable: 'TOKEN')]) {
		                script {
		                    def commitMsg = sh(script: "git log -1 --pretty=%B", returnStdout: true).trim()
		                    sh "curl --request POST \
		                        --header 'PRIVATE-TOKEN: ${TOKEN}' \
		                        --data-urlencode 'source_branch=${env.BRANCH_NAME}' \
		                        --data-urlencode 'target_branch=main' \
		                        --data-urlencode 'title=MR-${commitMsg}' \
		                        --data-urlencode 'description=${commitMsg}' \
		                        '${GITLAB_HOST}/api/v4/projects/${GIT_PROJECT_ID}/merge_requests'"
		                	}
		                }
                        }
                 }

                    
                      
		stage('Push to DockerHub') {
			steps {
				withCredentials([usernamePassword(credentialsId: 'docker_hub', passwordVariable: 'PSWD', usernameVariable: 'LOGIN')]) {
				script {

						sh 'sudo docker tag ${IMG_NAME} ${DOCKER_REPO}:${MAJOR}.${MINOR}.${PATCH}'
						sh 'echo ${PSWD} | docker login -u ${LOGIN} --password-stdin'
						sh 'sudo docker push ${DOCKER_REPO}:${MAJOR}.${MINOR}.${PATCH}'
						sh 'sudo docker push ${DOCKER_REPO}:latest'
						
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
						oci://registry-1.docker.io/talibro/weather_k8s \
						--set image.weather.repository=${DOCKER_REPO},image.weather.tag=${MAJOR}.${MINOR}.${PATCH} \
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
        
