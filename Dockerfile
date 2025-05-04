FROM public.ecr.aws/lambda/python:3.13

COPY requirements.txt .

RUN pip3 install --upgrade --no-cache-dir --target "${LAMBDA_TASK_ROOT}" -r requirements.txt

COPY ./app ${LAMBDA_TASK_ROOT}/app

# Define o handler (main.py com a variável `handler`)
CMD [ "app.main.handler" ]
