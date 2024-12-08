pipeline {
    environment {
        DOCKERHUB_CRED = credentials("DockerSid")
        PORT = "8000" 
        MINIKUBE_HOME = '~/.minikube'
    }
    agent any
    tools {nodejs "NODEJS"} 
    stages {
        stage("Stage 1: Git Clone") {
            steps {
                git credentialsId: 'GitHubSid', url: 'https://github.com/SiddharthChauhan303/SPE-Project-kub-hpa.git', branch: 'main'
            }
        }
        stage("Stage 8: Ansible"){
            steps {
                // sh '''
                // sudo ansible-playbook -i inventory-k8 playbook-k8-new.yaml
                // '''
                sh '''
                    kubectl apply -f deployment
                '''

            }

        }
    }
}