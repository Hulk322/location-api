pipeline {
    // This line is required for declarative pipelines. Just keep it here.
    agent {
            label 'master'
            }
    // This section contains environment variables which are available for use in the
    // pipeline's stages.
    environment {
            //region = "${region}"
        aws_ecr_arn = "865371802987.dkr.ecr.${region}.amazonaws.com"
        task_def_arn = "arn:aws:ecs:${region}:865371802987:task-definition"
        cluster_arn = "arn:aws:ecs:${region}:865371802987:cluster"
       // exec_role_arn = "arn:aws:iam::865371802987:role/ecsTaskExecutionRole"
        module_name = "${module_name}"
        container_port = "9015"
        host_port = "9015"
        //cpu_limit = "512"
        //memory_limit = "1024"

    }

  stages {

    stage('Add Config files') {
           steps {

           configFileProvider([configFile(fileId: 'commonTaskDef-AI', replaceTokens: true, targetLocation: 'taskdef.json')]) {

           }
               // Fetch settings.yal from AWS Config
               // sh "/usr/local/bin/aws appconfig get-configuration --application Job-Module --environment ${deployEnv} --configuration settings.yaml --client-id jenkins-job-module simplify_job/settings.yaml"
           }
     }

    stage('Build') {
        steps {
            // Get SHA1 of current commit
            script {
                commit_id = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
            }
            // Build the Docker image
              sh "docker build -t ${aws_ecr_arn}/${build_env}/${module_name}:build-v${BUILD_NUMBER} ."
        }
    }

    stage('Publish Image') {
        steps {
            // Get Docker login credentials for ECR
            sh "/usr/local/bin/aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin 865371802987.dkr.ecr.${region}.amazonaws.com"
            // Push Docker image
            sh "docker push ${aws_ecr_arn}/${build_env}/${module_name}:build-v${BUILD_NUMBER}"
        }
    }

    stage('Deploy') {
        steps {
            // Override image field in taskdef file
            // sh "sed -i 's|{{image}}|${docker_repo_uri}:build-${BUILD_NUMBER}|' taskdef.json"

            // Create a new task definition revision
            sh "/usr/local/bin/aws ecs register-task-definition --family ${build_env}-${module_name}-task --cli-input-json file://taskdef.json --region ${region}"

            // Update service on Fargate
            sh "/usr/local/bin/aws --region ${region} ecs update-service --cluster ${cluster_arn}/${build_env}-ai --service ${build_env}-${module_name}-service --task-definition ${task_def_arn}/${build_env}-${module_name}-task --desired-count 1"
        }
    }

  }

    post {
        always {
            // Clean up
            sh "docker rmi -f ${aws_ecr_arn}/${build_env}/${module_name}:build-v${BUILD_NUMBER}"
      }
      failure {
            //mail to: 'devops@simplifyvms.com',
            //subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
            //body: "Something is wrong with ${env.BUILD_URL}"
        emailext (
            to: 'devops',
            subject: '${DEFAULT_SUBJECT}',
            body: '${DEFAULT_CONTENT}',
            recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
    }
  }
}
