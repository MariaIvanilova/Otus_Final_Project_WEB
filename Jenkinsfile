pipeline {
    agent any

    environment {
        PHPADMIN_PORT = '8888'
        OPENCART_PORT = '8085'
        LOCAL_IP = '192.168.100.9'
        REPO_URL = 'https://github.com/MariaIvanilova/Otus_Final_Project_WEB.git'
        ALLURE_RESULTS = 'allure-results'
    }

    stages {
        stage('Checkout from GitHub') {
            steps {
                git branch: 'master',
                    url: env.REPO_URL
            }
        }

        stage('Clean Allure Results') {
            steps {
                script {
                    sh 'rm -rf allure-results || true'
                }
            }
        }

        stage('Start Infrastructure') {
            steps {
                sh '''
                    docker compose up -d mariadb opencart
                    until docker ps | grep mariadb; do sleep 3; done
                    until docker ps | grep opencart; do sleep 3; done
                    sleep 10
                '''
            }
        }

        stage('Build Test Image') {
            steps {
                sh 'docker build -t tests_opencart .'
            }
        }

        stage('Run Tests') {
            steps {
                sh """
                    docker run --name testing \
                      -e OPENCART_HOST="$OPENCART_HOST" \
                      -e BROWSER="$BROWSER" \
                      -e BROWSER_VERSION="$BROWSER_VERSION" \
                      -e EXECUTOR_URL="$EXECUTOR_URL" \
                      -e THREADS="$THREADS" \
                      tests_opencart \
                      --url "$OPENCART_HOST" --browser "$BROWSER" --bv "$BROWSER_VERSION" --executor "$EXECUTOR_URL" -n "$THREADS"
                """
            }
            post {
                always {
                    sh '''
                        docker cp testing:/app/allure-results . || true
                        docker rm -f testing || true
                    '''
                }
            }
        }

        stage('Stop Infrastructure') {
            steps {
                sh 'docker compose down --remove-orphans --timeout 2 || true'
            }
        }
    }
    post {
        always {
            allure includeProperties: false,
                jdk: '',
                results: [[path: "${ALLURE_RESULTS}"]]
        }
    }
}