FROM public.ecr.aws/lambda/python:3.9

COPY handler.py requirements.txt ./


RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/121.0.6167.85/win64/chrome-win64.zip
RUN unzip chromedriver-win64.zip -d ${LAMBDA_TASK_ROOT}/bin/
RUN rm chromedriver-win64.zip


RUN yum install -y unzip && \
    curl -Lo "/tmp/chromedriver.zip" "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/121.0.6167.85/win64/chrome-win64.zip" && \
    curl -Lo "/tmp/headless-chromium.zip" "https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-57/stable-headless-chromium-amazonlinux-2.zip" && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    unzip /tmp/headless-chromium.zip -d /opt/ && \
    rm /tmp/headless-chromium.zip && \
    rm /tmp/chromedriver.zip && \
    chmod +x /opt/chromedriver

CMD ["handler.run"]
