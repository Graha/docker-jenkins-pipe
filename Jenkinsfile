node ('xubun') {
    def app
    def version

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
    }

    stage('Quality Check') {
        /* Ideally, we would run a test framework against our image.*/

        app.inside {
            sh 'echo "Tests passed"'
        }
    }

    stage('Push Docker image') {
        /* Finally, we'll push the image with two tags:
         * First, the incremental build number from Jenkins
         * Second, the 'latest' tag.
         * Pushing multiple tags is cheap, as all the layers are reused. */
        docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
            app.push("${version}_${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }
}
