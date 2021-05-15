from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['antsalper4@correo.ugr.es'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}


def get_data():
    """Función que captura, preprocesa y almacena los datos"""
    import sys
    sys.path.append('/tmp/workflow/service')
    client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.pqrdu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.test

    collection = client["Prediction24API2"]["Datos"]

    data = pd.read_json('prediction24.json')

    dataframe = pd.DataFrame(data=data)

    dictMongo = dataframe.to_dict("registers")

    collection.insert_one({'data' : dictMongo}).inserted_id


dag = DAG(
    'CC-P2',
    default_args=default_args,
    description='Grafo de tareas de la practica 2',
    schedule_interval=timedelta(days=1),
)

SetupEnvironment = BashOperator(
                    task_id='setup_environment',
                    depends_on_past=False,
                    bash_command='mkdir -p /tmp/workflow/',
                    dag=dag
                    )

DownloadHumidity = BashOperator(
                        task_id='download_humidity',
                        depends_on_past=False,
                        bash_command='wget --output-document /tmp/workflow/humidity.csv.zip https://raw.githubusercontent.com/manuparra/MaterialCC2020/master/humidity.csv.zip',
                        dag=dag
                        )

DownloadTemperature = BashOperator(
                            task_id='download_temperature',
                            depends_on_past=False,
                            bash_command='wget --output-document /tmp/workflow/temperature.csv.zip https://raw.githubusercontent.com/manuparra/MaterialCC2020/master/temperature.csv.zip',
                            dag=dag
                            )

DownloadRepository = BashOperator(
                        task_id='download_repository',
                        depends_on_past=False,
                        bash_command='rm -rf /tmp/workflow/service/ ; mkdir /tmp/workflow/service ; git clone https://github.com/antoniosp7/cc-practica2-airflow.git /tmp/workflow/service',
                        dag=dag
                        )

UnzipData = BashOperator(
                        task_id='unzip_data',
                        depends_on_past=False,
                        bash_command='unzip -o /tmp/workflow/temperature.csv.zip -d /tmp/workflow ; unzip -o /tmp/workflow/humidity.csv.zip -d /tmp/workflow',
                        dag=dag
                        )

SaveData = PythonOperator(
                    task_id='save_data',
                    python_callable=get_data,
                    op_kwargs={},
                    dag=dag
                    )

DoTests = BashOperator(
                    task_id='do_tests',
                    depends_on_past=False,
                    bash_command='cd /tmp/workflow/service ; pytest tests.py',
                    dag=dag
                    )

SetupDocker = BashOperator(
                    task_id='setup_docker',
                    depends_on_past=False,
                    bash_command='cd /tmp/workflow/service ; docker run hello-world ; 	docker stop $(docker ps -a -q) ; 	docker rm $( docker ps -a -q) ; docker rmi $(docker images -q),
                    dag=dag
                    )


DeployArima = BashOperator(
                    task_id='desploy_arima',
                    depends_on_past=False,
                    bash_command='cd /tmp/workflow/service ; docker build -f Dockerfile1 -t service_v1 . ; docker run -d -p 8001:8001 -e PORT=8001 service_v1',
                    dag=dag
                    )


DeployApi = BashOperator(
                    task_id='deploy_api',
                    depends_on_past=False,
                    bash_command='cd /tmp/workflow/service ; docker build -f Dockerfile2 -t service_v2 . ; docker run -d -p 8002:8002 -e PORT=8002 service_v2',
                    dag=dag
                    )

SetupEnvironment >> [DownloadHumidity, DownloadTemperature, DownloadRepository] >> UnzipData >> SaveData >> DoTests >> SetupDocker >> [DeployArima, DeployApi]
