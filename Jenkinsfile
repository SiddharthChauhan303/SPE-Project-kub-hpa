pipeline {
    environment {
        DOCKERHUB_CRED = credentials("DockerSid")
        PORT = "8000" 
        // MINIKUBE_HOME = '/minikube'
        KUBECONFIG = credentials("K8sAuth")
    }
    agent any
    tools {nodejs "NODEJS"} 
    stages {
        stage("Stage 1: Git Clone") {
            steps {
                git credentialsId: 'GitHubSid', url: 'https://github.com/SiddharthChauhan303/SPE-Project-kub-hpa.git', branch: 'main'
            }
        }
        stage("Stage 8: Ansible") {
            steps {
                withCredentials([file(credentialsId: 'K8sAuth', variable: 'KUBECONFIG')]) {
                    sh '''
                        export KUBECONFIG=${KUBECONFIG}
                        kubectl apply -f deployment
                    '''
                }
            }
        }
    }
}