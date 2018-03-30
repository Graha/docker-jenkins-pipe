node ('ubuntu-slave') {
    def app
    def version
    def image_id
    
    stage('Cloning repository') {
        checkout scm
        env.WORKSPACE = pwd()
        version = readFile ("${env.WORKSPACE}/version.txt").trim()
    }

    stage('Prepare build environment') {
        /* ideal place for placing prepare like UI builds or configs */
        def commits = sh(
            script: "git log --oneline -n 10",
            returnStdout: true
        ).split('\n')
        sh 'echo "${commits}"'
        notifyStarted()
        sh 'pwd'
        sh 'ls'
    }
    
    stage('Building Docker image') {
        app = docker.build("graha/flaskpy")
        sh "docker images -q ${app.id} > docker.image.txt"
        image_id = readFile ("./docker.image.txt").trim()
    }

    stage('Quality Check') {
        /* Ideally, we would run a test framework against our image.*/
        resp = input "Confirm the quality?"
    }

    stage('Push Docker image') {
        /* Finally, we'll push the image with two tags:
         * First, the incremental build number from Jenkins
         * Second, the 'latest' tag.
         * Pushing multiple tags is cheap, as all the layers are reused. */
       resp = docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
            app.push("${version}_${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }
    
    stage('Deployment Approval') {
        /* Ideally, we would run a test framework against our image.*/
        input "Confirm the deployment?"
        app.inside {
            sh 'echo "Deployment Approved"'
        }
    }
    
    stage('Deployment Validation') {
        /* Ideally, we would run a test framework against our image.*/
        docker.image('graha/flaskpy:latest').withRun('-p 5000:5000') {
             sh 'echo "Deployed"'
             sh 'curl localhost:5000'
        }
    }
    
    stage('Cleanup') {
        notifySuccessful()
        sh "docker rmi -f ${image_id}"
    }
}


def notifyStarted() {
  //slackSend (color: '#FFFF00', message: "STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
  emailext (
      subject: "STARTED: CC Build '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
      body: """<p>STARTED: CC Build '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
        <p>Check console output at "<a href="${env.BUILD_URL}">${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>"</p>""",
      to: "grahaindia@gmail.com"
      //recipientProviders: [[$class: 'DevelopersRecipientProvider']]
    )
}

def notifySuccessful() {
  //slackSend (color: '#00FF00', message: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
  emailext (
      subject: "SUCCESSFUL: CC Build '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
      body: """<p>SUCCESSFUL: CC Build '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
        <p>Check console output at "<a href="${env.BUILD_URL}">${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>"</p>""",
      to: "grahaindia@gmail.com"
      //recipientProviders: [[$class: 'DevelopersRecipientProvider']]
    )
}

def notifyFailed() {
  //slackSend (color: '#FF0000', message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
  emailext (
      subject: "FAILED: CC Build '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
      body: """<p>FAILED: CC Build '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
        <p>Check console output at "<a href="${env.BUILD_URL}">${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>"</p>""",
      to: "grahaindia@gmail.com"
      //recipientProviders: [[$class: 'DevelopersRecipientProvider']]
    )
}
