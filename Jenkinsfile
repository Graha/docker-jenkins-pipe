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
        sh 'pwd'
        sh 'ls'
    }
    
    stage('Building Docker image') {
        app = docker.build("graha/flaskpy")
        image_id = sh 'docker images -q "${app.id}"'
        echo "Built Image ${app.id} -> ${image_id}"
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
}
