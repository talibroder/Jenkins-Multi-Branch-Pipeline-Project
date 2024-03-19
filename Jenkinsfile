pipeline {

	agent {
		label 'Agent1'
	}
    
	environment {
		IMG_NAME = 'weather'
		DOCKER_REPO = 'talibro/weather'
		CONT_NAME = 'Weatherapp'
		HELM_REPO = 'talibro/weather_k8s'
		GIT_PROJECT_ID = '3'
		GITLAB_HOST = 'http://51.20.190.148'
		GITLAB_API_TOKEN = credentials('merge-request-token')


	}
    
	stages {
	
		stage('Read Version from S3') {	
            		steps {
            			withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'talibr-admin-aws', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
		        		script {
		        			// Download and read the content of versioning.txt from S3
		        			sh 'aws s3 cp s3://weatherversion/versioning.txt versioning.txt'
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
        	
        	
        	stage('Docker build and run app') {
           		when {not {branch 'main'}}
			steps {
				script {
						sh 'sudo docker build -t ${IMG_NAME}:${MAJOR}.${MINOR}.${PATCH} -f ./Dockerfile .'
						sh 'sudo docker run --rm -d -p 5000:5000 --name ${CONT_NAME} ${IMG_NAME}:${MAJOR}.${MINOR}.${PATCH}'
						sh 'python3 app_test.py'
						sh 'python3 selenium_location.py'
					}
					
				}
				
			post {
				success {
					script {
						def branchName = env.BRANCH_NAME.toLowerCase()
                       				if (branchName.contains('fix')) {
                       					sh '''
                        					PATCH=$((PATCH + 1))
                						echo ${PATCH}
                						echo "${MAJOR}.${MINOR}.${PATCH}" > versioning.txt
                						cat versioning.txt
                					'''
       						}
       						 
                        			else if (branchName.contains('feature')) {
				   			sh ''' 
				   			    MINOR=$((MINOR + 1)) \
                    					    echo "${MAJOR}.${MINOR}.${PATCH}" > versioning.txt
                    					'''
						}
					}
				}
                	}
                }

       		stage('Create merge request') {
                	when {not {branch 'main'}}
               		steps {
		                script {
		                    def apiUrl = "https://gitlab.com/api/v4/projects/${env.GITLAB_PROJECT_ID}/merge_requests"
				    def requestBody = [
				        title: 'Your merge request title',
				        source_branch: 'feature-change-title', // Replace with your source branch
				        target_branch: 'main', // Replace with your target branch
				        remove_source_branch: true // Optional: Remove source branch after merge
				    ]
                    
				    def response = gitlab(
				        credentialsId: env.GITLAB_API_TOKEN,
				        apiEndpoint: env.GITLAB_HOST,
				        method: 'POST',
				        path: apiUrl,
				        requestBody: requestBody
				    )
                    
				    if (response.status == 201) {
				        echo 'Merge request created successfully!'
				    } else {
				        error "Failed to create merge request: ${response.content}"
				    }
						}
                        }
                 }

                    
                      
		stage('Push to DockerHub') {
			steps {
				withCredentials([usernamePassword(credentialsId: 'docker_hub', passwordVariable: 'PSWD', usernameVariable: 'LOGIN')]) {
				script {

						sh 'sudo docker tag ${IMG_NAME} ${DOCKER_REPO}:${MAJOR}.${MINOR}.${PATCH}'
						sh 'sudo docker tag ${IMG_NAME} ${DOCKER_REPO}:latest'
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
						oci://registry-1.docker.io/${HELM_REPO} \
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
					sh 'aws s3 cp versioning.txt s3://weatherversion/versioning.txt'
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
        
