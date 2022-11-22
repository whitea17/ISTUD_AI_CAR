FROM dustynv/jetson-inference:r32.5.0

WORKDIR /ISTUD_AI_CAR
COPY . .
RUN pip3 install Jetson.GPIO

CMD ["./app.sh"]